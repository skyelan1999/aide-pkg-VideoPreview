#!/bin/sh
set -eu
# Run inside the pinned Linux build image; /src is this plugin, /out is a writable output mount.
export SOURCE_DATE_EPOCH=1790000000 LC_ALL=C TZ=UTC
JOBS=${JOBS:-2}
python3 - <<'PY'
import json,hashlib
from pathlib import Path
r=Path('/src/runtime');j=json.loads((r/'source-lock.json').read_text())
for k in ('ffmpeg','x264'):
 p=r/'sources'/j[k]['archive'];assert hashlib.sha256(p.read_bytes()).hexdigest()==j[k]['sha256'],k
PY
mkdir -p /out/bin /out/licenses /out/build
cd /tmp
mkdir -p engine-build
cd engine-build
python3 - <<'PYEXTRACT'
import tarfile
for name in ('ffmpeg-9.0.2.tar.xz','x264.tar.gz'):
 with tarfile.open('/src/runtime/sources/'+name) as t:
  for m in t.getmembers():
   from pathlib import PurePosixPath
   if PurePosixPath(m.name).is_absolute() or '..' in PurePosixPath(m.name).parts or not (m.isfile() or m.isdir()):raise ValueError('Unsafe source archive')
  t.extractall('.')
PYEXTRACT
cd x264
./configure --prefix=/tmp/engine-build/prefix --enable-static --enable-pic --disable-cli --disable-opencl --disable-asm > /out/build/x264-configure.log 2>&1
make -j"$JOBS" > /out/build/x264-make.log 2>&1
make install > /out/build/x264-install.log 2>&1
cp COPYING /out/licenses/x264-COPYING
cd ../ffmpeg-9.0.2
PKG_CONFIG_PATH=/tmp/engine-build/prefix/lib/pkgconfig ./configure --prefix=/out \
 --disable-autodetect --disable-everything --disable-doc --disable-debug --disable-network --disable-devices --disable-x86asm --disable-asm \
 --enable-gpl --enable-libx264 --enable-ffmpeg --enable-ffprobe --enable-swscale --enable-swresample \
 --enable-protocol=file,pipe \
 --enable-decoder=h264,hevc,mpeg4,mpeg2video,mpeg1video,vp8,vp9,av1,prores,dnxhd,mjpeg,wmv1,wmv2,wmv3,vc1,flv,h263,theora,aac,mp3,mp2,ac3,eac3,flac,opus,vorbis,pcm_s16le,pcm_s24le,pcm_s32le,pcm_f32le \
 --enable-demuxer=mov,matroska,avi,asf,flv,mpegts,mpegps,mpegvideo,ogg,wav,mp3,aac,flac \
 --enable-parser=h264,hevc,mpeg4video,mpegvideo,vp8,vp9,av1,aac,mpegaudio,ac3,flac,opus,vorbis,vc1 \
 --enable-muxer=mp4,image2 --enable-encoder=libx264,aac,png \
 --enable-filter=scale,format,aresample,anull,null,transpose \
 --enable-bsf=aac_adtstoasc,extract_extradata,h264_mp4toannexb,hevc_mp4toannexb \
 --extra-cflags=-I/tmp/engine-build/prefix/include --extra-ldflags=-L/tmp/engine-build/prefix/lib > /out/build/ffmpeg-configure.log 2>&1
make -j"$JOBS" > /out/build/ffmpeg-make.log 2>&1
cp ffmpeg ffprobe /out/bin/
cp COPYING* LICENSE.md /out/licenses/
cp config.h ffbuild/config.mak /out/build/
/out/bin/ffmpeg -version > /out/build/version.txt 2>&1
/out/bin/ffmpeg -L > /out/build/license.txt 2>&1
/out/bin/ffmpeg -buildconf > /out/build/configuration.txt 2>&1
ldd /out/bin/ffmpeg > /out/build/system-libraries.txt
dpkg-query -W > /out/build/build-system-packages.txt
cp /src/runtime/source-lock.json /out/build/
echo 'This software is based in part on the work of the Independent JPEG Group. Upstream sources are unmodified. FFmpeg and x264 copyright notices and full corresponding source accompany this release.' > /out/licenses/NOTICE.txt
