import json
import os
from typing import Any

import requests

API_KEY = os.environ.get("__OMI_API_KEY")


def main() -> None:
    print("main()")
    # list_all(json_file="conversations.json")
    uuids = ["07cebbf1-1320-5559-bb94-643f5a7aeaa3"]
    for i in uuids:
        delete_one(i)


def delete_one(conversation: str) -> bool:
    URL = f"https://api.omi.me/v1/dev/user/conversations/{conversation}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    r = requests.delete(URL, headers=headers, timeout=30)
    r.raise_for_status()
    print(r.text)
    resp = r.json()
    if resp.get("success"):
        print(f"Deleted conversation {conversation}")
        return True
    else:
        print(f"Failed to delete conversation {conversation}")
        return False


def list_all(json_file: str | None = None) -> dict[str, Any]:
    URL = "https://api.omi.me/v1/dev/user/conversations"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    conversations: dict[str, Any] = {}  # keyed by id to drop overlaps between pages
    offset, limit = 0, 200

    while True:
        r = requests.get(
            URL,
            headers=headers,
            params={"limit": limit, "offset": offset, "include_transcript": True},
            timeout=30,
        )
        r.raise_for_status()

        if r.headers.get("X-Omi-List-Truncated", "").lower() == "true":
            raise RuntimeError(
                f"Truncated at offset {offset}; nothing saved. "
                "Narrow the range with start_date/end_date."
            )

        page = r.json()
        for c in page:
            conversations[c["id"]] = c
        print(f"offset={offset} got {len(page)}, total {len(conversations)}")

        if not page or r.headers.get("X-Omi-Has-More", "").lower() == "false":
            break
        offset = int(r.headers.get("X-Omi-Next-Offset", offset + len(page)))

    if json_file:
        with open(json_file, "w") as f:
            json.dump(list(conversations.values()), f, indent=2)
        print(f"Wrote {len(conversations)} conversations to {json_file}")

    return conversations
