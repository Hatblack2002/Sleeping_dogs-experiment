import importlib.util
import struct
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("pe_inspect", Path(__file__).parents[1] / "tools" / "pe_inspect.py")
pe_inspect = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pe_inspect)

def minimal_pe():
    data=bytearray(0x400)
    data[:2]=b"MZ"
    struct.pack_into("<I",data,0x3c,0x80)
    data[0x80:0x84]=b"PE\0\0"
    struct.pack_into("<HHIIIHH",data,0x84,0x8664,1,0x12345678,0,0,0xf0,0x22)
    o=0x98
    struct.pack_into("<H",data,o,0x20b)
    struct.pack_into("<I",data,o+16,0x1000)
    struct.pack_into("<Q",data,o+24,0x140000000)
    struct.pack_into("<II",data,o+32,0x1000,0x200)
    struct.pack_into("<II",data,o+56,0x2000,0x200)
    struct.pack_into("<I",data,o+108,16)
    s=o+0xf0
    data[s:s+8]=b".text\0\0\0"
    struct.pack_into("<IIII",data,s+8,0x100,0x1000,0x200,0x200)
    struct.pack_into("<I",data,s+36,0x60000020)
    data[0x200:0x204]=b"\x90\x90\xc3\0"
    return bytes(data)

class PEInspectorTests(unittest.TestCase):
    def test_parses_pe32_plus_headers_and_sections(self):
        result=pe_inspect.PE(minimal_pe()).report()
        self.assertEqual(result["format"],"PE32+")
        self.assertEqual(result["machine"],"AMD64")
        self.assertEqual(result["entry_point_rva"],0x1000)
        self.assertEqual(result["sections"][0]["name"],".text")
        self.assertEqual(result["image_base"],"0x140000000")

    def test_rejects_non_pe_input(self):
        with self.assertRaises(pe_inspect.PEError):
            pe_inspect.PE(b"not a PE")

    def test_rejects_truncated_section_data(self):
        data=bytearray(minimal_pe())
        struct.pack_into("<I",data,0x98+0xf0+20,0xfffffff0)
        with self.assertRaises(pe_inspect.PEError):
            pe_inspect.PE(bytes(data)).rva_offset(0x1000,4)

if __name__=="__main__":
    unittest.main()
