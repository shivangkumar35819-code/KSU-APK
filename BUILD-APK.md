# SHIV TEST

Fresh source base: tiann/KernelSU tag v3.3.0 (932014a).
App label and both home page titles use SHIV TEST.

Run Actions > Build SHIV TEST APK and all LKM > Run workflow on main.
The repository's persistent signing secrets sign the APK. The same certificate
hash and size are compiled into every driver using the second accepted
certificate slot. Signature verification remains enabled.

The build covers eight KMI targets: android12-5.10, android13-5.10,
android13-5.15, android14-5.15, android14-6.1, android15-6.6,
android16-6.12, and android17-6.18. Each has arm64 and x86_64 LKM builds.
Both Android daemons embed the complete set of freshly built drivers and
ksuinit. Desktop daemons are also built for Windows, macOS, and Linux.

Download SHIV-TEST-APK for the installable APK, or SHIV-TEST-FULL-BUNDLE
for the APK, 16 modules, 7 daemons, 2 init binaries, public signing certificate,
verification.json, and SHA256SUMS. No private signing keys are included.

These are LKM builds for supported GKI kernel interfaces, not universal
boot.img files or complete GKI kernel images. Historical release drivers
are not mixed across source versions. Use the module matching the device's
architecture and KMI. Runtime device testing requires a compatible Android
device and has not been performed by CI.
