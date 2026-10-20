import hashlib
import struct
import zipfile
from pathlib import Path

base = Path('artifacts/manager/SHIV-SU-v3.3.1.apk')
dirty = Path('artifacts/DirtyFrag.apk')
assert hashlib.sha256(base.read_bytes()).hexdigest() == '21f28c3e0ce36568b0649ce334fef59cf7a502c04a08a331912ba0fb228d249e'
assert hashlib.sha256(dirty.read_bytes()).hexdigest() == 'cf44c1ea9225ad47ccb100f6f5c7bdba3852436d807d3d9300673e19419596de'
daemon = Path('output/ksud').read_bytes()
assert daemon.startswith(b'\x7fELF')
assert b'ro-partitions' in daemon and b'soft-reboot' in daemon
old_version = struct.pack('<HBBI', 8, 0, 0x10, 32684)
new_version = struct.pack('<HBBI', 8, 0, 0x10, 32686)
for original, name, entry in [(base, 'SHIV-SU-updated', 'lib/arm64-v8a/libksud.so'),
                              (dirty, 'DirtyFrag-1.08-for-SHIV-SU', 'assets/ksud')]:
    with zipfile.ZipFile(original) as source, zipfile.ZipFile(f'output/{name}-unsigned.apk', 'w') as target:
        for item in source.infolist():
            data = source.read(item.filename)
            if item.filename == entry:
                data = daemon
            elif original == base and item.filename == 'AndroidManifest.xml':
                assert data.count(old_version) == 1
                data = data.replace(old_version, new_version)
            target.writestr(item, data)
