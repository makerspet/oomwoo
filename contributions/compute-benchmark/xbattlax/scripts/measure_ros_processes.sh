#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  measure_ros_processes.sh --pattern REGEX [options]

Options:
  --pattern REGEX      Process command-line regex to sample. Required.
  --duration SECONDS   Total sample duration. Default: 30.
  --interval SECONDS   Seconds between samples. Default: 1.
  --label LABEL        Free-form label written to each row. Default: run.
  --output FILE        CSV output path. Default: stdout.
  --help               Show this help.

Examples:
  bash measure_ros_processes.sh \
    --pattern 'ros2|component_container|python3|slam_toolbox|nav2' \
    --duration 60 \
    --interval 2 \
    --label slam_5hz_baseline \
    --output /tmp/oomwoo-slam-5hz-baseline.csv

Notes:
  This script is intended for Linux ROS2 targets. It reads /proc for RSS and
  PSS. PSS is blank when /proc/<pid>/smaps_rollup is not readable.
EOF
}

pattern=""
duration="30"
interval="1"
label="run"
output=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pattern)
      pattern="${2:-}"
      shift 2
      ;;
    --duration)
      duration="${2:-}"
      shift 2
      ;;
    --interval)
      interval="${2:-}"
      shift 2
      ;;
    --label)
      label="${2:-}"
      shift 2
      ;;
    --output)
      output="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$pattern" ]]; then
  echo "--pattern is required" >&2
  usage >&2
  exit 2
fi

if [[ ! -d /proc ]]; then
  echo "This sampler requires Linux /proc." >&2
  exit 1
fi

if ! [[ "$duration" =~ ^[0-9]+$ ]] || [[ "$duration" -lt 1 ]]; then
  echo "--duration must be a positive integer" >&2
  exit 2
fi

if ! [[ "$interval" =~ ^[0-9]+$ ]] || [[ "$interval" -lt 1 ]]; then
  echo "--interval must be a positive integer" >&2
  exit 2
fi

csv_escape() {
  local value="${1:-}"
  value="${value//$'\n'/ }"
  value="${value//$'\r'/ }"
  value="${value//\"/\"\"}"
  printf '"%s"' "$value"
}

read_status_kib() {
  local pid="$1"
  local key="$2"
  awk -v key="$key" '$1 == key ":" { print $2; found=1; exit } END { if (!found) print "" }' "/proc/$pid/status" 2>/dev/null || true
}

read_pss_kib() {
  local pid="$1"
  if [[ -r "/proc/$pid/smaps_rollup" ]]; then
    awk '$1 == "Pss:" { print $2; found=1; exit } END { if (!found) print "" }' "/proc/$pid/smaps_rollup" 2>/dev/null || true
  fi
}

read_cmdline() {
  local pid="$1"
  if [[ -r "/proc/$pid/cmdline" ]]; then
    tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null | sed 's/[[:space:]]*$//'
  fi
}

read_comm() {
  local pid="$1"
  if [[ -r "/proc/$pid/comm" ]]; then
    tr -d '\n' < "/proc/$pid/comm" 2>/dev/null
  fi
}

read_cpu_percent() {
  local pid="$1"
  ps -p "$pid" -o %cpu= 2>/dev/null | awk '{ print $1 }'
}

emit_header() {
  printf 'timestamp_utc,sample_index,label,pid,comm,cpu_percent,rss_kib,pss_kib,cmdline\n'
}

emit_row() {
  local timestamp="$1"
  local sample_index="$2"
  local pid="$3"
  local comm="$4"
  local cpu_percent="$5"
  local rss_kib="$6"
  local pss_kib="$7"
  local cmdline="$8"

  printf '%s,%s,' "$timestamp" "$sample_index"
  csv_escape "$label"
  printf ',%s,' "$pid"
  csv_escape "$comm"
  printf ',%s,%s,%s,' "$cpu_percent" "$rss_kib" "$pss_kib"
  csv_escape "$cmdline"
  printf '\n'
}

run_sampler() {
  local sample_index=0
  local started="$SECONDS"

  emit_header

  while (( SECONDS - started <= duration )); do
    local timestamp
    timestamp="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"

    mapfile -t pids < <(
      for proc in /proc/[0-9]*; do
        pid="${proc##*/}"
        cmdline="$(read_cmdline "$pid")"
        if [[ -n "$cmdline" && "$cmdline" =~ $pattern ]]; then
          printf '%s\n' "$pid"
        fi
      done
    )

    if [[ "${#pids[@]}" -eq 0 ]]; then
      emit_row "$timestamp" "$sample_index" "" "no_process_match" "" "" "" ""
    else
      local pid
      for pid in "${pids[@]}"; do
        if [[ ! -d "/proc/$pid" ]]; then
          continue
        fi
        emit_row \
          "$timestamp" \
          "$sample_index" \
          "$pid" \
          "$(read_comm "$pid")" \
          "$(read_cpu_percent "$pid")" \
          "$(read_status_kib "$pid" VmRSS)" \
          "$(read_pss_kib "$pid")" \
          "$(read_cmdline "$pid")"
      done
    fi

    sample_index=$((sample_index + 1))
    if (( SECONDS - started >= duration )); then
      break
    fi
    sleep "$interval"
  done
}

if [[ -n "$output" ]]; then
  mkdir -p "$(dirname "$output")"
  run_sampler > "$output"
else
  run_sampler
fi
