#include "NRL.h"
#include <algorithm>

namespace {
constexpr float OPEN_ANGLE = 90.0f;
constexpr float CLOSED_ANGLE = 0.0f;  // Trial endpoint; verify on the mechanism.
constexpr float SPEED_DEG_PER_SEC = 10.0f;
}

class GripperControl : public NRLOpMode {
    // Preserve the driver's standard 0..180 degree pulse mapping.
    HexaServo gripper{{ .signalPin = SERVO_1, .startAngle = OPEN_ANGLE }};
    float commandedAngle = OPEN_ANGLE;
    bool begun = false;
    bool failed = false;
    uint32_t lastTick = 0;
    uint32_t lastReport = 0;
    const char* state = "PRESS A BUTTON";

public:
    void init() override {
        HexaDCMotor::stopAll();
        // No servo movement on INIT or START. The first fresh button press
        // initializes to 90 degrees; its physical starting angle is unknown,
        // so that first positioning movement cannot be speed-guaranteed.
    }

    void start() override {
        lastTick = millis();
    }

    void loop() override {
        const uint32_t now = millis();
        // Cap delayed frames so a pause never produces a large catch-up step.
        const uint32_t elapsedMs = std::min<uint32_t>(now - lastTick, 100);
        lastTick = now;
        const bool open = gamepad1.pressed(BTN_X);
        const bool close = gamepad1.pressed(BTN_A);
        const bool stale = NRLComms::isInputStale();
        const bool exclusive = open != close;
        bool justInitialized = false;

        if (!begun && !stale && exclusive &&
            (gamepad1.justPressed(BTN_X) || gamepad1.justPressed(BTN_A))) {
            begun = gripper.begin();
            failed = !begun;
            justInitialized = begun;
            commandedAngle = OPEN_ANGLE;
        }

        if (failed) {
            state = "INIT FAILED";
        } else if (!begun) {
            state = "PRESS A BUTTON";
        } else if (stale) {
            state = "LINK LOST:HOLD";
        } else if (!exclusive || justInitialized) {
            state = "HOLDING";
        } else {
            const float step = SPEED_DEG_PER_SEC * (elapsedMs / 1000.0f);
            const float next = open
                ? std::min(OPEN_ANGLE, commandedAngle + step)
                : std::max(CLOSED_ANGLE, commandedAngle - step);
            if (next != commandedAngle) {
                commandedAngle = next;
                gripper.setPosition(commandedAngle);
            }
            state = open ? (commandedAngle >= OPEN_ANGLE ? "OPEN LIMIT" : "OPENING")
                         : (commandedAngle <= CLOSED_ANGLE ? "CLOSE LIMIT" : "CLOSING");
        }

        // Releasing both buttons (or holding both) keeps the last commanded
        // position. No servo commands come from raw input or stale packets.
        telemetry.addData("version", "GRIPPER SLOW 3");
        telemetry.addData("exit", "TOP LEFT TOGGLE");
        telemetry.addData("gripper", state);
        telemetry.addData("SELECT", open ? "OPEN: DOWN" : "UP");
        telemetry.addData("HOME", close ? "CLOSE: DOWN" : "UP");
        if (now - lastReport >= 250) {
            lastReport = now;
            telemetry.addData("target deg", commandedAngle);
            telemetry.addData("speed deg/s", SPEED_DEG_PER_SEC);
            telemetry.addData("battery V", power.getBatteryVoltage());
            telemetry.addData("link", stale ? "STALE" : "LIVE");
            if (Serial) {
                Serial.printf("[GripperSlow3] state=%s target=%.2f X=%u A=%u stale=%u\n",
                    state, commandedAngle, static_cast<unsigned>(open),
                    static_cast<unsigned>(close), static_cast<unsigned>(stale));
            }
        }
    }

    void stop() override {
        if (begun) gripper.detach();
        HexaDCMotor::stopAll();
    }
};

REGISTER_OPMODE(GripperControl, "Gripper Slow", TELEOP);
