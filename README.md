# AGV Graduation Project · Part 1: Mechanical & Cross-functional Prep

Mechanical design, manufacturing and the mechanical preparation for the electrical and software teams (CAD, URDF, mounting points). Part 1 runs **Sep 28 – Nov 15, 2026**. Electrical (Part 2) and Software (Part 3) will be added later.

📋 **Task board (tasks, deadlines, timeline):** https://salehnassar.github.io/agv-task-portal/

## Rules

- **Phases run in order: A → B → C → D.** A phase starts only when the previous phase is 100% complete. Tasks inside a phase run in parallel.
- **Document the same day.** Open your task folder below → **Add file → Upload files** → commit. Update the task README (pencil icon).
- **Commit messages:** `Task N: what you did`. When a task is finished: include **`Closes Task N`**, and the board moves it to Done automatically.
- Web upload max 25 MB per file; bigger CAD → GitHub Desktop (max 100 MB) or a STEP export.

## Tasks
| Task | Phase | Duration | Members | Deadline |
|---|---|---|---|---|
| [Task 1: Chassis CAD](Phase-A_design/01_chassis-cad/) | Phase A | 17 days | 4 | Wed Oct 14 |
| [Task 2: Wheel alignment calculations to choose the diameter of the wheels used](Phase-A_design/02_wheel-diameter-calcs/) | Phase A | 8 days | 1 | Mon Oct 5 |
| [Task 3: Lifting mechanism CAD edits (Design for Manufacturing)](Phase-A_design/03_lift-cad-dfm/) | Phase A | 15 days | 3 | Mon Oct 12 |
| [Task 4: Sheet metal cover CAD](Phase-A_design/04_sheet-metal-cover/) | Phase A | 17 days | 2 | Wed Oct 14 |
| [Task 5: Chassis with mechanism assembly](Phase-B_integration-and-analysis/05_chassis-mechanism-assembly/) | Phase B | 5 days | 2 | Mon Oct 19 |
| [Task 6: Chassis stress analysis](Phase-B_integration-and-analysis/06_chassis-stress-analysis/) | Phase B | 11 days | 3 | Sun Oct 25 |
| [Task 7: Mechanisms' modal analysis](Phase-B_integration-and-analysis/07_mechanism-modal-analysis/) | Phase B | 11 days | 3 | Sun Oct 25 |
| [Task 8: Purchase list (Al extrusion, Bearing, Wheels, Hoverboard motors)](Phase-B_integration-and-analysis/08_purchase-list/) | Phase B | 8 days | 2 | Thu Oct 22 |
| [Task 9: Chassis and mechanisms' manufacturing](Phase-C_manufacturing-and-urdf/09_manufacturing/) | Phase C | 14 days | 8 | Sun Nov 8 |
| [Task 10: CAD's URDF](Phase-C_manufacturing-and-urdf/10_cad-urdf/) | Phase C | 10 days | 2 | Wed Nov 4 |
| [Task 11: Electric components testing, connecting, and fixing to the chassis](Phase-D_electrical-and-simulation-prep/11_electrical-integration/) | Phase D | 7 days | 6 | Sun Nov 15 |
| [Task 12: New car simulation calculations and implementation](Phase-D_electrical-and-simulation-prep/12_new-car-simulation/) | Phase D | 7 days | 4 | Sun Nov 15 |

## Phase gates
| Gate | Date | Meaning |
|---|---|---|
| Gate A | Wed Oct 14 | Phase A 100% complete → Phase B unlocks |
| Gate B | Sun Oct 25 | Phase B 100% complete → Phase C unlocks |
| Gate C | Sun Nov 8 | Phase C 100% complete → Phase D unlocks |
| Part 1 | Sun Nov 15 | Part 1 (Mechanical & Prep) complete |

The earlier 35-task plan is kept for reference in [`archive/plan-v1/`](archive/plan-v1/).
