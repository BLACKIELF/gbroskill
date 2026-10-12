# Runtime licensing and state

`bin/gbro-publish` is MIT. `tiktok-entry.py` is AGPL-3.0-only because it imports and extends autotok. Its complete source and AGPL license are supplied. This repository is an aggregation, not a relicense of the included projects.

Vendor directories contain source, licenses and dependency manifests. Build tools, transitive packages, browsers and operating-system runtimes are installed separately under their own licenses. `node_modules`, virtual environments, author browser profiles, cookies, databases and account settings are not distributed.

The SAU source has the author's documented fixes plus a portable `conf.py`; original source differences are in `patches/social-auto-upload-local.patch`. `conf.py` reads `GBRO_CHROME`; it does not copy the original installation configuration. SAU's own cookies/logs are created locally under its runtime and must never be committed.

The optional upstream autotok launch videos and SAU sample environment/account config files are omitted. No executable source is removed. Third-party README images that reference those optional media files may not display offline.

Stylewx full upstream source is included; the local 0.6.0 runtime patch is supplied separately, not silently represented as an already-built patched server. The Skill caller accepts `GBRO_STYLEWX_ROOT`.
