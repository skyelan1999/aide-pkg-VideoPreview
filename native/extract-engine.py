import tarfile,sys,pathlib
archive,destination=sys.argv[1:];root=pathlib.Path(destination)
with tarfile.open(archive,'r:gz') as t:
 members=t.getmembers()
 if len(members)>100 or sum(m.size for m in members)>256*1048576:raise ValueError('Engine archive too large')
 for m in members:
  p=pathlib.PurePosixPath(m.name)
  if p.is_absolute() or '..' in p.parts or '\\' in m.name or not m.isfile() or p.parts[0] not in ('bin','licenses','build'):raise ValueError('Unsafe engine archive entry')
  dest=root.joinpath(*p.parts);dest.parent.mkdir(parents=True,exist_ok=True)
  with t.extractfile(m) as src,dest.open('xb') as out:
   while b:=src.read(1024*1024):out.write(b)
  dest.chmod(0o755 if p.parts[0]=='bin' else 0o644)
