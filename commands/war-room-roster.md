---
description: Scan the project and propose a domain-specific war-room roster (opt-in, heavier)
---

Build a project-specific roster for the war-room.

Run the `discover-roster` skill: reuse `.servo/manifest.yaml` if it exists, otherwise scan the project shallowly to infer 3–5 domains, then **propose** a roster of domain officers (persona + real slice + signature question) and show it to me. Ask before writing — only create `.war-room/roster.yaml` once I accept or adjust it.

This is optional. The default `/war-room` already works with five generic officers and no config; this just seats officers that read real slices of *this* codebase.
