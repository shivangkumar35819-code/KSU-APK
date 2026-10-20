Keep the existing SHIV-SU 3.3.1 application and interface-5 kernel/JNI core.

1. Add the supplied DirtyFrag 1.08 daemon's --ro-partitions and --soft-reboot
   launch-option compatibility to the existing SHIV-SU daemon. Preserve partition
   read-only behavior and use the existing soft-reboot implementation.
2. Compile with existing matching 3.3.1 LKM/ksuinit artifacts; run Android-target
   cargo check, clippy, and fmt in the repository-required sequence, then build.
3. Package the new ARM64 daemon into the original SHIV-SU APK and supplied
   DirtyFrag APK. Keep application DEX/resources, DirtyFrag native exploit,
   package IDs, and existing signing identity. Use v2-only signing.
4. Verify packaging and module identities, install, then perform one fresh
   device test. Require actual manager/root evidence before declaring success.

Earlier interface-4 diagnostic builds remain unverified and are superseded.
