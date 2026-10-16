# Module 3 — Programming the Robot

Complete study notes for **Phase 3 of the NRL Programming Curriculum**, covering Modules **3.1–3.9**.

Source: [NRL learning portal](https://nrlportal.theinnovationstory.com/#/youth-dashboard), inspected 15 October 2026. All lessons share the dashboard URL. These notes consolidate the lesson explanations, methods, settings, examples, warnings, and cross-references. Code is transcribed with formatting normalized; observations about inconsistencies are explicitly labelled. Examples have not been compiled or tested on hardware.

## Contents

1. Motors
2. Driving with TankDrive
3. Servos
4. The Gamepad
5. The Motion Sensor (IMU) & Heading
6. Telemetry
7. The Status LED
8. The OLED Display
9. Power & Battery

## 3.1 — Motors

A DC motor drives the robot's wheels. `HexaDCMotor` controls one motor's direction and speed through the board's driver.

### Declaration and configuration

```cpp
static HexaDCMotor leftMotor{{
    .dirPin = MOTOR_L_DIR,
    .pwmPin = MOTOR_L_PWM
}};
```

The double braces contain the configuration. Every motor needs a direction pin and a speed/PWM pin, named using constants from `BoardPins.h`. Optional `.flipped = true` reverses its direction in software, useful when its physical mounting is reversed.

| Method | Meaning |
|---|---|
| `begin()` | Initialize once in `init()`. |
| `setSpeed(int speed)` | Command from `-255` (full reverse) to `+255` (full forward). Zero means coast. Out-of-range commands are clamped. |
| `getSpeed()` | Return the last commanded speed. |
| `stop()` | Equivalent to `setSpeed(0)`. |
| `setFlipped(bool)` | Change direction reversal immediately. |

The speed magnitude uses an 8-bit range: zero plus 255 nonzero levels in each direction. The sign selects direction; magnitude selects drive effort. A small automatic deadband around zero prevents noise-induced stuttering.

### MotorRamp example

```cpp
#include "NRL.h"

static HexaDCMotor leftMotor{{ .dirPin = MOTOR_L_DIR, .pwmPin = MOTOR_L_PWM }};
static HexaDCMotor rightMotor{{ .dirPin = MOTOR_R_DIR, .pwmPin = MOTOR_R_PWM, .flipped = true }};

class MotorRamp : public NRLOpMode {
    int _speed = 0;

public:
    void init() override {
        leftMotor.begin();
        rightMotor.begin();
    }

    void loop() override {
        if (_speed < 220) _speed += 5; // creep up 5 units each pass
        leftMotor.setSpeed(_speed);
        rightMotor.setSpeed(_speed);
        telemetry.addData("speed", (float)_speed);
    }

    void stop() override {
        leftMotor.setSpeed(0);
        rightMotor.setSpeed(0);
    }
};

REGISTER_OPMODE(MotorRamp, "Motor Ramp", TELEOP);
```

Gradual acceleration helps reduce current spikes and wheel slip associated with jumping from zero to full power.

**Source discrepancy:** The lesson says the example ramps up and back down. The actual code increments by five per loop to 220, holds there, and commands zero in `stop()`. There is no gradual ramp down. Ramp timing depends on loop frequency.

Common mistakes: omitting `begin()` prevents operation; omitting motor shutdown in `stop()` can leave the robot rolling after the match.

## 3.2 — Driving with TankDrive

`TankDrive` converts a forward command and a turn command into the speeds needed for the left and right motors.

### Declaration

Declare the motors first, then construct the drive from them:

```cpp
static HexaDCMotor leftMotor{{ .dirPin = MOTOR_L_DIR, .pwmPin = MOTOR_L_PWM, .flipped = true }};
static HexaDCMotor rightMotor{{ .dirPin = MOTOR_R_DIR, .pwmPin = MOTOR_R_PWM }};
static TankDrive drive(leftMotor, rightMotor);
```

| Method | Meaning |
|---|---|
| `drive(float forward, float turn)` | Both arguments range from `-1.0` to `+1.0`. Positive forward moves ahead; positive turn steers right. |
| `stop()` | Stop both motors; use in the OpMode's `stop()`. |
| `setScale(float)` | Overall speed limit from 0 to 1; useful for precision mode. |
| `setRampRate(float)` | Limit how quickly the output changes. Lower values give smoother changes and gentler battery loading. |

Call `leftMotor.begin()` and `rightMotor.begin()` in `init()`. `TankDrive` itself does not need `begin()`.

### Normal driving

Left joystick up/down controls forward motion; right joystick left/right controls turning:

```cpp
void loop() override {
    drive.drive(gamepad1.leftY(), gamepad1.rightX());
}
```

### Precision mode

Hold the left bumper to limit the drive scale to 35%:

```cpp
void loop() override {
    drive.setScale(gamepad1.pressed(BTN_LB) ? 0.35f : 1.0f);
    drive.drive(gamepad1.leftY(), gamepad1.rightX());
}
```

If the robot turns incorrectly or the wheels oppose one another, the lesson recommends reversing the appropriate motor using `.flipped = true`.

**Example difference:** This lesson flips the left motor, while 3.1 flips the right. Choose the configuration appropriate to the robot's actual mounting; the examples are not consistent on which side is flipped.

## 3.3 — Servos

A servo moves to a requested angle and holds it, making it useful for arms, grippers, and claws. `HexaServo` uses degrees from 0 to 180.

```cpp
static HexaServo arm{{ .signalPin = SERVO_1, .startAngle = 90.0f, .settleMs = 0 }};
```

| Configuration | Meaning |
|---|---|
| `.signalPin` | Select `SERVO_1` through `SERVO_4`. |
| `.startAngle` | Position applied by `begin()`; default 90° (centre). |
| `.settleMs` | Default zero means hold indefinitely. A positive value automatically releases after that many idle milliseconds. |
| `.offsetDeg` | Calibration adjustment for a misaligned servo horn. |
| `.minAngle`, `.maxAngle` | Software travel limits to protect the mechanism. |

| Method | Meaning |
|---|---|
| `begin()` | Initialize and move to `startAngle`; call in `init()`. |
| `setPosition(float deg)` | Command an absolute angle, 0–180°. |
| `moveBy(float deg)` | Move relative to the current angle. |
| `getPosition()` | Return the current angle, as described by the lesson. |
| `setRampRate(float degPerSec)` | Limit movement speed; call before the first `setPosition()`. |
| `detach()` | Release the servo so it goes limp. |
| `attach()` | Re-engage the servo. |

With `.settleMs = 0`, the signal remains active to hold the commanded angle. The lesson stresses a clean power supply and points to Module 5.2 for weak-battery buzzing at rest.

### Published ArmToggle example

```cpp
#include "NRL.h"

static HexaServo arm{{ .signalPin = SERVO_1, .startAngle = 90.0f, .settleMs = 0 }};

class ArmToggle : public NRLOpMode {
public:
    void init() override {
        arm.begin();
    }

    void loop() override {
        arm.setPosition(90);
        telemetry.addData("arm", arm.getPosition());
    }

    void stop() override {
        arm.detach(); // let the servo relax
    }
};

REGISTER_OPMODE(ArmToggle, "Arm Toggle", TELEOP);
```

**Source discrepancy:** The description promises a button-controlled toggle between two poses using edge detection. The code instead repeatedly commands 90°; it contains no button check or toggle. The actual toggle pattern appears in 3.4.

Watch-outs: requests above the normal range are clamped (the lesson gives 200° becoming 180°); omitting `begin()` in `init()` prevents motion.

## 3.4 — The Gamepad

`gamepad1` is supplied automatically. Do not declare it yourself. It is refreshed at the start of each `loop()`.

### Controller diagram labels

The illustration labels the Driver Station Screen, left and right joysticks, left and right toggles, LB and RB, SELECT (X), BACK (Y), HOME (A), four D-pad directions, controller status LED, charging indicator LED, RESET, and BOOT.

### Joysticks

Every axis returns a float between `-1.0` and `+1.0`.

| Method | Input |
|---|---|
| `gamepad1.leftY()` | Left stick up/down; up is positive, normally forward. |
| `gamepad1.leftX()` | Left stick left/right. |
| `gamepad1.rightX()` | Right stick left/right, normally turning. |
| `gamepad1.rightY()` | Right stick up/down. |

### Buttons and edge detection

| Method | When true | Typical use |
|---|---|---|
| `pressed(BTN_X)` | Every loop while held | Continuous action, such as a held speed mode. |
| `justPressed(BTN_X)` | Only the loop when the button goes down | Toggle or start a sequence once. |
| `justReleased(BTN_X)` | Only the loop when the button goes up | Act on release. |

| Constant | Control |
|---|---|
| `BTN_X` | X face button / SELECT |
| `BTN_A` | A face button / HOME |
| `BTN_Y` | Y face button / BACK; reserved for system STOP |
| `BTN_LB`, `BTN_RB` | Left and right bumpers |
| `BTN_LT`, `BTN_RT` | Left and right trigger toggles |
| `BTN_DPAD_UP` | D-pad up |
| `BTN_DPAD_DOWN` | D-pad down |
| `BTN_DPAD_LEFT` | D-pad left |
| `BTN_DPAD_RIGHT` | D-pad right |

**`BTN_Y` is reserved:** it always invokes system STOP and cannot be used for your own controls.

### One press, one toggle

Using `pressed()` for a toggle would toggle repeatedly while the button remains held. Use `justPressed()`:

```cpp
bool _open = false;

void loop() override {
    if (gamepad1.justPressed(BTN_RB)) {
        _open = !_open;
        gripper.setPosition(_open ? 0 : 40);
    }
}
```

This snippet assumes a `gripper` servo has already been declared and initialized.

### Optional button bindings

The lesson also provides:

```cpp
void init() override {
    gamepad1.onPress(BTN_A, []{ arm.setPosition(120); });
    gamepad1.onPress(BTN_B, []{ arm.setPosition(30); });
}
```

Use `justPressed()` in `loop()` for most controls to keep logic together. Bindings can simplify many independent one-shot controls. For multi-step sequences, the lesson points to Actions in Module 4.2.

**Source inconsistency:** `BTN_B` is used in this binding example but does not appear in this lesson's button table or labelled controller diagram. Verify its availability in your kit/SDK before relying on it. This is also a partial snippet, not a complete servo OpMode.

## 3.5 — The Motion Sensor (IMU) & Heading

The Inertial Measurement Unit senses acceleration and rotation. Heading describes the direction the robot points, in degrees, and supports precise autonomous turns (covered further in Module 4.3).

### Framework-managed heading

For ordinary autonomous turns, the framework already maintains heading:

```cpp
float hdg = NRLComms::getHeading();     // heading in degrees
NRLComms::zeroHeading();               // make the current direction zero
bool ready = NRLComms::isHeadingReady(); // calibration complete?
```

### Your own IMU object

For raw acceleration, rotation rate, or other motion data, declare a `HexaIMU`. The text also mentions temperature, but does not provide a temperature getter.

```cpp
static HexaIMU imu{ hexaImuConfig() };

// In init():
// imu.begin();

// In loop():
imu.tick(millis());
imu.read();
// float az = imu.getAccelZ();
// float gz = imu.getGyroZ();
```

| Method | Meaning |
|---|---|
| `begin()` | Start the IMU; safe in `init()`. |
| `tick(millis())` | Call every loop to advance non-blocking calibration and heading integration. |
| `read()` | Refresh the readings before using the raw-data getters. |
| `getAccelX()`, `getAccelY()`, `getAccelZ()` | Acceleration in m/s²; Z is approximately 9.81 when flat. |
| `getGyroX()`, `getGyroY()`, `getGyroZ()` | Rotation rate in radians per second. |
| `getHeading()` | Integrated heading in degrees. |
| `isHeadingReady()` | Whether calibration has completed. |
| `zeroHeading()` | Reset heading to zero while retaining calibration. |

### Calibration and drift

Keep the robot still for approximately half a second after START. The lesson describes calibration as spreading over roughly the first 50 loop passes when `imu.tick(millis())` is called regularly.

Do not block `init()` with `delay()` to calibrate: it runs in a time-sensitive part of the framework, and blocking can cause the OpMode to abort immediately after INIT.

IMU-only heading drifts because there is no compass correction. The lesson considers it adequate for brief match turns and recommends zeroing immediately before a turn.

## 3.6 — Telemetry

Every OpMode has a built-in `telemetry` object for sending live numbers and text to the Controller screen. The lesson presents it as the primary debugging tool.

```cpp
void loop() override {
    telemetry.addData("heading", NRLComms::getHeading());
    telemetry.addData("speed", drive.getScale());
    telemetry.addData("status", _open ? "OPEN" : "SHUT");
}
```

Each unique key becomes one line. Sending the same key again updates that line. In this example, the key named `speed` displays `drive.getScale()`—the scale setting, not measured robot speed.

| Limit or behaviour | Value |
|---|---|
| Maximum unique keys | 64 |
| Maximum key length | 11 characters |
| Maximum value length | 15 characters |
| Transmission | Automatic, once per loop pass |
| Cleanup | Automatic when the OpMode stops |

Use `telemetry.addData(...)`; no separate send call is required. It buffers, batches, and deduplicates updates. The lesson discourages using lower-level send functions because they can flood the wireless link.

To diagnose a problem, publish the suspected variable and observe it live on the Controller.

## 3.7 — The Status LED

The robot's onboard NeoPixel provides a ready-made `userLed` object for program-specific signals.

| Method | Behaviour |
|---|---|
| `userLed.setSolid(r, g, b)` | Steady colour; each channel is 0–255. |
| `userLed.setBlink(r, g, b, periodMs)` | On/off blinking; default period 500 ms. |
| `userLed.setPulse(r, g, b, periodMs)` | Smooth brightness pulsing; default period 1000 ms. |
| `userLed.setOff()` | Turn off. |

The part contains two LED pixels. `botLed` belongs to the framework and indicates pairing/run state; leave it to the framework. `userLed` belongs to your application and needs no declaration or `begin()`.

### Battery warning example

```cpp
void loop() override {
    if (power.isBatteryLow())
        userLed.setBlink(255, 0, 0, 250); // fast red blink
    else
        userLed.setSolid(0, 60, 0);       // dim green
}
```

## 3.8 — The OLED Display

An optional robot-mounted OLED can show text, lines, rectangles, and circles using `HexaOLED`. Telemetry is sufficient for most programs, while the OLED is useful for pit debugging.

Declare the display, initialize it, and check initialization success. Drawing changes a memory buffer; **nothing reaches the physical screen until `display()` is called**.

### Full OLED heading example

```cpp
#include "NRL.h"
#include <HexaOLED.h>

// Config helpers come from RobotConfig.h through NRL.h and select
// the correct board buses for the IMU and OLED.
static HexaIMU imu{ hexaImuConfig() };

class OledHello : public NRLOpMode {
    HexaOLED _oled{ hexaOledConfig() };
    bool _oledOk = false;

public:
    void init() override {
        _oledOk = _oled.begin();
        // telemetry.addData("oled ok", _oledOk ? 1.0f : 0.0f);
        imu.begin();
    }

    void loop() override {
        // Call every loop. Initial ticks estimate gyro bias while still;
        // later ticks integrate gyro-Z to maintain heading.
        imu.tick(millis());

        if (!_oledOk) return;

        _oled.clearDisplay();
        _oled.setTextSize(1);
        _oled.setTextColor(HexaOLED::WHITE);
        _oled.setCursor(0, 0);
        _oled.print("HEADING:");
        _oled.setCursor(0, 12);

        if (!imu.isHeadingReady()) {
            _oled.print("calib...");
        } else {
            telemetry.addData("heading", imu.getHeading());
            _oled.print(imu.getHeading(), 1); // one decimal place
        }

        _oled.display();
    }
};

REGISTER_OPMODE(OledHello, "OLED Hello", TELEOP);
```

`hexaImuConfig()` and `hexaOledConfig()` select the appropriate device buses without hard-coded pin numbers. Without `imu.tick(millis())`, the lesson says the heading remains zero.

| Drawing method | Purpose |
|---|---|
| `clearDisplay()` | Clear the buffer, normally at the beginning of each frame. |
| `setCursor(x, y)` | Set text position. |
| `setTextSize(n)` | Set text scale; the lesson lists 1 or 2. |
| `setTextColor(HexaOLED::WHITE)` | Select white text, as used in the example. |
| `print(text)`, `print(number)` | Write text or numbers at the cursor. |
| `drawLine`, `drawRect`, `fillRect` | Draw lines and outlined/filled rectangles. |
| `drawCircle`, `fillCircle` | Draw outlined/filled circles. |
| `display()` | Transfer the buffer to the screen. |

For a blank screen, first check initialization success and whether `display()` is called. Clear each frame before drawing, or new text can overlap old text.

## 3.9 — Power & Battery

| Reading | Meaning |
|---|---|
| `power.getBatteryVoltage()` | Battery pack voltage, in volts. |
| `power.isBatteryLow()` | True below the configured low-battery threshold. |
| `power.getMainCurrent()` | Total battery current, in amps. |
| `power.getMotorCurrent()` | Combined motor-rail current. |
| `power.getServoCurrent()` | Servo-rail current, derived as main current minus motor current. |
| `power.readChannelVoltage(ADC_EXT_1)` | Voltage on an external analog input for a custom sensor. |

### Battery telemetry and LED example

```cpp
void loop() override {
    float v = power.getBatteryVoltage();
    telemetry.addData("battery", v);
    telemetry.addData("motor A", power.getMotorCurrent());
    userLed.setSolid(v < 10.5f ? 255 : 0, v < 10.5f ? 0 : 60, 0);
}
```

This example shows red below 10.5 V and dim green otherwise. The module does not specify the configured threshold used internally by `isBatteryLow()`, so do not assume it is necessarily the same as this example's 10.5 V comparison.

The lesson says voltage is calibrated out of the box. Current accuracy depends on individual board sensor calibration. Until readings have been checked against a meter, use current primarily as a relative load indicator: rising current means the system is working harder.

## Cross-references and course navigation

- Before this phase: Module 2.5 — Flashing and Pairing.
- After this phase: Module 4.1 — Writing an Autonomous OpMode.
- Module 3.3 refers to Module 3.4 for edge detection and Module 5.2 for servo power troubleshooting.
- Module 3.4 refers to Module 4.2 for Actions and multi-step sequences.
- Module 3.5 refers to Module 4.3 for precise autonomous turns.
- Module 3.8 refers to Module 3.6 for telemetry.

All nine lesson pages were inspected. The controller illustration's labels are transcribed above. Cross-referenced lessons outside Phase 3 are not included. Lesson completion controls were not changed.
