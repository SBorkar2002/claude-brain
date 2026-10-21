"""
Prepare a generated head for the film and print the numbers spec.py needs.

    python3 v10/sleephead.py ~/Downloads/whatever.png [outname]

Keys the flat background out (see keying.py -- generated art arrives on solid
grey or white and otherwise paints a rectangle over the scene), trims it, and
solves for the aspect ratio, scale and offset that make its FACE land in exactly
the same place at exactly the same size as face.png. Without that, swapping poses
reads as the head jumping and resizing rather than as an expression change.
"""
import os
import sys

from PIL import Image

import keying

PLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "public", "v10", "plates")


def main(src, name="face-sleep.png"):
    im = keying.trim(keying.key(Image.open(src)))
    out = os.path.join(PLATES, name)
    im.save(out)

    awake = keying.trim(keying.key(Image.open(os.path.join(PLATES, "face.png"))))
    aw, acx, acy = keying.head(awake)
    sw, scx, scy = keying.head(im)

    ar = im.width / im.height
    # make the sleeping face as wide as the awake face, in rendered pixels
    scale = (aw / sw) * (im.height / awake.height)
    print(f"wrote {out}  {im.width}x{im.height}")
    print(f"  awake head {aw}px wide, centred ({acx},{acy}) in {awake.width}x{awake.height}")
    print(f"  this  head {sw}px wide, centred ({scx},{scy}) in {im.width}x{im.height}")
    print()
    print("paste into spec.PLAIN['head']:")
    print(f"    awake_ar={awake.width / awake.height:.4f}, "
          f"awake_dx={0.5 - acx / awake.width:+.4f}, awake_dy={0.5 - acy / awake.height:+.4f},")
    print(f"    asleep_ar={ar:.4f}, asleep_scale={scale:.4f}, "
          f"asleep_dx={0.5 - scx / im.width:+.4f}, asleep_dy={0.5 - scy / im.height:+.4f},")


if __name__ == "__main__":
    if not 2 <= len(sys.argv) <= 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
