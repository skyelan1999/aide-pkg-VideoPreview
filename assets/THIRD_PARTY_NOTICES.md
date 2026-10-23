# Third-party notices

## Included in the plugin ZIP

- Aide workbench MessagePort client, copied unmodified from `internal/server/web/plugin-workbench-client.js`, Aide commit `1827f3724ebb13325ecb3230018d64cfca4b7c03`. Copyright (c) 2026 Skye Lan. MIT; full license in `licenses/Aide-MIT.txt`. The generated viewer embeds this client. Source: https://github.com/skyelan1999/aide .
- All project adapters, UI, styles and test fixtures in this repository were written for this plugin. Wrapper license: MIT in LICENSE. No proprietary editing application SDK, icons, logos, fonts, binaries or project samples are included.

## Host facilities, not redistributed here

Python 3 standard library (XML/JSON/gzip/ZIP parsing) and Node.js standard library run inside the user's existing Aide runtime. Browser HTML media decoding is supplied by the user's browser/OS. This ZIP does not bundle Python, Node, codec libraries or a decoder engine. Their upstream/runtime licenses remain applicable to their distributors.

## Optional FFmpeg engine (separate download)

The plugin invokes independent command-line FFmpeg/ffprobe programs; no FFmpeg library is linked into the JavaScript/Python wrapper. The separate engine contains **FFmpeg 9.0.2 + x264** and is distributed under **GPL-2.0-or-later**, with the original copyright notices, GPL/LGPL license texts and IJG acknowledgment in its licenses/ folder. This describes the inspected engine build, not all possible FFmpeg builds. It is built with --enable-gpl, without --enable-version3, --enable-nonfree or unlisted external codec libraries. System libc/libm are listed in each build manifest.

完整对应源码 (complete corresponding source), including the exact upstream FFmpeg and x264 archives, source-lock hashes, unmodified-source declaration, build scripts, Docker toolchain definition, actual configurations and build-system package manifests, is provided on the SAME release server as the binary:

https://github.com/skyelan1999/aide-pkg-VideoPreview/releases/tag/v0.1.0

Source asset: `video-engine-corresponding-source-v0.1.0.tar.gz`. Binary assets: `video-engine-linux-arm64.tar.gz`, `video-engine-linux-amd64.tar.gz`. Source access does not require purchase or a third-party account. The source asset and exact binary SHA-256/byte counts are pinned in runtime/catalog.json and the release checksums. Retain these notices and provide the corresponding sources when redistributing an engine; the MIT wrapper license does not replace GPL obligations for the engine.

FFmpeg source signature was checked against the official release key fingerprint FCF986EA15E6E293A5644F10B4322F04D67658D8. x264 is pinned to official VideoLAN stable commit b35605ace3ddf7c1a5d67a2eb553f034aef41d55. No upstream source modifications are applied; configuration and local process-integration code are in this repository. Exact build inputs are in runtime/source-lock.json.

The older imageio-ffmpeg 0.6.0 candidate is not used, downloaded or redistributed. Its BSD wrapper license was not used to describe its differently licensed binary. Browser/system decoders remain host-provided. Open-source license compliance does not itself grant any separate codec patent license; distribution circumstances may require separate assessment. No proprietary editor SDK or DRM bypass is included.

Primary sources: https://ffmpeg.org/legal.html ; https://ffmpeg.org/download.html ; https://code.videolan.org/videolan/x264 .

## Format compatibility and trademarks

Premiere Pro, Final Cut Pro, DaVinci Resolve, CapCut/Jianying and Kdenlive names identify supported/interoperable formats. This is an independent project; no affiliation, endorsement or native editor rendering equivalence is claimed. Format names do not confer a license to vendor SDKs or user content. Public format references are linked in README; no vendor documentation is reproduced in the package.
