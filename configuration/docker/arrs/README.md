# \*arr stack

Self-hosted Usenet media automation, deployed via Docker Compose. Prowlarr
manages indexers centrally and pushes configuration to Sonarr, Radarr,
Lidarr, and Bazarr. SABnzbd handles the actual downloads. The stack is
pre-wired for the [DrunkenSlug](https://drunkenslug.com) indexer.

## Architecture

```plaintext
                  +-------------+
                  |  Prowlarr   |  ← single point of indexer management
                  |  :9696      |     (DrunkenSlug API key lives here)
                  +------+------+
                         | API push (indexer + download client config)
                         | — Bazarr is NOT pushed to; see below
        +----------------+---------+
        |          |               |
   +----v----+ +---v----+ +----v---+
   | Sonarr  | | Radarr | | Lidarr |
   | :8989   | | :7878  | | :8686  |
   +----+----+ +---+----+ +----+---+
        |          |           |
        |  search via Prowlarr API
        |  send NZB to SABnzbd
        |          |           |
        +----------v-----------+
                   |
              +----v----+
              | SABnzbd |  downloads to /data/usenet/complete/<cat>
              | :8080   |
              +----+----+
                   |
                   | hardlink (same /data mount)
                   v
            /data/media/{tv,movies,music}
                   ^
                   | reads libraries, writes subtitles next to media
                   |
              +----+----+
              | Bazarr  |  configured manually against
              | :6767   |  Sonarr & Radarr APIs (NOT Prowlarr)
              +---------+
```

Every container that touches media mounts the same host directory at
`/data` — Sonarr, Radarr, Lidarr, Bazarr, SABnzbd (and qBittorrent or
plundrio when enabled). Prowlarr is the only *arr app that doesn't:
it manages indexers via APIs and never reads or writes media. The
shared `/data` mount is what makes hardlinking work between SABnzbd's
`complete/` folder and the *arr libraries — atomic moves and zero
duplication on disk.

## What's included

| Service          | Port | Purpose                                          |
| ---------------- | ---- | ------------------------------------------------ |
| Prowlarr         | 9696 | Indexer manager — DrunkenSlug lives here         |
| SABnzbd          | 8080 | Usenet downloader                                |
| Sonarr           | 8989 | TV automation                                    |
| Radarr           | 7878 | Movie automation                                 |
| Lidarr           | 8686 | Music automation                                 |
| Bazarr           | 6767 | Subtitle automation                              |
| gluetun          | —    | VPN gateway — _disabled by default_ (see below)  |
| qBittorrent      | 8082 | Torrent client routed via gluetun — _disabled_   |
| plundrio         | 9091 | put.io as a Transmission RPC client — _disabled_ |
| broadlinkmanager | —    | Pre-existing service, untouched                  |

## Prerequisites

- Docker (with Compose v2 — `docker compose`, not `docker-compose`)
- A DrunkenSlug account and API key
- ~10 GB free for the stack itself; plan separately for media

## Quick start

```bash
./bootstrap.sh        # creates .env, directory tree, sets ownership
make up               # docker compose up -d
```

If `make` isn't your style:

```bash
docker compose up -d
```

## Configuration

After the stack is up, configure in this order. The order matters because
each step depends on the previous service being reachable.

### 1. SABnzbd — http://localhost:8080

On first launch SABnzbd runs a setup wizard:

- **Server**: enter your Usenet provider's NNTP details (host, port, username,
  password, connections).
- **Folders**: set Temporary Download Folder to `/data/usenet/incomplete` and
  Completed Download Folder to `/data/usenet/complete`.
- Note the API key under **Config → General → Security** — you'll need it
  for Prowlarr.

### 2. Prowlarr — http://localhost:9696

Prowlarr is the spine of the stack. Configure once, sync to everything.

**Add the indexer:**

- **Indexers → Add Indexer → DrunkenSlug** (or pick the Newznab preset and
  fill in `https://drunkenslug.com`).
- Paste your DrunkenSlug API key. Test, then save.

**Register the \*arr apps:**

- **Settings → Apps → Add** — one entry each for Sonarr, Radarr, Lidarr.
  (Bazarr is _not_ in Prowlarr's Apps list — it's a subtitle add-on, not
  a media manager. It's configured separately in step 4.)
- Use the container names as hostnames since all services share
  `arr-network`:
  - Sonarr: `http://sonarr:8989`
  - Radarr: `http://radarr:7878`
  - Lidarr: `http://lidarr:8686`
- The API key for each \*arr app is found in its own UI under
  **Settings → General**.
- Click Test, then Save. Prowlarr immediately pushes the DrunkenSlug
  indexer to that app.

**Register the download client:**

- **Settings → Download Clients → Add → SABnzbd**.
- Host: `sabnzbd`, Port: `8080`, API key: the one from step 1.
- Save. Prowlarr pushes the SABnzbd config to every registered \*arr app.

### 3. \*arr apps

Most configuration is now inherited from Prowlarr. Verify in each app:

- **Indexers** — DrunkenSlug should appear, marked as managed by Prowlarr.
- **Download Clients** — SABnzbd should appear.
- **Media Management → Root Folders** — add `/data/media/tv` (Sonarr),
  `/data/media/movies` (Radarr), `/data/media/music` (Lidarr).

### 4. Bazarr

Bazarr is the odd one out — it doesn't talk to Prowlarr. Configure
manually:

- **Settings → Sonarr** — `http://sonarr:8989` and Sonarr's API key.
- **Settings → Radarr** — `http://radarr:7878` and Radarr's API key.
- **Settings → Languages → Subtitles Languages** — pick your preferences.
- **Settings → Providers** — enable a few subtitle sources (OpenSubtitles,
  Subscene, etc).

## Future: torrent support via gluetun

The compose file ships with `gluetun` (a VPN gateway) and `qBittorrent`
(a torrent client) defined as commented-out services. The Usenet path
covered above doesn't need a VPN; this section is only for adding
BitTorrent later.

### Why a VPN for torrents but not Usenet

Usenet traffic is a single encrypted TCP connection from your machine to
your news provider — your IP is shared with one company under contract,
not with random peers. BitTorrent is peer-to-peer, so every other client
in a swarm sees your IP and your ISP can fingerprint the traffic. A VPN
with a _killswitch_ is the standard safety measure: if the tunnel drops
mid-download, gluetun's built-in firewall blocks all traffic dead instead
of leaking your real IP into the swarm.

### Architecture

```plaintext
                +-----------------------------+
                | gluetun container           |
                |   - VPN tunnel (WireGuard)  |
                |   - killswitch firewall     |
                |   +---------------------+   |
                |   | qBittorrent process |   |  shares gluetun's
                |   | (no own network)    |   |  network namespace
                |   +---------------------+   |
                +--------------+--------------+
                               |
                  arr-network DNS: gluetun:8082
                               |
            Sonarr/Radarr/Prowlarr ──► download client
```

The decisive bit: qBittorrent uses `network_mode: "service:gluetun"`,
which means it has _no_ network interfaces of its own. It sees
gluetun's interfaces, including the VPN tunnel. The side effect every
newcomer hits — qBit's web UI is reachable at `http://gluetun:8082`,
**not** `http://qbittorrent:8082`, because qBit's container name has no
network to attach DNS to.

### Enabling the stack

1. **Choose a VPN provider** with WireGuard support if possible (faster
   and simpler than OpenVPN). Mullvad and ProtonVPN are common picks for
   the \*arr ecosystem because both support port forwarding (improves
   torrent peer connectivity) and have anonymous payment options.
2. **Fill in `.env`** with VPN credentials. See `env.example.template`
   for worked examples covering Mullvad WireGuard, ProtonVPN WireGuard,
   and NordVPN OpenVPN.
3. **Uncomment the `gluetun` and `qbittorrent` blocks** in
   `docker-compose.yml`. Both must be uncommented together — qBit
   depends on gluetun.
4. **Bring them up:**

   ```bash
   docker compose up -d gluetun qbittorrent
   make logs-gluetun     # confirm "VPN is up" before doing anything else
   ```

5. **Get the qBittorrent password**: linuxserver.io's qBit image prints
   a temporary password in the logs on first boot. Read it with
   `make logs-qbittorrent` and log in at <http://localhost:8082> to
   change it.
6. **Register qBittorrent in Prowlarr** → Settings → Download Clients →
   Add → qBittorrent:
   - Host: `gluetun` (not `qbittorrent`!)
   - Port: `8082`
   - Username/Password: from step 5
   - Category: leave blank or use `tv-sonarr`, `movies-radarr`, etc.
     so the \*arr apps can filter their downloads.
7. Prowlarr will push the qBit config to Sonarr/Radarr/Lidarr alongside
   the existing SABnzbd config. The *arr apps then have *two\* download
   clients and will pick whichever has the better release for each grab.

### Verifying the killswitch

A quick paranoia check after enabling:

```bash
# qBit's external IP — should match the VPN exit, not your home IP
docker compose exec qbittorrent curl -s ifconfig.me
echo                                            # newline, ifconfig.me omits one

# Your host's external IP — should NOT match
curl -s ifconfig.me
echo
```

If those two match, the VPN isn't routing qBit's traffic and you should
stop and debug before downloading anything.

## Future: cloud torrenting via put.io

The compose file ships with a second commented torrent option:
[`plundrio`](https://github.com/elsbrock/plundrio), a put.io client that
implements the Transmission RPC API so the \*arr apps can talk to it
exactly as they would a local Transmission daemon.

### Why this is fundamentally different from gluetun + qBittorrent

| Concern              | gluetun + qBittorrent            | plundrio + put.io                        |
| -------------------- | -------------------------------- | ---------------------------------------- |
| Where P2P happens    | Your machine                     | put.io's servers                         |
| Your IP in swarm?    | Yes (VPN-masked)                 | No, never                                |
| Local CPU/RAM        | qBit + VPN overhead              | None for downloading, just HTTPS pull    |
| Local bandwidth used | Full (download + seed back)      | Download only (no seeding from your end) |
| Cost                 | VPN subscription (~£3-7/mo)      | put.io subscription (~£8-15/mo)          |
| Trust model          | VPN provider sees encrypted blob | put.io sees what you download            |
| Dependency           | VPN tunnel must be up            | put.io must be up                        |
| Killswitch concern   | Critical (gluetun firewall)      | Not applicable (no swarm exposure)       |

The two are **not** mutually exclusive. Both can be enabled and registered
as separate download clients in the \*arr apps; Sonarr/Radarr will pick
whichever offers a better release per grab. Or you can pick exactly one,
and leave the other commented.

### Why plundrio over putioarr

Both projects bridge put.io to the \*arr download-client interface via
Transmission RPC. plundrio was chosen here because:

- More active maintenance (last commit ~April 2026 vs ~March 2026 for
  putioarr).
- Cleaner issue backlog (3 vs 11 open).
- Pure environment-variable configuration — no TOML config file to keep
  in sync. Docker Compose-friendly.
- Stateless design supports parallel workers (`PLDR_WORKERS`) for fast
  pulls from put.io's edge.
- *arr-side configuration stays in the *arr apps, not duplicated into the
  proxy. Single source of truth.

### Architecture

```plaintext
   Sonarr/Radarr/Prowlarr  ──Transmission RPC──►  plundrio (port 9091)
                                                         │
                                                         │ put.io API
                                                         ▼
                                                   put.io cloud
                                                  (peers, swarm,
                                                   seeding done here)
                                                         │
                                                         │ HTTPS pull
                                                         ▼
                                          /data/torrents/complete/<release>
                                                         │
                                                         │ hardlink
                                                         ▼
                                              /data/media/{tv,movies,music}
```

The bind-mount layout puts plundrio's completion directory
(`/data/torrents/complete/...`) under the same `media-data/` host root
that Sonarr/Radarr use. That's what keeps hardlinks working — exactly
the same trick we use for SABnzbd's `/data/usenet/complete/`.

### Enabling plundrio

1. **Get a put.io OAuth token.**
   - Sign in at <https://put.io>, then visit <https://app.put.io/oauth>.
   - Click "Create New Application", give it any name (e.g.
     `plundrio-arr`), and use `http://localhost` for the callback URL
     (plundrio doesn't use it).
   - The application's "OAuth Token" field is your `PUTIO_TOKEN`.
2. **Set `PUTIO_TOKEN`** in `.env` (uncomment the put.io section).
3. **Uncomment the `plundrio:` block** in `docker-compose.yml`.
4. **Bring it up:**

   ```bash
   docker compose up -d plundrio
   make logs-plundrio    # confirm "auth OK" / no token errors
   ```

5. **Register in Prowlarr** → Settings → Download Clients → Add →
   **Transmission**:
   - Host: `plundrio`
   - Port: `9091`
   - URL Base: `/transmission` (Transmission's default)
   - Category: `tv-sonarr`, `movies-radarr`, `music-lidarr` per \*arr app
   - Save → Prowlarr pushes the config to every connected \*arr app.

6. **Set the \*arr root folders** (if not already set during initial
   configuration). Since put.io completes go to
   `/data/torrents/complete/<category>/<release>`, \*arr's auto-import
   will pick them up — the existing `/data/media/<type>` root folder is
   the destination, not the source.

## File layout

```plaintext
.
├── docker-compose.yml          # service definitions
├── env.template                # copy to .env, edit
├── env.example.template        # annotated reference for env.template
├── bootstrap.sh                # one-shot setup
├── backup.sh                   # archive config/ + .env + compose
├── Makefile                    # task shortcuts
├── README.md                   # this file
├── .gitignore                  # ignores secrets, state, archives
├── data/                       # broadlinkmanager state (existing)
├── config/                     # *arr app state (created by bootstrap)
│   ├── prowlarr/
│   ├── sabnzbd/
│   ├── sonarr/
│   ├── radarr/
│   ├── lidarr/
│   ├── bazarr/
│   ├── gluetun/                # empty until gluetun service is enabled
│   ├── qbittorrent/            # empty until qBittorrent service is enabled
│   └── plundrio/               # empty until plundrio (put.io) is enabled
├── media-data/                 # shared /data mount (created by bootstrap)
│   ├── usenet/                 # SABnzbd
│   │   ├── incomplete/
│   │   └── complete/{tv,movies,music}/
│   ├── torrents/               # plundrio (put.io), when enabled
│   │   └── complete/{tv,movies,music}/
│   └── media/{tv,movies,music}/
└── backups/                    # produced by backup.sh
```

## Common operations

| Task                    | Command            |
| ----------------------- | ------------------ |
| Start                   | `make up`          |
| Stop                    | `make down`        |
| Restart all             | `make restart`     |
| Update images           | `make pull`        |
| Status                  | `make ps`          |
| All logs                | `make logs`        |
| Single service logs     | `make logs-sonarr` |
| Backup config           | `make backup`      |
| Render resolved compose | `make config`      |

Run `make` with no arguments for the full list with descriptions.

## Backup and restore

`./backup.sh` (or `make backup`) creates a timestamped tarball in
`backups/` containing `config/`, `.env`, and `docker-compose.yml`.
Combined with the images on Docker Hub, this is enough to rebuild the
entire stack on a new host.

To restore:

```bash
docker compose down
rm -rf config/                 # only if you're recovering from corruption
tar -xzf backups/arr-stack-YYYYMMDDTHHMMSS.tar.gz
docker compose up -d
```

`media-data/` is intentionally not backed up — media is regenerable from
the indexer, the library is large, and the \*arr apps will re-import any
files they find in their root folders on next scan.

## Troubleshooting

**Sonarr can't reach SABnzbd / Prowlarr can't reach Sonarr.**
Use container names, not `localhost`. From inside any container,
`http://sabnzbd:8080` works because all services are on `arr-network`.
`localhost` inside a container points at the container itself.

**Permission denied writing to /data/media/...**
PUID/PGID in `.env` doesn't match the host user that owns `media-data/`.
Re-run `sudo ./bootstrap.sh` to chown, or edit `.env` to match the
existing owner (`stat -c %u media-data` on Linux, `stat -f %u media-data`
on macOS).

**Sonarr is copying files instead of hardlinking, doubling disk usage.**
SABnzbd and Sonarr must see the same filesystem under `/data`. Check
that both services have the `./media-data:/data` mount and that nothing
points elsewhere (e.g. `/downloads` or `/tv`).

**Sonarr can't reach qBittorrent at `http://qbittorrent:8082`.**
qBittorrent runs in gluetun's network namespace and has no network of
its own — `qbittorrent` doesn't resolve on `arr-network`. Use
`http://gluetun:8082` instead. This is the most common gluetun-pattern
gotcha.

**plundrio logs say `401 Unauthorized` from put.io.**
The `PUTIO_TOKEN` in `.env` is wrong, expired, or has been revoked. Visit
<https://app.put.io/oauth>, open your application, and copy the OAuth
Token field again (not the API Key — they're separate things on the
put.io side). Restart plundrio after updating `.env`:
`docker compose up -d plundrio`.

**plundrio downloads complete on put.io but files never reach `/data/torrents/complete/`.**
Most often a permission issue: plundrio is writing as a UID that can't
create files under `media-data/torrents/`. Either run
`sudo ./bootstrap.sh` again to chown the tree, or comment out the
`user:` line in plundrio's compose block and let it run as root (less
ideal but unblocks you).

**`*arr` says the Transmission download client is unreachable.**
Check the URL Base — Sonarr/Radarr default to `/transmission/` for
Transmission, which is what plundrio expects. Also confirm the host is
`plundrio` (the container name on `arr-network`), not `localhost`.

**gluetun container starts but qBittorrent can't reach the internet.**
Check the gluetun logs (`make logs-gluetun`) for VPN auth errors. The
killswitch is doing its job: blocking all traffic until the tunnel is
established. Bad WireGuard keys or a dead VPN server are the usual
culprits.

**Prowlarr pushed an indexer but Sonarr doesn't see it.**
Hit **Settings → Indexers → Sync App Indexers** in Prowlarr. The push
on Save sometimes races with the \*arr app starting up.

**`docker compose` says version mismatch / unknown directive.**
You're on Compose v1. The `x-arr-common` YAML anchor and `services`
top-level extensions need Compose v2. Either upgrade to Docker Desktop
recent or install the `docker-compose-plugin` package.

## Credits

- [TRaSH Guides](https://trash-guides.info) — the canonical reference for
  \*arr folder structure, hardlinks, and quality profiles.
- [Servarr Wiki](https://wiki.servarr.com) — official documentation for
  the \*arr family.
- [linuxserver.io](https://www.linuxserver.io) — the container images used
  here.
