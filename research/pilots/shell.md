# Shell — SW2021 diagnostic pilot

**Status:** AUTHORED; independent primary-source review outstanding; runtime NOT TESTED.

## Sources inspected in installed SW2021 Design Help

1. [Shell Feature Diagnostics / Error Diagnostics](https://help.solidworks.com/2021/english/solidworks/sldworks/t_Shell_Feature_Diagnostics.htm) — t_Shell_Feature_Diagnostics.htm. 2021 Shell PropertyManager can diagnose Entire body or Failing faces, report minimum curvature radius and display mesh/curvature.
2. [Error Message - Shell Errors](https://help.solidworks.com/2021/english/solidworks/sldworks/HIDE_SHELL_MODEL_FAIL.htm) — HIDE_SHELL_MODEL_FAIL.htm. 2021 examples list adjacent-face offsets, small faces/edges, and curvature limits as possible causes; recommends Check and surface offsets.
3. [Shell Diagnostic Cut](https://help.solidworks.com/2021/english/solidworks/sldworks/c_Shell_Diagnostic_Cut.htm) — c_Shell_Diagnostic_Cut.htm. 2021 instructions suggest cut-extrude regions away and retry shell to localise a problem.

## Observable symptoms

- Shell feature reports failure or incomplete operation at a specified thickness.
- A shell attempt fails despite a successful temporary surface offset on one or more individual faces.
- A previously successful shell fails after changes to parent geometry.

## Competing hypotheses

- Thickness exceeds a local minimum curvature radius.
- Opposing/adjacent surfaces collide or an offset passes through another face.
- Small sliver faces, edges, three-sided vertex or topology causes kernel failure.
- Missing/rebuilt parent geometry or outdated selection changes the intended shell problem.

## shell-error-diagnostics

**Procedure:** On a disposable copy edit the failing Shell feature; use Error Diagnostics > Entire body and Failing faces, then Check body/faces; note callouts, minimum curvature radius and suspect regions.

**Conditions / side effects:** 2021 part document, recorded active configuration and target thickness in mm; inspection does not itself alter the body, but editing/saving the feature can; do not commit geometry edits.

**Probe mode:** `ui_only`

**Rivals:** Local curvature versus interference/small-face problems.

**Basis:** DOCUMENTED: Shell Feature Diagnostics; interpretation of why a callout matters is a hypothesis.

**API member:** not applicable: UI-only procedure; no API member asserted

| Observation | Interpretation | Inference limit | Next step |
|---|---|---|---|
| Minimum radius smaller than target wall thickness and callout at suspect face | Supports local curvature as candidate. | Does not prove it is the sole failure or that decreasing thickness yields a globally valid shell. | On the disposable copy retry a smaller thickness and compare diagnostics. |
| Curvature check passes at target thickness, but Shell still fails | Weakens simple local-radius explanation; look at offsets intersecting neighbours or small faces. | Does not eliminate local curvature elsewhere or other solver constraints. | Run targeted offset/cut probe. |
| Inconclusive: diagnostics unavailable, blank, or feature cannot be edited | No reliable result for this probe. | Do not infer valid geometry from an absent diagnostic. | Confirm active configuration, feature existence and reproducible failure first. |

## shell-targeted-offset

**Procedure:** On a disposable copy, use Offset Surface at the same distance on selected suspect face(s), testing normal direction and opposite direction separately; compare success/failure and visible interference.

**Conditions / side effects:** Part in same configuration; offset distance equals target shell thickness (record in mm), direction, selected face and effect; create/remove only disposable reference surfaces.

**Probe mode:** `disposable_copy`

**Rivals:** Intrinsic local offset limitation versus global intersection/trim/topology failure.

**Basis:** DOCUMENTED: Shell Errors recommends offset surfaces; whole-shell implication is ENGINEERING HYPOTHESIS.

**API member:** not applicable: UI-only procedure; no API member asserted

| Observation | Interpretation | Inference limit | Next step |
|---|---|---|---|
| Selected face fails surface offset in one direction | Supports that this local offset is problematic. | Does not show it is the only cause or that this direction matches the shell interior everywhere. | Inspect curvature and adjacent faces in the reported area. |
| All selected faces return offset surfaces but Shell still fails | Local operations are possible for tested faces; global coupling remains suspect. | Individual offsets do not validate mutual intersections, trims, closure or final shell topology. | Examine neighbours and run diagnostic-cut localisation. |
| Inconclusive: offset cannot be tested or input selection is ambiguous | No reliable geometric inference. | This is not a passed offset test. | Record affected face and use built-in Error Diagnostics or inspect geometry manually. |

## shell-diagnostic-cut

**Procedure:** On disposable copy, cut away one suspected region with Cut-Extrude, retry Shell with otherwise unchanged parameters; progressively vary the removed region.

**Conditions / side effects:** Part copy; identical configuration, shell thickness/removal faces; document cut volume and compare each retained geometry; cutting changes topology and must never touch production.

**Probe mode:** `disposable_copy`

**Rivals:** Localised topology/interference versus causes remaining elsewhere.

**Basis:** DOCUMENTED: Shell Diagnostic Cut; causal localisation is conditional on controlled geometry changes.

**API member:** not applicable: UI-only procedure; no API member asserted

| Observation | Interpretation | Inference limit | Next step |
|---|---|---|---|
| Shell works after removing a specific region | The removed region or its interactions are implicated. | Does not identify the unique faulty face; cut changes global topology too. | Narrow removal using smaller cuts and inspect the boundary. |
| Shell still fails after a cut | A cause may remain in the retained model or be introduced by the cut. | Cannot prove the removed region was irrelevant. | Try a different partition and compare thickness/curvature. |
| Inconclusive: cut destroys shell intent or yields non-comparable geometry | No valid localisation under these changed conditions. | Do not claim the original model is fixed or causality proved. | Return to unmodified copy and use local Check diagnostics. |

## Limitations

- No runtime invocation or model fixture was used for these pilot steps.
- Successful surface offsets are not a proof of whole-shell success.
- A failed Shell creation may leave no persistent failed feature-tree node.
- The installed 2021 Help text was read; no 2021 API signatures were asserted for UI diagnostics.
