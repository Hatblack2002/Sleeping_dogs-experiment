package com.vertil.sleepingdogs;

import android.app.Activity;
import android.opengl.GLSurfaceView;
import android.os.Bundle;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.graphics.Color;
import android.view.Window;
import android.view.WindowManager;

public final class MainActivity extends Activity {
    static { System.loadLibrary("nativeprobe"); }
    private static native String vulkanProbe();
    private GLSurfaceView surface;
    private NativeLabRenderer renderer;
    private TextView status;
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        FrameLayout root = new FrameLayout(this);
        surface = new GLSurfaceView(this);
        surface.setEGLContextClientVersion(3);
        renderer = new NativeLabRenderer();
        surface.setRenderer(renderer);
        surface.setRenderMode(GLSurfaceView.RENDERMODE_CONTINUOUSLY);
        root.addView(surface, new FrameLayout.LayoutParams(-1, -1));
        status = new TextView(this);
        status.setTextColor(Color.WHITE);
        status.setTextSize(14);
        status.setPadding(20, 14, 20, 14);
        status.setBackgroundColor(0x9908121b);
        status.setText("SLEEPING DOGS · NATIVE GRAPHICS LAB  |  OpenGL ES 3");
        FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(-2, -2, Gravity.TOP | Gravity.LEFT);
        root.addView(status, lp);
        TextView controls = new TextView(this);
        controls.setText("TOUCH: rotate scene     •     TEST BUILD — NOT GAMEPLAY");
        controls.setTextColor(Color.WHITE);
        controls.setTextSize(13);
        controls.setPadding(20, 12, 20, 12);
        controls.setBackgroundColor(0x9908121b);
        FrameLayout.LayoutParams cp = new FrameLayout.LayoutParams(-2, -2, Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL);
        root.addView(controls, cp);
        surface.setOnTouchListener(new View.OnTouchListener() {
            float lastX, lastY;
            public boolean onTouch(View v, MotionEvent e) {
                if (e.getAction() == MotionEvent.ACTION_DOWN) { lastX=e.getX(); lastY=e.getY(); return true; }
                if (e.getAction() == MotionEvent.ACTION_MOVE) {
                    renderer.drag(e.getX()-lastX, e.getY()-lastY);
                    lastX=e.getX(); lastY=e.getY(); return true;
                }
                return true;
            }
        });
        setContentView(root);
        status.post(() -> status.setText(vulkanProbe()));
    }
    @Override protected void onPause() { super.onPause(); if(surface!=null) surface.onPause(); }
    @Override protected void onResume() { super.onResume(); if(surface!=null) surface.onResume(); }
}
