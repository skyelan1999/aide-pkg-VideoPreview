# Verification — 2026-10-23

Release state is separate from these checks. Requires the Blob-media host change in Aide PR #47, targeted to RC6. Production port 9999 is untouched.

## Automated and native checks

- 20 Python tests PASS: FCPXML rational times/DOCTYPE; OTIO legacy and modern active references/gaps; xmeml; Jianying microseconds; MLT inclusive frame/blank timing; gzip Premiere; DRP directory-only; malformed/oversized/entity input; safe engine extraction; package allowlist and original bridge license.
- 4 Node tests PASS: actual opaque project upload/offset rejection/parse/reclaim, asset path policy, finite timestamp display and SRT conversion.
- Actual CI engine build: both native ARM64 and AMD64 passed [run 39927635064](https://github.com/skyelan1999/aide-pkg-VideoPreview/actions/runs/39927635064). Source archive SHA-256 and official FFmpeg detached signature verified. Both engine identities are FFmpeg 9.0.2, GPL-2.0-or-later, with x264, without nonfree/version3, and only libc/libm system dependencies. Exact notices/build manifests accompany each engine.
- Actual media integration PASS on ARM64 and AMD64: 2-second MPEG4/PCM AVI becomes H264/AAC MP4; silent VP9 MKV becomes silent H264 MP4; corrupt video returns error without a proxy. Invalid opaque IDs/offsets and missing explicit install confirmation are rejected. Cancellation during upload stops the worker and removes its temporary source (ARM64). ARM64 ran natively; AMD64 execution ran under Docker emulation, separately from its native CI build.
- Installer PASS with the real CI archive through a disposable loopback server: wrong digest rejected before execution; correct digest installed and ffprobe executed; reuse caused no second download. This is installer integration, not yet proof of public release availability.
- Complete corresponding-source asset contains exact FFmpeg/x264 source archives, source locks, signature/key, build scripts/Dockerfile, both actual configure files, original licenses and toolchain/package/runtime-library records. No upstream source modifications. Asset digest is pinned in runtime/catalog.json and release checksums.

## Safari acceptance

An independent Aide instance at 18490 has no model credentials and uses generated test footage. Synthetic FCPXML displays lanes, clips and its relative media reference. Existing H264 native MP4 playback, seek, approximate frame stepping and A/B loop at EOF were observed. AVI fails native decode as expected; explicit local conversion produces a 640x360/2-second compatible copy, Safari plays to 2.00s with audio controls. See docs/evidence/safari-project-player.jpg and safari-ffmpeg-proxy.jpg. The prepublication engine is seeded from the exact pinned CI ARM64 archive; this is distinct from public installer acceptance.

Host PR #47 quick/windows/Go race/gate all PASS in run 39927183129. A separate local full receipt remains in progress. Blob media permission keeps external networking disabled and iframe origin opaque.

Additional final Safari checks PASS: local SRT file picker loads and visibly renders “字幕验收 · VIDEO PREVIEW”; host export handoff downloads project-index.json (761 bytes, parsed FCPXML/one media) and frame-0.000.png (87,722 bytes, valid 640x360 PNG). The initial iframe-local download produced no file; fixed under Issue #2 using the existing top-level host Save control. Screenshot: docs/evidence/safari-subtitle-export.jpg.

## Public project examples

Read-only inspection of upstream OpenTimelineIO v0.17.0 tests/sample_data, downloaded only into ignored local test storage. No external sample is redistributed. Modern Clip.2 source references were repaired under Issue #1. MissingReference samples correctly have zero external media. Nested/effect/transition indexes do not claim composited rendering.

| Sample | Tracks | Clips | External media | SHA-256 |
|---|---:|---:|---:|---|
| multitrack.otio | 3 | 12 | 0 | 8982f905993ca4c7113423e63fdd7d2eff69d56ed4659a080e3281b7e7f038e0 |
| nested_example.otio | 2 | 8 | 0 | b9bc0f25590f724b7adc8ebfe4543256cc899b81f33ed4e75cd17cb6323f52cb |
| premiere_example.otio | 8 | 29 | 6 | 412c2dc0cd78397ea1c5ecf9e76c8f12c853c4c32203564644e2df82e561e35a |
| simple_cut.otio | 1 | 4 | 4 | a85440060aa8b421fb7430dcf4c6d9a89a78b256198767afcfff1496ededf7eb |
| transition.otio | 1 | 5 | 4 | c7fe66127f5b1c6a651ce55d3115b910b0efb53e4e275b5e1ee954079c72e9cc |

Source pattern: https://github.com/AcademySoftwareFoundation/OpenTimelineIO/tree/v0.17.0/tests/sample_data .

## Boundaries

No native proprietary-editor rendering acceptance is claimed. Premiere XML/gzip is a media/sequence index; DRP is archive-directory inspection; AEP/VEG only offer interchange-format guidance. No DRM, title/effect compositing, accurate retiming or grading. Proxy limits: 128 MiB input, at most 720p/first5min/80MiB, 10-minute conversion deadline. Original files remain read only. Large/variant real private projects, every codec/profile/browser, fullscreen/PiP, subtitle offset variants are not yet accepted unless separately recorded below.

The old imageio binary candidate was excluded. No unverified GPL3/nonfree decoder is shipped. The wrapper/bridge are MIT; optional engine GPL obligations remain separate. Patent rights are not inferred from open-source licensing.

## Published plugin and public installer acceptance

Video Preview0.1.0 published at https://github.com/skyelan1999/aide-pkg-VideoPreview/releases/tag/v0.1.0 from3935bcde407a85be372909f9fabca697b2da151c. All six payload/build-manifest assets downloaded anonymously with matching SHA256SUMS; downloaded source archive contains the exact locked upstream source hashes and actual configurations for both architectures. See docs/release-0.1.0.json. Fresh empty-cache installation from the public GitHub URLs PASS on ARM64(native) and AMD64(Docker emulation); both then passed AVI/MKV proxy conversion, corrupt-input rejection and upload cancellation/source cleanup. A test harness initially assumed ffprobe at /engine; corrected the harness to point to the actual installed cache without product changes, then reran both paths successfully.

PR47 merged as2ac30f63543b6af9b08e4a105a8700772b2d2773 by explicit user-authorized admin merge, without fabricated approval or changed branch protection. Local full verification completed all24 Go shards, all other race packages and vet successfully, but the last optional STEP check targeted the old default aide:local image and failed. No passing full receipt was claimed. A new complete main-checkout run targets the tested aide:video-preview-host-20261023 image via AIDE_TEST_IMAGE. RC6 and marketplace publication remain separate pending gates.
