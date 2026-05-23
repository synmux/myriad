#!/usr/bin/env bash
#
# ytdlp-parallel.sh — download a (large) YouTube playlist with several parallel
# yt-dlp workers, each shown live in its own tmux pane.
#
# How it works:
#   1. Read cookies from your browser ONCE and flatten the playlist to a list
#      of video URLs.
#   2. Distribute those URLs round-robin across N chunk files.
#   3. Open a tmux window with one pane per chunk; each pane runs
#      `yt-dlp -a <chunk>` so its live progress is visible.
#
# A shared --download-archive makes every run resumable: finished videos are
# skipped, and anything that failed (deleted/private/throttled) is retried the
# next time you run the script with the same output directory.
#
# Targets bash (works with the bash 3.2 that ships on macOS). Needs: yt-dlp, tmux.

set -euo pipefail

# ---- defaults ---------------------------------------------------------------
jobs=4
playlist_url="https://www.youtube.com/playlist?list=WL" # Watch Later
output_dir="./downloads"
browser="chrome"
remux_format="mp4"
fragments=1

script_name="$(basename "$0")"

# ---- helpers ----------------------------------------------------------------
usage() {
	cat <<USAGE
$script_name — download a YouTube playlist with parallel yt-dlp workers in tmux.

Usage: $script_name [options]
  -j, --jobs N        parallel workers / tmux panes (default: $jobs)
  -u, --url URL       playlist URL (default: Watch Later, list=WL)
  -o, --output DIR    output directory (default: $output_dir)
  -b, --browser NAME  browser to read cookies from (default: $browser)
  -f, --format EXT    remux container; pass '' to disable (default: $remux_format)
  -N, --fragments N   concurrent fragments per worker, speeds up DASH/HLS (default: $fragments)
  -h, --help          show this help and exit

Every run is resumable thanks to a shared download-archive. Re-run the same
command to pick up where a previous run stopped. Delete the archive file
(printed on launch) to force a full re-download.
USAGE
}

die() {
	printf 'error: %s\n' "$1" >&2
	exit 1
}

note() {
	printf '==> %s\n' "$1"
}

warn() {
	printf 'warning: %s\n' "$1" >&2
}

# ---- argument parsing -------------------------------------------------------
# Supports both "--opt value" and "--opt=value", plus short forms.
while [ "$#" -gt 0 ]; do
	case "$1" in
	-j | --jobs)
		jobs="$2"
		shift 2
		;;
	-u | --url)
		playlist_url="$2"
		shift 2
		;;
	-o | --output)
		output_dir="$2"
		shift 2
		;;
	-b | --browser)
		browser="$2"
		shift 2
		;;
	-f | --format)
		remux_format="$2"
		shift 2
		;;
	-N | --fragments)
		fragments="$2"
		shift 2
		;;
	-h | --help)
		usage
		exit 0
		;;
	--jobs=*)
		jobs="${1#*=}"
		shift
		;;
	--url=*)
		playlist_url="${1#*=}"
		shift
		;;
	--output=*)
		output_dir="${1#*=}"
		shift
		;;
	--browser=*)
		browser="${1#*=}"
		shift
		;;
	--format=*)
		remux_format="${1#*=}"
		shift
		;;
	--fragments=*)
		fragments="${1#*=}"
		shift
		;;
	*) die "unknown option: $1 (try --help)" ;;
	esac
done

# ---- validation -------------------------------------------------------------
case "$jobs" in
'' | *[!0-9]*) die "--jobs must be a positive integer (got '$jobs')" ;;
esac
[ "$jobs" -ge 1 ] || die "--jobs must be at least 1"

case "$fragments" in
'' | *[!0-9]*) die "--fragments must be a positive integer (got '$fragments')" ;;
esac
[ "$fragments" -ge 1 ] || die "--fragments must be at least 1"

for required_tool in yt-dlp tmux; do
	command -v "$required_tool" >/dev/null 2>&1 ||
		die "required tool not found: $required_tool (install with: brew install $required_tool)"
done

# ---- paths ------------------------------------------------------------------
# Make the output directory absolute so tmux panes resolve it regardless of cwd.
case "$output_dir" in
/*) ;;
*) output_dir="$PWD/$output_dir" ;;
esac

state_dir="$output_dir/.ytdlp-state"
cookie_file="$state_dir/cookies.txt"
archive_file="$state_dir/archive.txt"
urls_file="$state_dir/urls.txt"
worker_script="$state_dir/worker.sh"

mkdir -p "$output_dir" "$state_dir"

# ---- step 1: cookies + URL extraction --------------------------------------
# Passing both --cookies-from-browser and --cookies makes yt-dlp read the
# browser once and write a reusable cookie file, so the workers don't all
# fight over the browser's locked cookie database.
note "Reading cookies from '$browser' and flattening playlist…"
set +e
yt-dlp \
	--cookies-from-browser "$browser" \
	--cookies "$cookie_file" \
	--flat-playlist \
	--print url \
	"$playlist_url" >"$urls_file"
extract_status=$?
set -e

if [ ! -s "$urls_file" ]; then
	die "no video URLs extracted (yt-dlp exit $extract_status). Are you signed in to YouTube in $browser? On macOS you may need to grant Keychain access or quit $browser first."
fi

url_count="$(grep -c . "$urls_file" || true)"
note "Found $url_count videos."

# Prefer the exported cookie file; fall back to live browser reads if yt-dlp
# did not write one (then warn, because parallel browser reads can contend).
if [ -s "$cookie_file" ]; then
	cookie_args=(--cookies "$cookie_file")
	note "Cookies exported to $cookie_file (holds your YouTube session — keep it private)."
else
	cookie_args=(--cookies-from-browser "$browser")
	warn "No cookie file written; workers will read '$browser' directly (slower, may contend on the browser)."
fi

# ---- step 2: split URLs round-robin into chunks -----------------------------
# Round-robin (NR % jobs) interleaves the list so each worker gets a similar mix
# of short and long videos rather than one worker copping a heavy contiguous run.
rm -f "$state_dir"/chunk.*.txt
awk -v dir="$state_dir" -v workers="$jobs" '
  { chunk = sprintf("%s/chunk.%d.txt", dir, NR % workers); print > chunk }
' "$urls_file"

chunk_files=()
for chunk in "$state_dir"/chunk.*.txt; do
	[ -s "$chunk" ] || continue
	chunk_files+=("$chunk")
done
[ "${#chunk_files[@]}" -ge 1 ] || die "no chunk files were produced from $urls_file"

worker_count="${#chunk_files[@]}"
note "Launching $worker_count worker(s)."
if [ "$worker_count" -gt 8 ]; then
	warn "More than 8 workers: YouTube may throttle you (HTTP 429) and tmux may run out of pane space. A lower --jobs is usually faster overall."
fi

# ---- step 3: build the per-worker yt-dlp invocation -------------------------
ytdlp_args=("${cookie_args[@]}")
ytdlp_args+=(--download-archive "$archive_file")          # resume + skip finished videos
ytdlp_args+=(--concurrent-fragments "$fragments")         # intra-video parallelism (DASH/HLS)
ytdlp_args+=(--ignore-errors --no-overwrites)             # survive dead/private videos
ytdlp_args+=(-o "$output_dir/%(title)s [%(id)s].%(ext)s") # [id] keeps names unique
[ -n "$remux_format" ] && ytdlp_args+=(--remux-video "$remux_format")

# Generate a worker script. The static parts come from quoted heredocs (so $1
# etc. stay literal); the resolved yt-dlp arguments are written one-per-line via
# printf '%q', which safely re-quotes paths/templates back into a bash array.
cat >"$worker_script" <<'WORKER_HEADER'
#!/usr/bin/env bash
set -uo pipefail
chunk_file="$1"
echo "▶ worker starting on: $chunk_file"
ytdlp_args=(
WORKER_HEADER

printf '  %q\n' "${ytdlp_args[@]}" >>"$worker_script"

cat >>"$worker_script" <<'WORKER_FOOTER'
)
yt-dlp "${ytdlp_args[@]}" -a "$chunk_file"
status=$?
echo
echo "✔ worker finished: $chunk_file (yt-dlp exit ${status})"
WORKER_FOOTER
chmod +x "$worker_script"

# ---- step 4: launch the tmux session ---------------------------------------
session="ytdlp-$$"

# If anything below fails before we hand control over, tear the session down so
# we don't leave an orphaned, half-built session behind.
cleanup_on_error() {
	tmux kill-session -t "$session" 2>/dev/null || true
}
trap cleanup_on_error ERR

tmux new-session -d -s "$session" -n downloads
tmux set-window-option -t "$session" pane-border-status top
tmux set-window-option -t "$session" pane-border-format ' #{pane_title} '

# We already have pane #1; add one pane per remaining chunk, re-tiling after
# each split so tmux keeps reclaiming space (avoids "no space for new pane").
pane_index=1
while [ "$pane_index" -lt "$worker_count" ]; do
	tmux split-window -t "$session"
	tmux select-layout -t "$session" tiled >/dev/null
	pane_index=$((pane_index + 1))
done
tmux select-layout -t "$session" tiled >/dev/null

# Collect stable pane IDs (%0, %3, …) — independent of the user's pane-base-index.
pane_ids=()
while IFS= read -r pane_id; do
	pane_ids+=("$pane_id")
done < <(tmux list-panes -t "$session" -F '#{pane_id}')

# Dispatch one worker into each pane and title the pane border.
dispatch_index=0
while [ "$dispatch_index" -lt "$worker_count" ]; do
	target_pane="${pane_ids[$dispatch_index]}"
	target_chunk="${chunk_files[$dispatch_index]}"
	chunk_lines="$(grep -c . "$target_chunk" || true)"
	tmux select-pane -t "$target_pane" -T "worker $((dispatch_index + 1)) · ${chunk_lines} videos"
	tmux send-keys -t "$target_pane" "bash $(printf '%q' "$worker_script") $(printf '%q' "$target_chunk")" C-m
	dispatch_index=$((dispatch_index + 1))
done

# ---- step 5: hand the session over -----------------------------------------
note "tmux session: $session"
note "Output dir:   $output_dir"
note "Archive:      $archive_file  (delete to force a full re-download)"
echo
echo "Inside tmux:  detach = Ctrl-b then d   ·   kill everything = tmux kill-session -t $session"
echo "Panes stay open showing each worker's summary when done. Re-run this command to resume."
echo

trap - ERR
if [ -n "${TMUX-}" ]; then
	# Already inside tmux: switch the current client to the new session.
	tmux switch-client -t "$session"
elif [ -t 1 ]; then
	tmux attach-session -t "$session"
else
	note "Not attached to a terminal; session left running. Attach with: tmux attach -t $session"
fi
