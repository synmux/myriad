# Optional services

Two services that aren't part of the default stack but can be added when
needed. Each is the K8s translation of the matching commented-out
service in the project root `docker-compose.yml`.

| Manifest                   | What it deploys                            | Replaces                            |
| -------------------------- | ------------------------------------------ | ----------------------------------- |
| `gluetun-qbittorrent.yaml` | Multi-container Pod: gluetun + qBittorrent | Compose's `gluetun` + `qbittorrent` |
| `plundrio.yaml`            | put.io download client (Transmission RPC)  | Compose's `plundrio`                |

Both register with the \*arr apps as download clients via Prowlarr's
"Settings → Download Clients" page. Service names within the cluster:

- qBittorrent (via gluetun): `http://qbittorrent:8082`
- plundrio: `http://plundrio:9091`

## Prerequisites

The base stack (parent directory) must be applied first — these manifests
reference the `arr-stack` namespace, the `arr-stack-config` ConfigMap,
and the `media-data` PVC.

```bash
cd ..
kubectl apply -k .            # base stack
cd optional
```

## Step 1 — create the Secret(s)

```bash
cp secret.example.yaml secret.yaml
$EDITOR secret.yaml           # fill in real values
kubectl apply -f secret.yaml
```

`secret.yaml` is gitignored. The example file contains placeholders for
both `vpn-credentials` (gluetun) and `putio-credentials` (plundrio); you
only need to fill in the credentials for the services you're enabling.

If you want only one of the two, edit the kustomization to drop the
other manifest before applying:

```yaml
# kustomization.yaml
resources:
  - plundrio.yaml # only plundrio, no gluetun
```

## Step 2 — apply

```bash
kubectl apply -k .
kubectl -n arr-stack get pods -w
```

For gluetun-qbittorrent, watch the gluetun container's logs to confirm
the VPN tunnel comes up before configuring it as a download client:

```bash
kubectl -n arr-stack logs -f deploy/gluetun-qbittorrent -c gluetun
# look for "Healthy! ... DNS lookup ... working"
```

## Step 3 — register with Prowlarr

Port-forward Prowlarr if you haven't:

```bash
kubectl -n arr-stack port-forward svc/prowlarr 9696:9696
```

Then in Prowlarr → Settings → Download Clients → Add:

### qBittorrent (via gluetun)

- Type: **qBittorrent**
- Host: `qbittorrent` (the Service name; not `gluetun-qbittorrent`)
- Port: `8082`
- Username/Password: as configured in qBit's web UI on first run

### plundrio

- Type: **Transmission**
- Host: `plundrio`
- Port: `9091`
- URL Base: `/transmission`
- Category: e.g. `tv-sonarr`, `movies-radarr`, `music-lidarr`

Prowlarr pushes the new download client to all connected \*arr apps on
save.

## Verifying the gluetun killswitch

```bash
# Should show the VPN exit IP (NOT your home IP)
kubectl -n arr-stack exec deploy/gluetun-qbittorrent -c qbittorrent -- \
  wget -qO- ifconfig.me
echo
```

If that returns your real IP, gluetun isn't routing qBit's traffic.
Don't download anything until the killswitch is verified.

## Why the qBittorrent Pod is named `gluetun-qbittorrent`

The Deployment manages a single Pod containing two containers
(`gluetun` and `qbittorrent`). The name reflects that — there's no
separate qBittorrent Pod to deploy. The Service that the \*arr apps
connect to is named `qbittorrent` (matches what they expect to type).

This is the K8s equivalent of Compose's `network_mode: "service:gluetun"`
trick, expressed in K8s vocabulary: same network namespace, achieved by
co-locating in one Pod instead of by referencing another container's
network mode.
