# SolidWorks Indexing System

This indexing system is used to identify and organize all SolidWorks assemblies, subassemblies, and parts of the AMR chassis and its subsystems.

## 1. Index Structure

| Code | Description |
|---|---|
| `00` | Main Assembly |
| `01` | Subassembly |
| `02` | Part |


## 2. Subsystem Index

| Letter | Subsystem | Description |
|---|---|---|
| `A` | AMR | Main robot assembly |
| `C` | Chassis | Structural frame and base plate |
| `D` | Drive System | Drive wheels, motors, and its components |
| `L` | Lifting Mechanism | Scissor-lift assembly and its components |
| `E` | Electronics | Electronics mounting and enclosure components |
| `S` | Sensors | LiDAR and other sensor mounting components |
| `F` | Fixtures | Bolts, nuts, T-nuts, brackets, joining plates |

## 3. Examples

| Index | Component Name | Type |
|---|---|---|
| `A-00` | AMR Assembly | Main Assembly |
| `C-01` | Chassis Assembly | Subassembly |
| `C-02` | First Base Plate | Part |
| `D-01` | 6.5 inch Hoverboard Wheel | Subassembly |
| `D-02` | Drive Wheel Mount | Part |
| `L-01` | Lifting Mechanism Assembly | Subassembly |
| `L-02` | Scissor Arm | Part |
| `E-01` | Electronics Assembly | Subassembly |
| `S-02` | LiDAR Mount | Part |

**Naming convention:** `[(Subsystem Letter)-(Component Type Code)] Component Name`