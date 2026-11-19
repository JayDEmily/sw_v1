# SOLIDWORKS 2021 primary-source inspection record — 19 November 2026

**Read only.** The installed `sldworks.chm` was accessed via Remote Desktop Commander on `DESKTOP-I188O30`; relevant members were read directly from the 7-Zip CHM stream (`7z.exe e -so CHM TOPIC.htm`). No CHM was edited or copied. The web Help URLs below identify the corresponding 2021 sections; because web `open` returned a JavaScript shell, the installed CHM, **not** the dynamic page body, substantiates the content summaries below.

- Installed file: `C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\lang\english\sldworks.chm`
- Size: approximately 95 MB; SHA-256 `9e4357baab971a63bb3a8c4e431cae579ba42f8c3a6d2a69d410f513cb77aec6` (PowerShell `Get-FileHash`)
- Context: executable version `29.1.0.0061`, SOLIDWORKS 2021 SP1; this is installed Design Help content, not a runtime CAD test.

## Specific topics opened and paraphrased

| CHM topic (exact member name) | Corresponding 2021 URL | Directly observed content summary |
|---|---|---|
| `t_Shell_Feature_Diagnostics.htm` | https://help.solidworks.com/2021/english/solidworks/sldworks/t_Shell_Feature_Diagnostics.htm | Shell PropertyManager exposes Error Diagnostics (Entire body / Failing faces), Check body/faces, displayed minimum radius of curvature; display mesh or curvature; Go to offset surface. |
| `HIDE_SHELL_MODEL_FAIL.htm` | https://help.solidworks.com/2021/english/solidworks/sldworks/HIDE_SHELL_MODEL_FAIL.htm | Failure can relate to offset into neighbouring faces, small faces/edges, local radius less than shell thickness; suggestions include reducing thickness, Check, offset surfaces, additive extrude and diagnostic cutting. |
| `c_Shell_Diagnostic_Cut.htm` | https://help.solidworks.com/2021/english/solidworks/sldworks/c_Shell_Diagnostic_Cut.htm | Remove model regions using a cut-extrude, retry shell, progressively localise failures. |
| `t_Creating_3D_Splines.htm` | https://help.solidworks.com/2021/english/solidworks/sldworks/t_Creating_3D_Splines.htm | Create spline inside a 3D sketch, place points, use Tab to change planes. |
| `HIDD_DVE_SKETCH_SPLINE_3D.htm` | https://help.solidworks.com/2021/english/solidworks/sldworks/HIDD_DVE_SKETCH_SPLINE_3D.htm | Existing Relations, X/Y/Z spline-point coordinates, handle tangent weighting, radial/polar direction, reset handle, Relax Spline, Proportional. |
| `c_Sketch_Relations_in_3D_Sketches.htm` | https://help.solidworks.com/2021/english/solidworks/sldworks/c_Sketch_Relations_in_3D_Sketches.htm | 3D-sketch relations include spline-handle along-axis relations, tangent/equal-curvature relations, relations across sketch planes. |
| `t_Using_Control_Polygons.htm` | https://help.solidworks.com/2021/english/solidworks/sldworks/t_Using_Control_Polygons.htm | Move control polygon and set XYZ coordinates (3D spline); Relax Spline may smooth shape after moving. |
| `c_Example_of_Concentric_Mate_Error_SWassy.htm` | https://help.solidworks.com/2021/english/solidworks/sldworks/c_example_of_concentric_mate_error_swassy.htm | Second concentric mate between hole pairs can overdefine assembly if hole-to-hole centre spacings differ. |
| `t_techniques_fixing_mate_problems.htm` | https://help.solidworks.com/2021/english/solidworks/sldworks/t_techniques_fixing_mate_problems.htm | MateXpert, View Mates / errors, suppressing conflicting mates, checking fixed components, and checking remaining DOF can narrow mate conflicts. `Force Mate` can break another mate. |
| `t_allowing_misaligned_concentric_mates.htm` | https://help.solidworks.com/2021/english/solidworks/sldworks/t_allowing_misaligned_concentric_mates.htm | Explicit misalignment options may accommodate two different hole spacings within a permitted tolerance, and the misaligned mates appear in their own folder. |

**Evidence boundary:** There was no source-page preservation beyond these paraphrases and the CHM hash; another reviewer can reproduce retrieval on the same installed 2021 archive. Source provenance is strong enough to support **authorship** of pilot hypotheses but does not substitute for a separately identified reviewer reopening them, nor does it establish runtime behaviour under specific geometry.
