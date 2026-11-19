"""One-time structured pilot authoring from independently inspected source excerpts."""
import json
from pathlib import Path
from src.queue import validate_card

root=Path(__file__).resolve().parent
BASE='https://help.solidworks.com/2021/english/solidworks/sldworks/'

def source(topic, section, fact):
    return dict(url=BASE+topic, section=section, fact=fact, status='offline-chm',
                offline_topic=topic, local_archive_sha256='9e4357baab971a63bb3a8c4e431cae579ba42f8c3a6d2a69d410f513cb77aec6')

def out(obs,meaning,limits,next_step):
    return dict(observation=obs,meaning=meaning,limits=limits,next_step=next_step)

def probe(ident,test,conditions,rivals,basis,outcomes,mode='ui_only'):
    return dict(id=ident, test=test, mode=mode, conditions=conditions,rivals=rivals,basis=basis,
                member='not applicable: UI-only procedure; no API member asserted', outcomes=outcomes)

shell=dict(
 sources=[
   source('t_Shell_Feature_Diagnostics.htm','Shell Feature Diagnostics / Error Diagnostics','2021 Shell PropertyManager can diagnose Entire body or Failing faces, report minimum curvature radius and display mesh/curvature.'),
   source('HIDE_SHELL_MODEL_FAIL.htm','Error Message - Shell Errors','2021 examples list adjacent-face offsets, small faces/edges, and curvature limits as possible causes; recommends Check and surface offsets.'),
   source('c_Shell_Diagnostic_Cut.htm','Shell Diagnostic Cut','2021 instructions suggest cut-extrude regions away and retry shell to localise a problem.')],
 symptoms=['Shell feature reports failure or incomplete operation at a specified thickness.',
           'A shell attempt fails despite a successful temporary surface offset on one or more individual faces.',
           'A previously successful shell fails after changes to parent geometry.'],
 rivals=['Thickness exceeds a local minimum curvature radius.',
         'Opposing/adjacent surfaces collide or an offset passes through another face.',
         'Small sliver faces, edges, three-sided vertex or topology causes kernel failure.',
         'Missing/rebuilt parent geometry or outdated selection changes the intended shell problem.'],
 probes=[
  probe('shell-error-diagnostics',
    'On a disposable copy edit the failing Shell feature; use Error Diagnostics > Entire body and Failing faces, then Check body/faces; note callouts, minimum curvature radius and suspect regions.',
    '2021 part document, recorded active configuration and target thickness in mm; inspection does not itself alter the body, but editing/saving the feature can; do not commit geometry edits.',
    'Local curvature versus interference/small-face problems.',
    'DOCUMENTED: Shell Feature Diagnostics; interpretation of why a callout matters is a hypothesis.',[
      out('Minimum radius smaller than target wall thickness and callout at suspect face','Supports local curvature as candidate.','Does not prove it is the sole failure or that decreasing thickness yields a globally valid shell.','On the disposable copy retry a smaller thickness and compare diagnostics.'),
      out('Curvature check passes at target thickness, but Shell still fails','Weakens simple local-radius explanation; look at offsets intersecting neighbours or small faces.','Does not eliminate local curvature elsewhere or other solver constraints.','Run targeted offset/cut probe.'),
      out('Inconclusive: diagnostics unavailable, blank, or feature cannot be edited','No reliable result for this probe.','Do not infer valid geometry from an absent diagnostic.','Confirm active configuration, feature existence and reproducible failure first.')]),
  probe('shell-targeted-offset',
    'On a disposable copy, use Offset Surface at the same distance on selected suspect face(s), testing normal direction and opposite direction separately; compare success/failure and visible interference.',
    'Part in same configuration; offset distance equals target shell thickness (record in mm), direction, selected face and effect; create/remove only disposable reference surfaces.',
    'Intrinsic local offset limitation versus global intersection/trim/topology failure.',
    'DOCUMENTED: Shell Errors recommends offset surfaces; whole-shell implication is ENGINEERING HYPOTHESIS.',[
      out('Selected face fails surface offset in one direction','Supports that this local offset is problematic.','Does not show it is the only cause or that this direction matches the shell interior everywhere.','Inspect curvature and adjacent faces in the reported area.'),
      out('All selected faces return offset surfaces but Shell still fails','Local operations are possible for tested faces; global coupling remains suspect.','Individual offsets do not validate mutual intersections, trims, closure or final shell topology.','Examine neighbours and run diagnostic-cut localisation.'),
      out('Inconclusive: offset cannot be tested or input selection is ambiguous','No reliable geometric inference.','This is not a passed offset test.','Record affected face and use built-in Error Diagnostics or inspect geometry manually.')],mode='disposable_copy'),
  probe('shell-diagnostic-cut',
    'On disposable copy, cut away one suspected region with Cut-Extrude, retry Shell with otherwise unchanged parameters; progressively vary the removed region.',
    'Part copy; identical configuration, shell thickness/removal faces; document cut volume and compare each retained geometry; cutting changes topology and must never touch production.',
    'Localised topology/interference versus causes remaining elsewhere.',
    'DOCUMENTED: Shell Diagnostic Cut; causal localisation is conditional on controlled geometry changes.',[
      out('Shell works after removing a specific region','The removed region or its interactions are implicated.','Does not identify the unique faulty face; cut changes global topology too.','Narrow removal using smaller cuts and inspect the boundary.'),
      out('Shell still fails after a cut','A cause may remain in the retained model or be introduced by the cut.','Cannot prove the removed region was irrelevant.','Try a different partition and compare thickness/curvature.'),
      out('Inconclusive: cut destroys shell intent or yields non-comparable geometry','No valid localisation under these changed conditions.','Do not claim the original model is fixed or causality proved.','Return to unmodified copy and use local Check diagnostics.')],mode='disposable_copy')],
 limitations=['No runtime invocation or model fixture was used for these pilot steps.',
              'Successful surface offsets are not a proof of whole-shell success.',
              'A failed Shell creation may leave no persistent failed feature-tree node.',
              'The installed 2021 Help text was read; no 2021 API signatures were asserted for UI diagnostics.'])

spline=dict(
 sources=[
  source('t_Creating_3D_Splines.htm','Creating 3D Splines','2021 Help describes spline placement in a 3D sketch and Tab to switch planes while creating it.'),
  source('HIDD_DVE_SKETCH_SPLINE_3D.htm','3D Spline PropertyManager','The 2021 3D spline panel exposes existing relations, point XYZ coordinates, tangent controls, reset and Relax Spline.'),
  source('c_Sketch_Relations_in_3D_Sketches.htm','Sketch Relations in 3D Sketches','2021 Help describes relations on 3D spline handles, axis alignment and relations across sketch planes.'),
  source('t_Using_Control_Polygons.htm','Using Control Polygons','Control polygon nodes may be moved and XYZ set; Relax Spline can smooth an edited curve.')],
 symptoms=['A dragged point or handle moves a 3D spline unexpectedly in depth or alters nearby curvature.',
           'The spline changes shape or appears discontinuous after control polygon edits.',
           'A spline point/handle will not move as expected, or solver status indicates constraints.'],
 rivals=['Point or control handle is constrained by existing 3D sketch relations.',
         'An unintended active placement plane or XYZ coordinate is responsible for apparent out-of-plane motion.',
         'Tangent handle weighting, direction or internal continuity controls rather than the selected point govern curvature.',
         'A control polygon edit changes multiple spline spans and needs re-parameterisation or deliberate smoothness constraints.'],
 probes=[
  probe('spline-inspect-3d-relations',
    'Select the spline in the active 3D sketch, open 3D Spline PropertyManager, inspect Existing Relations and select each relation to highlight affected geometry; record Fully/Under Defined status.',
    '2021 3D sketch, active document/configuration, read UI values only; no changes required; record point/handle and named relations.',
    'Constraint-driven movement versus free point/handle curvature edits.',
    'DOCUMENTED: 3D Spline PropertyManager and Sketch Relations in 3D Sketches.',[
      out('A relation highlights the moved point/handle or external entity','Constraint is a supported candidate for the unexpected motion.','Highlighting alone does not prove solver causality.','On a disposable copy selectively suppress/remove that relation and compare.'),
      out('No relevant relation highlights and spline is under-defined','Simple relation lock is less likely.','Unshown constraints, handle weighting and plane selection remain possible.','Inspect XYZ coordinates, tangent properties and placement plane.'),
      out('Inconclusive: spline panel or relation highlight cannot be obtained','Cannot determine relation constraints from this test.','Do not infer unconstrained movement.','Verify entity type and open the intended 3D sketch.')]),
  probe('spline-xyz-plane-control',
    'For the affected spline point, read its X/Y/Z values and intended plane; in a disposable test sketch change only one coordinate or recreate a point with explicit plane switching, comparing projected views.',
    '3D sketch; same coordinate system; XYZ values in model length units (record mm); creation-plane switching uses Tab; editing must be on a disposable copy.',
    'Actual depth/plane change versus view projection or spline-handle effect.',
    'DOCUMENTED: Creating 3D Splines and 3D Spline PropertyManager; diagnosis is a hypothesis.',[
      out('Z or another out-of-plane coordinate changes with the unexpected motion','Supports a genuine 3D positional change.','Does not identify which relation or action caused it.','Check relation highlights and active reference geometry.'),
      out('XYZ coordinates are unchanged but curvature appears different','Point displacement is unlikely to explain the difference.','Handle direction, view projection or changes elsewhere remain possible.','Inspect tangent and control polygon controls.'),
      out('Inconclusive: coordinate reference or selected point cannot be matched','No trustworthy comparison.','Do not infer the curve moved in XYZ.','Identify point index and reference system before retesting.')],mode='disposable_copy'),
  probe('spline-handle-continuity',
    'On disposable copy, record tangent weighting/radial/polar direction and internal-continuity setting; change one handle control at a time, then try Reset This Handle or Relax Spline and compare curvature combs.',
    'Same 3D sketch and point index, record controls and display curvature; modifying handles/relaxing spline changes geometry and may affect dependent features.',
    'Tangent-control curvature versus control-polygon placement or constraint effects.',
    'DOCUMENTED: 3D Spline PropertyManager and Using Control Polygons; downstream shape prediction is a hypothesis.',[
      out('Curvature becomes smooth after Reset Handle or Relax Spline','Supports handle/parameterisation sensitivity as a mechanism.','Does not prove the resulting curve satisfies design tolerance or downstream feature constraints.','Quantify curvature/tangent mismatch and rebuild only in disposable test.'),
      out('Curvature anomaly remains with controls reset','Weakens one-handle adjustment as complete explanation.','Point positions and relations can still impose the shape.','Inspect point coordinates, relations and control polygon nodes.'),
      out('Inconclusive: control is unavailable or edited spline differs in other respects','No valid inference about the original cause.','Unavailable controls do not imply they are unimportant.','Document entity and active controls for separate reproduction.')],mode='disposable_copy')],
 limitations=['No API access is inferred from UI features; no spline API member was claimed.',
              'A smooth-looking spline does not establish design tolerances, curvature continuity or successful downstream sweep.',
              'No installed SOLIDWORKS runtime tests were performed.'])

mate=dict(
 sources=[
  source('c_example_of_concentric_mate_error_swassy.htm','Example: Concentric Mate Error','2021 Help shows a second concentric mate overdefining an assembly if the two hole-centre distances differ.'),
  source('t_techniques_fixing_mate_problems.htm','Techniques for Fixing Mate Problems','2021 Help recommends MateXpert, examining red mates, suppressing conflicting mates, DOF inspection and considering fixed components.'),
  source('t_allowing_misaligned_concentric_mates.htm','Allowing Misaligned Concentric Mates','2021 Help describes deliberately allowed concentric misalignment with an option/tolerance and separate Misaligned mate folder.')],
 symptoms=['Adding a second concentric mate produces an over-defined assembly.',
           'A formerly solved concentric mate conflicts after geometry or fixed-state changes.',
           'Two mating hole patterns are nearly aligned but exact concentric constraints cannot both be solved.'],
 rivals=['Hole-to-hole centre distances differ between two components, making exact coaxiality impossible for both pairs.',
         'Other mates restrict a component position or degrees of freedom and conflict with the requested axis.',
         'A component is fixed or an in-context reference changed, preventing desired alignment.',
         'Intended design permits finite misalignment, but exact concentric relations were incorrectly specified.'],
 probes=[
  probe('mate-hole-pitch',
    'On a disposable assembly copy, inspect the two hole axes and compare centre-to-centre spacings of the paired holes in the respective part coordinate contexts, before adding an exact second concentric mate.',
    '2021 assembly, active configuration and component transforms; lengths in mm; record each pair, measurement method and applied mates; read-only geometry inspection on a copy.',
    'Mismatched hole spacing versus conflict solely from another mate.',
    'DOCUMENTED: Example: Concentric Mate Error; measurement-based diagnosis is a hypothesis.',[
      out('Corresponding hole spacings differ beyond measurement tolerance','Explains why two exact concentric mates cannot generally be satisfied simultaneously.','Does not prove the mismatch is an unintended CAD error or rule out additional mate conflicts.','Confirm engineering design intent, hole tolerances and optional misalignment capability.'),
      out('Hole spacings agree within measured resolution but mate fails','Weakens pitch mismatch as sole explanation.','Axes may be angled or another mate/fixed state may still conflict.','Inspect MateXpert and existing degrees of freedom.'),
      out('Inconclusive: axes/centres or configurations are not comparable','No pitch conclusion.','Do not treat approximate graphics alignment as exact geometry.','Identify comparable axial geometry and consistent coordinate frame.')]),
  probe('mate-conflict-isolation',
    'In a disposable copy, run MateXpert/View Mate Errors, inspect highlighted red mates and component fixed states; temporarily suppress one competing mate at a time and inspect remaining degrees of freedom.',
    'Record assembly/configuration, pre-existing mate graph and suppression changes; suppressing or floating changes assembly state; only disposable fixture; avoid Force Mate because it can break other mates.',
    'Conflicting mate network / fixed component versus intrinsically impossible geometric relationship.',
    'DOCUMENTED: Techniques for Fixing Mate Problems; resolving a mate after suppression is conditional evidence.',[
      out('Target concentric mate solves only when another mate is suppressed or a component floated','The suppressed mate/fixed condition participates in the conflict.','Does not mean suppressing it is the correct design solution.','Review desired kinematic degrees of freedom and replace a redundant constraint deliberately.'),
      out('Target mate still fails after irrelevant mates are suppressed','The tested conflicts were not sufficient to explain failure.','A geometry mismatch, remaining constraint or stale reference may still exist.','Compare hole axes/pitches and inspect mate references.'),
      out('Inconclusive: MateXpert cannot identify sources or suppression yields unstable results','No reliable unique conflicting mate identified.','Do not use Force Mate to claim causal isolation.','Construct minimal two-component test assembly from copies.')],mode='disposable_copy'),
  probe('mate-intended-misalignment',
    'If design permits intentional mismatch, inspect the misaligned-concentric-mate option and tolerance on disposable assembly; compare exact-mate failure with explicitly permitted misalignment.',
    '2021 assembly, recorded linear misalignment tolerance in mm, actual hole spacing difference and position; enabling this changes mate conditions, so disposable copy only.',
    'Design-approved misalignment versus accidental geometric overdefinition.',
    'DOCUMENTED: Allowing Misaligned Concentric Mates; correctness for a particular design requires separate engineering judgement.',[
      out('Second mate succeeds only with nonzero allowed misalignment','Supports deliberate mismatch accommodation as the mechanism.','Does not establish acceptable fit, stress, assembly or manufacturing tolerance.','Check tolerancing and functional design intent before accepting any model change.'),
      out('Second mate still fails with allowed misalignment','Specified tolerance or another conflict may be insufficient.','Does not disprove mismatch as a contributor.','Compare the residual error to allowed tolerance and inspect other mates.'),
      out('Inconclusive: option unavailable or permission/design tolerance unknown','No conclusion about whether misalignment is intended.','Do not silently add tolerance to make the assembly solve.','Record unmet option or engineering design clarification as unresolved.')],mode='disposable_copy')],
 limitations=['A solvable mate does not prove dimensional fit or mechanical correctness.',
              'Enabling misalignment changes assembly constraint semantics; must not be presented as generic repair.',
              'No installed SOLIDWORKS runtime tests, actual assemblies or API calls were performed.'])

for ident, title, data in [('shell','Shell',shell),('spline-3d','3D spline',spline),('mate-concentric','Concentric mate',mate)]:
    validate_card(data)
    path=root/'pilots'/(ident+'.json')
    obj=dict(id=ident, title=title, status='AUTHORED_NOT_INDEPENDENTLY_REVIEWED',
             documented_in='research/evidence/OFFLINE_HELP_INDEX.md',
             environment='SOLIDWORKS 2021 SP1 offline Design Help',
             runtime_status='NOT_TESTED', data=data)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    lines=['# '+title+' — SW2021 diagnostic pilot', '',
       '**Status:** AUTHORED; independent primary-source review outstanding; runtime NOT TESTED.', '',
       '## Sources inspected in installed SW2021 Design Help','']
    for i,s in enumerate(data['sources'],1):
        lines.append('%d. [%s](%s) — %s. %s'%(i,s['section'],s['url'],s['offline_topic'],s['fact']))
    lines.extend(['','## Observable symptoms',''])
    lines.extend('- '+x for x in data['symptoms'])
    lines.extend(['','## Competing hypotheses',''])
    lines.extend('- '+x for x in data['rivals'])
    for p in data['probes']:
        lines.extend(['','## '+p['id'], '', '**Procedure:** '+p['test'], '', '**Conditions / side effects:** '+p['conditions'],
           '', '**Probe mode:** `'+p['mode']+'`', '', '**Rivals:** '+p['rivals'],
           '', '**Basis:** '+p['basis'], '', '**API member:** '+p['member'], '', '| Observation | Interpretation | Inference limit | Next step |', '|---|---|---|---|'])
        for o in p['outcomes']:
            lines.append('| '+' | '.join(o[k].replace('|','/') for k in ('observation','meaning','limits','next_step'))+' |')
    lines.extend(['','## Limitations',''])
    lines.extend('- '+x for x in data['limitations'])
    (root/'pilots'/(ident+'.md')).write_text('\n'.join(lines)+'\n',encoding='utf8')
print('Three structured pilot cards generated and schema-checked')
