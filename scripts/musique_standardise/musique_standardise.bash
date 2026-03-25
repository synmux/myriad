#!/usr/bin/env bash
set -uo pipefail

SRC="/Users/dave/work/musique"
DST="/Users/dave/work/musique.clean"

converted=0
copied=0
errors=0

while IFS= read -r -d '' file; do
	rel="${file#"$SRC"/}"
	dest="$DST/$rel"
	mkdir -p "$(dirname "$dest")"

	ext="${file##*.}"
	ext_lower="$(echo "$ext" | tr '[:upper:]' '[:lower:]')"

	case "$ext_lower" in
	flac)
		# ffprobe csv gives: sample_rate,bits_per_raw_sample
		info=$(ffprobe -v quiet -select_streams a:0 \
			-show_entries stream=sample_rate,bits_per_raw_sample \
			-of csv=p=0:s=, "$file" 2>/dev/null || true)
		sr=$(echo "$info" | cut -d',' -f1 | tr -cd '0-9')
		bits=$(echo "$info" | cut -d',' -f2 | tr -cd '0-9')

		if [[ $sr == "44100" && $bits == "16" ]]; then
			cp -p "$file" "$dest"
			copied=$((copied + 1))
		else
			if ffmpeg -nostdin -y -hide_banner -loglevel error \
				-i "$file" \
				-map 0 \
				-map_metadata 0 \
				-c:v copy \
				-c:a flac -ar 44100 -sample_fmt s16 \
				"$dest"; then
				converted=$((converted + 1))
				echo "CONVERTED: $rel  (was ${bits:-?}bit/${sr:-?}Hz)"
			else
				errors=$((errors + 1))
				echo "ERROR: $rel"
			fi
		fi
		;;
	m4a)
		# ffprobe csv gives: codec_name,sample_rate
		info=$(ffprobe -v quiet -select_streams a:0 \
			-show_entries stream=codec_name,sample_rate \
			-of csv=p=0:s=, "$file" 2>/dev/null || true)
		codec=$(echo "$info" | cut -d',' -f1 | tr -cd 'a-z0-9')
		sr=$(echo "$info" | cut -d',' -f2 | tr -cd '0-9')

		if [[ $sr == "44100" && $codec == "aac" ]]; then
			cp -p "$file" "$dest"
			copied=$((copied + 1))
		else
			if ffmpeg -nostdin -y -hide_banner -loglevel error \
				-i "$file" \
				-map 0 \
				-map_metadata 0 \
				-c:v copy \
				-c:a aac -b:a 256k -ar 44100 \
				-movflags +faststart \
				"$dest"; then
				converted=$((converted + 1))
				echo "CONVERTED: $rel  (was ${codec}/${sr}Hz)"
			else
				errors=$((errors + 1))
				echo "ERROR: $rel"
			fi
		fi
		;;
	*)
		# Non-audio file (lrc, jpg, m3u, etc.) — just copy
		cp -p "$file" "$dest"
		copied=$((copied + 1))
		;;
	esac
done < <(find "$SRC" -type f ! -name '.DS_Store' -print0)

echo ""
echo "Done. Converted: $converted  Copied: $copied  Errors: $errors"
