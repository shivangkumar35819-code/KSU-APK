"""Verify complete SHIV TEST release artifacts before bundling."""
import hashlib
import json
from pathlib import Path
import struct
import sys
from zipfile import ZipFile

root = Path(sys.argv[1]).resolve()
kmis = (
    "android12-5.10", "android13-5.10", "android13-5.15",
    "android14-5.15", "android14-6.1", "android15-6.6",
    "android16-6.12", "android17-6.18",
)
cert = root / "manager-certificate/manager-cert.der"
cert_hash = hashlib.sha256(cert.read_bytes()).hexdigest()
records = []
for arch, machine in (("aarch64", 183), ("x86_64", 62)):
    for kmi in kmis:
        path = root / f"{arch}-{kmi}-lkm/{kmi}_kernelsu.ko"
        data = path.read_bytes()
        if data[:6] != b"\x7fELF\x02\x01" or struct.unpack_from("<HH", data, 16) != (1, machine):
            raise SystemExit(f"Invalid module ELF type/architecture: {path}")
        if cert_hash.encode() not in data:
            raise SystemExit(f"Manager certificate missing from module: {path}")
        records.append({"architecture": arch, "kmi": kmi, "sha256": hashlib.sha256(data).hexdigest()})
apks = list((root / "SHIV-TEST-APK").glob("*.apk"))
if len(apks) != 1:
    raise SystemExit("Expected exactly one release APK")
with ZipFile(apks[0]) as apk:
    for abi in ("arm64-v8a", "x86_64"):
        data = apk.read(f"lib/{abi}/libksud.so")
        if not data.startswith(b"\x7fELF"):
            raise SystemExit(f"Missing valid ksud for {abi}")
for target in ("aarch64-linux-android", "x86_64-linux-android", "x86_64-pc-windows-gnu", "aarch64-apple-darwin", "x86_64-apple-darwin", "aarch64-unknown-linux-musl", "x86_64-unknown-linux-musl"):
    files = list((root / f"ksud-{target}").glob("ksud*"))
    if not files or any(p.stat().st_size == 0 for p in files):
        raise SystemExit(f"Missing daemon: {target}")
(root / "verification.json").write_text(json.dumps({"base": "v3.3.0", "app": "SHIV TEST", "manager_certificate_sha256": cert_hash, "modules": records}, indent=2) + "\n")
files = sorted(p for p in root.rglob("*") if p.is_file() and p.name != "SHA256SUMS")
(root / "SHA256SUMS").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root).as_posix()}\n" for p in files))
print(f"Verified {len(records)} matching modules, both APK ABIs, and all 7 daemon targets.")
