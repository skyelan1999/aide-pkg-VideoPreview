# Third-party notices

## Included in the plugin ZIP

- Aide workbench MessagePort client, copied unmodified from `internal/server/web/plugin-workbench-client.js`, Aide commit `1827f3724ebb13325ecb3230018d64cfca4b7c03`. Copyright (c) 2026 Skye Lan. MIT; full license in `licenses/Aide-MIT.txt`. The generated viewer embeds this client. Source: https://github.com/skyelan1999/aide .
- All project adapters, UI, styles and test fixtures in this repository were written for this plugin. Wrapper license: MIT in LICENSE. No proprietary editing application SDK, icons, logos, fonts, binaries or project samples are included.

## Host facilities, not redistributed here

Python 3 standard library (XML/JSON/gzip/ZIP parsing) and Node.js standard library run inside the user's existing Aide runtime. Browser HTML media decoding is supplied by the user's browser/OS. This ZIP does not bundle Python, Node, codec libraries or a decoder engine. Their upstream/runtime licenses remain applicable to their distributors.

## Optional decoder candidate: NOT shipped or enabled

`imageio-ffmpeg 0.6.0` is BSD-2-Clause for its wrapper; that does NOT describe the FFmpeg executable's license. The Linux ARM64 wheel's `ffmpeg-linux-aarch64-v7.0.2` was executed with `-version` and `-L`: it enables `--enable-gpl --enable-version3` and libx264/libx265. It reports GPL version 3 or later. `--enable-nonfree` was absent in that inspected build. AMD64 has not yet been inspected; no inference of its complete binary license/compliance is made.

The candidate download catalog and binary are excluded from installation and packaging. No FFmpeg downloader or bundled engine is included. Before enabling redistribution, obtain and verify the exact corresponding source, build scripts/configuration, all linked-library notices, relevant (L)GPL distribution/relinking materials, and codec/patent distribution considerations. A general upstream URL or Python wrapper license is not sufficient evidence of that closure.

Evidence and sources (checked 2026-10-23):
- https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.0.2/LICENSE.md
- https://raw.githubusercontent.com/imageio/imageio-ffmpeg/v0.6.0/LICENSE
- PyPI wheel SHA-256 and binary `-version`/`-L` are recorded in docs/license-audit.json.

## Format compatibility and trademarks

Premiere Pro, Final Cut Pro, DaVinci Resolve, CapCut/Jianying and Kdenlive names identify supported/interoperable formats. This is an independent project; no affiliation, endorsement or native editor rendering equivalence is claimed. Format names do not confer a license to vendor SDKs or user content. Public format references are linked in README; no vendor documentation is reproduced in the package.
