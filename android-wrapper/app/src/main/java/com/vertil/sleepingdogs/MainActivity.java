package com.vertil.sleepingdogs;

import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.Typeface;
import android.net.Uri;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

public final class MainActivity extends Activity {
    private static final String[] WINLATOR_PACKAGES = {
        "com.winlator",
        "com.winlator.cmod"
    };

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.rgb(16, 20, 25));
        getWindow().setNavigationBarColor(Color.rgb(16, 20, 25));
        getWindow().getDecorView().setSystemUiVisibility(0);

        LinearLayout page = new LinearLayout(this);
        page.setOrientation(LinearLayout.VERTICAL);
        page.setPadding(dp(24), dp(28), dp(24), dp(24));
        page.setBackgroundColor(Color.rgb(16, 20, 25));
        page.setGravity(Gravity.CENTER_VERTICAL);

        TextView eyebrow = text("ANDROID COMPATIBILITY EXPERIMENT", 12, Color.rgb(135, 166, 190));
        eyebrow.setLetterSpacing(0.08f);
        page.addView(eyebrow);

        TextView title = text("SLEEPING DOGS", 30, Color.WHITE);
        title.setTypeface(Typeface.create("sans-serif-condensed", Typeface.BOLD));
        title.setPadding(0, dp(10), 0, dp(2));
        page.addView(title);

        TextView subtitle = text("Definitive Edition · launcher prototype", 16, Color.rgb(202, 211, 219));
        page.addView(subtitle);

        View rule = new View(this);
        rule.setBackgroundColor(Color.rgb(64, 86, 103));
        LinearLayout.LayoutParams ruleParams = new LinearLayout.LayoutParams(-1, dp(1));
        ruleParams.setMargins(0, dp(24), 0, dp(22));
        page.addView(rule, ruleParams);

        TextView explanation = text(
            "This app does not contain the game or an emulator. It checks for a compatible Winlator installation and opens it so you can configure your legally owned PC game files.",
            16, Color.rgb(220, 226, 232));
        explanation.setLineSpacing(dp(4), 1.0f);
        page.addView(explanation);

        Button launch = new Button(this);
        launch.setText("OPEN WINLATOR");
        launch.setAllCaps(false);
        launch.setTextSize(16);
        LinearLayout.LayoutParams buttonParams = new LinearLayout.LayoutParams(-1, dp(54));
        buttonParams.setMargins(0, dp(26), 0, dp(10));
        page.addView(launch, buttonParams);
        launch.setOnClickListener(v -> openWinlator());

        Button download = new Button(this);
        download.setText("GET OFFICIAL WINLATOR");
        download.setAllCaps(false);
        download.setTextSize(14);
        page.addView(download, new LinearLayout.LayoutParams(-1, dp(48)));
        download.setOnClickListener(v ->
            startActivity(new Intent(Intent.ACTION_VIEW,
                Uri.parse("https://github.com/brunodev85/winlator/releases"))));

        TextView note = text(
            "Next test gate: launch HKShip.exe from a Winlator container, then record menu, gameplay, controls, audio and sustained performance on the target phone.",
            13, Color.rgb(158, 172, 184));
        note.setPadding(0, dp(24), 0, 0);
        page.addView(note);

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.addView(page);
        setContentView(scroll);
    }

    private void openWinlator() {
        PackageManager pm = getPackageManager();
        for (String packageName : WINLATOR_PACKAGES) {
            try {
                Intent launch = pm.getLaunchIntentForPackage(packageName);
                if (launch != null) {
                    launch.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    startActivity(launch);
                    return;
                }
            } catch (RuntimeException ignored) {
                // Continue checking known package identifiers.
            }
        }
        Toast.makeText(this,
            "Winlator was not detected. Install it from the official release page first.",
            Toast.LENGTH_LONG).show();
        startActivity(new Intent(Intent.ACTION_VIEW,
            Uri.parse("https://github.com/brunodev85/winlator/releases")));
    }

    private TextView text(String value, int size, int color) {
        TextView view = new TextView(this);
        view.setText(value);
        view.setTextSize(size);
        view.setTextColor(color);
        return view;
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }
}
