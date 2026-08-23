#!/bin/zsh
# Rasterize output/*.svg -> *.png at 2x via headless Chrome, driven by output/manifest.txt (name w h).
# Chrome occasionally hangs on exit after the screenshot is written; the watchdog waits for the
# PNG to appear and stabilize, then terminates the browser.
set -u
OUTDIR="$(cd "$(dirname "$0")/../output" && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
if [ ! -x "$CHROME" ]; then
  echo "Chrome not found at $CHROME (set CHROME=/path/to/chrome)" >&2
  exit 1
fi

while read fn w h; do
  svg="$OUTDIR/$fn"
  out="${svg%.svg}.png"
  rm -f "$out"
  prof=$(mktemp -d "${TMPDIR:-/tmp}/v32cr-XXXXXX")
  "$CHROME" --headless=new --user-data-dir="$prof" --no-first-run --disable-gpu \
    --hide-scrollbars --force-device-scale-factor=2 --window-size=$w,$h \
    --virtual-time-budget=3000 --timeout=10000 --screenshot="$out" "file://$svg" \
    < /dev/null > /dev/null 2>&1 &
  pid=$!
  # watchdog: wait for screenshot, confirm size stable, then reap the browser
  ok=0
  for i in {1..240}; do
    if [ -s "$out" ]; then
      s1=$(stat -f%z "$out"); sleep 1; s2=$(stat -f%z "$out")
      if [ "$s1" = "$s2" ]; then ok=1; break; fi
    fi
    if ! kill -0 $pid 2>/dev/null; then [ -s "$out" ] && ok=1; break; fi
    sleep 0.5
  done
  kill $pid 2>/dev/null
  wait $pid 2>/dev/null
  rm -rf "$prof"
  if [ $ok -eq 1 ]; then
    echo "$out $(stat -f%z "$out")"
  else
    echo "FAILED: $out" >&2
    exit 1
  fi
done < "$OUTDIR/manifest.txt"
