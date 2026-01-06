# AGENTS.md

Guide for AI agents working in this repository.

## Overview

**myriad** is a personal grab-bag repository containing experiments, prototypes, scripts, research, images, configurations, and documentation. It is NOT a typical software project with a single codebase.

### Repository Structure

- **`main` branch**: Small scripts, documentation, research, images, configuration templates, and submodules
- **Other branches**: Full projects with their own dependencies (package.json, pyproject.toml, etc.)
- **`meta/boneyard`**: Archive requests for retired code
- **`meta/monorepo`**: Historical snapshot (read-only)

## Directory Layout (main branch)

```plaintext
myriad/
├── configuration/     # Templates for AI assistants, linters, services
│   ├── claude/        # Claude configuration template
│   ├── cursor/rules/  # Cursor rules (.mdc files)
│   ├── trunk/         # Trunk linter configs
│   ├── typescript/    # TypeScript configs (tsconfig templates)
│   ├── mise/          # mise task runner configs
│   ├── github/        # GitHub workflow templates
│   └── ...
├── data/              # Data files (compressed, redacted)
├── docs/              # Documentation
├── images/            # Image assets (AVIF format)
├── planning/          # Architecture diagrams (Mermaid)
├── research/          # Research documents, comparisons, guides
├── submodules/        # External repos kept checked out
├── writing/           # Writing projects
└── .trunk/            # Active Trunk configuration
```

## Commands

### Linting & Formatting

Uses [Trunk](https://trunk.io) for unified linting/formatting:

```bash
# Format all files
trunk fmt -a

# Format specific file
trunk fmt <filename>

# Check all files
trunk check -a

# Check with existing issues shown
trunk check -a --show-existing

# Auto-fix issues
trunk check --fix -a
```

**Enabled linters**: oxipng, svgo, taplo, actionlint, bandit, black, checkov, isort, ruff, shellcheck, shfmt, yamllint, markdownlint, prettier, trufflehog

### Git Hooks (via Trunk)

- **Pre-commit**: `trunk-fmt-pre-commit`
- **Pre-push**: `trunk-check-pre-push`

## Package Managers

### JavaScript/TypeScript

Use **`bun`** for all JS/TS projects:

```bash
bun install
bun run <script>
bun run build
bun run test
```

### Python

Use **`uv`** for all Python projects:

```bash
uv sync              # Install/update dependencies
uv run <command>     # Run commands
uv add <package>     # Add dependency
uv remove <package>  # Remove dependency
```

## Configuration Templates

The `configuration/` directory contains reusable templates. Copy and adapt for new projects:

| Directory                   | Purpose                                                |
| --------------------------- | ------------------------------------------------------ |
| `claude/CLAUDE.md`          | Claude Code agent instructions template                |
| `cursor/rules/*.mdc`        | Cursor AI rules (Cloudflare, TypeScript, Python, etc.) |
| `trunk/`                    | Trunk linter configurations                            |
| `typescript/tsconfig*.json` | TypeScript configuration templates                     |
| `github/workflows/`         | GitHub Actions workflow templates                      |
| `dotfiles/`                 | Common dotfiles (.gitignore, .env.example, etc.)       |
| `mise/`                     | mise task runner configs                               |
| `mcp/`                      | Model Context Protocol server configs                  |

### Cursor Rules Available

- `cloudflare.mdc` - Cloudflare Workers development
- `typescript.mdc` - TypeScript best practices
- `python.mdc` - Python best practices
- `github-actions.mdc` - GitHub Actions workflows
- `formatting-linting.mdc` - Linting and formatting procedures
- `git.mdc` - Git workflows and conventions
- `packages-projects.mdc` - Package manager guidance
- `rich.mdc` - Python Rich library
- `smithery.mdc` - MCP server registry

## Conventions

### The 10 Commandments (from CLAUDE.md template)

1. **BREAK**: Ship breaking changes freely. Document in AGENTS.md.
2. **PERFECT**: Take unlimited time for correctness. Refactor aggressively.
3. **TEST**: Test everything with logic/side effects.
4. **SYNC**: AGENTS.md = source of truth. Keep docs in sync.
5. **VERIFY**: Run lint/typecheck/test before proceeding.
6. **COMMIT**: `git add -A . && oco --fgm --yes` after each feature/fix.
7. **REAL**: Use actual service calls only. No mocks (except tests).
8. **COMPLETE**: Finish all code or mark `TODO: [description]`.
9. **TRACK**: TODOs use 6-hex IDs (e.g., `TODO: (37c7b2)`).
10. **SHARE**: Extract duplicated logic immediately.

### Code Style

- **TypeScript**: ES modules, TypeScript by default, feature-based directory structure
- **Python**: PEP 8, use `uv`, minimum Python 3.10+
- **File naming**: lowercase with hyphens/underscores
- **Images**: AVIF format preferred

## GitHub Workflows

Located in `.github/workflows/`:

- `claude-code-review.yaml` - Claude Code PR review automation
- `claude.yaml` - Claude automation
- `devskim.yaml` - Security scanning

## Working with Branches

Projects requiring dependencies live on separate branches:

```bash
# List all branches
git branch -a

# Checkout a project branch
git checkout <branch-name>

# Check branch-specific README/AGENTS.md for that project's instructions
```

## Submodules

External repositories are tracked as submodules in `submodules/`:

```bash
# Initialize submodules
git submodule update --init --recursive

# Update all submodules
git submodule update --remote
```

## Notes

- This repository uses a branch-per-project model for complex work
- The `main` branch is for lightweight content and templates
- Configuration templates are meant to be copied, not symlinked
- When working on a specific project, check its branch for project-specific instructions
