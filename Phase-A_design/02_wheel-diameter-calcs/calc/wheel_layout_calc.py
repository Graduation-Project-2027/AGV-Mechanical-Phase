"""Task 2 v2: wheel layout check for the NEW chassis ([A-00] Main AMR Assembly, Task 1).

All coordinates are in the frame of "[A-00] Main AMR Assembly.SLDASM", read with the SolidWorks API
on 2026-10-20 from the latest version on GitHub (commit e98996c):

    Origin = centre of the robot in plan (X = 0, Z = 0)
    X = across the robot (width),  Y = up,  Z = along the robot (length),  mm
    Y = 0 is the UNDERSIDE of the 1 mm "Ground" part -> the floor surface is Y = +1.0

Run:  python wheel_layout_calc.py   -> regenerates ../wheel_layout_coordinates.csv, ../wheel_layout_drawing.svg, results.json
"""
import csv
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

# ----------------------------------------------------------------------------- MEASURED FROM THE CAD
FLOOR_Y = 1.0                    # top face of [A-02] Ground
FRAME_X = 262.0                  # 3030 frame outer faces at X = +/-262 (524 wide)
FRAME_Z = 328.0                  # 3030 frame outer faces at Z = +/-328 (656 long)
FRAME_BOTTOM_Y = 46.35           # underside of the bottom 3030 profiles
BOTTOM_PROFILE_TOP_Y = 76.35     # top of the bottom profiles = underside of the First Plate
PLATE_TOP_Y = 79.35              # First Plate 3 mm (X +/-230, Z +/-290)
FRAME_TOP_Y = 166.35             # top of the top 3030 profiles
LOWEST_CHASSIS_Y = 36.35         # cross joints / tee brackets (lowest non-wheel parts)
SIDE_PROFILE_X = (232.0, 262.0)  # bottom side profiles (each side), Y 46.35..76.35

DRIVE_AXLE_Y = 87.0              # hub-motor axle centre ("axe" part)
DRIVE_AXLE_Z = 0.0
DRIVE_PLANE_X = 294.3            # tyre mid-plane (tyre X 271.3..317.3)
DRIVE_TYRE_X = (271.3, 317.3)
DRIVE_TYRE_D = 172.0             # tyre OD from the rotated "pneu" bounding box (240.2 / (0.587 + 0.810))
DRIVE_AXLE_R = 9.7               # axle shaft radius (box 19.4 mm)
DRIVE_AXLE_INNER_X = 216.2       # inner end of the axle (inside the frame)

CASTER_AXIS_X = 175.0            # swivel axis (centre of the caster top plate)
CASTER_AXIS_Z = 230.8
CASTER_WHEEL_D = 50.7
CASTER_LEAD = 23.0               # swivel axis -> wheel axle (wheel trails towards the robot centre)
CASTER_TOP_Y = 77.85             # top of the caster model ("UPPER BASE")
CASTER_MOUNT_Y = BOTTOM_PROFILE_TOP_Y  # casters hang under the First Plate

# ----------------------------------------------------------------------------- DESIGN INPUTS
TYRE_DEFLECTION = 1.0            # mm under load (solid tyre)
SUSP_DOWN = 5.0                  # mm the wheel must be able to drop (floor dips)
SUSP_UP = 5.0                    # mm the wheel must be able to rise (bumps)
AXLE_CLEARANCE_MIN = 1.0         # mm left between axle and frame at full droop
M_EMPTY = 36.8                   # kg, "Mass budget" sheet of wheel_layout_calculator.xlsx (CAD has no materials yet)
M_PAYLOAD = 100.0
H_CG_LOADED, H_CG_EMPTY, CG_OFFSET = 0.50, 0.15, 0.05
ACCEL, SLOPE_DEG, CRR = 0.5, 2.0, 0.015
MU_NOM, MU_WORST, G = 0.5, 0.4, 9.81
PRELOAD = 120.0                  # N per drive wheel (raised from 100 N: heavier robot)
FLOOR_TOL, FORCE_VAR = 5.0, 0.25

R = {}
r_free = DRIVE_TYRE_D / 2
r_loaded = r_free - TYRE_DEFLECTION

# 1) vertical alignment as modelled
R['caster_contact_y'] = FLOOR_Y
R['drive_contact_y_as_modelled'] = DRIVE_AXLE_Y - r_free
R['drive_contact_error_mm'] = R['drive_contact_y_as_modelled'] - FLOOR_Y
R['caster_mount_height_above_floor'] = CASTER_MOUNT_Y - FLOOR_Y
R['caster_model_height'] = CASTER_TOP_Y - FLOOR_Y
R['caster_plate_overlap_mm'] = CASTER_TOP_Y - CASTER_MOUNT_Y
R['ground_clearance_frame'] = FRAME_BOTTOM_Y - FLOOR_Y
R['ground_clearance_lowest'] = LOWEST_CHASSIS_Y - FLOOR_Y
R['frame_top_above_floor'] = FRAME_TOP_Y - FLOOR_Y
R['drive_top_y'] = DRIVE_AXLE_Y + r_free
R['drive_top_above_frame_top'] = R['drive_top_y'] - FRAME_TOP_Y

# 2) axle vs the bottom side profile (the axle passes over it at Z = 0)
R['axle_gap_to_bottom_profile'] = (DRIVE_AXLE_Y - DRIVE_AXLE_R) - BOTTOM_PROFILE_TOP_Y
need = SUSP_DOWN + AXLE_CLEARANCE_MIN
# Under load the axle sits at floor + loaded radius. The wheel must be able to DROP by SUSP_DOWN without the
# axle touching the bottom side profile it passes over. The axle height above the floor is fixed by the tyre,
# so the fix is to LOWER the frame (shorter installed casters) by L mm:
gap_loaded = (FLOOR_Y + r_loaded - DRIVE_AXLE_R) - BOTTOM_PROFILE_TOP_Y
R['axle_gap_loaded_now'] = gap_loaded
lower = max(0, math.ceil(need - gap_loaded))
R['proposed_frame_lowering_mm'] = lower
R['proposed_axle_y'] = FLOOR_Y + r_loaded
R['proposed_axle_gap_loaded'] = gap_loaded + lower
R['proposed_caster_mount_height'] = R['caster_mount_height_above_floor'] - lower
R['proposed_clearance_frame'] = R['ground_clearance_frame'] - lower
R['proposed_clearance_lowest'] = R['ground_clearance_lowest'] - lower
R['proposed_frame_top_above_floor'] = R['frame_top_above_floor'] - lower
R['proposed_tyre_top_above_frame_top'] = R['drive_top_above_frame_top'] + lower
R['tyre_gap_to_frame'] = DRIVE_TYRE_X[0] - FRAME_X

# 3) plan geometry
R['track'] = 2 * DRIVE_PLANE_X
R['width_over_tyres'] = 2 * DRIVE_TYRE_X[1]
R['caster_track'] = 2 * CASTER_AXIS_X
R['caster_base'] = 2 * CASTER_AXIS_Z
R['caster_swivel_radius'] = CASTER_LEAD + CASTER_WHEEL_D / 2
R['rotation_radius'] = math.hypot(FRAME_X, FRAME_Z)

# 4) stability (casters swivelled inwards: contact moves to the robot centre by the lead)
cin = (CASTER_AXIS_X - CASTER_LEAD, CASTER_AXIS_Z - CASTER_LEAD)
p1, p2 = cin, (DRIVE_PLANE_X, 0.0)
side = abs(p2[0] * p1[1] - p2[1] * p1[0]) / math.hypot(p2[0] - p1[0], p2[1] - p1[1])
R['margin_long_m'] = cin[1] / 1000
R['margin_side_m'] = side / 1000
R['margin_min_m'] = min(R['margin_long_m'], R['margin_side_m'])
R['tip_accel_loaded'] = G * (R['margin_min_m'] - CG_OFFSET) / H_CG_LOADED
R['tip_accel_empty'] = G * R['margin_min_m'] / H_CG_EMPTY

# 5) drive, traction, casters
m_l = M_EMPTY + M_PAYLOAD
th = math.radians(SLOPE_DEG)
rm = r_loaded / 1000
f_flat = m_l * (G * CRR + ACCEL)
f_slope = m_l * (G * CRR * math.cos(th) + G * math.sin(th) + ACCEL)
R['loaded_mass'] = m_l
R['torque_flat'] = f_flat / 2 * rm
R['torque_slope'] = f_slope / 2 * rm
R['rpm_1mps'] = 60 / (math.pi * DRIVE_TYRE_D / 1000)
R['preload_fraction'] = 2 * PRELOAD / (M_EMPTY * G)
R['caster_load_empty'] = (M_EMPTY * G - 2 * PRELOAD) / 4
R['caster_load_static'] = (m_l * G - 2 * PRELOAD) / 4
base = R['caster_base'] / 1000
R['caster_load_worst'] = R['caster_load_static'] + m_l * ACCEL * H_CG_LOADED / base / 2 + m_l * G * CG_OFFSET / base / 2
R['caster_rating_kg'] = R['caster_load_worst'] * 1.5 / G
R['a_slip_nom'] = (2 * MU_NOM * PRELOAD - m_l * G * CRR) / m_l
R['a_slip_worst'] = (2 * MU_WORST * PRELOAD - m_l * G * CRR) / m_l
R['a_slip_slope_worst'] = (2 * MU_WORST * PRELOAD - m_l * G * (CRR * math.cos(th) + math.sin(th))) / m_l
R['k_wheel'] = FORCE_VAR * PRELOAD / FLOOR_TOL
R['preload_compression'] = PRELOAD / R['k_wheel']

# ----------------------------------------------------------------------------- OUTPUTS
rows = [
    ("floor_surface", "", FLOOR_Y, "", "", "Top face of [A-02] Ground. Heights above the floor = Y - 1.0"),
    ("drive_axle_left", -DRIVE_PLANE_X, DRIVE_AXLE_Y, DRIVE_AXLE_Z, DRIVE_TYRE_D, "Tyre mid-plane X; axle centre as modelled (no preload/suspension yet)"),
    ("drive_axle_right", DRIVE_PLANE_X, DRIVE_AXLE_Y, DRIVE_AXLE_Z, DRIVE_TYRE_D, "Tyre mid-plane X; axle centre as modelled (no preload/suspension yet)"),
]
for sx in (-1, 1):
    for sz in (-1, 1):
        rows.append((f"caster_{'left' if sx < 0 else 'right'}_{'zneg' if sz < 0 else 'zpos'}", sx * CASTER_AXIS_X, CASTER_MOUNT_Y,
                     sz * CASTER_AXIS_Z, CASTER_WHEEL_D, "Swivel axis; caster plate under the First Plate (Y 76.35)"))
rows.append(("robot_centre", 0.0, FLOOR_Y, 0.0, "", "Assembly origin projected on the floor (rotation centre, base_link)"))
with open(os.path.join(OUT, "wheel_layout_coordinates.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["item", "x_mm", "y_mm", "z_mm", "wheel_diameter_mm", "note"])
    w.writerows(rows)
with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, indent=2)


def svg():
    s = 0.85
    W, H = 1180, 1210
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Arial, sans-serif" font-size="13">',
           '<rect width="100%" height="100%" fill="#ffffff"/>',
           '<style>.frame{fill:#d9dde3;stroke:#59616c;stroke-width:1.5}.plate{fill:#eef0f3;stroke:#9aa3ad;stroke-width:1}.drive{fill:#2f6fde;stroke:#1d3f80;stroke-width:1.5}'
           '.caster{fill:#d27d16;stroke:#7a4a0d;stroke-width:1.5}.env{fill:none;stroke:#d27d16;stroke-dasharray:4 3}'
           '.dim{stroke:#c0392b;stroke-width:1}.txt{fill:#1b1f24}.dimtxt{fill:#c0392b;font-weight:bold}.poly{fill:#1f9d63;fill-opacity:.10;stroke:#1f9d63;stroke-dasharray:6 4}'
           '.cl{stroke:#888;stroke-dasharray:10 4 2 4}.warn{fill:#c0392b;font-weight:bold}</style>',
           '<text x="20" y="30" font-size="18" font-weight="bold" class="txt">Task 2 v2: wheel layout of the new chassis ([A-00] Main AMR Assembly)</text>']
    cx, cz = 480, 380                 # page position of the origin (top view)

    def X(x): return cx + x * s
    def Z(z): return cz + z * s
    out.append('<text x="20" y="55" class="txt">TOP VIEW. Origin (0,0) = robot centre; X to the right, Z down the page; mm.</text>')
    out.append(f'<rect class="frame" x="{X(-FRAME_X)}" y="{Z(-FRAME_Z)}" width="{2*FRAME_X*s}" height="{2*FRAME_Z*s}"/>')
    out.append(f'<rect class="plate" x="{X(-230)}" y="{Z(-290)}" width="{460*s}" height="{580*s}"/>')
    poly = [(cin[0], cin[1]), (DRIVE_PLANE_X, 0), (cin[0], -cin[1]), (-cin[0], -cin[1]), (-DRIVE_PLANE_X, 0), (-cin[0], cin[1])]
    out.append(f'<polygon class="poly" points="{" ".join(f"{X(x)},{Z(z)}" for x, z in poly)}"/>')
    out.append(f'<line class="cl" x1="{X(0)}" y1="{Z(-370)}" x2="{X(0)}" y2="{Z(370)}"/><line class="cl" x1="{X(-360)}" y1="{Z(0)}" x2="{X(360)}" y2="{Z(0)}"/>')
    out.append(f'<circle cx="{X(0)}" cy="{Z(0)}" r="6" fill="#c0392b"/><text x="{X(0)+10}" y="{Z(0)-10}" class="warn">Origin (0,0,0)</text>')
    for sx in (-1, 1):
        out.append(f'<rect class="drive" x="{X(sx*DRIVE_PLANE_X - 23)}" y="{Z(-DRIVE_TYRE_D/2)}" width="{46*s}" height="{DRIVE_TYRE_D*s}" rx="6"/>')
        for sz in (-1, 1):
            out.append(f'<circle class="env" cx="{X(sx*CASTER_AXIS_X)}" cy="{Z(sz*CASTER_AXIS_Z)}" r="{R["caster_swivel_radius"]*s}"/>')
            out.append(f'<rect class="caster" x="{X(sx*CASTER_AXIS_X)-11}" y="{Z(sz*CASTER_AXIS_Z)-15}" width="22" height="30" rx="4"/>')
            out.append(f'<circle cx="{X(sx*CASTER_AXIS_X)}" cy="{Z(sz*CASTER_AXIS_Z)}" r="3" fill="#1b1f24"/>')

    def hdim(x1, x2, zl, label):
        out.append(f'<line class="dim" x1="{X(x1)}" y1="{Z(zl)}" x2="{X(x2)}" y2="{Z(zl)}"/>')
        for xx in (x1, x2):
            out.append(f'<line class="dim" x1="{X(xx)}" y1="{Z(zl)-6}" x2="{X(xx)}" y2="{Z(zl)+6}"/>')
        out.append(f'<text class="dimtxt" text-anchor="middle" x="{(X(x1)+X(x2))/2}" y="{Z(zl)-6}">{label}</text>')

    def vdim(z1, z2, xl, label, zt=None):
        out.append(f'<line class="dim" x1="{X(xl)}" y1="{Z(z1)}" x2="{X(xl)}" y2="{Z(z2)}"/>')
        for zz in (z1, z2):
            out.append(f'<line class="dim" x1="{X(xl)-6}" y1="{Z(zz)}" x2="{X(xl)+6}" y2="{Z(zz)}"/>')
        ty = Z(zt) if zt is not None else (Z(z1) + Z(z2)) / 2 + 4
        out.append(f'<text class="dimtxt" x="{X(xl)+8}" y="{ty}">{label}</text>')

    hdim(-DRIVE_PLANE_X, DRIVE_PLANE_X, 130, f"track {R['track']:.1f}  (wheels at X = ±{DRIVE_PLANE_X})")
    hdim(-CASTER_AXIS_X, CASTER_AXIS_X, -300, f"casters X = ±{CASTER_AXIS_X:.0f}")
    hdim(-FRAME_X, FRAME_X, -350, f"frame {2*FRAME_X:.0f} (X = ±{FRAME_X:.0f})")
    vdim(-CASTER_AXIS_Z, CASTER_AXIS_Z, 360, f"casters Z = ±{CASTER_AXIS_Z}", zt=-120)
    vdim(-FRAME_Z, FRAME_Z, 420, f"frame {2*FRAME_Z:.0f} (Z = ±{FRAME_Z:.0f})", zt=60)
    out.append(f'<text x="20" y="{Z(FRAME_Z)+50}" class="txt">Blue = 6.5 in hub-motor drive wheels (tyre Ø{DRIVE_TYRE_D:.0f} x 46, axle at Z = 0). Orange = 2 in casters, dashed = swivel envelope R{R["caster_swivel_radius"]:.0f}. Grey inner = First Plate.</text>')
    out.append(f'<text x="20" y="{Z(FRAME_Z)+70}" class="txt">Green dashed = worst-case support polygon (casters swivelled inwards).</text>')

    # side view (from +X): horizontal = Z, vertical = Y
    fy0 = 1120
    def SZ(z): return cx + z * s
    def SY(y): return fy0 - (y - FLOOR_Y) * s * 1.6
    out.append(f'<text x="20" y="{SY(230)}" class="txt">SIDE VIEW (from the right, vertical scale x1.6). Floor = Y 1.0 (top of the Ground part).</text>')
    out.append(f'<line x1="{SZ(-400)}" y1="{SY(FLOOR_Y)}" x2="{SZ(400)}" y2="{SY(FLOOR_Y)}" stroke="#1b1f24" stroke-width="2"/>')
    out.append(f'<rect class="frame" x="{SZ(-FRAME_Z)}" y="{SY(FRAME_TOP_Y)}" width="{2*FRAME_Z*s}" height="{(FRAME_TOP_Y-FRAME_BOTTOM_Y)*s*1.6}" fill-opacity=".6"/>')
    out.append(f'<ellipse class="drive" cx="{SZ(0)}" cy="{SY(DRIVE_AXLE_Y)}" rx="{r_free*s}" ry="{r_free*s*1.6}" fill-opacity=".8"/>')
    out.append(f'<circle cx="{SZ(0)}" cy="{SY(DRIVE_AXLE_Y)}" r="4" fill="#fff"/>')
    for sz in (-1, 1):
        out.append(f'<rect class="caster" x="{SZ(sz*CASTER_AXIS_Z)-10}" y="{SY(CASTER_MOUNT_Y)}" width="20" height="{(CASTER_MOUNT_Y-FLOOR_Y-CASTER_WHEEL_D)*s*1.6}"/>')
        out.append(f'<ellipse class="caster" cx="{SZ(sz*(CASTER_AXIS_Z-CASTER_LEAD))}" cy="{SY(FLOOR_Y+CASTER_WHEEL_D/2)}" rx="{CASTER_WHEEL_D/2*s}" ry="{CASTER_WHEEL_D/2*s*1.6}"/>')

    def sdim(y1, y2, zl, label, left=False):
        out.append(f'<line class="dim" x1="{SZ(zl)}" y1="{SY(y1)}" x2="{SZ(zl)}" y2="{SY(y2)}"/>')
        for yy in (y1, y2):
            out.append(f'<line class="dim" x1="{SZ(zl)-6}" y1="{SY(yy)}" x2="{SZ(zl)+6}" y2="{SY(yy)}"/>')
        out.append(f'<text class="dimtxt" text-anchor="{"end" if left else "start"}" x="{SZ(zl)+(-8 if left else 8)}" y="{(SY(y1)+SY(y2))/2+4}">{label}</text>')
    sdim(FLOOR_Y, CASTER_MOUNT_Y, -380, f"{CASTER_MOUNT_Y-FLOOR_Y:.2f} floor to caster plate", left=True)
    sdim(FLOOR_Y, FRAME_BOTTOM_Y, -340, f"{FRAME_BOTTOM_Y-FLOOR_Y:.2f}", left=True)
    out.append(f'<text class="dimtxt" text-anchor="middle" x="{SZ(0)}" y="{SY(DRIVE_TYRE_D + FLOOR_Y) - 10}">drive axle Y {DRIVE_AXLE_Y:.1f} · tyre Ø{DRIVE_TYRE_D:.0f} · top Y {DRIVE_AXLE_Y + r_free:.0f}</text>')
    sdim(FLOOR_Y, FRAME_TOP_Y, 380, f"{FRAME_TOP_Y-FLOOR_Y:.2f} floor to frame top")
    out.append(f'<text x="20" y="{SY(FLOOR_Y)+30}" class="warn">Check: axle-to-profile gap {R["axle_gap_to_bottom_profile"]:.2f} mm (needs ≥ {need:.0f} for suspension droop) · tyre top {R["drive_top_above_frame_top"]:.2f} mm above the frame top · caster model {R["caster_plate_overlap_mm"]:.1f} mm into the plate.</text>')
    out.append('</svg>')
    return "\n".join(out)


with open(os.path.join(OUT, "wheel_layout_drawing.svg"), "w", encoding="utf-8", newline="\n") as f:
    f.write(svg())

if __name__ == "__main__":
    print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in R.items()}, indent=1))
