# SHIV-SU v3.3.1 APK and LKM build

Based on upstream tag `v3.3.1`, commit `0c0fdb960178fa12d80d6cbcfdcb6ad8be6a865d`.
App label and the home page title are SHIV-SU.
Manager features, package name, kernel interfaces, and root policies are unchanged.

The Build Manager workflow builds LKM modules, ksuinit, ksud, and the release APK.
Download the final installable APK from the `manager` artifact, not `manager-gradle`.
LKM artifacts are specific to their Android kernel KMI and architecture.
An APK cannot add LKM support to an incompatible device kernel.

## Rebuild

Open Actions > Build Manager > Run workflow on main.
Repository secrets KEYSTORE, KEYSTORE_PASSWORD, KEY_PASSWORD, and KEY_ALIAS
provide the persistent repository signing identity. The workflow extracts the
certificate hash and size and passes them to LKM builds so Manager verification
matches the signed APK. Do not replace these secrets between updates.

This repository uses its own signing certificate, not tiann's private key.
Its APK cannot update the official APK in place, and its LKM modules must be
used with its matching Manager. Keep the official artifacts separate.

CI installs Android ksud binaries in jniLibs before the Manager Gradle build.
The final repack step embeds the built daemons and signs the completed APK.

For a label-only rebuild, run Build SHIV-SU APK with a Build Manager run ID
containing all three Android ksud artifacts. Download the SHIV-SU-APK artifact.
Both Material and Miuix home page titles use the shared app_name resource.
