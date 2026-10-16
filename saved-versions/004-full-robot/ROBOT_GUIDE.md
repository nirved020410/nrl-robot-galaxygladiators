# Galaxy TeleOp: complete robot controls

## Version 004 — prepared and built, not uploaded

Prepared on 15 October 2026 for team 185, Galaxy Gladiators, channel 6.
The robot program is called **Galaxy TeleOp**. It controls the drive system,
the gripper on servo 1, and the lifting arm on servo 4.

Build passed, including compile-time movement checks. The last verified robot
upload remains version 003, Gripper Slow. The earlier report that the program
would appear but not start has not yet been resolved on hardware. A diagnostic
capture showed program advertising but no program START message during that
capture; it does not establish the cause.

The controller already contains the supplied kit firmware. It sends joystick
and button data to this robot program. No editable controller source is supplied
with the kit and no new controller firmware is required for these controls.

## Controls

| Physical control | Action |
| --- | --- |
| Left joystick up/down | Forward/reverse |
| Right joystick left/right | Turn left/right |
| SELECT (X) — upper button left of screen | Hold to open the gripper toward 90 degrees |
| HOME (A) — lowest, farthest-left button | Hold to close the gripper toward 0 degrees |
| D-pad up | Hold to raise the arm toward 135 degrees |
| D-pad down | Hold to lower the arm toward 45 degrees |
| Release servo buttons | Hold the last commanded servo positions |
| Left bumper (LB) — top-left shoulder button | Hold for 20% precision driving; normal limit is 50% |
| Right bumper (RB) — top-right shoulder button | Pause: stop wheels and freeze servo targets |
| Top-left toggle | Open the framework's exit confirmation; follow the screen prompt |

The top-left toggle and left bumper are different controls. BACK (Y) is the
middle of the three left face buttons; it is not assigned as a program stop.

After START, a wireless interruption, or a pause, release SELECT/HOME/D-pad,
release RB, and center both driving axes. The display changes from
RELEASE INPUTS to RUNNING. This prevents driving from resuming with a held stick.

## Initialization and movement

**INIT commands both servos to 90 degrees.** These are trial starting poses;
their first physical movement may be fast because the software cannot measure
the servos' existing angles. Servos initialize before motors as required by the
SDK. The wheels remain stopped through INIT.

After START, both servo targets move at 10 degrees/second while a direction
button is held. Releasing the button holds the target. Holding both directions
for the same servo cancels movement. A full gripper command from 0 to 90 takes
about 9 seconds; arm neutral to either endpoint takes about 4.5 seconds.
The display reports commanded angles, not measured shaft position.

Drive input has a center deadband and acceleration smoothing. Combined forward
and turn inputs are normalized so they respect the selected drive-power cap.
Centering both driving axes stops the wheels immediately rather than ramping down.

Stale wireless input stops wheel commands and freezes servo targets in this
program. The SDK also applies its own disconnect handling. On confirmed exit,
the program stops motors and releases both servos. Support any load carried by
the arm before exiting, since releasing the servo removes holding torque.
The framework limits a TELEOP run to approximately 2 minutes 30 seconds.

## Wiring and settings that still need verification

The production SDK provides MOTOR_L and MOTOR_R. This program assumes the front
and rear wheels on each side share that side's channel. The photo shows four
motor plugs, but their electrical grouping and wheel mapping have not been verified.
The bench-only MOTOR_3/MOTOR_4 pins are not used as production motor outputs.

The default left motor direction is normal; right is reversed, matching one of
the kit examples. Verify direction with the wheels raised before driving on the
floor. If one side moves backward, change that side's REVERSED setting.

Gripper 0/90 and arm 45/90/135 are trial limits, not measured safe endpoints.
Release the relevant button before any linkage binds. If D-pad up lowers the
arm, swap ARM_UP and ARM_DOWN. Adjust the actual safe endpoints after testing.

All calibration values are in RobotFirmware/opmodes/GalaxySettings.h. The motion
checks deliberately verify the requested 10-degree/second behavior; if that
requirement changes, update those checks along with the settings.

## Files and saved versions

- RobotFirmware/opmodes/GalaxyTeleOp.cpp: complete program and stop handling.
- RobotFirmware/opmodes/GalaxySettings.h: motor reversal, speeds, servo endpoints.
- RobotFirmware/opmodes/GalaxyMotion.h: movement calculations used by the program.
- RobotFirmware/opmodes/GalaxyMotionChecks.cpp: compile-time behavioral checks.
- RobotFirmware/opmodes/GripperControl.cpp: retained standalone Gripper Slow program.
- saved-versions/004-full-robot: snapshot of all working OpModes and required
  project build files, compiled images, guide, and file hashes.

Earlier saved versions 001–003 remain intact. Keep future snapshots in new
numbered folders. The compiled robot firmware.bin is an application image, not
a merged full-flash image; use PlatformIO's robot upload workflow.

## First run after upload

1. Set the controller to channel 6 and pair it with the robot.
2. Select Galaxy TeleOp. Follow the controller's INIT and START prompts.
3. Expect both servos to move to their trial 90-degree positions at INIT.
4. Release the buttons and center the sticks until the status is RUNNING.
5. Check wheel directions at low input, then test each servo independently.
6. If the program will not start, capture the actual controller screen. Robot
   serial output now records INIT results, START, periodic RUNNING/PAUSED status,
   and STOP, which distinguishes program execution from menu navigation.

Compilation validates software interfaces and movement calculations. It does
not validate wiring, mechanical limits, power delivery, or physical operation.
