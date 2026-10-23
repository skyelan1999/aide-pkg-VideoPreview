# Video Preview 0.1.0 — public project-first preview

User request 2026-10-23: public Aide all-purpose video preview, supporting both editing projects and video assets, prioritizing project files; explicitly audit third-party copyright.

One compact workbench shows a source/proxy player, project counts, track/clip index, searchable media references and supported limitations. All adapters normalize into `{format,name,sequences,tracks:[{name,kind,clips:[{name,start,duration,source}]}],media:[{name,path,status}],warnings}`. Times are seconds; unavailable times stay null. Use source-editor exports rather than inventing private binary schema decoding. No original writes or arbitrary path following. Manual local media association does not persist a path rewrite.

Acceptance: synthetic OTIO, FCPXML, xmeml, Jianying, MLT, gzip Premiere and ZIP DRP cases; malicious XML/archive/JSON rejection; inaccessible-path and unknown-schema behavior; actual Aide project rendering and media playback; codec failure clearly states limitation; ZIP license/inventory audit. FFmpeg compatibility engine is deliberately withheld until binary/source/license audit is complete. Future engine work must stay optional, with no default-host image increase.

This is an inspector and media preview, not a substitute renderer for native editor effects. Real vendor/version fixtures must be added with permission and kept out of public bundles if private.
