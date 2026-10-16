#include "NRL.h"

// Calibration step: 90 degrees is a trial command, not a measured open pose.
// Keep the normal 0..180 pulse mapping; changing minAngle/maxAngle would
// rescale that mapping rather than simply limit this test's travel.
class Gripper90Test : public NRLOpMode {
    HexaServo gripper{{ .signalPin = SERVO_1, .startAngle = 90.0f }};
    bool begun = false;
    bool holding = false;
    bool failed = false;
    uint32_t selectCount = 0;
    uint32_t lastReport = 0;
    const char* lastAction = "NONE";

public:
    void init() override {
        HexaDCMotor::stopAll();
        // Defer begin(): it immediately commands startAngle. INIT and START
        // must leave the gripper uncommanded until a fresh X press.
    }

    void loop() override {
        const bool selectEdge = gamepad1.justPressed(BTN_X);
        if (selectEdge) ++selectCount;
        // A takes priority if both buttons are pressed. This releases servo 1;
        // it deliberately does not guess an uncalibrated closed position.
        if (gamepad1.pressed(BTN_A)) {
            lastAction = "HOME: RELEASE";
            if (holding) gripper.detach();
            holding = false;
        } else if (selectEdge) {
            lastAction = "SELECT: 90";
            if (!begun) {
                begun = gripper.begin();
                failed = !begun;
            } else if (!holding) {
                gripper.attach();
            }
            if (begun) {
                gripper.setPosition(90.0f);
                holding = true;
            }
        }

        const char* state = failed ? "INIT FAILED" :
                          (holding ? "HOLDING 90" : "RELEASED");
        telemetry.addData("version", "GRIPPER CHECK 2");
        telemetry.addData("gripper", failed ? "INIT FAILED" :
                          (holding ? "HOLDING 90" : "RELEASED"));
        telemetry.addData("SELECT", gamepad1.pressed(BTN_X) ? "DOWN" : "UP");
        telemetry.addData("HOME", gamepad1.pressed(BTN_A) ? "DOWN" : "UP");
        telemetry.addData("last action", lastAction);
        telemetry.addData("X presses", static_cast<float>(selectCount));

        // Slow diagnostics show loop activity and raw received inputs without
        // changing which controls can move the gripper. Raw input is never used
        // to bypass the framework's held-button or stale-input protection.
        const uint32_t now = millis();
        if (now - lastReport >= 500) {
            lastReport = now;
            float lx, ly, rx, ry;
            uint16_t buttons;
            uint32_t packets;
            NRLGamepad::read(lx, ly, rx, ry, buttons, packets);
            char raw[12];
            snprintf(raw, sizeof(raw), "0x%04X", static_cast<unsigned>(buttons));
            telemetry.addData("raw buttons", raw);
            telemetry.addData("packets", static_cast<float>(packets));
            telemetry.addData("uptime sec", static_cast<float>(now / 1000));
            telemetry.addData("link", NRLComms::isInputStale() ? "STALE" : "LIVE");
            telemetry.addData("battery V", power.getBatteryVoltage());
            if (Serial) {
                Serial.printf("[GripperCheck2] state=%s last=%s X=%u A=%u presses=%lu raw=%s packets=%lu stale=%u battery=%.2f\n",
                    state, lastAction, static_cast<unsigned>(gamepad1.pressed(BTN_X)),
                    static_cast<unsigned>(gamepad1.pressed(BTN_A)),
                    static_cast<unsigned long>(selectCount), raw,
                    static_cast<unsigned long>(packets),
                    static_cast<unsigned>(NRLComms::isInputStale()), power.getBatteryVoltage());
            }
        }
    }

    void stop() override {
        if (begun) gripper.detach();
        holding = false;
        HexaDCMotor::stopAll();
    }
};

REGISTER_OPMODE(Gripper90Test, "Gripper Check 2", TELEOP);
