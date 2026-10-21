import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);

// Remotion's bundled chrome-headless-shell ships unsigned and this Mac's
// endpoint security SIGKILLs it on launch (exit 137 -- it cannot even print
// --version). The installed Google Chrome is signed, so it survives. Without
// this line every render dies and the whole pipeline looks broken.
Config.setBrowserExecutable(
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
);

// Rendering with the default worker pool fails on this machine -- the workers
// visit localhost:3000 and get no response. A single worker renders fine.
Config.setConcurrency(1);
