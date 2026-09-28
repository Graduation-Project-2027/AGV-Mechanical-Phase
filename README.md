# AGV Mechanical Phase (GP2)

All work for the mechanical phase of the AGV: new aluminum-profile chassis, differential drive wheels, and the four-scissor lift (Sep 28 – Nov 9, 2026).

📋 **Task portal (tasks, deadlines, timeline):** https://salehnassar.github.io/agv-task-portal/

## ⚠️ Rule: document everything the same day

1. Every task already has a folder here (see the table below). Open **your** task folder.
2. **Add file → Upload files**, drag your files in, **Commit changes**. Web upload max 25 MB per file; bigger CAD → GitHub Desktop (max 100 MB) or a STEP export.
3. Edit the task's `README.md` (pencil icon): log what you did, key numbers and decisions, open issues.
4. Commit message format: `[task code] what you did`, e.g. `[1.2] Frame v2: added cross-members for lift base`.
5. Send the folder link to the team leader so the task is marked as documented in the portal.

**No upload = not done.**

## Structure
| Folder | Parent task | Category |
|---|---|---|
| [T1_chassis-cad/](T1_chassis-cad/) | SolidWorks design of the new chassis (aluminum profiles + 4-side aluminum sheet enclosure) | A · Chassis & Wheels |
| [T2_wheel-config/](T2_wheel-config/) | Wheel configuration in CAD: 2 middle drive wheels (2 motors + 2 encoders) + 1 front caster | A · Chassis & Wheels |
| [T3_market-research/](T3_market-research/) | Market research & cost estimation: suppliers, workshops and detailed pricing table | A · Chassis & Wheels |
| [T4_chassis-fabrication/](T4_chassis-fabrication/) | Procurement, fabrication & assembly of the chassis at the selected workshops | A · Chassis & Wheels |
| [T5_lift-cad/](T5_lift-cad/) | Find a proven, ready-made SolidWorks four-scissor lift model and extract reliable dimensions | B · Lifting Mechanism (Four-Scissor) |
| [T6_lift-materials-and-mfg/](T6_lift-materials-and-mfg/) | Manufacturing methods & material selection for the selected lift | B · Lifting Mechanism (Four-Scissor) |
| [T7_lift-fabrication/](T7_lift-fabrication/) | Fabrication, assembly & testing of the lifting mechanism | B · Lifting Mechanism (Four-Scissor) |

## All tasks by deadline
| Code | Task | Assigned | Deadline |
|---|---|---|---|
| 1.1 | [Define chassis requirements & design envelope](T1_chassis-cad/1.1_define-chassis-requirements-and-design/) | Member 1 (owner), Member 2, Member 7 | Wed Sep 30 |
| 2.1 | [Replace omni wheels with the differential layout](T2_wheel-config/2.1_replace-omni-wheels/) | Member 3 (owner) | Thu Oct 1 |
| 2.2 | [Drive motor & encoder sizing](T2_wheel-config/2.2_drive-motor-and-encoder-sizing/) | Member 4 (owner) | Sun Oct 4 |
| 5.1 | [Search for ready-made four-scissor lift CAD](T5_lift-cad/5.1_search-for-ready-made-four-scissor-lift/) | Member 7 (owner), Member 8 | Mon Oct 5 |
| 1.2 | [Model the aluminum-profile frame](T1_chassis-cad/1.2_model-the-aluminum-profile-frame/) | Member 1 (owner) | Thu Oct 8 |
| 3.1 | [Suppliers: motors, encoders, wheels & caster](T3_market-research/3.1_suppliers-motors-encoders-wheels/) | Member 5 (owner), Member 4 | Thu Oct 8 |
| 3.2 | [Suppliers: aluminum profiles, sheets & connectors](T3_market-research/3.2_suppliers-aluminum-profiles-sheets/) | Member 6 (owner) | Thu Oct 8 |
| 5.2 | [Shortlist & compare candidates](T5_lift-cad/5.2_shortlist-and-compare-candidates/) | Member 8 (owner), Member 7 | Thu Oct 8 |
| 1.3 | [Model the 4-side aluminum-sheet enclosure](T1_chassis-cad/1.3_model-the-4-side-aluminum-sheet/) | Member 2 (owner) | Mon Oct 12 |
| 2.3 | [Model motor, encoder, wheel & caster mounts](T2_wheel-config/2.3_model-motor-encoder-wheel-and-caster/) | Member 3 (owner), Member 4 | Mon Oct 12 |
| 3.3 | [Workshop survey & quotations](T3_market-research/3.3_workshop-survey-and-quotations/) | Member 6 (owner), Member 10 | Mon Oct 12 |
| 3.4 | [Detailed pricing table v1](T3_market-research/3.4_detailed-pricing-table-v1/) | Member 5 (owner), Member 6 | Mon Oct 12 |
| 5.3 | [Select model, verify & extract dimensions](T5_lift-cad/5.3_select-model-verify-and-extract/) | Member 7 (owner), Member 8 | Mon Oct 12 |
| 6.1 | [Material selection study for the lift](T6_lift-materials-and-mfg/6.1_material-selection-study-for-the-lift/) | Member 9 (owner), Member 10 | Mon Oct 12 |
| 1.4 | [Frame structural check (FEA)](T1_chassis-cad/1.4_frame-structural-check-fea/) | Member 1 (owner), Member 2 | Thu Oct 15 |
| 2.4 | [Stability & tip-over check (CG vs. 3-point support)](T2_wheel-config/2.4_stability-and-tip-over-check-cg-vs-3/) | Member 3 (owner), Member 4 | Thu Oct 15 |
| 3.5 | [Final pricing table & budget approval](T3_market-research/3.5_final-pricing-table-and-budget-approval/) | Member 5 (owner), Member 6 | Thu Oct 15 |
| 5.4 | [Finalize lift CAD & integrate into chassis](T5_lift-cad/5.4_finalize-lift-cad-and-integrate-into/) | Member 8 (owner), Member 7, Member 1 | Thu Oct 15 |
| 6.2 | [Manufacturing method per lift part](T6_lift-materials-and-mfg/6.2_manufacturing-method-per-lift-part/) | Member 10 (owner), Member 9 | Thu Oct 15 |
| 1.5 | [Chassis design freeze & manufacturing drawings](T1_chassis-cad/1.5_chassis-design-freeze-and-manufacturing/) | Member 2 (owner), Member 1 | Mon Oct 19 |
| 3.6 | [Lock in workshop deals](T3_market-research/3.6_lock-in-workshop-deals/) | Member 6 (owner), Member 10, Member 5 | Mon Oct 19 |
| 6.3 | [Finalize materials & lift manufacturing drawings](T6_lift-materials-and-mfg/6.3_finalize-materials-and-lift/) | Member 9 (owner), Member 8 | Mon Oct 19 |
| 4.1 | [Procure aluminum materials](T4_chassis-fabrication/4.1_procure-aluminum-materials/) | Member 6 (owner), Member 3 | Thu Oct 22 |
| 4.2 | [Procure motors, encoders, wheels & caster](T4_chassis-fabrication/4.2_procure-motors-encoders-wheels/) | Member 5 (owner), Member 4 | Mon Oct 26 |
| 4.3 | [Incoming inspection & workshop hand-off](T4_chassis-fabrication/4.3_incoming-inspection-and-workshop-hand/) | Member 2 (owner), Member 3 | Mon Oct 26 |
| 7.1 | [Procure lift materials & hardware](T7_lift-fabrication/7.1_procure-lift-materials-and-hardware/) | Member 9 (owner), Member 10 | Mon Oct 26 |
| 4.4 | [Cut & drill profiles; cut & bend sheets](T4_chassis-fabrication/4.4_cut-and-drill-profiles-cut-and-bend/) | Member 1 (owner), Member 2 | Sun Nov 1 |
| 7.2 | [Manufacture lift parts at the workshop](T7_lift-fabrication/7.2_manufacture-lift-parts-at-the-workshop/) | Member 10 (owner), Member 9 | Mon Nov 2 |
| 4.5 | [Frame assembly + drive-train installation](T4_chassis-fabrication/4.5_frame-assembly-drive-train-installation/) | Member 3 (owner), Member 4, Member 1 | Thu Nov 5 |
| 7.3 | [Assemble the four-scissor lift](T7_lift-fabrication/7.3_assemble-the-four-scissor-lift/) | Member 7 (owner), Member 8 | Thu Nov 5 |
| 4.6 | [Enclosure sheet fitting](T4_chassis-fabrication/4.6_enclosure-sheet-fitting/) | Member 2 (owner), Member 6 | Fri Nov 6 |
| 7.4 | [Mount the lift on the chassis](T7_lift-fabrication/7.4_mount-the-lift-on-the-chassis/) | Member 7 (owner), Member 8, Member 9 | Sat Nov 7 |
| 4.7 | [Chassis initial mechanical tests](T4_chassis-fabrication/4.7_chassis-initial-mechanical-tests/) | Member 4 (owner), Member 5, Member 3 | Mon Nov 9 |
| 7.5 | [Lift functional & load tests](T7_lift-fabrication/7.5_lift-functional-and-load-tests/) | Member 8 (owner), Member 10, Member 9 | Mon Nov 9 |
| 7.6 | [Mechanical test report & hand-over](T7_lift-fabrication/7.6_mechanical-test-report-and-hand-over/) | Member 7 (owner), Member 1 | Mon Nov 9 |

Members are listed as placeholders (Member 1–10); the team leader shares who is who.
