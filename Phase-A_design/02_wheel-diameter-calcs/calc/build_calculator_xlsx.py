"""Build wheel_layout_calculator.xlsx (live formulas) for Task 2.

Mirrors wheel_layout_calc.py so the team can change inputs in Excel without Python.
"""
import os
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wheel_layout_calculator.xlsx")
F = "Arial"
BLUE = Font(name=F, color="0000FF")
BLACK = Font(name=F)
GREEN = Font(name=F, color="008000")
BOLD = Font(name=F, bold=True)
TITLE = Font(name=F, bold=True, size=14)
HEAD = Font(name=F, bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="2F4F6F")
SEC_FILL = PatternFill("solid", fgColor="DCE3EA")
KEY_FILL = PatternFill("solid", fgColor="FFFF00")
RES_FILL = PatternFill("solid", fgColor="E8F4EC")
thin = Side(style="thin", color="B7BEC7")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
CAD = "Measured from Assem_Base.SLDASM (SolidWorks API, 2026-10-09)"

wb = Workbook()


def header(ws, row, cols):
    for i, h in enumerate(cols, start=1):
        c = ws.cell(row=row, column=i, value=h)
        c.font, c.fill, c.alignment, c.border = HEAD, HEAD_FILL, Alignment(vertical="center", wrap_text=True), BOX


def section(ws, row, text, ncols):
    ws.cell(row=row, column=1, value=text).font = BOLD
    for i in range(1, ncols + 1):
        ws.cell(row=row, column=i).fill = SEC_FILL


# ------------------------------------------------------------------ Inputs
wi = wb.active
wi.title = "Inputs"
wi["A1"] = "Task 2 · Wheel layout calculator · INPUTS"
wi["A1"].font = TITLE
wi["A2"] = ("Edit only the BLUE values (yellow = key decisions). Coordinates use the SolidWorks frame of Assem_Base: "
            "X = width, Y = up, Z = length, mm. All results update automatically.")
wi["A2"].font = Font(name=F, italic=True)
header(wi, 4, ["Parameter", "Value", "Unit", "Source / note"])
inputs = [
    ("Frame (from CAD)", None),
    ("frame_bottom_y", "Frame bottom face Y (caster mounting face, lower 400 mm cross members)", -140, "mm", CAD),
    ("frame_top_y", "Frame top face Y", 0, "mm", CAD),
    ("frame_x_min", "Frame X min (cross-member end)", -47.5, "mm", CAD),
    ("frame_x_max", "Frame X max (cross-member end)", 352.5, "mm", CAD),
    ("cross_z1", "Lower cross member 1, centre line Z", 20, "mm", CAD),
    ("cross_z2", "Lower cross member 2, centre line Z", 590, "mm", CAD),
    ("centre_x", "Robot centre X", 152.5, "mm", CAD + " (frame symmetry)"),
    ("centre_z", "Robot centre Z", 305, "mm", CAD + " (frame symmetry)"),
    ("rail_outer_x", "Right side rail outer face X (left face mirrors about centre X)", 305, "mm", CAD),
    ("old_ground_y", "Old ground level Y (mecanum D133)", -161.8, "mm", CAD + " (lowest roller point)"),
    ("table_top_y", "Lift table top Y (lowered)", 3.35, "mm", CAD),
    ("lidar_top_y", "LiDAR top Y", 42.6, "mm", CAD),
    ("lidar_z_min", "Furthest part along -Z (LiDAR housing)", -49.53, "mm", CAD),
    ("lidar_z_max", "Furthest part along +Z (LiDAR housing)", 664.53, "mm", CAD),
    ("Drive wheels (hoverboard hub motor)", None),
    ("drive_d", "Drive wheel diameter", 165, "mm", "6.5 in hub motor = 165.1 mm nominal. MEASURE the purchased wheel and update."),
    ("tyre_w", "Tyre width", 55, "mm", "Typical 6.5 in hub; measure."),
    ("tyre_defl", "Tyre deflection under load", 1, "mm", "Solid rubber tyre, estimate."),
    ("track", "Track width (wheel centre to wheel centre)", 480, "mm", "Design choice: tyres outside the side rails, ~37 mm clear of the side panels."),
    ("drive_z", "Drive axle Z", "=B13", "mm", "At mid-length so the robot turns about its own centre."),
    ("Casters", None),
    ("caster_d", "Caster wheel diameter", 50, "mm", "2 in swivel caster."),
    ("caster_h", "Installed caster height (cross-member face to floor)", 75, "mm", "Design value: every 2 in caster (64-73 mm) fits with a spacer plate."),
    ("caster_lead", "Caster swivel lead (axis to wheel axle)", 35, "mm", "Typical 2 in caster; check datasheet."),
    ("caster_inset", "Caster axis inset from cross-member ends", 30, "mm", "Leaves room for a 60 x 60 mm adapter plate."),
    ("caster_sel_h", "Selected caster: total height (datasheet)", 73, "mm", "Example: Richelieu 50 mm twin nylon w/ brake (73 mm, 60 kg)."),
    ("caster_sel_kg", "Selected caster: load rating per caster", 60, "kg", "From the same datasheet."),
    ("Masses and motion", None),
    ("m_empty", "Robot mass, empty", "='Mass budget'!C14", "kg", "Linked to the Mass budget sheet."),
    ("m_payload", "Design payload", 100, "kg", "GP1 sizing basis (Graduation 1 report)."),
    ("h_cg_empty", "CG height above floor, empty", 0.15, "m", "Estimate."),
    ("h_cg_loaded", "CG height above floor, loaded and lift raised", 0.5, "m", "Conservative estimate (rack on top)."),
    ("cg_offset", "Possible payload CG offset from centre", 0.05, "m", "Rack not perfectly centred."),
    ("accel", "Target acceleration, loaded", 0.5, "m/s2", "Typical warehouse AMR."),
    ("slope", "Floor slope / ramp", 2, "deg", "Check case."),
    ("crr", "Rolling resistance coefficient", 0.015, "-", "Hard tyres on concrete/epoxy."),
    ("mu_nom", "Tyre-floor friction, nominal", 0.5, "-", "Solid rubber on smooth floor."),
    ("mu_worst", "Tyre-floor friction, worst", 0.4, "-", "Dusty / polished floor."),
    ("g", "Gravity", 9.81, "m/s2", "Constant."),
    ("Suspension (drive wheels)", None),
    ("preload", "Spring force pressing EACH drive wheel on the floor", 100, "N", "Key design value: must stay below ~70% of the empty weight / 2."),
    ("floor_tol", "Vertical variation to absorb (floor + build), +/-", 5, "mm", "Assumption."),
    ("force_var", "Allowed +/- change of wheel force over that travel", 0.25, "-", "25%."),
    ("lever_i", "Suspension lever ratio i = spring travel / wheel travel", 1, "-", "1 for a vertical slide; arm length ratio for a swing arm."),
]
names = {}
r = 5
for item in inputs:
    if item[1] is None:
        section(wi, r, item[0], 4)
    else:
        key, label, val, unit, note = item
        wi.cell(row=r, column=1, value=label).font = BLACK
        c = wi.cell(row=r, column=2, value=val)
        c.font = GREEN if isinstance(val, str) and "!" in val else (BLACK if isinstance(val, str) else BLUE)
        wi.cell(row=r, column=3, value=unit).font = BLACK
        wi.cell(row=r, column=4, value=note).font = Font(name=F, size=9, color="555555")
        for col in range(1, 5):
            wi.cell(row=r, column=col).border = BOX
        names[key] = f"Inputs!$B${r}"
    r += 1
for key in ("drive_d", "track", "caster_h", "m_payload", "preload"):
    wi[names[key].split("!")[1].replace("$", "")].fill = KEY_FILL
wi.column_dimensions["A"].width = 62
wi.column_dimensions["B"].width = 12
wi.column_dimensions["C"].width = 8
wi.column_dimensions["D"].width = 90
wi.freeze_panes = "A5"


def N(k):
    return names[k]


# ------------------------------------------------------------------ Mass budget
wm = wb.create_sheet("Mass budget")
wm["A1"] = "Mass budget (empty robot)"
wm["A1"].font = TITLE
header(wm, 3, ["Item", "Qty", "Mass total (kg)", "Unit mass (kg)", "Source / note"])
mass = [
    ("Frame, lift and sensors (current CAD total)", 1, 8.75, "SolidWorks mass of Assem_Base INCLUDING the old mecanum wheels and brackets (to be removed) -> conservative. Check every part has a material assigned."),
    ("Hoverboard hub motor 6.5 in with tyre", 2, 3.1, "Parallax 6.5 in hub motor listing: 3.1 kg each."),
    ("Swivel caster 2 in + adapter plate", 4, 0.35, "Estimate."),
    ("Drive suspension module (bracket, arm, spring)", 2, 1.0, "Estimate."),
    ("Battery 36 V ~10 Ah Li-ion", 1, 3.0, "Estimate."),
    ("Electronics (controllers, drivers, ESP32/PC, wiring)", 1, 2.5, "Estimate."),
    ("Aluminium sheet cover (1.5 mm)", 1, 2.6, "~0.65 m2 x 1.5 mm x 2700 kg/m3."),
    ("Fasteners, brackets, misc.", 1, 1.0, "Estimate."),
]
for i, (item, q, m, note) in enumerate(mass, start=4):
    wm.cell(row=i, column=1, value=item).font = BLACK
    wm.cell(row=i, column=2, value=q).font = BLUE
    wm.cell(row=i, column=4, value=m).font = BLUE
    wm.cell(row=i, column=3, value=f"=B{i}*D{i}").font = BLACK
    wm.cell(row=i, column=5, value=note).font = Font(name=F, size=9, color="555555")
    for col in range(1, 6):
        wm.cell(row=i, column=col).border = BOX
wm["A12"] = "Subtotal"
wm["C12"] = "=SUM(C4:C11)"
wm["A13"] = "Design margin (10%)"
wm["C13"] = "=0.1*C12"
wm["A14"] = "Empty robot mass used in calculations"
wm["C14"] = "=C12+C13"
for rr in (12, 13, 14):
    wm[f"A{rr}"].font = BOLD
    wm[f"C{rr}"].font = BOLD
    wm[f"C{rr}"].number_format = "0.0"
wm["C14"].fill = RES_FILL
for rr in range(4, 12):
    wm[f"C{rr}"].number_format = "0.00"
wm.column_dimensions["A"].width = 60
wm.column_dimensions["B"].width = 6
wm.column_dimensions["C"].width = 16
wm.column_dimensions["D"].width = 15
wm.column_dimensions["E"].width = 70

# ------------------------------------------------------------------ Results
wr = wb.create_sheet("Results")
wr["A1"] = "Task 2 · RESULTS (formulas, do not edit)"
wr["A1"].font = TITLE
header(wr, 3, ["Result", "Value", "Unit", "How it is calculated / check"])
res = {}
rr = 4


def put(key, label, formula, unit, note, fmt="0.0"):
    global rr
    wr.cell(row=rr, column=1, value=label).font = BLACK
    c = wr.cell(row=rr, column=2, value=formula)
    c.font, c.number_format, c.fill = BLACK, fmt, RES_FILL
    wr.cell(row=rr, column=3, value=unit).font = BLACK
    wr.cell(row=rr, column=4, value=note).font = Font(name=F, size=9, color="555555")
    for col in range(1, 5):
        wr.cell(row=rr, column=col).border = BOX
    res[key] = f"$B${rr}"
    rr += 1


def sec(text):
    global rr
    section(wr, rr, text, 4)
    rr += 1


sec("1. Vertical alignment: the casters define the floor plane")
put("ground", "Floor level Y", f"={N('frame_bottom_y')}-{N('caster_h')}", "mm", "Frame bottom face - installed caster height")
put("r_loaded", "Drive wheel loaded radius", f"={N('drive_d')}/2-{N('tyre_defl')}", "mm", "D/2 - tyre deflection")
put("axle_y", "Drive axle Y (suspension at mid-travel)", f"={res['ground']}+{res['r_loaded']}", "mm", "Floor + loaded radius: put the axle here in CAD")
put("wheel_top", "Drive wheel top Y", f"={res['ground']}+{N('drive_d')}", "mm", "For the cover wheel wells")
put("clearance", "Ground clearance under the frame", f"={N('frame_bottom_y')}-{res['ground']}", "mm", "Equal to the installed caster height")
put("dh", "Robot gets higher than the old robot by", f"={N('old_ground_y')}-{res['ground']}", "mm", "Check rack/shelf clearance in the warehouse")
put("table", "Lift table top above floor (lowered)", f"={N('table_top_y')}-{res['ground']}", "mm", "")
put("lidar", "LiDAR top above floor", f"={N('lidar_top_y')}-{res['ground']}", "mm", "")
put("spacer", "Spacer plate for the selected caster", f"={N('caster_h')}-{N('caster_sel_h')}", "mm", "Caster plate + spacer must equal the installed height")
put("spacer_ok", "Selected caster fits?", f'=IF({res["spacer"]}<0,"NO: caster too tall, raise the installed height","OK")', "", "", "@")

sec("2. Plan positions (X = width, Z = length)")
put("dl_x", "Left drive wheel centre X", f"={N('centre_x')}-{N('track')}/2", "mm", "")
put("dr_x", "Right drive wheel centre X", f"={N('centre_x')}+{N('track')}/2", "mm", "")
put("d_z", "Drive wheels Z", f"={N('drive_z')}", "mm", "")
put("cl_x", "Left casters X (swivel axis)", f"={N('frame_x_min')}+{N('caster_inset')}", "mm", "")
put("cr_x", "Right casters X (swivel axis)", f"={N('frame_x_max')}-{N('caster_inset')}", "mm", "")
put("c_track", "Caster track (X spacing)", f"={res['cr_x']}-{res['cl_x']}", "mm", "")
put("c_base", "Caster wheelbase (Z spacing)", f"={N('cross_z2')}-{N('cross_z1')}", "mm", "")
put("width", "Overall width over the tyres", f"={N('track')}+{N('tyre_w')}", "mm", "Old robot (mecanum): 650 mm")
put("gap", "Gap: inner tyre face to side-rail outer face", f"={res['dr_x']}-{N('tyre_w')}/2-{N('rail_outer_x')}", "mm", "Room for the axle clamp + suspension")
put("swivel_r", "Caster swivel envelope radius", f"={N('caster_lead')}+{N('caster_d')}/2", "mm", "Keep this circle free (cover skirt, brackets)")
put("rot_r", "In-place rotation radius (incl. LiDAR housings)", f"=SQRT(MAX({N('centre_x')}-{N('frame_x_min')},{N('frame_x_max')}-{N('centre_x')})^2+MAX({N('centre_z')}-{N('lidar_z_min')},{N('lidar_z_max')}-{N('centre_z')})^2)", "mm", "Robot turns about its centre")

sec("3. Stability (worst case: casters swivelled inward by the lead)")
put("p1x", "Edge point A x: left caster inner contact", f"={res['cl_x']}+{N('caster_lead')}", "mm", "")
put("p1z", "Edge point A z", f"={N('cross_z1')}+{N('caster_lead')}", "mm", "")
put("p2x", "Edge point B x: left drive wheel contact", f"={res['dl_x']}", "mm", "")
put("p2z", "Edge point B z", f"={N('drive_z')}", "mm", "")
put("m_side", "Margin to the side edge (caster to drive wheel)",
    f"=ABS(({res['p2z']}-{res['p1z']})*{N('centre_x')}-({res['p2x']}-{res['p1x']})*{N('centre_z')}+{res['p2x']}*{res['p1z']}-{res['p2z']}*{res['p1x']})/SQRT(({res['p2z']}-{res['p1z']})^2+({res['p2x']}-{res['p1x']})^2)/1000",
    "m", "Distance from the centre to that support-polygon edge", "0.000")
put("m_long", "Margin to the end edge (between two casters)", f"=MIN({N('centre_z')}-({N('cross_z1')}+{N('caster_lead')}),({N('cross_z2')}-{N('caster_lead')})-{N('centre_z')})/1000", "m", "", "0.000")
put("m_min", "Smallest stability margin", f"=MIN({res['m_side']},{res['m_long']})", "m", "", "0.000")
put("tip_loaded", "Tip-over acceleration limit, loaded", f"={N('g')}*({res['m_min']}-{N('cg_offset')})/{N('h_cg_loaded')}", "m/s2", "Must be well above the acceleration you use", "0.00")
put("tip_empty", "Tip-over acceleration limit, empty", f"={N('g')}*{res['m_min']}/{N('h_cg_empty')}", "m/s2", "", "0.00")

sec("4. Drive force, torque and traction")
put("m_loaded", "Loaded mass", f"={N('m_empty')}+{N('m_payload')}", "kg", "")
put("r_m", "Loaded radius", f"={res['r_loaded']}/1000", "m", "", "0.0000")
put("f_flat", "Total drive force, loaded, flat, at target acceleration", f"={res['m_loaded']}*({N('g')}*{N('crr')}+{N('accel')})", "N", "m (g Crr + a)")
put("f_slope", "Total drive force, loaded, on the slope, at target acceleration", f"={res['m_loaded']}*({N('g')}*{N('crr')}*COS(RADIANS({N('slope')}))+{N('g')}*SIN(RADIANS({N('slope')}))+{N('accel')})", "N", "m (g Crr cos + g sin + a)")
put("t_flat", "Torque per wheel, flat case", f"={res['f_flat']}/2*{res['r_m']}", "N·m", "Compare with the hub motor's continuous torque", "0.00")
put("t_slope", "Torque per wheel, slope case", f"={res['f_slope']}/2*{res['r_m']}", "N·m", "", "0.00")
put("rpm1", "Wheel speed at 1 m/s", f"=60/(PI()*{N('drive_d')}/1000)", "rpm", "Hub motors run ~600 rpm no-load at 36 V")
put("n_flat_w", "Normal force needed per drive wheel, flat (mu worst)", f"={res['f_flat']}/2/{N('mu_worst')}", "N", "Spring preload should reach this")
put("n_slope_w", "Normal force needed per drive wheel, slope (mu worst)", f"={res['f_slope']}/2/{N('mu_worst')}", "N", "")

sec("5. Suspension preload and caster loads")
put("pre_frac", "Drive preload as a fraction of the empty weight", f"=2*{N('preload')}/({N('m_empty')}*{N('g')})", "-", "Keep below ~0.7 so the casters stay loaded when empty", "0%")
put("c_empty", "Load per caster, empty", f"=({N('m_empty')}*{N('g')}-2*{N('preload')})/4", "N", "Must stay positive (> ~15 N)")
put("c_static", "Load per caster, loaded, static, centred", f"=({res['m_loaded']}*{N('g')}-2*{N('preload')})/4", "N", "")
put("c_worst", "Load per caster, loaded, worst (braking + CG offset)",
    f"={res['c_static']}+{res['m_loaded']}*{N('accel')}*{N('h_cg_loaded')}/({res['c_base']}/1000)/2+{res['m_loaded']}*{N('g')}*{N('cg_offset')}/({res['c_base']}/1000)/2", "N", "")
put("c_req", "Required caster rating (x1.5, 4 rigid casters on an uneven floor)", f"={res['c_worst']}*1.5/{N('g')}", "kg", "")
put("c_ok", "Selected caster rating OK?", f'=IF({N("caster_sel_kg")}>={res["c_req"]},"OK","NO: choose a stronger caster")', "", "", "@")
put("a_trac_nom", "Max acceleration before wheel slip, loaded, flat (mu nominal)", f"=(2*{N('mu_nom')}*{N('preload')}-{res['m_loaded']}*{N('g')}*{N('crr')})/{res['m_loaded']}", "m/s2", "Limit the motor controller below this", "0.00")
put("a_trac_worst", "Max acceleration before wheel slip, loaded, flat (mu worst)", f"=(2*{N('mu_worst')}*{N('preload')}-{res['m_loaded']}*{N('g')}*{N('crr')})/{res['m_loaded']}", "m/s2", "", "0.00")
put("a_trac_slope", "Max acceleration before wheel slip, loaded, on the slope (mu worst)", f"=(2*{N('mu_worst')}*{N('preload')}-{res['m_loaded']}*{N('g')}*({N('crr')}*COS(RADIANS({N('slope')}))+SIN(RADIANS({N('slope')}))))/{res['m_loaded']}", "m/s2", "Negative = cannot start uphill loaded", "0.00")
put("k_wheel", "Max suspension rate at the wheel", f"={N('force_var')}*{N('preload')}/{N('floor_tol')}", "N/mm", "Softer is better: force stays near the preload")
put("comp", "Preload compression at the wheel", f"={N('preload')}/{res['k_wheel']}", "mm", "")
put("travel", "Suspension working travel at the wheel", f"=2*{N('floor_tol')}", "mm", "")
put("k_spring", "Spring rate at the spring (with lever ratio)", f"={res['k_wheel']}/{N('lever_i')}^2", "N/mm", "")
put("f_spring", "Spring force at preload (with lever ratio)", f"={N('preload')}/{N('lever_i')}", "N", "")
wr.column_dimensions["A"].width = 66
wr.column_dimensions["B"].width = 16
wr.column_dimensions["C"].width = 8
wr.column_dimensions["D"].width = 62
wr.freeze_panes = "A4"

# ------------------------------------------------------------------ Coordinates
wc = wb.create_sheet("Coordinates")
wc["A1"] = "Key coordinates for the CAD team (Assem_Base frame, mm)"
wc["A1"].font = TITLE
header(wc, 3, ["Item", "X", "Y", "Z", "Wheel D", "Note"])
R_ = lambda k: f"Results!{res[k]}"
coords = [
    ("Floor plane", "", f"={R_('ground')}", "", "", "All 6 contact points lie on this plane"),
    ("Drive axle, left", f"={R_('dl_x')}", f"={R_('axle_y')}", f"={R_('d_z')}", f"={N('drive_d')}", "Hub-motor axle centre, suspension at mid-travel"),
    ("Drive axle, right", f"={R_('dr_x')}", f"={R_('axle_y')}", f"={R_('d_z')}", f"={N('drive_d')}", "Hub-motor axle centre, suspension at mid-travel"),
    ("Caster 1 (left, end Z=0)", f"={R_('cl_x')}", f"={N('frame_bottom_y')}", f"={N('cross_z1')}", f"={N('caster_d')}", "Swivel axis on the cross-member bottom face"),
    ("Caster 2 (right, end Z=0)", f"={R_('cr_x')}", f"={N('frame_bottom_y')}", f"={N('cross_z1')}", f"={N('caster_d')}", "Swivel axis on the cross-member bottom face"),
    ("Caster 3 (left, end Z=610)", f"={R_('cl_x')}", f"={N('frame_bottom_y')}", f"={N('cross_z2')}", f"={N('caster_d')}", "Swivel axis on the cross-member bottom face"),
    ("Caster 4 (right, end Z=610)", f"={R_('cr_x')}", f"={N('frame_bottom_y')}", f"={N('cross_z2')}", f"={N('caster_d')}", "Swivel axis on the cross-member bottom face"),
    ("Robot centre (base_link)", f"={N('centre_x')}", f"={R_('ground')}", f"={N('centre_z')}", "", "Rotation centre for in-place turns; on the floor"),
]
for i, row in enumerate(coords, start=4):
    for j, v in enumerate(row, start=1):
        c = wc.cell(row=i, column=j, value=v)
        c.font = GREEN if isinstance(v, str) and "!" in v else BLACK
        c.border = BOX
        if 2 <= j <= 5:
            c.number_format = "0.0"
wc.column_dimensions["A"].width = 30
for col in "BCDE":
    wc.column_dimensions[col].width = 11
wc.column_dimensions["F"].width = 52

# ------------------------------------------------------------------ Caster options
wo = wb.create_sheet("Caster options")
wo["A1"] = "2 in (50 mm) swivel caster candidates"
wo["A1"].font = TITLE
header(wo, 3, ["Caster", "Total height (mm)", "Rating per caster (kg)", "Spacer needed (mm)", "Fits height?", "Strong enough?", "Source"])
opts = [
    ("Revvo 50 mm low-profile twin nylon", 64, 160, "https://uk.rs-online.com/web/p/castor-wheels/0750834"),
    ("Richelieu 50 mm twin nylon with brake", 73, 60, "https://www.homedepot.ca/product/richelieu-2-inch-50-mm-contemporary-twin-wheel-nylon-swivel-caster-with-brake-silver-and-black-60-kg/1001090267"),
    ("Richelieu 50 mm double-ring with brake", 65, 40, "https://www.homedepot.ca/product/richelieu-2-inch-50-mm-contemporary-double-ring-swivel-caster-with-brake-40-kg/1001694602"),
    ("Generic 50 mm PU plate caster", 70, 29.5, "https://vxb.com/products/2-inch-swivel-plate-casters-blue-50-pack"),
]
for i, (n, h, kg, src) in enumerate(opts, start=4):
    vals = [n, h, kg, f"={N('caster_h')}-B{i}", f'=IF(D{i}>=0,"OK","too tall")',
            f'=IF(C{i}>=Results!{res["c_req"]},"OK","too weak")', src]
    for j, v in enumerate(vals, start=1):
        c = wo.cell(row=i, column=j, value=v)
        c.font = BLUE if j in (2, 3) else (GREEN if isinstance(v, str) and "!" in v else BLACK)
        c.border = BOX
wo["A9"] = "Add local options in new rows (copy the formulas in D:F). Required rating comes from Results."
wo["A9"].font = Font(name=F, italic=True)
wo.column_dimensions["A"].width = 40
for col in "BCDEF":
    wo.column_dimensions[col].width = 16
wo.column_dimensions["G"].width = 60

for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if c.font is None or c.font.name != F:
                c.font = Font(name=F, bold=c.font.bold if c.font else False, color=c.font.color if c.font else None,
                              italic=c.font.italic if c.font else False, size=c.font.size if c.font else 11)

wb.save(OUT)
print("saved", OUT)
