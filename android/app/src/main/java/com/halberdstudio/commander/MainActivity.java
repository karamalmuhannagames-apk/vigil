package com.halberdstudio.commander;

import android.app.Activity;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.view.WindowManager;
import android.webkit.RenderProcessGoneDetail;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.window.OnBackInvokedDispatcher;
import androidx.webkit.WebSettingsCompat;
import androidx.webkit.WebViewAssetLoader;
import androidx.webkit.WebViewFeature;

/**
 * The game's shell. The whole game is the web app in assets/, served from a private local address.
 * Nothing Android-default is ever shown: no system error pages, no long-press menus, no zoom controls,
 * no instant close on Back, and a crash of the page engine restarts the game instead of closing it.
 */
public class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final String START = "https://" + HOST + "/assets/app/start.html";
    private static final String PROBLEM = "https://" + HOST + "/assets/app/problem.html";
    private WebView web;
    private WebViewAssetLoader loader;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        Window w = getWindow();
        w.getDecorView().setBackgroundColor(Color.BLACK);
        w.addFlags(WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            w.getAttributes().layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
        }
        loader = new WebViewAssetLoader.Builder()
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();
        web = makeWebView();
        setContentView(web);
        hideSystemBars();
        if (Build.VERSION.SDK_INT >= 33) {
            getOnBackInvokedDispatcher().registerOnBackInvokedCallback(OnBackInvokedDispatcher.PRIORITY_DEFAULT, this::handleBack);
        }
        if (state != null && web.restoreState(state) != null) return;
        web.loadUrl(START);
    }

    private WebView makeWebView() {
        WebView v = new WebView(this);
        v.setBackgroundColor(Color.BLACK);
        v.setOverScrollMode(View.OVER_SCROLL_NEVER);
        v.setVerticalScrollBarEnabled(false);
        v.setHorizontalScrollBarEnabled(false);
        v.setLongClickable(false);
        v.setOnLongClickListener(x -> true);
        v.setHapticFeedbackEnabled(false);
        WebSettings s = v.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setTextZoom(100);
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        s.setSupportMultipleWindows(false);
        if (WebViewFeature.isFeatureSupported(WebViewFeature.ALGORITHMIC_DARKENING)) {
            WebSettingsCompat.setAlgorithmicDarkeningAllowed(s, false);
        }
        v.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                WebResourceResponse r = loader.shouldInterceptRequest(request.getUrl());
                String path = request.getUrl().getPath();
                if (r != null && path != null) {
                    if (path.endsWith(".js") || path.endsWith(".mjs")) r.setMimeType("text/javascript");
                    else if (path.endsWith(".ogg")) r.setMimeType("audio/ogg");
                    else if (path.endsWith(".json")) r.setMimeType("application/json");
                }
                return r;
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return !HOST.equals(request.getUrl().getHost());
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                if (request.isForMainFrame()) showProblem("load");
            }

            @Override
            public void onReceivedHttpError(WebView view, WebResourceRequest request, WebResourceResponse response) {
                if (request.isForMainFrame()) showProblem("missing");
            }

            @Override
            public boolean onRenderProcessGone(WebView view, RenderProcessGoneDetail detail) {
                // The page engine stopped (low memory or a crash): rebuild it and start again, never close the app.
                ViewGroup parent = (ViewGroup) view.getParent();
                if (parent != null) parent.removeView(view);
                view.destroy();
                web = makeWebView();
                setContentView(web);
                web.loadUrl(START + "?restart=1");
                return true;
            }
        });
        return v;
    }

    private void showProblem(String kind) {
        if (web.getUrl() != null && web.getUrl().startsWith(PROBLEM)) return;
        web.loadUrl(PROBLEM + "?kind=" + kind);
    }

    /** Back goes back inside the game; on the first screen it sends the game to the background (never kills it). */
    private void handleBack() {
        web.evaluateJavascript("(window.gameBack && window.gameBack()) ? 'handled' : 'home'", result -> {
            if (result == null || !result.contains("handled")) moveTaskToBack(true);
        });
    }

    @SuppressWarnings("deprecation")
    @Override
    public void onBackPressed() { handleBack(); }

    private void hideSystemBars() {
        if (Build.VERSION.SDK_INT >= 30) {
            WindowInsetsController c = getWindow().getInsetsController();
            if (c != null) {
                c.hide(WindowInsets.Type.statusBars() | WindowInsets.Type.navigationBars());
                c.setSystemBarsBehavior(WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
            }
        } else {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_FULLSCREEN
                    | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                    | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN);
        }
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) hideSystemBars();
    }

    @Override
    protected void onSaveInstanceState(Bundle out) { super.onSaveInstanceState(out); web.saveState(out); }

    @Override
    protected void onPause() {
        super.onPause();
        web.evaluateJavascript("document.dispatchEvent(new Event('appPause'))", null);
        web.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        web.onResume();
        web.evaluateJavascript("document.dispatchEvent(new Event('appResume'))", null);
        hideSystemBars();
    }

    @Override
    protected void onDestroy() {
        if (web != null) web.destroy();
        super.onDestroy();
    }
}
