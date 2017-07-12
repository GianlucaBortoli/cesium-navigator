var options = {
    /* options, if any */
};
// Setup tracing with the given options.
wtf.trace.prepare(options);
// Optionally, create the on-screen HUD for better control.
wtf.hud.prepare(options);
// Start recording a trace immediately (if desired).
wtf.trace.start(options);