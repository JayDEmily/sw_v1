# 3D spline — SW2021 diagnostic pilot

**Status:** AUTHORED; independent primary-source review outstanding; runtime NOT TESTED.

## Sources inspected in installed SW2021 Design Help

1. [Creating 3D Splines](https://help.solidworks.com/2021/english/solidworks/sldworks/t_Creating_3D_Splines.htm) — t_Creating_3D_Splines.htm. 2021 Help describes spline placement in a 3D sketch and Tab to switch planes while creating it.
2. [3D Spline PropertyManager](https://help.solidworks.com/2021/english/solidworks/sldworks/HIDD_DVE_SKETCH_SPLINE_3D.htm) — HIDD_DVE_SKETCH_SPLINE_3D.htm. The 2021 3D spline panel exposes existing relations, point XYZ coordinates, tangent controls, reset and Relax Spline.
3. [Sketch Relations in 3D Sketches](https://help.solidworks.com/2021/english/solidworks/sldworks/c_Sketch_Relations_in_3D_Sketches.htm) — c_Sketch_Relations_in_3D_Sketches.htm. 2021 Help describes relations on 3D spline handles, axis alignment and relations across sketch planes.
4. [Using Control Polygons](https://help.solidworks.com/2021/english/solidworks/sldworks/t_Using_Control_Polygons.htm) — t_Using_Control_Polygons.htm. Control polygon nodes may be moved and XYZ set; Relax Spline can smooth an edited curve.

## Observable symptoms

- A dragged point or handle moves a 3D spline unexpectedly in depth or alters nearby curvature.
- The spline changes shape or appears discontinuous after control polygon edits.
- A spline point/handle will not move as expected, or solver status indicates constraints.

## Competing hypotheses

- Point or control handle is constrained by existing 3D sketch relations.
- An unintended active placement plane or XYZ coordinate is responsible for apparent out-of-plane motion.
- Tangent handle weighting, direction or internal continuity controls rather than the selected point govern curvature.
- A control polygon edit changes multiple spline spans and needs re-parameterisation or deliberate smoothness constraints.

## spline-inspect-3d-relations

**Procedure:** Select the spline in the active 3D sketch, open 3D Spline PropertyManager, inspect Existing Relations and select each relation to highlight affected geometry; record Fully/Under Defined status.

**Conditions / side effects:** 2021 3D sketch, active document/configuration, read UI values only; no changes required; record point/handle and named relations.

**Probe mode:** `ui_only`

**Rivals:** Constraint-driven movement versus free point/handle curvature edits.

**Basis:** DOCUMENTED: 3D Spline PropertyManager and Sketch Relations in 3D Sketches.

**API member:** not applicable: UI-only procedure; no API member asserted

| Observation | Interpretation | Inference limit | Next step |
|---|---|---|---|
| A relation highlights the moved point/handle or external entity | Constraint is a supported candidate for the unexpected motion. | Highlighting alone does not prove solver causality. | On a disposable copy selectively suppress/remove that relation and compare. |
| No relevant relation highlights and spline is under-defined | Simple relation lock is less likely. | Unshown constraints, handle weighting and plane selection remain possible. | Inspect XYZ coordinates, tangent properties and placement plane. |
| Inconclusive: spline panel or relation highlight cannot be obtained | Cannot determine relation constraints from this test. | Do not infer unconstrained movement. | Verify entity type and open the intended 3D sketch. |

## spline-xyz-plane-control

**Procedure:** For the affected spline point, read its X/Y/Z values and intended plane; in a disposable test sketch change only one coordinate or recreate a point with explicit plane switching, comparing projected views.

**Conditions / side effects:** 3D sketch; same coordinate system; XYZ values in model length units (record mm); creation-plane switching uses Tab; editing must be on a disposable copy.

**Probe mode:** `disposable_copy`

**Rivals:** Actual depth/plane change versus view projection or spline-handle effect.

**Basis:** DOCUMENTED: Creating 3D Splines and 3D Spline PropertyManager; diagnosis is a hypothesis.

**API member:** not applicable: UI-only procedure; no API member asserted

| Observation | Interpretation | Inference limit | Next step |
|---|---|---|---|
| Z or another out-of-plane coordinate changes with the unexpected motion | Supports a genuine 3D positional change. | Does not identify which relation or action caused it. | Check relation highlights and active reference geometry. |
| XYZ coordinates are unchanged but curvature appears different | Point displacement is unlikely to explain the difference. | Handle direction, view projection or changes elsewhere remain possible. | Inspect tangent and control polygon controls. |
| Inconclusive: coordinate reference or selected point cannot be matched | No trustworthy comparison. | Do not infer the curve moved in XYZ. | Identify point index and reference system before retesting. |

## spline-handle-continuity

**Procedure:** On disposable copy, record tangent weighting/radial/polar direction and internal-continuity setting; change one handle control at a time, then try Reset This Handle or Relax Spline and compare curvature combs.

**Conditions / side effects:** Same 3D sketch and point index, record controls and display curvature; modifying handles/relaxing spline changes geometry and may affect dependent features.

**Probe mode:** `disposable_copy`

**Rivals:** Tangent-control curvature versus control-polygon placement or constraint effects.

**Basis:** DOCUMENTED: 3D Spline PropertyManager and Using Control Polygons; downstream shape prediction is a hypothesis.

**API member:** not applicable: UI-only procedure; no API member asserted

| Observation | Interpretation | Inference limit | Next step |
|---|---|---|---|
| Curvature becomes smooth after Reset Handle or Relax Spline | Supports handle/parameterisation sensitivity as a mechanism. | Does not prove the resulting curve satisfies design tolerance or downstream feature constraints. | Quantify curvature/tangent mismatch and rebuild only in disposable test. |
| Curvature anomaly remains with controls reset | Weakens one-handle adjustment as complete explanation. | Point positions and relations can still impose the shape. | Inspect point coordinates, relations and control polygon nodes. |
| Inconclusive: control is unavailable or edited spline differs in other respects | No valid inference about the original cause. | Unavailable controls do not imply they are unimportant. | Document entity and active controls for separate reproduction. |

## Limitations

- No API access is inferred from UI features; no spline API member was claimed.
- A smooth-looking spline does not establish design tolerances, curvature continuity or successful downstream sweep.
- No installed SOLIDWORKS runtime tests were performed.
