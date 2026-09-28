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
| 1.1 | [Define chassis requirements & design envelope](T1_chassis-cad/1.1_define-chassis-requirements-and-design/) | Yasmin Mohamed (owner), Basmala Mohamed, Saleh Nassar | Wed Sep 30 |
| 2.1 | [Replace omni wheels with the differential layout](T2_wheel-config/2.1_replace-omni-wheels/) | Ahmed Alattar (owner) | Thu Oct 1 |
| 2.2 | [Drive motor & encoder sizing](T2_wheel-config/2.2_drive-motor-and-encoder-sizing/) | Youssef Wahba (owner) | Sun Oct 4 |
| 5.1 | [Search for ready-made four-scissor lift CAD](T5_lift-cad/5.1_search-for-ready-made-four-scissor-lift/) | Saleh Nassar (owner), Nadine Elframawy | Mon Oct 5 |
| 1.2 | [Model the aluminum-profile frame](T1_chassis-cad/1.2_model-the-aluminum-profile-frame/) | Yasmin Mohamed (owner) | Thu Oct 8 |
| 3.1 | [Suppliers: motors, encoders, wheels & caster](T3_market-research/3.1_suppliers-motors-encoders-wheels/) | Nada Ali (owner), Youssef Wahba | Thu Oct 8 |
| 3.2 | [Suppliers: aluminum profiles, sheets & connectors](T3_market-research/3.2_suppliers-aluminum-profiles-sheets/) | Ahmed Elbrolosy (owner) | Thu Oct 8 |
| 5.2 | [Shortlist & compare candidates](T5_lift-cad/5.2_shortlist-and-compare-candidates/) | Nadine Elframawy (owner), Saleh Nassar | Thu Oct 8 |
| 1.3 | [Model the 4-side aluminum-sheet enclosure](T1_chassis-cad/1.3_model-the-4-side-aluminum-sheet/) | Basmala Mohamed (owner) | Mon Oct 12 |
| 2.3 | [Model motor, encoder, wheel & caster mounts](T2_wheel-config/2.3_model-motor-encoder-wheel-and-caster/) | Ahmed Alattar (owner), Youssef Wahba | Mon Oct 12 |
| 3.3 | [Workshop survey & quotations](T3_market-research/3.3_workshop-survey-and-quotations/) | Ahmed Elbrolosy (owner), Omar Farahat | Mon Oct 12 |
| 3.4 | [Detailed pricing table v1](T3_market-research/3.4_detailed-pricing-table-v1/) | Nada Ali (owner), Ahmed Elbrolosy | Mon Oct 12 |
| 5.3 | [Select model, verify & extract dimensions](T5_lift-cad/5.3_select-model-verify-and-extract/) | Saleh Nassar (owner), Nadine Elframawy | Mon Oct 12 |
| 6.1 | [Material selection study for the lift](T6_lift-materials-and-mfg/6.1_material-selection-study-for-the-lift/) | Basant Salah (owner), Omar Farahat | Mon Oct 12 |
| 1.4 | [Frame structural check (FEA)](T1_chassis-cad/1.4_frame-structural-check-fea/) | Yasmin Mohamed (owner), Basmala Mohamed | Thu Oct 15 |
| 2.4 | [Stability & tip-over check (CG vs. 3-point support)](T2_wheel-config/2.4_stability-and-tip-over-check-cg-vs-3/) | Ahmed Alattar (owner), Youssef Wahba | Thu Oct 15 |
| 3.5 | [Final pricing table & budget approval](T3_market-research/3.5_final-pricing-table-and-budget-approval/) | Nada Ali (owner), Ahmed Elbrolosy | Thu Oct 15 |
| 5.4 | [Finalize lift CAD & integrate into chassis](T5_lift-cad/5.4_finalize-lift-cad-and-integrate-into/) | Nadine Elframawy (owner), Saleh Nassar, Yasmin Mohamed | Thu Oct 15 |
| 6.2 | [Manufacturing method per lift part](T6_lift-materials-and-mfg/6.2_manufacturing-method-per-lift-part/) | Omar Farahat (owner), Basant Salah | Thu Oct 15 |
| 1.5 | [Chassis design freeze & manufacturing drawings](T1_chassis-cad/1.5_chassis-design-freeze-and-manufacturing/) | Basmala Mohamed (owner), Yasmin Mohamed | Mon Oct 19 |
| 3.6 | [Lock in workshop deals](T3_market-research/3.6_lock-in-workshop-deals/) | Ahmed Elbrolosy (owner), Omar Farahat, Nada Ali | Mon Oct 19 |
| 6.3 | [Finalize materials & lift manufacturing drawings](T6_lift-materials-and-mfg/6.3_finalize-materials-and-lift/) | Basant Salah (owner), Nadine Elframawy | Mon Oct 19 |
| 4.1 | [Procure aluminum materials](T4_chassis-fabrication/4.1_procure-aluminum-materials/) | Ahmed Elbrolosy (owner), Ahmed Alattar | Thu Oct 22 |
| 4.2 | [Procure motors, encoders, wheels & caster](T4_chassis-fabrication/4.2_procure-motors-encoders-wheels/) | Nada Ali (owner), Youssef Wahba | Mon Oct 26 |
| 4.3 | [Incoming inspection & workshop hand-off](T4_chassis-fabrication/4.3_incoming-inspection-and-workshop-hand/) | Basmala Mohamed (owner), Ahmed Alattar | Mon Oct 26 |
| 7.1 | [Procure lift materials & hardware](T7_lift-fabrication/7.1_procure-lift-materials-and-hardware/) | Basant Salah (owner), Omar Farahat | Mon Oct 26 |
| 4.4 | [Cut & drill profiles; cut & bend sheets](T4_chassis-fabrication/4.4_cut-and-drill-profiles-cut-and-bend/) | Yasmin Mohamed (owner), Basmala Mohamed | Sun Nov 1 |
| 7.2 | [Manufacture lift parts at the workshop](T7_lift-fabrication/7.2_manufacture-lift-parts-at-the-workshop/) | Omar Farahat (owner), Basant Salah | Mon Nov 2 |
| 4.5 | [Frame assembly + drive-train installation](T4_chassis-fabrication/4.5_frame-assembly-drive-train-installation/) | Ahmed Alattar (owner), Youssef Wahba, Yasmin Mohamed | Thu Nov 5 |
| 7.3 | [Assemble the four-scissor lift](T7_lift-fabrication/7.3_assemble-the-four-scissor-lift/) | Saleh Nassar (owner), Nadine Elframawy | Thu Nov 5 |
| 4.6 | [Enclosure sheet fitting](T4_chassis-fabrication/4.6_enclosure-sheet-fitting/) | Basmala Mohamed (owner), Ahmed Elbrolosy | Fri Nov 6 |
| 7.4 | [Mount the lift on the chassis](T7_lift-fabrication/7.4_mount-the-lift-on-the-chassis/) | Saleh Nassar (owner), Nadine Elframawy, Basant Salah | Sat Nov 7 |
| 4.7 | [Chassis initial mechanical tests](T4_chassis-fabrication/4.7_chassis-initial-mechanical-tests/) | Youssef Wahba (owner), Nada Ali, Ahmed Alattar | Mon Nov 9 |
| 7.5 | [Lift functional & load tests](T7_lift-fabrication/7.5_lift-functional-and-load-tests/) | Nadine Elframawy (owner), Omar Farahat, Basant Salah | Mon Nov 9 |
| 7.6 | [Mechanical test report & hand-over](T7_lift-fabrication/7.6_mechanical-test-report-and-hand-over/) | Saleh Nassar (owner), Yasmin Mohamed | Mon Nov 9 |

Members are listed as placeholders (Yasmin Mohamed–10); the team leader shares who is who.
