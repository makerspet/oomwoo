# oomwoo Modules

The project is split into modules that can be built in parallel. Each module gets
a folder and an `RFM.md` (see [docs/RFM-TEMPLATE.md](docs/RFM-TEMPLATE.md)).
Contributors submit attempts under `<module>/<github-username>/`; the maintainer
selects among compliant candidates. Modules are **swappable** — a non-selected
design is still a valid learning exercise and a fallback.

**Phase legend:** `MVP` = needed for the Aug 31 2026 bare-bones build ·
`P2` = next phase · `P3+` = later. **Safety** = requires maintainer safety review.

> ⚠️ Hardware modules cannot be finalized until the interface specs in
> `ARCHITECTURE.md` (§4, §5.2, §5.3) are frozen. Software/sim modules and SOTA
> research can start immediately.

## Hardware modules

| Module | ID | Phase | Notes |
|---|---|---|---|
| Chassis / base frame (reference) | `hw-chassis` | MVP | Integration backbone; defines mechanical interface. Maintainer-owned. |
| Left drive wheel assembly | `hw-wheel-left` | MVP | Motor + encoder + suspension/mount. |
| Right drive wheel assembly | `hw-wheel-right` | MVP | Mirror of left; share design. |
| Caster / universal wheel | `hw-caster` | MVP | Passive support wheel. |
| Motor driver + power distribution PCB | `hw-power-pcb` | MVP | **Safety.** Drives wheels + fan, distributes rails. |
| Battery pack + holder | `hw-battery` | MVP | **Safety.** Chemistry/voltage per ARCHITECTURE §5.3. |
| Compute mount (RPi 5) | `hw-compute-mount` | MVP | Mount + airflow for Pi 5. |
| LiDAR mount | `hw-lidar-mount` | MVP | Fits LD14P; parametric for other models. |
| Suction fan / impeller | `hw-suction` | MVP | Airflow path + impeller. |
| Main brush assembly | `hw-main-brush` | MVP | Roller brush + drive. |
| Dust bin + filter | `hw-dustbin` | MVP | Removable bin, filter interface. |
| Bumper (mechanical + switches) | `hw-bumper` | MVP | Contact detection. |
| Cliff sensors + mounts | `hw-cliff` | MVP | IR drop detection at edges/stairs. |
| Top cover / shell | `hw-shell` | MVP | Cosmetic + protective; LiDAR clearance. |
| Wiring harness | `hw-harness` | MVP | Connector pinouts per ARCHITECTURE §5.3. |
| Side brush | `hw-side-brush` | P2 | Edge cleaning. |
| Wheel-drop sensors | `hw-wheel-drop` | P2 | Lift detection. |
| Charging dock (basic) | `hw-dock` | P2 | **Safety.** Contacts + alignment. |

## Software modules

| Module | ID | Phase | Notes |
|---|---|---|---|
| URDF / robot description | `sw-urdf` | MVP | Drives sim + TF. Can start now. |
| Gazebo sim + residential worlds | `sw-sim` | MVP | Multiple home layouts. Can start now. |
| LiDAR driver integration | `sw-lidar` | MVP | Wrap `kaiaai/LDS` / `lds2d`. |
| Base controller (diff-drive) | `sw-base-controller` | MVP | Onboard vs micro-ROS: open question. |
| Odometry (encoders + IMU) | `sw-odometry` | MVP | Wheel odom, optional IMU fusion. |
| Teleop (manual drive) | `sw-teleop` | MVP | Keyboard/gamepad/web. |
| SLAM (manual mapping) | `sw-slam` | MVP | slam_toolbox or cartographer; manual for MVP. |
| Regression / CI tests | `sw-regression-tests` | MVP | Sim-based tests gating PRs. Can start now. |
| Diagnostics / telemetry | `sw-diagnostics` | MVP | Health, logs. |
| Autonomous exploration (sim first) | `sw-exploration` | P2 | Frontier exploration in sim. |
| Navigation (Nav2) | `sw-nav2` | P2 | Path planning + obstacle avoidance. |
| Coverage path planning | `sw-coverage` | P2 | Full-floor cleaning paths. |
| Sensor integration (bumper/cliff) | `sw-sensors` | P2 | Reactive behaviors. |
| Behavior / state management | `sw-behavior` | P2 | Mission/state machine. |
| Home Assistant integration | `sw-homeassistant` | P2 | MQTT/HA entity, map, control. |
| App runtime layer (Podman) | `sw-app-runtime` | P3+ | ROS2-agnostic app sandbox. North star. |
| Web UI / dashboard | `sw-webui` | P3+ | Local control + map view. |

## Non-engineering contributions (also wanted)

| Track | Phase | Notes |
|---|---|---|
| 3D-print validation | MVP | Confirm parts print cleanly on common FDM printers. |
| Real-home testing | MVP/P2 | Build and report on real floors. |
| Docs / build guides | MVP | Turn working modules into step-by-step instructions. |
| Posts / videos / demos | ongoing | Content that grows the project (highly valued). |
| SOTA research | ongoing | Best-in-class prior art per module (part of each RFM). |
