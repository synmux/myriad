# \*arr stack on Kubernetes

A Kubernetes port of the Docker Compose stack at the project root. Same
services, same hardlink-friendly storage layout, same DrunkenSlug + SABnzbd
configuration story. Translated into K8s primitives:

| Compose                       | Kubernetes                                        |
| ----------------------------- | ------------------------------------------------- |
| service                       | Deployment + Service                              |
| `./config/<app>:/config`      | per-app PersistentVolumeClaim (RWO, 1Gi)          |
| `./media-data:/data` (shared) | one PersistentVolumeClaim (RWX) bound to all pods |
| custom bridge `arr-network`   | the `arr-stack` namespace + Service DNS           |
| `.env`                        | ConfigMap (PUID/PGID/TZ) + Secret (VPN, put.io)   |
| `network_mode: service:X`     | multi-container Pod (gluetun + qBittorrent)       |
| `# commented service`         | manifests under `optional/` not in main kustomize |

## Prerequisites

- Kubernetes 1.27+ (any flavour: Docker Desktop, kind, k3s, Minikube,
  EKS/GKE/AKS).
- `kubectl` 1.27+.
- Built-in `kubectl kustomize` (no separate install needed since 1.14).
- For the default storage layout: a single-node cluster, OR an RWX-capable
  storage class. See "Storage" below.

## Quick start

```bash
# 1. Adjust the hostPath in storage.yaml to match your environment
#    (default: /Users/dave/work/media-data).
$EDITOR storage.yaml

# 2. Adjust ConfigMap values if 1000:1000 / Europe/London don't match.
$EDITOR configmap.yaml

# 3. Apply.
kubectl apply -k .

# 4. Watch the rollout.
kubectl -n arr-stack get pods -w
```

## Accessing the web UIs

The Services are `ClusterIP` by default — internal only. For browser
access, the simplest portable option is `kubectl port-forward`:

```bash
kubectl -n arr-stack port-forward svc/prowlarr 9696:9696   # http://localhost:9696
kubectl -n arr-stack port-forward svc/sabnzbd  8080:8080
kubectl -n arr-stack port-forward svc/sonarr   8989:8989
kubectl -n arr-stack port-forward svc/radarr   7878:7878
kubectl -n arr-stack port-forward svc/lidarr   8686:8686
kubectl -n arr-stack port-forward svc/bazarr   6767:6767
```

For a more permanent setup, switch the Services to `LoadBalancer` (works
on Docker Desktop and any cloud cluster) or stand up an Ingress
controller (Traefik, nginx, Caddy) and write Ingress resources hostname-
mapped to each Service.

## Storage

The `media-data` PVC is the most important resource in the stack. Every
Pod that touches media files mounts it at `/data` — that's SABnzbd,
Sonarr, Radarr, Lidarr, Bazarr (and qBittorrent + plundrio when the
optional manifests are applied). Prowlarr is the exception: it manages
indexers and pushes config to other apps via their APIs, but never
reads or writes media itself. The shared mount is what makes hardlinks
work between SABnzbd's complete folder and the \*arr libraries (and
between plundrio's complete folder and the libraries, when enabled).

### Single-node clusters (default)

`storage.yaml` defines a static `hostPath` PV at
`/Users/dave/work/media-data`. Edit the path before applying. Single-
node clusters can mount this RWX even though hostPath isn't formally
multi-writer — the kernel sees one filesystem on one node.

### Multi-node clusters

You need an RWX-capable storage class. Options:

- **NFS**: install `nfs-subdir-external-provisioner` pointed at an NFS
  server. Replace `storage.yaml` with a regular PVC that requests
  `storageClassName: nfs-client` and `accessModes: [ReadWriteMany]`.
- **Longhorn**: enable RWX volumes (Longhorn provisions an in-cluster
  NFS server in front of its block storage).
- **CephFS via Rook**: native distributed filesystem.
- **Cloud-managed**: AWS EFS, Azure Files, GCP Filestore via their
  respective CSI drivers.

In all cases the \*arr Pods don't need to change — only the PV/PVC in
`storage.yaml`.

## Configuration order

After the stack is up and you've port-forwarded into each service, the
configuration walkthrough is identical to the Compose version (see the
project root `README.md`). Briefly:

1. **SABnzbd** — set Usenet provider details, point Folders at
   `/data/usenet/incomplete` and `/data/usenet/complete`. Note the API key.
2. **Prowlarr** — add DrunkenSlug indexer; register Sonarr/Radarr/Lidarr
   using their _Service_ names: `http://sonarr:8989`, `http://radarr:7878`,
   `http://lidarr:8686`. Register SABnzbd as `http://sabnzbd:8080` with the
   API key from step 1.
3. **Bazarr** — manually point at `http://sonarr:8989` and
   `http://radarr:7878` with their respective API keys (Bazarr doesn't
   integrate with Prowlarr).

The DNS short-names (`sonarr`, `sabnzbd`, etc.) work because every
Service lives in the same `arr-stack` namespace. Use the FQDN
(`prowlarr.arr-stack.svc.cluster.local`) only if you need cross-namespace
addressing.

## Optional services

See `optional/README.md` for:

- **gluetun + qBittorrent** — VPN-routed local torrent client, deployed
  as a multi-container Pod.
- **plundrio** — put.io as a Transmission-RPC download client.

Both are NOT applied by `kubectl apply -k .`. Apply explicitly when
ready: `kubectl apply -k optional/` (after creating the corresponding
Secret).

## Common operations

| Task                       | Command                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------- |
| Apply the main stack       | `kubectl apply -k .`                                                                              |
| Watch rollout              | `kubectl -n arr-stack get pods -w`                                                                |
| Tail logs (all)            | `kubectl -n arr-stack logs -f -l app.kubernetes.io/part-of=arr-stack --all-containers --tail=100` |
| Tail one app's logs        | `kubectl -n arr-stack logs -f deploy/sonarr --tail=100`                                           |
| Shell into a pod           | `kubectl -n arr-stack exec -it deploy/sonarr -- /bin/bash`                                        |
| Port-forward Prowlarr      | `kubectl -n arr-stack port-forward svc/prowlarr 9696:9696`                                        |
| Render manifests (dry-run) | `kubectl kustomize .`                                                                             |
| Delete the stack           | `kubectl delete -k .` (PVCs deleted; data on hostPath remains)                                    |

## File layout

```plaintext
kubernetes/
├── README.md                    # this file
├── kustomization.yaml           # main entrypoint for the active stack
├── namespace.yaml
├── configmap.yaml               # PUID, PGID, TZ
├── storage.yaml                 # shared media-data PV + PVC
├── prowlarr.yaml                # PVC + Deployment + Service
├── sabnzbd.yaml
├── sonarr.yaml
├── radarr.yaml
├── lidarr.yaml
├── bazarr.yaml
└── optional/
    ├── README.md
    ├── kustomization.yaml       # optional services entrypoint
    ├── secret.example.yaml      # template — copy to secret.yaml
    ├── gluetun-qbittorrent.yaml # multi-container Pod
    └── plundrio.yaml
```

## Differences from the Compose version

- **No `broadlinkmanager`**. That service was preserved in the Compose
  file because it pre-existed the \*arr work; for K8s it's out of scope —
  add a separate manifest if you want to bring it along.
- **No bootstrap script**. Kustomize + the static PV's
  `type: DirectoryOrCreate` handle directory creation. Equivalent of
  `bootstrap.sh` is just `kubectl apply -k .`.
- **No backup script**. Use `velero` for full-cluster backups, or take
  PVC snapshots via your storage class's `VolumeSnapshot` if supported.
  For ad-hoc backup of a single config, `kubectl cp` from a running pod
  works.
- **Secrets are first-class**. The Compose `.env` becomes a ConfigMap
  for non-secret data and Secrets for VPN/put.io credentials. The
  `optional/secret.example.yaml` shows the structure.
