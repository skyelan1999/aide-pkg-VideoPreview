# Video Preview · 视频预览

Public, independent, read-only Aide plugin focused on **editing project files first**, with browser-native video playback alongside the project index. MIT wrapper; see [third-party notices](THIRD_PARTY_NOTICES.md). No codec engine is bundled in the plugin or default Aide image. An explicitly installed, precompiled FFmpeg engine is available separately.

## Project support in 0.1.0

| Format | Implemented boundary |
|---|---|
| `.otio` | Track/clip index, source ranges, external-media references; basic sequential cuts/gaps. No transition/effect compositing. |
| `.fcpxml` | Asset references, projects, raw lane/offset/duration index. Nested/retimed structures are not flattened. |
| Final Cut 7 / Premiere `.xml`, `.xmeml` | `xmeml` clip timing and external-file index. |
| Jianying/CapCut `.json` draft | Unencrypted materials/tracks/segments, microsecond target ranges. Ordinary JSON is rejected and returned to the native viewer. |
| `.kdenlive`, `.mlt` | MLT producer resources, playlist entries and blanks, profile rate. Not tractor compositing. |
| `.prproj` | XML or gzip XML media/sequence index only; private object/tick timeline is not guessed. Export FCP XML/OTIO for a useful timing index. |
| `.drp` | ZIP directory inspection only; proprietary Resolve timelines are not decoded. |
| `.aep`, `.veg` | Recognized handoff/error guidance; no binary project decoder. Export an interchange format from the editor. |

Project inspection is not a rendered edit. Color grading, titles, masks, effects, plugins, nested timelines and speed ramps require the original editor/exported proxy. This version does not produce a composited movie from a project.

## Video tools

MP4/MOV/WebM and other registered extensions are offered to browser-native decoding. Support depends on actual container + codecs and browser/OS; registration does not guarantee playback. Playback/seek, 0.25–3x speed, A/B looping, approximate frame stepping with configurable reference fps, PNG frame export through the host’s top Save button, rotate/fit, local SRT/WebVTT and subtitle offset, and browser-available PiP/fullscreen. The current iframe/host may deny PiP/fullscreen. Screenshots capture the decoded original frame, not CSS rotation or subtitle overlays.

Same-directory descendant media references can be read through Aide's bound document bridge on explicit click. Absolute paths, network URLs, parent paths and Windows paths are displayed but not followed. “关联本地视频” allows manual read-only browser selection. No automatic filesystem scan, network asset fetch, original-file editing or content upload. Missing/unreachable files are reported after a requested read; untested references remain **unverified**.

Limits: 16 MiB project input/decompressed XML, 2 MiB JSON bridge output, 128 MiB Aide-bound video (bounded in-memory blob), 512 MiB manually selected local video, 2 MiB subtitle, 12-second parser timeout. Archives are indexed, never extracted. Size checks are not a complete snapshot guarantee; reopen a project if it changes during reading. Completed parses are removed immediately; uploads older than 5 minutes are reclaimed on the next tool invocation.

## Optional compatibility engine

Click **安装兼容引擎** to download the matching Linux ARM64/AMD64 engine (about 8 MB, checksum verified). Aide Docker on macOS/Windows uses the same Linux engine; no local compilation is needed. Then select **生成兼容预览** for a local H.264/AAC MP4 copy. FFmpeg 9.0.2 with x264 supports common legacy containers/codecs, but damaged, encrypted/DRM and unusual profiles can still fail. The copy is limited to 720p, the first 5 minutes, 80 MiB and a 10-minute processing deadline; HDR/color fidelity is not preserved. Inputs are read only and never uploaded remotely. Only one conversion runs at once; loss of the UI connection cancels after 40 seconds. Cancel is explicit. Network protocols and playlist demuxers are disabled in the engine.

Engine license is **GPL-2.0-or-later**, separate from the MIT wrapper. Original licenses, exact upstream sources, build scripts and actual ARM64/AMD64 configurations accompany the binaries on the [same Release](https://github.com/skyelan1999/aide-pkg-VideoPreview/releases/tag/v0.1.0). See [third-party notices](THIRD_PARTY_NOTICES.md). Engine cache is outside the core image at `~/.cache/aide-video-preview`; uninstalling the plugin does not remove that cache. Temporary source copies are reclaimed by the worker; completed proxies are bounded and reclaimed on subsequent conversions.

## Install and build

Install the ZIP under Aide Plugins → Upload, enable, then open a supported file. **Requires Aide 0.1.17.5 RC6** (or a compatible host with bound-document protocol 1 and Blob media CSP); [host PR #47](https://github.com/skyelan1999/aide/pull/47) adds the required sandbox media support. Python 3 and Node are provided by Aide. Release/market availability is recorded in the release notes, separately from local tests. `scripts/package.py` builds the reproducible lightweight plugin ZIP, excluding engine binaries, source archives, tests and caches. A normal user does not compile anything.

`python3 -m unittest discover -s tests -p '*test.py'`; `node --test tests/*.test.cjs`; `python3 scripts/package.py`.

Format references: [OTIO](https://opentimelineio.readthedocs.io/en/latest/), [FCPXML](https://developer.apple.com/documentation/professional-video-applications/fcpxml-reference), [MLT XML](https://www.mltframework.org/docs/mltxml/). These are independent adapters, not copied vendor SDKs. Packaged tests use synthetic fixtures. Additional public OTIO examples were tested locally without redistributing the samples; provenance is recorded in docs/verification.md.
