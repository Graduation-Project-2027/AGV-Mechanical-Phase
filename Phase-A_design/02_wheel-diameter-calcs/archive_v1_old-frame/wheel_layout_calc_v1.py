"""Task 2: wheel layout, diameters and alignment for the new 6-wheel AGV base.

Layout (like the RobiHaul / MiR style): 2 drive wheels (hoverboard hub motors) at mid-length,
one per side, on a spring suspension + 4 swivel casters at the corners.

All coordinates are in the SolidWorks assembly frame of Assem_Base.SLDASM (read from the CAD):
    X = across the robot (width),  Y = up,  Z = along the robot (length),  units = mm.
Change the INPUTS below and re-run: every output (CSV, SVG drawing, JSON) is regenerated.

    python wheel_layout_calc.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)  # the Task 2 folder

# ----------------------------------------------------------------------------- INPUTS
# Frame (measured from Assem_Base.SLDASM, 2026-10-09)
FRAME_X = (-47.5, 352.5)        # 400 mm cross members (outer ends)
FRAME_Z = (0.0, 610.0)          # 400 mm cross members at z 0..40 and 570..610
FRAME_TOP_Y = 0.0               # top face of the upper profiles
FRAME_BOTTOM_Y = -140.0         # bottom face of the lower 400 mm cross members (caster mounting face)
SIDE_RAIL_OUTER_X = (0.0, 305.0)  # outer faces of the lower 600 mm side rails (left x=0 face is at x=0? see note)
SIDE_RAIL_LOWER_Y = (-120.0, -100.0)  # lower 600 mm side rails (drive-module mounting face, outer side)
CROSS_MEMBER_Z = (20.0, 590.0)  # centre lines of the two lower cross members
CENTER_X = 152.5                # robot centre line (frame symmetric)
CENTER_Z = 305.0                # robot mid-length
LIDAR_HOUSING_Z = (-49.53, 664.53)  # longest parts along Z (for the rotation envelope)
OLD_GROUND_Y = -161.8           # old mecanum (D = 133 mm) contact level, for comparison
TABLE_TOP_Y = 3.35              # lift table top (lowered)
LIDAR_TOP_Y = 42.6

# Drive wheels: 6.5" hoverboard hub motor with solid tyre
DRIVE_D_NOMINAL = 165.0         # mm (6.5 in = 165.1 mm) -> MEASURE the purchased wheel and update
DRIVE_TYRE_WIDTH = 55.0         # mm (typical; measure)
DRIVE_TYRE_DEFLECTION = 1.0     # mm under load (solid rubber)
TRACK_WIDTH = 480.0             # mm, centre-to-centre of the two drive wheels (see layout notes)
DRIVE_Z = CENTER_Z              # drive axle at mid-length -> robot turns about its own centre

# Casters: 2" (50 mm) swivel casters, plate mounted under the lower cross members
CASTER_WHEEL_D = 50.0
CASTER_HEIGHT_DESIGN = 75.0     # mm, installed height from the cross-member bottom face to the floor
CASTER_LEAD = 35.0              # mm, horizontal offset swivel axis -> wheel axle (check datasheet)
CASTER_PLATE_ADAPTER = 60.0     # mm square adapter plate (caster plates are 38-51 mm, profile is 40 mm wide)
CASTER_X_INSET = 30.0           # mm, caster axis inset from the cross-member ends
CASTER_TYPES = [                # candidates found in research: (name, total height mm, rating kg)
    ("Revvo 50 mm low-profile twin nylon", 64.0, 160.0),
    ("Richelieu 50 mm twin nylon w/ brake", 73.0, 60.0),
    ("Generic 50 mm PU plate caster", 70.0, 29.5),
]

# Masses and motion targets
M_EMPTY = 30.2                  # kg, empty robot: "Mass budget" sheet of wheel_layout_calculator.xlsx
M_PAYLOAD = 100.0               # kg, design payload (GP1 sizing basis)
H_CG_EMPTY = 0.15               # m, CG height above floor, empty
H_CG_LOADED = 0.50              # m, CG height above floor, loaded + lift raised (conservative)
CG_OFFSET_LOADED = 0.05         # m, possible payload CG offset from centre (each direction)
ACCEL_TARGET = 0.5              # m/s^2 (loaded)
SLOPE_DEG = 2.0                 # floor slope / ramp to check
CRR = 0.015                     # rolling resistance (hard tyres on concrete/epoxy)
MU_NOMINAL = 0.5                # tyre-floor friction, solid rubber on smooth floor
MU_WORST = 0.4                  # dusty / polished floor
G = 9.81

# Suspension
DRIVE_PRELOAD_N = 100.0         # N pressing each drive wheel on the floor
FLOOR_TOLERANCE = 5.0           # mm, +/- vertical variation the suspension must absorb (floor + build)
MAX_FORCE_VARIATION = 0.25      # allowed +/- change of drive force over that travel

# ----------------------------------------------------------------------------- CALCULATION
R = {}

# 1) Vertical alignment: casters define the floor plane, drive axle placed relative to it
ground_y = FRAME_BOTTOM_Y - CASTER_HEIGHT_DESIGN
drive_r_loaded = DRIVE_D_NOMINAL / 2 - DRIVE_TYRE_DEFLECTION
axle_y = ground_y + drive_r_loaded
R['ground_y'] = ground_y
R['drive_axle_y_nominal'] = axle_y
R['drive_wheel_top_y'] = ground_y + DRIVE_D_NOMINAL
R['ground_clearance_under_frame'] = FRAME_BOTTOM_Y - ground_y
R['height_change_vs_old'] = OLD_GROUND_Y - ground_y
R['table_top_above_floor'] = TABLE_TOP_Y - ground_y
R['lidar_top_above_floor'] = LIDAR_TOP_Y - ground_y
R['caster_spacers'] = [
    {"caster": n, "total_height": h, "rating_kg": kg, "spacer_mm": round(CASTER_HEIGHT_DESIGN - h, 1)}
    for (n, h, kg) in CASTER_TYPES]

# 2) Plan positions
drive_left_x = CENTER_X - TRACK_WIDTH / 2
drive_right_x = CENTER_X + TRACK_WIDTH / 2
caster_x = (FRAME_X[0] + CASTER_X_INSET, FRAME_X[1] - CASTER_X_INSET)
casters = [(x, z) for z in CROSS_MEMBER_Z for x in caster_x]
R['drive_wheels'] = {"left": (drive_left_x, axle_y, DRIVE_Z), "right": (drive_right_x, axle_y, DRIVE_Z)}
R['casters'] = casters
R['caster_track_x'] = caster_x[1] - caster_x[0]
R['caster_wheelbase_z'] = CROSS_MEMBER_Z[1] - CROSS_MEMBER_Z[0]
R['overall_width_over_tyres'] = TRACK_WIDTH + DRIVE_TYRE_WIDTH
R['drive_inner_tyre_face_gap_to_rail'] = (drive_right_x - DRIVE_TYRE_WIDTH / 2) - SIDE_RAIL_OUTER_X[1]
R['caster_swivel_radius'] = CASTER_LEAD + CASTER_WHEEL_D / 2

# 3) In-place rotation envelope (turns about the midpoint of the drive axle = robot centre)
half_w = max(CENTER_X - FRAME_X[0], FRAME_X[1] - CENTER_X, TRACK_WIDTH / 2 + DRIVE_TYRE_WIDTH / 2)
half_l = max(CENTER_Z - LIDAR_HOUSING_Z[0], LIDAR_HOUSING_Z[1] - CENTER_Z)
R['rotation_radius'] = math.hypot(max(CENTER_X - FRAME_X[0], FRAME_X[1] - CENTER_X), half_l)

# 4) Support polygon and tip-over (casters can swivel inward by the lead: worst case)
pts = []
for (x, z) in casters:
    pts.append((x + (CASTER_LEAD if x < CENTER_X else -CASTER_LEAD),
                z + (CASTER_LEAD if z < CENTER_Z else -CASTER_LEAD)))
pts += [(drive_left_x, DRIVE_Z), (drive_right_x, DRIVE_Z)]


def hull(points):
    points = sorted(set(points))
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def dist_to_edges(poly, c):
    out = []
    for i in range(len(poly)):
        (x1, z1), (x2, z2) = poly[i], poly[(i + 1) % len(poly)]
        num = abs((z2 - z1) * c[0] - (x2 - x1) * c[1] + x2 * z1 - z2 * x1)
        out.append(num / math.hypot(x2 - x1, z2 - z1))
    return out


poly = hull(pts)
d = dist_to_edges(poly, (CENTER_X, CENTER_Z))
d_min = min(d) / 1000
d_long = (min(CENTER_Z - min(p[1] for p in poly), max(p[1] for p in poly) - CENTER_Z)) / 1000
R['support_polygon'] = poly
R['tip_margin_min_m'] = d_min
R['tip_margin_long_m'] = d_long
R['tip_accel_limit_loaded'] = G * (d_min - CG_OFFSET_LOADED) / H_CG_LOADED
R['tip_accel_limit_loaded_longitudinal'] = G * (d_long - CG_OFFSET_LOADED) / H_CG_LOADED
R['tip_accel_limit_empty'] = G * d_min / H_CG_EMPTY

# 5) Drive force, torque and speed
m_loaded = M_EMPTY + M_PAYLOAD
th = math.radians(SLOPE_DEG)
r_m = drive_r_loaded / 1000


def drive_force(m, a, slope):
    return m * (G * CRR * math.cos(slope) + G * math.sin(slope) + a)


cases = {
    "loaded, flat, a=%.1f" % ACCEL_TARGET: drive_force(m_loaded, ACCEL_TARGET, 0),
    "loaded, %g deg slope, a=%.1f" % (SLOPE_DEG, ACCEL_TARGET): drive_force(m_loaded, ACCEL_TARGET, th),
    "loaded, %g deg slope, constant speed" % SLOPE_DEG: drive_force(m_loaded, 0, th),
    "empty, flat, a=1.0": drive_force(M_EMPTY, 1.0, 0),
}
R['drive_cases'] = {k: {"total_N": v, "per_wheel_N": v / 2, "torque_per_wheel_Nm": v / 2 * r_m,
                        "normal_force_needed_mu_nom_N": v / 2 / MU_NOMINAL,
                        "normal_force_needed_mu_worst_N": v / 2 / MU_WORST} for k, v in cases.items()}
R['wheel_rpm_at_1mps'] = 1.0 / (math.pi * DRIVE_D_NOMINAL / 1000) * 60

# 6) Suspension preload: what the casters and drive wheels carry
w_empty, w_loaded = M_EMPTY * G, m_loaded * G
R['preload_fraction_of_empty_weight'] = 2 * DRIVE_PRELOAD_N / w_empty
R['caster_load_empty_N'] = (w_empty - 2 * DRIVE_PRELOAD_N) / 4
R['caster_load_loaded_static_N'] = (w_loaded - 2 * DRIVE_PRELOAD_N) / 4
transfer = m_loaded * ACCEL_TARGET * H_CG_LOADED / (R['caster_wheelbase_z'] / 1000) / 2
offset = w_loaded * CG_OFFSET_LOADED / (R['caster_wheelbase_z'] / 1000) / 2
R['caster_load_loaded_worst_N'] = R['caster_load_loaded_static_N'] + transfer + offset
R['caster_rating_required_kg'] = R['caster_load_loaded_worst_N'] * 1.5 / G  # x1.5: 4 rigid casters on an uneven floor
R['traction_accel_limit'] = {
    mu: (2 * mu * DRIVE_PRELOAD_N - drive_force(m_loaded, 0, 0)) / m_loaded for mu in (MU_NOMINAL, MU_WORST)}
R['traction_accel_limit_slope'] = {
    mu: (2 * mu * DRIVE_PRELOAD_N - drive_force(m_loaded, 0, th)) / m_loaded for mu in (MU_NOMINAL, MU_WORST)}
k_wheel = MAX_FORCE_VARIATION * DRIVE_PRELOAD_N / FLOOR_TOLERANCE
R['spring_rate_at_wheel_max_N_per_mm'] = k_wheel
R['spring_preload_compression_at_wheel_mm'] = DRIVE_PRELOAD_N / k_wheel
R['suspension_travel_at_wheel_mm'] = 2 * FLOOR_TOLERANCE

# ----------------------------------------------------------------------------- OUTPUTS
def r1(v):
    return round(v, 1)


rows = [
    ("ground_plane", "-", r1(ground_y), "-", "-", "Floor level (all 6 contact points must lie on this plane)"),
    ("drive_axle_left", r1(drive_left_x), r1(axle_y), r1(DRIVE_Z), DRIVE_D_NOMINAL, "Hub-motor axle centre, suspension at mid-travel"),
    ("drive_axle_right", r1(drive_right_x), r1(axle_y), r1(DRIVE_Z), DRIVE_D_NOMINAL, "Hub-motor axle centre, suspension at mid-travel"),
]
names = {(0, 0): "caster_1_left_end1", (1, 0): "caster_2_right_end1", (0, 1): "caster_3_left_end2", (1, 1): "caster_4_right_end2"}
for i, (x, z) in enumerate(casters):
    key = names[(0 if x < CENTER_X else 1, 0 if z < CENTER_Z else 1)]
    rows.append((key, r1(x), FRAME_BOTTOM_Y, r1(z), CASTER_WHEEL_D,
                 "Swivel axis; top of caster adapter plate bolted to the cross-member bottom face"))
rows.append(("robot_centre", CENTER_X, "-", CENTER_Z, "-", "Rotation centre for in-place turns (base_link)"))
import csv  # noqa: E402  (notes contain commas -> proper quoting)
with open(os.path.join(OUT, "wheel_layout_coordinates.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["item", "x_mm", "y_mm", "z_mm", "wheel_diameter_mm", "note"])
    w.writerows(rows)

# Hub-motor size comparison (same floor plane, same casters, same loaded slope case).
# Masses for 8 in / 10 in are estimates; 6.5 in from the Parallax listing.
SIZES = [("6.5 in", 165.1, 55, 3.1), ("8 in", 203.2, 60, 3.8), ("10 in", 254.0, 80, 4.6)]
cmp_rows = []
f_slope = drive_force(m_loaded, ACCEL_TARGET, th)
for name, dia, width, kg in SIZES:
    rl = dia / 2 - DRIVE_TYRE_DEFLECTION
    cmp_rows.append({
        "size": name, "diameter_mm": dia, "tyre_width_mm": width, "mass_kg_est": kg,
        "axle_y": round(ground_y + rl, 1), "wheel_top_y": round(ground_y + dia, 1),
        "wheel_top_above_frame_top_mm": round(ground_y + dia - FRAME_TOP_Y, 1),
        "torque_per_wheel_slope_case_Nm": round(f_slope / 2 * rl / 1000, 2),
        "wheel_rpm_at_1mps": round(60 / (math.pi * dia / 1000), 1),
        "max_step_mm_approx": round(0.2 * dia / 2),
    })
R["hub_motor_comparison"] = cmp_rows
with open(os.path.join(OUT, "hub_motor_size_comparison.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(cmp_rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(cmp_rows)

with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, indent=2, default=lambda o: list(o))


# ---- SVG drawing: top view + side view
def svg():
    s = 0.9            # px per mm
    W, H = 1180, 1270
    ox_top, oz_top = 120, 70          # top view origin offset (x right, z down)
    side_y0 = 1150                    # side view: floor line y (px), below the top view
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Arial, sans-serif" font-size="13">',
           '<rect width="100%" height="100%" fill="#ffffff"/>',
           '<style>.frame{fill:#d9dde3;stroke:#59616c;stroke-width:1.5}.drive{fill:#2f6fde;stroke:#1d3f80;stroke-width:1.5}'
           '.caster{fill:#d27d16;stroke:#7a4a0d;stroke-width:1.5}.env{fill:none;stroke:#d27d16;stroke-dasharray:4 3}'
           '.dim{stroke:#c0392b;stroke-width:1}.txt{fill:#1b1f24}.dimtxt{fill:#c0392b;font-weight:bold}.poly{fill:#1f9d63;fill-opacity:.10;stroke:#1f9d63;stroke-dasharray:6 4}'
           '.cl{stroke:#888;stroke-dasharray:10 4 2 4}</style>',
           '<text x="20" y="30" font-size="18" font-weight="bold" class="txt">Task 2: new wheel layout (2 drive + 4 casters), CAD frame of Assem_Base</text>']

    def X(x): return ox_top + (x - (-200)) * s
    def Z(z): return oz_top + (z - (-80)) * s

    out.append('<text x="20" y="55" class="txt">TOP VIEW (looking down, X to the right, Z down the page). Dimensions in mm.</text>')
    out.append(f'<rect class="frame" x="{X(FRAME_X[0])}" y="{Z(FRAME_Z[0])}" width="{(FRAME_X[1]-FRAME_X[0])*s}" height="{(FRAME_Z[1]-FRAME_Z[0])*s}"/>')
    out.append(f'<text x="{X(CENTER_X)-50}" y="{Z(CENTER_Z)+150}" class="txt">frame 400 x 610</text>')
    out.append(f'<polygon class="poly" points="{" ".join(f"{X(x)},{Z(z)}" for x, z in poly)}"/>')
    out.append(f'<line class="cl" x1="{X(CENTER_X)}" y1="{Z(-60)}" x2="{X(CENTER_X)}" y2="{Z(670)}"/>')
    out.append(f'<line class="cl" x1="{X(-180)}" y1="{Z(CENTER_Z)}" x2="{X(485)}" y2="{Z(CENTER_Z)}"/>')
    for x in (drive_left_x, drive_right_x):
        out.append(f'<rect class="drive" x="{X(x-DRIVE_TYRE_WIDTH/2)}" y="{Z(DRIVE_Z-DRIVE_D_NOMINAL/2)}" width="{DRIVE_TYRE_WIDTH*s}" height="{DRIVE_D_NOMINAL*s}" rx="6"/>')
    for (x, z) in casters:
        out.append(f'<circle class="env" cx="{X(x)}" cy="{Z(z)}" r="{R["caster_swivel_radius"]*s}"/>')
        out.append(f'<rect class="caster" x="{X(x)-9}" y="{Z(z)-22}" width="18" height="44" rx="5"/>')
        out.append(f'<circle cx="{X(x)}" cy="{Z(z)}" r="3" fill="#1b1f24"/>')

    def hdim(x1, x2, zline, label):
        out.append(f'<line class="dim" x1="{X(x1)}" y1="{Z(zline)}" x2="{X(x2)}" y2="{Z(zline)}"/>')
        for xx in (x1, x2):
            out.append(f'<line class="dim" x1="{X(xx)}" y1="{Z(zline)-6}" x2="{X(xx)}" y2="{Z(zline)+6}"/>')
        out.append(f'<text class="dimtxt" x="{(X(x1)+X(x2))/2-28}" y="{Z(zline)-6}">{label}</text>')

    def vdim(z1, z2, xline, label):
        out.append(f'<line class="dim" x1="{X(xline)}" y1="{Z(z1)}" x2="{X(xline)}" y2="{Z(z2)}"/>')
        for zz in (z1, z2):
            out.append(f'<line class="dim" x1="{X(xline)-6}" y1="{Z(zz)}" x2="{X(xline)+6}" y2="{Z(zz)}"/>')
        out.append(f'<text class="dimtxt" x="{X(xline)+8}" y="{(Z(z1)+Z(z2))/2}">{label}</text>')

    hdim(drive_left_x, drive_right_x, DRIVE_Z + 120, f"track {TRACK_WIDTH:.0f}")
    hdim(caster_x[0], caster_x[1], -50, f"caster track {R['caster_track_x']:.0f}")
    vdim(CROSS_MEMBER_Z[0], CROSS_MEMBER_Z[1], 560, f"caster base {R['caster_wheelbase_z']:.0f}")
    vdim(CROSS_MEMBER_Z[0], DRIVE_Z, 490, f"{DRIVE_Z-CROSS_MEMBER_Z[0]:.0f}")
    out.append(f'<text x="{X(-195)}" y="{Z(640)+30}" class="txt">Blue = 6.5" hub-motor drive wheels (axle at Z={DRIVE_Z:.0f}). Orange = 2" swivel casters, dashed circle = swivel envelope R{R["caster_swivel_radius"]:.0f}.</text>')
    out.append(f'<text x="{X(-195)}" y="{Z(640)+50}" class="txt">Green dashed = worst-case support polygon (casters swivelled inward). Centre lines through robot centre X={CENTER_X}, Z={CENTER_Z:.0f}.</text>')

    # side view (looking from +X): horizontal = Z, vertical = Y
    def SZ(z): return ox_top + 110 + (z - (-80)) * s
    def SY(y): return side_y0 - (y - ground_y) * s
    out.append(f'<text x="20" y="{side_y0-235}" class="txt">SIDE VIEW (from the right, Z to the right, Y up). Floor = Y {ground_y:.1f}.</text>')
    out.append(f'<line x1="{SZ(-80)}" y1="{SY(ground_y)}" x2="{SZ(700)}" y2="{SY(ground_y)}" stroke="#1b1f24" stroke-width="2"/>')
    out.append(f'<rect class="frame" x="{SZ(FRAME_Z[0])}" y="{SY(FRAME_TOP_Y)}" width="{(FRAME_Z[1]-FRAME_Z[0])*s}" height="{(FRAME_TOP_Y-FRAME_BOTTOM_Y)*s}"/>')
    out.append(f'<circle class="drive" cx="{SZ(DRIVE_Z)}" cy="{SY(axle_y)}" r="{DRIVE_D_NOMINAL/2*s}" fill-opacity=".85"/>')
    out.append(f'<circle cx="{SZ(DRIVE_Z)}" cy="{SY(axle_y)}" r="4" fill="#fff"/>')
    for z in CROSS_MEMBER_Z:
        out.append(f'<rect class="caster" x="{SZ(z)-12}" y="{SY(FRAME_BOTTOM_Y)}" width="24" height="{(CASTER_HEIGHT_DESIGN-CASTER_WHEEL_D)*s}"/>')
        out.append(f'<circle class="caster" cx="{SZ(z)}" cy="{SY(ground_y+CASTER_WHEEL_D/2)}" r="{CASTER_WHEEL_D/2*s}"/>')
    def sdim(y1, y2, zline, label, left=False):
        out.append(f'<line class="dim" x1="{SZ(zline)}" y1="{SY(y1)}" x2="{SZ(zline)}" y2="{SY(y2)}"/>')
        for yy in (y1, y2):
            out.append(f'<line class="dim" x1="{SZ(zline)-6}" y1="{SY(yy)}" x2="{SZ(zline)+6}" y2="{SY(yy)}"/>')
        anchor = 'end' if left else 'start'
        tx = SZ(zline) - 8 if left else SZ(zline) + 8
        out.append(f'<text class="dimtxt" text-anchor="{anchor}" x="{tx}" y="{(SY(y1)+SY(y2))/2+4}">{label}</text>')
    sdim(ground_y, FRAME_BOTTOM_Y, -40, f"{CASTER_HEIGHT_DESIGN:.0f} = caster height = clearance", left=True)
    sdim(ground_y, axle_y, DRIVE_Z + 95, f"axle {drive_r_loaded:.1f}")
    sdim(ground_y, FRAME_TOP_Y, 650, f"{FRAME_TOP_Y-ground_y:.0f} floor to frame top")
    out.append(f'<text x="{SZ(-80)}" y="{SY(ground_y)+28}" class="txt">Drive axle Y = {axle_y:.1f} (ground {ground_y:.1f} + loaded radius {drive_r_loaded:.1f}); caster plates on the cross-member bottom face Y = {FRAME_BOTTOM_Y:.0f}.</text>')
    out.append(f'<text x="{SZ(-80)}" y="{SY(ground_y)+48}" class="txt">Drive wheels are spring-loaded (preload {DRIVE_PRELOAD_N:.0f} N each, travel +/-{FLOOR_TOLERANCE:.0f} mm); casters are rigid and define the floor plane.</text>')
    out.append('</svg>')
    return "\n".join(out)


with open(os.path.join(OUT, "wheel_layout_drawing.svg"), "w", encoding="utf-8", newline="\n") as f:
    f.write(svg())

if __name__ == "__main__":
    print(json.dumps({k: v for k, v in R.items() if k not in ('support_polygon',)}, indent=1, default=lambda o: list(o)))
