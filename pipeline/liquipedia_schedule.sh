#!/bin/bash
# Schedule the daily Liquipedia fetch on macOS (launchd).
#
#   bash pipeline/liquipedia_schedule.sh start    # Sat/Sun/Mon from 00:00 KST: fetch the previous Korean day
#   bash pipeline/liquipedia_schedule.sh stop     # remove the schedule
#   bash pipeline/liquipedia_schedule.sh status
#   bash pipeline/liquipedia_schedule.sh run      # make launchd run the job once now
#
# launchd wakes the job every hour on the hour (it works in Mac local time, so this keeps the KST
# schedule right through daylight saving). On Korean Sat/Sun/Mon the job fetches the previous Korean
# day once every match of that day is finished on Liquipedia; until then it retries the next hour.
# Output: tmp/liquipedia/<date>/{match_info,series,potm}.csv (+ .done), log: tmp/liquipedia/fetch.log
set -euo pipefail

LABEL="com.owcsstatlab.liquipedia-daily"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$REPO/tmp/liquipedia/fetch.log"

case "${1:-}" in
  start)
    PYTHON="$(command -v python3)"
    mkdir -p "$HOME/Library/LaunchAgents" "$REPO/tmp/liquipedia"
    cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>WorkingDirectory</key><string>$REPO</string>
  <key>EnvironmentVariables</key><dict><key>PYTHON</key><string>$PYTHON</string></dict>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>$REPO/pipeline/liquipedia_schedule.sh</string><string>tick</string></array>
  <key>StartCalendarInterval</key><dict><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict>
</plist>
PLIST
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
    launchctl bootstrap "gui/$(id -u)" "$PLIST"
    echo "scheduled: Sat/Sun/Mon 00:00 KST -> $REPO/tmp/liquipedia/<date>/ (log: tmp/liquipedia/fetch.log)"
    ;;
  stop)
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
    rm -f "$PLIST"
    echo "stopped: schedule removed"
    ;;
  status)
    if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then echo "scheduled ($PLIST)"; else echo "not scheduled"; fi
    ;;
  run)
    launchctl kickstart -p "gui/$(id -u)/$LABEL"
    ;;
  tick)  # called by launchd every hour
    case "$(TZ=Asia/Seoul date +%u)" in 6|7|1) ;; *) exit 0 ;; esac  # Korean Sat, Sun, Mon
    DAY="$(TZ=Asia/Seoul date -v-1d +%F)"
    [ -f "$REPO/tmp/liquipedia/$DAY/.done" ] && exit 0
    echo "=== $(date '+%F %T %Z') fetching $DAY (KST)"
    if "${PYTHON:-python3}" pipeline/fetch_liquipedia.py --date "$DAY"; then
      touch "$REPO/tmp/liquipedia/$DAY/.done"
    else
      echo "not complete yet; retrying next hour"
    fi
    ;;
  *)
    sed -n '2,13p' "$0"; exit 1
    ;;
esac
