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
| 2026-10-10 | Saleh | Report: explained the coordinate origin and added the same locations measured from the frame |
| 2026-10-09 | Saleh | v1 wheel layout: CAD measured via SolidWorks API, 6.5 in hub motors + 4 x 2 in casters, alignment, loads, calculator, drawing |

## Key results / numbers / decisions
Full report: **[wheel_layout_report.md](wheel_layout_report.md)**. All coordinates are in the `Assem_Base.SLDASM` frame (X width, Y up, Z length, mm). **Origin (0,0,0):** X = 0 is the outer face of the left side profile, Y = 0 is the frame top (down is negative), Z = 0 is the cross-member end face at the lift-motor end ([details](wheel_layout_report.md#where-is-0-0-0)).

- **Layout:** 2 drive wheels at mid-length + 4 swivel casters at the corners. **The drive wheels are spring-loaded** (100 N preload each, ±5 mm travel); the casters are rigid and define the floor.
- **Drive wheels:** 6.5 in hoverboard hub motors, Ø165 mm. Axles at **X −87.5 / 392.5, Y −133.5, Z 305**; track 480 mm.
- **Casters:** 2 in (50 mm) swivel, **rated ≥ 60 kg**, installed height 75 mm (with a spacer). Axes at **X −17.5 / 322.5, Z 20 / 590**, on the cross-member bottom face Y −140.
- **Floor plane Y = −215.** Ground clearance is 75 mm, so the robot is **+53 mm taller** than the old one (check against the racks).
- **Torque needed:** 5.25 N·m per wheel (loaded, 2° slope, 0.5 m/s²). **Limit loaded acceleration to 0.4 m/s².**
- **Stable:** loaded tip-over limit 3.4 m/s²; in-place rotation radius 411 mm.

## Files in this folder
- `wheel_layout_report.md`: decisions, numbers, checks, hand-off per task
- `wheel_layout_drawing.svg`: dimensioned top + side view
- `wheel_layout_coordinates.csv`: axle, caster and floor coordinates for CAD
- `wheel_layout_calculator.xlsx`: live calculator (edit the blue inputs)
- `hub_motor_size_comparison.csv`: 6.5 / 8 / 10 in comparison
- `calc/`: Python sources (`wheel_layout_calc.py` regenerates the SVG and CSV files; `build_calculator_xlsx.py` builds the workbook)

## Open issues & next steps
- Measure the purchased hub motor and caster, update the calculator inputs, and re-run.
- Confirm the +53 mm height against the rack clearance.
- Decide which end is the front, and the suspension concept (slide or trailing arm) with Task 1.
- Assign materials to every CAD part to confirm the mass budget.
