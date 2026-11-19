# Source admission and provenance — L01

Verified from the exact ChatGPT project uploads on 19 November 2026. Source files were copied byte-for-byte to `source/originals/`; each ZIP was extracted **without running contents** into `source/extracted/`. Files in the extracted folders are historical inputs and are not silently promoted to executable tools.

| File | SHA-256 |
|---|---|
| `source/originals/PartCrawler.bas` | `7cd1d511d5d47dca1d1e80b43b8cba934c5fb75551419e59e89dab2471aaf7c2` |
| `source/originals/SW2021-Research-This.zip` | `c761be9e239d64e1b8e35c56583482c84f45968e427b79d93753a412790127df` |
| `source/originals/SW2021-Research-Builder.zip` | `8d0e8c9ffe21d5f6fb96e90788ae50f259c90d9a939e5847de964df82de10f2e` |
| `source/extracted/builder/build.py` | `241ed1dc8bfa17093d4c024dfe71ac564354af1f7f2890df22e78e5aefe5aa98` |
| `source/extracted/builder/WORK_ORDER.md` | `0529849181f9fa604b79f1efd3a9c4361ab5013b7a49091a6ea6a634acdaf1aa` |
| `source/extracted/builder/START.txt` | `84421e99bd0995e83e29237ad4749a64233eaf79b5debcae641eb974fe2f33a2` |

The original filenames and contents are preserved. `WORK_ORDER.md` at repository root is a byte-for-byte copy of the original builder work order. The upgraded root `build.py` delegates to `src/queue.py`; it does **not** replace the archived original. Runtime model data, source facts and returned reviews are not included within the uploaded starter archives.

To verify: `sha256sum source/originals/* source/extracted/builder/*`; then compare to this manifest. Only original public research code and documentation were imported; no user CAD parts or proprietary geometry.
