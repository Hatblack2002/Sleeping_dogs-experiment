package com.vertil.sleepingdogs;

import android.opengl.GLES30;
import android.opengl.GLSurfaceView;
import android.opengl.Matrix;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.FloatBuffer;
import javax.microedition.khronos.egl.EGLConfig;
import javax.microedition.khronos.opengles.GL10;

final class NativeLabRenderer implements GLSurfaceView.Renderer {
    private int program, vbo, mvpLoc, modelLoc, colorLoc, lightLoc;
    private final float[] projection=new float[16], view=new float[16], model=new float[16], vp=new float[16], mvp=new float[16];
    private volatile float yaw=25f, pitch=-12f;
    private long frames, start;
    private static final String VS="#version 300 es\nlayout(location=0) in vec3 aPos; layout(location=1) in vec3 aNormal; uniform mat4 uMVP; uniform mat4 uModel; out vec3 n; out vec3 p; void main(){ vec4 w=uModel*vec4(aPos,1.0); p=w.xyz; n=mat3(uModel)*aNormal; gl_Position=uMVP*vec4(aPos,1.0); }";
    private static final String FS="#version 300 es\nprecision highp float; in vec3 n; in vec3 p; uniform vec4 uColor; uniform vec3 uLight; out vec4 frag; void main(){ vec3 N=normalize(n); vec3 L=normalize(uLight-p); float d=max(dot(N,L),0.0); float rim=pow(1.0-max(dot(N,normalize(-p)),0.0),2.0); vec3 c=uColor.rgb*(0.22+0.78*d)+vec3(0.08,0.18,0.22)*rim; frag=vec4(c,1.0); }";
    private static final float[] CUBE={
      -1,-1,-1,0,0,-1, 1,-1,-1,0,0,-1, 1,1,-1,0,0,-1, -1,-1,-1,0,0,-1, 1,1,-1,0,0,-1, -1,1,-1,0,0,-1,
      -1,-1,1,0,0,1, 1,1,1,0,0,1, 1,-1,1,0,0,1, -1,-1,1,0,0,1, -1,1,1,0,0,1, 1,1,1,0,0,1,
      -1,-1,-1,-1,0,0, -1,1,1,-1,0,0, -1,-1,1,-1,0,0, -1,-1,-1,-1,0,0, -1,1,-1,-1,0,0, -1,1,1,-1,0,0,
      1,-1,-1,1,0,0, 1,-1,1,1,0,0, 1,1,1,1,0,0, 1,-1,-1,1,0,0, 1,1,1,1,0,0, 1,1,-1,1,0,0,
      -1,-1,-1,0,-1,0, 1,-1,1,0,-1,0, 1,-1,-1,0,-1,0, -1,-1,-1,0,-1,0, -1,-1,1,0,-1,0, 1,-1,1,0,-1,0,
      -1,1,-1,0,1,0, 1,1,-1,0,1,0, 1,1,1,0,1,0, -1,1,-1,0,1,0, 1,1,1,0,1,0, -1,1,1,0,1,0
    };
    private FloatBuffer cube;
    NativeLabRenderer() { cube=ByteBuffer.allocateDirect(CUBE.length*4).order(ByteOrder.nativeOrder()).asFloatBuffer(); cube.put(CUBE).position(0); }
    public void drag(float dx,float dy) { yaw+=dx*0.45f; pitch=Math.max(-70,Math.min(70,pitch+dy*0.35f)); }
    @Override public void onSurfaceCreated(GL10 gl,EGLConfig config) {
        GLES30.glClearColor(0.025f,0.055f,0.085f,1f); GLES30.glEnable(GLES30.GL_DEPTH_TEST); GLES30.glEnable(GLES30.GL_CULL_FACE);
        int vs=shader(GLES30.GL_VERTEX_SHADER,VS), fs=shader(GLES30.GL_FRAGMENT_SHADER,FS);
        program=GLES30.glCreateProgram(); GLES30.glAttachShader(program,vs); GLES30.glAttachShader(program,fs); GLES30.glLinkProgram(program);
        int[] ok={0}; GLES30.glGetProgramiv(program,GLES30.GL_LINK_STATUS,ok,0);
        if(ok[0]==0) throw new RuntimeException("GLES program link failed: "+GLES30.glGetProgramInfoLog(program));
        mvpLoc=GLES30.glGetUniformLocation(program,"uMVP"); modelLoc=GLES30.glGetUniformLocation(program,"uModel"); colorLoc=GLES30.glGetUniformLocation(program,"uColor"); lightLoc=GLES30.glGetUniformLocation(program,"uLight");
        int[] b={0}; GLES30.glGenBuffers(1,b,0); vbo=b[0]; GLES30.glBindBuffer(GLES30.GL_ARRAY_BUFFER,vbo); GLES30.glBufferData(GLES30.GL_ARRAY_BUFFER,CUBE.length*4,cube,GLES30.GL_STATIC_DRAW);
        start=System.nanoTime();
    }
    private int shader(int type,String src){int s=GLES30.glCreateShader(type); GLES30.glShaderSource(s,src); GLES30.glCompileShader(s); int[] ok={0}; GLES30.glGetShaderiv(s,GLES30.GL_COMPILE_STATUS,ok,0); if(ok[0]==0) throw new RuntimeException("GLES shader compile failed: "+GLES30.glGetShaderInfoLog(s)); return s;}
    @Override public void onSurfaceChanged(GL10 gl,int w,int h){GLES30.glViewport(0,0,w,h); Matrix.perspectiveM(projection,0,48f,(float)w/Math.max(1,h),0.1f,100f);}
    @Override public void onDrawFrame(GL10 gl){
        GLES30.glClear(GLES30.GL_COLOR_BUFFER_BIT|GLES30.GL_DEPTH_BUFFER_BIT);
        Matrix.setLookAtM(view,0,0,2.6f,8.8f,0,0,0,0,1,0);
        Matrix.multiplyMM(vp,0,projection,0,view,0); GLES30.glUseProgram(program); GLES30.glBindBuffer(GLES30.GL_ARRAY_BUFFER,vbo);
        GLES30.glEnableVertexAttribArray(0); GLES30.glEnableVertexAttribArray(1);
        GLES30.glVertexAttribPointer(0,3,GLES30.GL_FLOAT,false,24,0); GLES30.glVertexAttribPointer(1,3,GLES30.GL_FLOAT,false,24,12);
        float t=(System.nanoTime()-start)/1_000_000_000f;
        drawCube(-2.25f,-0.15f,0f,0.9f,0.9f,0.9f,0.10f,0.55f,0.72f);
        drawCube(0f,0.45f,0f,0.78f,1.35f,0.78f,0.85f,0.30f,0.12f);
        drawCube(2.1f,-0.35f,0f,0.72f,0.72f,0.72f,0.95f,0.68f,0.18f);
        drawCube(0f,-1.35f,-0.8f,3.5f,0.12f,2.0f,0.10f,0.22f,0.24f);
        frames++;
    }
    private void drawCube(float x,float y,float z,float sx,float sy,float sz,float r,float g,float b){
        Matrix.setIdentityM(model,0); Matrix.translateM(model,0,x,y,z); Matrix.rotateM(model,0,yaw,0,1,0); Matrix.rotateM(model,0,pitch,1,0,0); Matrix.scaleM(model,0,sx,sy,sz);
        Matrix.multiplyMM(mvp,0,vp,0,model,0); GLES30.glUniformMatrix4fv(mvpLoc,1,false,mvp,0); GLES30.glUniformMatrix4fv(modelLoc,1,false,model,0);
        GLES30.glUniform4f(colorLoc,r,g,b,1f); GLES30.glUniform3f(lightLoc,-3f,5f,5f); GLES30.glDrawArrays(GLES30.GL_TRIANGLES,0,36);
    }
}
