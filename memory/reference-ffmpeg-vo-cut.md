---
name: reference-ffmpeg-vo-cut
description: "ffmpeg gotcha — put -ss BEFORE -i when cutting VO segments with afade, or the fade runs on original timestamps and silences the clip"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 33bb43b4-c232-415a-b741-3929b64ec3f5
  modified: 2026-09-11T08:34:07.951Z
---

When slicing a VO line out of a longer ElevenLabs file with ffmpeg **and**
applying `afade`, put `-ss <start> -t <dur>` **before** `-i` (input-side seek,
resets output PTS to 0). If `-ss` goes *after* `-i` (output seek), the filter
timeline keeps the original PTS, so `afade=t=out:st=<dur-x>` fires immediately
and **silences every clip that starts past ~1.7s.**

This bit me on the graph episode: 90% of the VO rendered silent (only the first
line of each voice survived), because I used `-i file -ss X -to Y -af afade…`.

**Correct form:**
```
ffmpeg -ss $START -t $DUR -i in.mp3 \
  -af "afade=t=in:st=0:d=0.03,afade=t=out:st=$(DUR-0.08):d=0.08" out.mp3
```
Verify after cutting with `volumedetect` (mean_volume of -91 dB = silent clip).
Whisper (`openai-whisper`, base model) with `word_timestamps=True` gives the
start/end boundaries per line.
