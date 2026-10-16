# Gripper Slow: controls and saved versions

The latest complete robot program is version 007, Galaxy TeleOp, built with
faster servos, reduced drive response, and reversed arm/steering commands.
See ROBOT_GUIDE.md for the latest upload status. Version 005 and the supplied
controller firmware were previously uploaded and verified on 16 October 2026.
See ROBOT_GUIDE.md for its controls, calibration assumptions, and build status.
The older guide below describes the retained standalone Gripper Slow test,
version 003; select Galaxy TeleOp for the full robot controls.

## Earlier standalone test: version 003, 15 October 2026

Robot program: Gripper Slow. Working source:
RobotFirmware/opmodes/GripperControl.cpp.

The robot build passed and was uploaded to COM14 with flash verification.
The supplied controller firmware was uploaded to COM13 with flash verification.
The kit does not include editable controller source; gripper logic runs on the
robot using buttons transmitted by the supplied controller firmware.
Physical gripper movement and endpoints still need operator verification.

## Start and control

1. Power both devices and pair them on channel 6.
2. Select Gripper Slow, then INIT and START. Release the button used to start.
3. Hold SELECT to increase the servo command toward 90 degrees (trial open).
4. Hold HOME to decrease it toward 0 degrees (trial closed).
5. Release the button to hold the current commanded position.
6. To exit, flip the TOP-LEFT TOGGLE and follow the on-screen confirmation.
   Exiting detaches/releases the gripper servo.

SELECT is the uppermost of the three buttons left of the screen, nearest the
screen (X). HOME is the lowest and farthest left (A). BACK (Y) is between them.
Use the left toggle for exit, not BACK. The program displays an exit reminder.

## Motion behavior

- Only servo port 1 is commanded. Wheels and the lifting arm are not controlled
  by this gripper program.
- The first fresh SELECT or HOME press initializes the servo at 90 degrees.
  Its physical starting position is unknown, so this initial move may be fast.
  INIT and START do not initialize the servo.
- After initialization, the commanded angle changes at 10 degrees per second
  while one direction button is held. Full 0-to-90 travel takes about 9 seconds
  under normal loop timing. This is command timing, not measured shaft speed.
- Holding both buttons holds position. Stale wireless input does not advance
  the target. Delayed loops are capped to avoid large catch-up steps.
- 0 and 90 are trial endpoints, not verified mechanical limits. Release the
  button before the mechanism binds; use the exit toggle to release the servo.
- There is no automatic repeating open/close cycle: the loop continually checks
  the buttons and only changes the target while a direction is held.
- The framework limits a TELEOP run to approximately 2 minutes 30 seconds.

## Screen readings

The screen shows GRIPPER SLOW 3, SELECT/HOME button state, motion state, target
degrees, 10 degrees/second, battery voltage, link status, and the exit reminder.
Target degrees is a software command, not a physical position measurement.

If the mechanism does not move, check whether target degrees changes while HOME
is held after initialization, and report the displayed state and battery voltage.
SELECT alone cannot increase a target that is already at the 90-degree limit.

## Saved versions

- 001-gripper-90-test: first single-position test (SELECT commands 90; HOME releases).
- 002-gripper-check: button and link diagnostics, with the same first-test controls.
- 003-gripper-slow: held-button control at 10 degrees/second with an exit reminder.

Each version is preserved under saved-versions. Version 003 includes its robot
source, application/bootloader/partition binaries, build settings, this guide,
the supplied controller image/manifest/flasher, and file checksums. Robot
firmware.bin is an application image, not a full merged flash image; use the
project's PlatformIO upload workflow. The archived controller files are reference
copies: use ControllerFirmware/flash_controller.py with its existing prebuilt
folder to upload the controller while preserving its settings area.

Save subsequent changes in new numbered folders; do not overwrite past versions.
Keep historical source outside RobotFirmware/opmodes to avoid compiling it into
the current firmware.
