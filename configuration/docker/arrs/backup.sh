#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# backup.sh — archive the *arr stack state.
#
# What's included:
#   - config/             SQLite databases for every *arr app + SABnzbd
#                         (indexer settings, library metadata, API keys,
#                         download history, custom formats, notifications).
#   - .env                PUID/PGID/TZ values used at deployment time.
#   - docker-compose.yml  service definitions.
#
# What's excluded:
#   - media-data/         too large, regenerable from the indexer.
#
# The result is a timestamped tarball in backups/ that, combined with the
# images on Docker Hub, is enough to bring the whole stack back from scratch.
# -----------------------------------------------------------------------------

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

backup_directory="backups"
timestamp="$(date +%Y%m%dT%H%M%S)"
archive_path="${backup_directory}/arr-stack-${timestamp}.tar.gz"

mkdir -p "${backup_directory}"

# Build the include list dynamically so a partial setup (say, no .env yet)
# still produces a useful archive instead of erroring out.
include_paths=()
[[ -d config ]] && include_paths+=("config")
[[ -f .env ]] && include_paths+=(".env")
[[ -f docker-compose.yml ]] && include_paths+=("docker-compose.yml")

if [[ ${#include_paths[@]} -eq 0 ]]; then
	echo "ERROR: nothing to back up — config/, .env, and docker-compose.yml all missing." >&2
	exit 1
fi

echo "Archiving ${include_paths[*]} to ${archive_path}..."
tar -czf "${archive_path}" "${include_paths[@]}"

# du -h is portable across macOS BSD coreutils and GNU coreutils, unlike
# stat which has different flag syntax on each.
archive_size="$(du -h "${archive_path}" | cut -f1)"
echo "Backup complete: ${archive_path} (${archive_size})"

# Soft retention warning — never delete automatically (destructive).
backup_count="$(find "${backup_directory}" -maxdepth 1 -name 'arr-stack-*.tar.gz' | wc -l | tr -d ' ')"
if [[ ${backup_count} -gt 10 ]]; then
	echo
	echo "Note: ${backup_count} backups in ${backup_directory}/."
	echo "Consider pruning older ones manually."
fi

cat <<EOF

To restore from this archive:
    docker compose down
    rm -rf config/        # only if a corrupt config is what you're recovering from
    tar -xzf ${archive_path}
    docker compose up -d
EOF
