# Program selection failure - 16 October 2026

## Confirmed

- Robot COM14: USB serial identity 9C:13:9E:E4:DF:94.
- Controller COM13: USB serial identity 9C:13:9E:90:AF:EC.
- Firmware upload and flash hash verification previously passed on both boards.
- User reports all demos and Galaxy TeleOp remain on the program menu after SELECT.
- User reports BACK responds but SELECT does not open other screens either.
- During the simultaneous 45-second capture, the controller continuously logged
  BOT:ON PAIR:3. Robot logged an advertisement of six OpModes about every five seconds.
- No INIT, START, GalaxyTeleOp execution, reset, or link-loss messages appeared
  in this capture. User confirmed pressing SELECT while the recording ran.

Capture: both-start-20261016-082445.txt.

## What this does not establish

- The controller logs do not report raw SELECT button state.
- An online indication does not establish that the controller regards the robot
  as ready to accept a program selection, or that an INIT command was sent.
- Absence of execution messages does not prove whether the command was never
  transmitted, was rejected, or was otherwise not acted upon.
- A faulty SELECT switch is possible but not confirmed.

## Next evidence needed

Close-up of the entire controller screen, including the status banner above
the program names, and the robot's OLED status screen. The user could not read
the controller banner. Resolve readiness/error state before changing robot
movement code or assuming a physical button failure.

No firmware changes, start commands, or movement commands were made in this test.
