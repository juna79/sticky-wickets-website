# The Sticky Wickets Cricket Club

Single-page site (hash-routed views) for the Sticky Wickets, Tigoni, Kenya.

- `index.html` is fully self-contained (CSS, JS, photos and bios are embedded). Deploy this file as-is.
- Rebuild after changing content: `python3 build/single.py` (needs Pillow). Bios live in `build/bios.json`; photos in `assets/`.

Netlify: no build command, publish directory `/` (repo root).
