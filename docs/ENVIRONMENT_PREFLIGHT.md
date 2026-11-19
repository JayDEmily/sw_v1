# Read-only environment preflight (19 November 2026)

Observed via Remote Desktop Commander on `DESKTOP-I188O30`; no runtime SOLIDWORKS exercise, macros, installer changes, settings changes or CAD-file edits.

- Windows 11 Home, 64-bit, approximately 15.8 GB RAM.
- SOLIDWORKS 2021 SP1.0 (`SLDWORKS.exe` file version `29.1.0.0061`) installed at `C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS`. User confirms licence is fine (user report, not direct runtime test).
- VBA 7.1 64-bit, `swVBAServer`, COM registration and `sldworks.tlb`, `swconst.tlb`, `swcommands.tlb`, `swpublished.tlb` present.
- Offline 2021 API Help at `C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS\\api\\sldworksapi.chm`; other API CHMs and interop binaries present. **No generic inference that installed API files prove runtime macro correctness.**
- Windows Python 3.13.15; Ubuntu WSL2 Python 3.14.4 and Git 2.53.0; local checkout `/home/jds/sw_v1`.
- Installed extensions include Flow Simulation, CAM, Inspection, Plastics, Visualize, Electrical and PCB. **User usage:** yes Flow Simulation, CAM, Inspection, Plastics, Visualize; no Electrical or PCB; no need for photorealistic-rendering tutorials. Phase-1 remains core modelling/mates. Add-in diagnostic coverage requires separate future scope admission; preserve frozen governance unless explicitly amended.

**Installation recommendation:** No further modules needed for L01–L04. A model runner with independent review context is **not bundled**; it must be provided or explicitly configured before automatic source-reopened review is claimed. The offline Design Help availability and application runtime/feature access were not verified during the read-only preflight.
