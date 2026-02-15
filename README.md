## extsplit

Split audio files from `input/` into top-level bucket directories named:

`<extension>.<bit_depth>.<sample_rate>`

Example: `flac.24.96000`

The script scans `.m4a`, `.mp3`, and `.flac` files and preserves relative
directory structure under each bucket.

Metadata is read using the Python `mutagen` library (no `ffprobe` subprocess).
If bit depth or sample rate is unavailable for a file, `unknown` is used.

By default, files are copied. Use `--mv` to move instead.

### Usage

```bash
uv run main.py
```

Move instead of copy:

```bash
uv run main.py --mv
```

Dry run (no filesystem changes):

```bash
uv run main.py --dry-run
```

Optional input directory:

```bash
uv run main.py /path/to/input --dry-run
```
