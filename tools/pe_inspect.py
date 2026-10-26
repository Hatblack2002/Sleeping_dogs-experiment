#!/usr/bin/env python3
"""Read-only PE32+ inspection for the independent native-port toolchain.

This parser deliberately does not execute or modify the input binary. It reports
machine/entry point, image layout, sections, imports, exports and base relocations.
"""
from __future__ import annotations
import argparse
import json
import struct
import sys
from pathlib import Path

MACHINE_NAMES = {0x8664: "AMD64", 0xAA64: "ARM64", 0x14C: "I386"}
DIR_NAMES = ["EXPORT", "IMPORT", "RESOURCE", "EXCEPTION", "SECURITY", "BASERELOC",
             "DEBUG", "ARCH", "GLOBALPTR", "TLS", "LOAD_CONFIG", "BOUND_IMPORT",
             "IAT", "DELAY_IMPORT", "COM_DESCRIPTOR", "RESERVED"]

class PEError(ValueError):
    pass

class PE:
    def __init__(self, data: bytes):
        self.data = data
        self.sections = []
        self.imports = []
        self.exports = []
        self.relocations = []
        self._parse_headers()

    def need(self, off, size):
        if off < 0 or size < 0 or off + size > len(self.data):
            raise PEError(f"truncated/out-of-range structure at 0x{off:x} size 0x{size:x}")

    def unpack(self, fmt, off):
        size = struct.calcsize(fmt); self.need(off, size)
        return struct.unpack_from(fmt, self.data, off)

    def cstr(self, off, limit=4096):
        self.need(off, 1)
        end = self.data.find(b"\0", off, min(len(self.data), off + limit))
        if end < 0: raise PEError(f"unterminated string at file offset 0x{off:x}")
        return self.data[off:end].decode("utf-8", "replace")

    def _parse_headers(self):
        if self.data[:2] != b"MZ": raise PEError("missing DOS MZ signature")
        peoff, = self.unpack("<I", 0x3c)
        if self.data[peoff:peoff+4] != b"PE\0\0": raise PEError("missing PE signature")
        self.need(peoff, 24)
        machine, nsec, timestamp, symptr, nsyms, optsize, chars = self.unpack("<HHIIIHH", peoff+4)
        self.machine = machine; self.section_count = nsec; self.timestamp = timestamp
        self.characteristics = chars
        opt = peoff + 24
        magic, = self.unpack("<H", opt)
        if magic != 0x20b: raise PEError(f"expected PE32+ (0x20b), got 0x{magic:x}")
        self.entry, = self.unpack("<I", opt+16)
        self.image_base, = self.unpack("<Q", opt+24)
        self.section_alignment, self.file_alignment = self.unpack("<II", opt+32)
        self.image_size, self.headers_size = self.unpack("<II", opt+56)
        ndirs, = self.unpack("<I", opt+108)
        self.directories = []
        for i in range(min(ndirs, 16)):
            rva, size = self.unpack("<II", opt+112+i*8)
            self.directories.append((rva, size))
        sec_off = opt + optsize
        for i in range(nsec):
            self.need(sec_off+i*40, 40)
            raw = self.data[sec_off+i*40:sec_off+(i+1)*40]
            name = raw[:8].split(b"\0",1)[0].decode("ascii","replace")
            vsize, va, rsize, rptr = struct.unpack_from("<IIII", raw, 8)
            flags, = struct.unpack_from("<I", raw, 36)
            self.sections.append({"name":name,"virtual_address":va,"virtual_size":vsize,
                                  "raw_offset":rptr,"raw_size":rsize,"characteristics":flags})
        self._parse_imports()
        self._parse_exports()
        self._parse_relocations()

    def rva_offset(self, rva, size=1):
        if rva < self.headers_size and rva + size <= len(self.data): return rva
        for s in self.sections:
            span = max(s["virtual_size"], s["raw_size"])
            if s["virtual_address"] <= rva and rva + size <= s["virtual_address"] + span:
                delta = rva - s["virtual_address"]
                if delta + size > s["raw_size"]: raise PEError(f"RVA 0x{rva:x} points into unbacked section data")
                off = s["raw_offset"] + delta; self.need(off,size); return off
        raise PEError(f"RVA 0x{rva:x} is not mapped to file data")

    def directory(self, idx):
        return self.directories[idx] if idx < len(self.directories) else (0,0)

    def _parse_imports(self):
        rva, size = self.directory(1)
        if not rva or not size: return
        off = self.rva_offset(rva, 20)
        for _ in range(min(size//20, 65536)):
            oft, stamp, chain, name_rva, ft = self.unpack("<IIIII", off)
            if not (oft or stamp or chain or name_rva or ft): break
            dll = self.cstr(self.rva_offset(name_rva))
            thunk_rva = oft or ft
            funcs=[]
            for n in range(65536):
                entoff=self.rva_offset(thunk_rva+n*8,8)
                value,=self.unpack("<Q",entoff)
                if not value: break
                if value & (1<<63): funcs.append({"ordinal":value & 0xffff})
                else:
                    noff=self.rva_offset(value & 0x7fffffffffffffff,3)
                    hint,=self.unpack("<H",noff)
                    funcs.append({"name":self.cstr(noff+2),"hint":hint})
            self.imports.append({"dll":dll,"functions":funcs})
            off += 20

    def _parse_exports(self):
        rva, size = self.directory(0)
        if not rva or not size: return
        off=self.rva_offset(rva,40)
        _,_,_,name_rva,base,nfunc,nname,funcs_rva,names_rva,ords_rva=self.unpack("<IIHHIIIIIII",off)
        fn_off=self.rva_offset(funcs_rva,nfunc*4) if nfunc else 0
        names_off=self.rva_offset(names_rva,nname*4) if nname else 0
        ords_off=self.rva_offset(ords_rva,nname*2) if nname else 0
        by_index={}
        for i in range(nname):
            nrva,=self.unpack("<I",names_off+i*4); oi,=self.unpack("<H",ords_off+i*2)
            by_index[oi]=self.cstr(self.rva_offset(nrva))
        for i in range(min(nfunc,200000)):
            frva,=self.unpack("<I",fn_off+i*4)
            if frva:
                self.exports.append({"ordinal":base+i,"name":by_index.get(i),"rva":frva,
                                     "forwarder":self.cstr(self.rva_offset(frva)) if rva <= frva < rva+size else None})

    def _parse_relocations(self):
        rva,size=self.directory(5)
        if not rva or not size: return
        off=self.rva_offset(rva,8); end=off+size; self.need(off,size)
        while off+8 <= end:
            page,block=self.unpack("<II",off)
            if page==0 and block==0: break
            if block<8 or block%2 or off+block>end: raise PEError("invalid base-relocation block")
            for p in range(off+8,off+block,2):
                item,=self.unpack("<H",p); typ=item>>12; delta=item&0xfff
                if typ: self.relocations.append({"type":typ,"rva":page+delta})
            off+=block

    def report(self):
        return {"format":"PE32+","machine":MACHINE_NAMES.get(self.machine, f"0x{self.machine:04x}"),
                "machine_id":self.machine,"timestamp":self.timestamp,"characteristics":self.characteristics,
                "entry_point_rva":self.entry,"image_base":f"0x{self.image_base:x}",
                "image_size":self.image_size,"headers_size":self.headers_size,
                "section_alignment":self.section_alignment,"file_alignment":self.file_alignment,
                "sections":self.sections,"imports":self.imports,"exports":self.exports,
                "base_relocations":{"count":len(self.relocations),"types":sorted({x["type"] for x in self.relocations}),
                                    "entries":self.relocations}}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("binary",type=Path)
    ap.add_argument("--summary",action="store_true",help="omit per-symbol import/export and relocation entries")
    args=ap.parse_args()
    try:
        result=PE(args.binary.read_bytes()).report()
        if args.summary:
            result["imports"]=[{"dll":x["dll"],"function_count":len(x["functions"])} for x in result["imports"]]
            result["exports"]={"count":len(result["exports"]),"named_count":sum(bool(x["name"]) for x in result["exports"])}
            result["base_relocations"].pop("entries",None)
        print(json.dumps(result,indent=2))
    except (OSError,PEError,struct.error) as e:
        print(f"pe_inspect: {e}",file=sys.stderr); return 2
    return 0
if __name__=="__main__": raise SystemExit(main())
