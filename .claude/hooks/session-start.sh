#!/bin/bash
# Installs what the video skills (ghost-editor, motion-design, lemo-opuscar) need in a cloud session.
# Idempotent: every step is skipped when already done. A failed optional step is reported, not fatal.
set -uo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

SK="$CLAUDE_PROJECT_DIR/.claude/skills"
PIP="pip3 install --break-system-packages --quiet --disable-pip-version-check"
warn() { echo "! $*" >&2; }

# 1. Python tools: ghost-editor (whisper, opencv, yt-dlp, google-genai) and motion-design (playwright, imageio-ffmpeg)
python3 - <<'PY' 2>/dev/null || $PIP openai-whisper opencv-python-headless yt-dlp google-genai playwright imageio-ffmpeg pillow numpy || warn "pip install failed"
import whisper, cv2, yt_dlp, google.genai, playwright, imageio_ffmpeg, PIL, numpy
cv2.FaceDetectorYN
PY

# 2. lemo-opuscar: style library in ~/lemo-opuscar plus its Node/Python packages
LEMO="$SK/lemo-opuscar/scripts/setup.sh"
sh "$LEMO" >/dev/null || warn "lemo-opuscar library download failed"

# The proxy blocks cdn.playwright.dev, so point the revision lemo's playwright expects at the preinstalled headless shell.
link_headless_shell() {
  local bj="$HOME/lemo-opuscar/node_modules/playwright-core/browsers.json"
  [ -f "$bj" ] || return 0
  local rev src dst
  rev=$(node -p "require('$bj').browsers.find(b => b.name === 'chromium-headless-shell').revision")
  dst="${PLAYWRIGHT_BROWSERS_PATH:-$HOME/.cache/ms-playwright}/chromium_headless_shell-$rev"
  [ -e "$dst/INSTALLATION_COMPLETE" ] && return 0
  src=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-linux 2>/dev/null | sort -V | tail -1)
  [ -n "$src" ] || { warn "no preinstalled headless shell to link"; return 0; }
  mkdir -p "$dst/chrome-headless-shell-linux64"
  for f in "$src"/*; do ln -sfn "$f" "$dst/chrome-headless-shell-linux64/"; done
  ln -sfn "$src/headless_shell" "$dst/chrome-headless-shell-linux64/chrome-headless-shell"
  touch "$dst/DEPENDENCIES_VALIDATED" "$dst/INSTALLATION_COMPLETE"
}
# First pass installs node_modules (its browser download may fail), then link the browser and finish the venv.
sh "$LEMO" deps >/dev/null 2>&1 || true
link_headless_shell
sh "$LEMO" deps | tail -3 || warn "lemo-opuscar deps failed"

# 3. ghost-editor sound effects and music (needs assets.mixkit.co in the environment's allowed domains)
GE="$SK/ghost-editor"
if [ "$(ls "$GE"/library/sfx/*.wav 2>/dev/null | wc -l)" -lt 30 ] || ! ls "$GE"/library/music/*.mp3 >/dev/null 2>&1; then
  python3 "$GE/scripts/library_restore.py" >/dev/null 2>&1 || warn "ghost-editor sfx/music not downloaded (is assets.mixkit.co allowed?)"
fi

exit 0
