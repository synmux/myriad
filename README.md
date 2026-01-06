# Myriad 🌈

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/daveio/myriad)

_One repository to rule them all, one repository to find them..._

A grab-bag of experiments, prototypes, scripts, research, and configurations I've written over the years. If any of it is useful to you, have at it.

## Repository Structure

This repo uses a **branch-per-project** model:

| Branch                                                                 | Contents                                                             |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [`main`](https://github.com/daveio/myriad/tree/main)                   | Documentation, research, images, configuration templates, submodules |
| [`meta/boneyard`](https://github.com/daveio/myriad/tree/meta/boneyard) | Request retired code to be rehydrated from backups                   |
| [`meta/monorepo`](https://github.com/daveio/myriad/tree/meta/monorepo) | Historical snapshot (read-only fallback)                             |
| Other branches                                                         | Full projects with their own dependencies                            |

## Main Branch Contents

```plaintext
myriad/
├── configuration/   # Reusable templates (Claude, Cursor, Trunk, TypeScript, etc.)
├── data/            # Data files
├── docs/            # Documentation
├── images/          # Image assets (AVIF)
├── planning/        # Architecture diagrams (Mermaid)
├── research/        # Research documents, comparisons, guides
├── submodules/      # External repos kept checked out
└── writing/         # Writing projects
```

### Configuration Templates

The `configuration/` directory contains ready-to-use templates:

- **AI Assistants**: Claude instructions, Cursor rules, Goose hints
- **Linting**: Trunk configs, Biome, ESLint
- **Languages**: TypeScript configs, Python tooling
- **CI/CD**: GitHub Actions workflows, Dependabot
- **Services**: Cloudflare, MCP servers, PostgreSQL

## Current Projects

### Pendant Audio Capture

Wearable audio recording pendant based on M5 Capsule (ESP32-S3).

|              |                                                                                               |
| ------------ | --------------------------------------------------------------------------------------------- |
| **Hardware** | M5 Capsule with microphone and SD card                                                        |
| **Features** | Voice-activated recording, audio filtering, SD storage                                        |
| **Status**   | In development (Phase 1: Audio capture)                                                       |
| **Docs**     | [Learning Pathway](docs/PENDANT-LEARNING-PATHWAY.md) \| [Quick Start](pendant/QUICK-START.md) |

## For AI Agents

See [`AGENTS.md`](AGENTS.md) for commands, conventions, and detailed guidance.

## License

See [`LICENSE`](LICENSE).
