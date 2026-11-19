# Concentric mate — SW2021 diagnostic pilot

**Status:** AUTHORED; independent primary-source review outstanding; runtime NOT TESTED.

## Sources inspected in installed SW2021 Design Help

1. [Example: Concentric Mate Error](https://help.solidworks.com/2021/english/solidworks/sldworks/c_example_of_concentric_mate_error_swassy.htm) — c_example_of_concentric_mate_error_swassy.htm. 2021 Help shows a second concentric mate overdefining an assembly if the two hole-centre distances differ.
2. [Techniques for Fixing Mate Problems](https://help.solidworks.com/2021/english/solidworks/sldworks/t_techniques_fixing_mate_problems.htm) — t_techniques_fixing_mate_problems.htm. 2021 Help recommends MateXpert, examining red mates, suppressing conflicting mates, DOF inspection and considering fixed components.
3. [Allowing Misaligned Concentric Mates](https://help.solidworks.com/2021/english/solidworks/sldworks/t_allowing_misaligned_concentric_mates.htm) — t_allowing_misaligned_concentric_mates.htm. 2021 Help describes deliberately allowed concentric misalignment with an option/tolerance and separate Misaligned mate folder.

## Observable symptoms

- Adding a second concentric mate produces an over-defined assembly.
- A formerly solved concentric mate conflicts after geometry or fixed-state changes.
- Two mating hole patterns are nearly aligned but exact concentric constraints cannot both be solved.

## Competing hypotheses

- Hole-to-hole centre distances differ between two components, making exact coaxiality impossible for both pairs.
- Other mates restrict a component position or degrees of freedom and conflict with the requested axis.
- A component is fixed or an in-context reference changed, preventing desired alignment.
- Intended design permits finite misalignment, but exact concentric relations were incorrectly specified.

## mate-hole-pitch

**Procedure:** On a disposable assembly copy, inspect the two hole axes and compare centre-to-centre spacings of the paired holes in the respective part coordinate contexts, before adding an exact second concentric mate.

**Conditions / side effects:** 2021 assembly, active configuration and component transforms; lengths in mm; record each pair, measurement method and applied mates; read-only geometry inspection on a copy.

**Probe mode:** `ui_only`

**Rivals:** Mismatched hole spacing versus conflict solely from another mate.

**Basis:** DOCUMENTED: Example: Concentric Mate Error; measurement-based diagnosis is a hypothesis.

**API member:** not applicable: UI-only procedure; no API member asserted

| Observation | Interpretation | Inference limit | Next step |
|---|---|---|---|
| Corresponding hole spacings differ beyond measurement tolerance | Explains why two exact concentric mates cannot generally be satisfied simultaneously. | Does not prove the mismatch is an unintended CAD error or rule out additional mate conflicts. | Confirm engineering design intent, hole tolerances and optional misalignment capability. |
| Hole spacings agree within measured resolution but mate fails | Weakens pitch mismatch as sole explanation. | Axes may be angled or another mate/fixed state may still conflict. | Inspect MateXpert and existing degrees of freedom. |
| Inconclusive: axes/centres or configurations are not comparable | No pitch conclusion. | Do not treat approximate graphics alignment as exact geometry. | Identify comparable axial geometry and consistent coordinate frame. |

## mate-conflict-isolation

**Procedure:** In a disposable copy, run MateXpert/View Mate Errors, inspect highlighted red mates and component fixed states; temporarily suppress one competing mate at a time and inspect remaining degrees of freedom.

**Conditions / side effects:** Record assembly/configuration, pre-existing mate graph and suppression changes; suppressing or floating changes assembly state; only disposable fixture; avoid Force Mate because it can break other mates.

**Probe mode:** `disposable_copy`

**Rivals:** Conflicting mate network / fixed component versus intrinsically impossible geometric relationship.

**Basis:** DOCUMENTED: Techniques for Fixing Mate Problems; resolving a mate after suppression is conditional evidence.

**API member:** not applicable: UI-only procedure; no API member asserted

| Observation | Interpretation | Inference limit | Next step |
|---|---|---|---|
| Target concentric mate solves only when another mate is suppressed or a component floated | The suppressed mate/fixed condition participates in the conflict. | Does not mean suppressing it is the correct design solution. | Review desired kinematic degrees of freedom and replace a redundant constraint deliberately. |
| Target mate still fails after irrelevant mates are suppressed | The tested conflicts were not sufficient to explain failure. | A geometry mismatch, remaining constraint or stale reference may still exist. | Compare hole axes/pitches and inspect mate references. |
| Inconclusive: MateXpert cannot identify sources or suppression yields unstable results | No reliable unique conflicting mate identified. | Do not use Force Mate to claim causal isolation. | Construct minimal two-component test assembly from copies. |

## mate-intended-misalignment

**Procedure:** If design permits intentional mismatch, inspect the misaligned-concentric-mate option and tolerance on disposable assembly; compare exact-mate failure with explicitly permitted misalignment.

**Conditions / side effects:** 2021 assembly, recorded linear misalignment tolerance in mm, actual hole spacing difference and position; enabling this changes mate conditions, so disposable copy only.

**Probe mode:** `disposable_copy`

**Rivals:** Design-approved misalignment versus accidental geometric overdefinition.

**Basis:** DOCUMENTED: Allowing Misaligned Concentric Mates; correctness for a particular design requires separate engineering judgement.

**API member:** not applicable: UI-only procedure; no API member asserted

| Observation | Interpretation | Inference limit | Next step |
|---|---|---|---|
| Second mate succeeds only with nonzero allowed misalignment | Supports deliberate mismatch accommodation as the mechanism. | Does not establish acceptable fit, stress, assembly or manufacturing tolerance. | Check tolerancing and functional design intent before accepting any model change. |
| Second mate still fails with allowed misalignment | Specified tolerance or another conflict may be insufficient. | Does not disprove mismatch as a contributor. | Compare the residual error to allowed tolerance and inspect other mates. |
| Inconclusive: option unavailable or permission/design tolerance unknown | No conclusion about whether misalignment is intended. | Do not silently add tolerance to make the assembly solve. | Record unmet option or engineering design clarification as unresolved. |

## Limitations

- A solvable mate does not prove dimensional fit or mechanical correctness.
- Enabling misalignment changes assembly constraint semantics; must not be presented as generic repair.
- No installed SOLIDWORKS runtime tests, actual assemblies or API calls were performed.
