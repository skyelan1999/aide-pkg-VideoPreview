# Video Preview · 视频预览

Public, independent, read-only Aide plugin focused on **editing project files first**, with browser-native video playback alongside the project index. MIT wrapper; see [third-party notices](THIRD_PARTY_NOTICES.md). No codec engine is bundled or automatically downloaded, so Aide's default image stays unchanged.

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

MP4/MOV/WebM and other registered extensions are offered to browser-native decoding. Support depends on actual container + codecs and browser/OS; registration does not guarantee playback. Playback/seek, 0.25–3x speed, A/B looping, approximate frame stepping with configurable reference fps, PNG frame download, rotate/fit, local SRT/WebVTT and subtitle offset, and browser-available PiP/fullscreen. The current iframe/host may deny PiP/fullscreen. Screenshots capture the decoded original frame, not CSS rotation or subtitle overlays.

Same-directory descendant media references can be read through Aide's bound document bridge on explicit click. Absolute paths, network URLs, parent paths and Windows paths are displayed but not followed. “关联本地视频” allows manual read-only browser selection. No automatic filesystem scan, network asset fetch, original-file editing or content upload. Missing/unreachable files are reported after a requested read; untested references remain **unverified**.

Limits: 16 MiB project input/decompressed XML, 2 MiB JSON bridge output, 128 MiB Aide-bound video (bounded in-memory blob), 512 MiB manually selected local video, 2 MiB subtitle, 12-second parser timeout. Archives are indexed, never extracted. Size checks are not a complete snapshot guarantee; reopen a project if it changes during reading. Completed parses are removed immediately; uploads older than 5 minutes are reclaimed on the next tool invocation.

## Install and build

Development candidate: install the ZIP under Aide Plugins → Upload, enable, then open a supported file. Requires Aide file-handler/workbench protocol 1 with bound-document methods and Python 3. Actual video playback additionally requires the local-Blob media host patch in [Aide PR #47](https://github.com/skyelan1999/aide/pull/47); the current stock release has not been accepted for this playback path. No marketplace or plugin Release publication is claimed yet. Source checkout's `scripts/package.py` embeds Aide's MIT bridge and builds a reproducible ZIP; it includes licenses and excludes decoder candidates, tests and caches. A normal user does not compile anything.

`python3 -m unittest discover -s tests -p '*test.py'`; `node --test tests/*.test.cjs`; `python3 scripts/package.py`.

Format references: [OTIO](https://opentimelineio.readthedocs.io/en/latest/), [FCPXML](https://developer.apple.com/documentation/professional-video-applications/fcpxml-reference), [MLT XML](https://www.mltframework.org/docs/mltxml/). These are independent adapters, not copied vendor SDKs. Only synthetic fixtures are used.
