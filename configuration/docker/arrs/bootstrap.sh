#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# bootstrap.sh — prepare the *arr stack on a fresh host.
#
# What it does (idempotent — safe to re-run):
#   1. Copies env.template to .env if .env doesn't already exist.
#   2. Creates the media-data/ and config/ directory tree expected by
#      docker-compose.yml.
#   3. Sets ownership of those directories to PUID:PGID from .env so the
#      linuxserver.io containers can write into them without permission
#      churn on first import.
#
# Run from the project directory:
#
#     ./bootstrap.sh
#
# If file ownership matters on your host (typical Linux server) and your
# user is not root, re-run under sudo so the chown step succeeds:
#
#     sudo ./bootstrap.sh
# -----------------------------------------------------------------------------

set -euo pipefail

# Resolve the project root from the script location so the script works no
# matter where it's invoked from.
project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$project_root"

# -----------------------------------------------------------------------------
# Step 1 — .env initialisation
# -----------------------------------------------------------------------------
if [[ ! -f .env ]]; then
	if [[ ! -f env.template ]]; then
		echo "ERROR: env.template not found in $project_root." >&2
		echo "Cannot create .env. Aborting." >&2
		exit 1
	fi
	cp env.template .env
	echo "Created .env from env.template."
else
	echo ".env already exists; leaving it alone."
fi

# Source the env file so we can read PUID/PGID. The defaults below match
# the ${VAR:-default} fallbacks in docker-compose.yml so behaviour is
# consistent whether or not .env defines the values explicitly.
# shellcheck disable=SC1091
source .env
target_uid="${PUID:-1000}"
target_gid="${PGID:-1000}"

# -----------------------------------------------------------------------------
# Step 2 — directory tree
# -----------------------------------------------------------------------------
# TRaSH Guides layout: every container mounts /data on the same host root,
# so SABnzbd's complete folder and the *arr libraries share a filesystem
# and can hardlink between each other.
media_directories=(
	"media-data/usenet/incomplete"
	"media-data/usenet/complete/tv"
	"media-data/usenet/complete/movies"
	"media-data/usenet/complete/music"
	# Pre-created for the optional plundrio (put.io) service. Sibling of
	# usenet/ so torrent and Usenet downloads stay visually separated while
	# remaining on the same filesystem (preserves hardlink capability).
	"media-data/torrents/complete/tv"
	"media-data/torrents/complete/movies"
	"media-data/torrents/complete/music"
	"media-data/media/tv"
	"media-data/media/movies"
	"media-data/media/music"
)

config_directories=(
	"config/prowlarr"
	"config/sabnzbd"
	"config/sonarr"
	"config/radarr"
	"config/lidarr"
	"config/bazarr"
	# Pre-created so they're ready when gluetun + qbittorrent are uncommented
	# in docker-compose.yml. Empty directories cost nothing on disk and save
	# an ownership dance on activation day.
	"config/gluetun"
	"config/qbittorrent"
	"config/plundrio"
)

echo "Creating directory tree..."
for directory in "${media_directories[@]}" "${config_directories[@]}"; do
	mkdir -p "$directory"
done

# -----------------------------------------------------------------------------
# Step 3 — ownership
# -----------------------------------------------------------------------------
# Only root can chown to an arbitrary UID. If we're already that UID, the
# created directories already have the right owner. Otherwise, attempt the
# chown and degrade gracefully if it fails so the script stays idempotent.
current_uid="$(id -u)"
if [[ $current_uid -eq 0 ]] || [[ $current_uid -eq $target_uid ]]; then
	if chown -R "${target_uid}:${target_gid}" media-data config 2>/dev/null; then
		echo "Ownership set to ${target_uid}:${target_gid}."
	else
		echo "WARNING: chown failed even though running as UID $current_uid." >&2
		echo "         Containers may hit permission errors on first run." >&2
	fi
else
	cat <<EOF >&2
Skipping chown: running as UID $current_uid, target is ${target_uid}.
Directories were created but not re-owned. If your *arr containers can't
write into them, re-run with sudo:

    sudo ./bootstrap.sh

(On macOS with Docker Desktop you can ignore this — the Linux VM
normalises ownership across the boundary.)
EOF
fi

# -----------------------------------------------------------------------------
# Step 4 — summary
# -----------------------------------------------------------------------------
echo
echo "Bootstrap complete. Tree:"
find media-data config -type d 2>/dev/null | sort | sed 's|^|  |'
echo
echo "Next steps:"
echo "  1. Review .env (PUID/PGID/TZ)."
echo "  2. docker compose up -d"
echo "  3. Configure SABnzbd → Prowlarr (add DrunkenSlug + apps + SAB) → done."
