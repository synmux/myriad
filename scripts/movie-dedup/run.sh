#!/usr/bin/env fish
uv run uvicorn movie_dedup.app:app --host 127.0.0.1 --port 8765
