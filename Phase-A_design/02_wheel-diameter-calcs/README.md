# Task 2: Wheel alignment calculations to choose the diameter of the wheels used

**Phase:** Phase A · Design  
**Deliverable:** Calculation sheet + recommended wheel/motor size  
**Deadline, assignees and head-count:** see the [task portal](https://salehnassar.github.io/agv-task-portal/) (set by the team leader).

## What to do
Calculate the required wheel diameter and drive layout: traction and torque for robot + 100 kg payload, target speed, ground clearance, obstacle/threshold height, and alignment of the two drive wheels with the caster (all contact points on one plane, parallel axles). Compare the available hoverboard hub-motor sizes (e.g., 6.5 in, 8 in, 10 in) and recommend one. The result feeds the chassis CAD.

## Upload in this folder
- [x] Calculation sheet (Excel/PDF) with all assumptions
- [x] Comparison of candidate wheel sizes
- [x] README: chosen diameter and why

When the task is finished, write **`Closes Task 2`** in your commit message. The task board moves it to Done automatically.

---
_Fill in below the SAME DAY you work on this task (edit with the pencil icon)._

## Log
| Date | Who | What was done |
|---|---|---|
| YYYY-MM-DD | Member X | ... |
| 2026-09-30 | Saleh | Testing the board automation |
| 2026-10-20 | Saleh | v2: redid Task 2 on the new chassis CAD ([A-00] Main AMR Assembly, origin at the robot centre); found the axle/profile clash and the fix (frame -7 mm) |
| 2026-10-10 | Saleh | Report: explained the coordinate origin and added the same locations measured from the frame |
| 2026-10-09 | Saleh | v1 wheel layout: CAD measured via SolidWorks API, 6.5 in hub motors + 4 x 2 in casters, alignment, loads, calculator, drawing |

## Key results / numbers / decisions
**v2 (2026-10-20), based on the new chassis `[A-00] Main AMR Assembly` (Task 1).** Full report: **[wheel_layout_report.md](wheel_layout_report.md)**. v1 (old frame) is in `archive_v1_old-frame/`.

- **Reference point:** origin = robot centre (X 0, Z 0); Y up; the floor surface is **Y = +1.0** (the Ground part is 1 mm thick).
- **As modelled:** frame 524 × 656 (X ±262, Z ±328); drive tyres Ø172 at **X ±294.3, axle Y 87, Z 0** (track 588.6); casters at **X ±175, Z ±230.8**. All six wheels touch the floor plane ✔.
- ❌ **The axle sits on the bottom side profile under load** (gap −0.05 mm), so there is no room for the suspension. **Fix: lower the frame 7 mm.** Move Ground +7 (floor Y 8), move the axle +7 (Y 94), and use casters with **68.35 mm** installed height (for example a 64 mm low-profile caster + 4.35 mm spacer). The axle gap then becomes 6.95 mm.
- ❌ The caster model (76.85 mm) is 1.5 mm too tall for its space. ⚠️ The tyres stick out above the frame top (13.65 mm after the fix), so the cover needs wheel wells. ⚠️ No suspension and no materials in the CAD yet.
- **Drive:** preload **120 N per wheel**, spring ≤ 6 N/mm, ±5 mm travel; torque **5.75 N·m** per wheel; limit loaded acceleration to 0.5 m/s².
- **Casters:** rated **≥ 60 kg** each (worst load 385 N). **Stability:** tip-over limit loaded 3.1 m/s².

## Files in this folder
- `wheel_layout_report.md`: v2 report (reference point, measurements, problems + fix, final positions, loads, what each task should do)
- `wheel_layout_drawing.svg`: top + side view, as modelled
- `wheel_layout_coordinates.csv`: axle, caster and floor coordinates (Task 1 frame)
- `wheel_layout_calculator.xlsx`: live calculator (inputs = CAD measurements)
- `calc/`: Python sources
- `archive_v1_old-frame/`: v1, based on the old Assem_Base frame (superseded)

## Open issues & next steps
- Team to confirm the 7 mm frame lowering (or choose another option, see report section 3).
- Measure the real hub motor and caster; update the calculator.
- Define the front end of the robot.
