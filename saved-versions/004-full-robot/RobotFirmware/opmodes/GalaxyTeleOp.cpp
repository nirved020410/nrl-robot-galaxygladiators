#include "NRL.h"
#include "GalaxyMotion.h"
#include <cmath>

class GalaxyTeleOp : public NRLOpMode {
    HexaServo gripper{{ .signalPin = SERVO_1, .startAngle = GalaxySettings::GRIP_START }};
    HexaServo arm{{ .signalPin = SERVO_4, .startAngle = GalaxySettings::ARM_START }};
    HexaDCMotor left{{ .dirPin = MOTOR_L_DIR, .pwmPin = MOTOR_L_PWM,
                       .flipped = GalaxySettings::LEFT_REVERSED }};
    HexaDCMotor right{{ .dirPin = MOTOR_R_DIR, .pwmPin = MOTOR_R_PWM,
                        .flipped = GalaxySettings::RIGHT_REVERSED }};
    TankDrive drive{left, right};
    bool ready = false;
    bool requireNeutral = true;
    bool gripReady = false;
    bool armReady = false;
    float gripAngle = GalaxySettings::GRIP_START;
    float armAngle = GalaxySettings::ARM_START;
    uint32_t lastTick = 0;
    uint32_t lastReport = 0;
    const char* state = "NOT INITIALIZED";

    void releaseOutputs() {
        drive.stop();
        HexaDCMotor::stopAll();
        if (gripReady) gripper.detach();
        if (armReady) arm.detach();
    }

public:
    void init() override {
        // SDK requirement: initialize servos before motors to establish PWM
        // allocation in the supported order. INIT commands both start angles.
        // Physical positions are unknown, so these initial moves may be fast.
        HexaDCMotor::stopAll();
        gripReady = gripper.begin();
        armReady = arm.begin();
        const bool leftReady = left.begin();
        const bool rightReady = right.begin();
        ready = gripReady && armReady && leftReady && rightReady;
        drive.setScale(GalaxySettings::DRIVE_SCALE);
        drive.setRampRate(GalaxySettings::DRIVE_RAMP_PER_TICK);
        drive.stop();
        state = ready ? "INIT READY" : "HARDWARE ERROR";
        if (!ready) releaseOutputs();
        telemetry.addData("status", state);
        if (Serial) Serial.printf("[GalaxyTeleOp] INIT grip=%u arm=%u left=%u right=%u\n",
            gripReady, armReady, leftReady, rightReady);
    }

    void start() override {
        lastTick = millis();
        requireNeutral = true;
        state = ready ? "RELEASE INPUTS" : "HARDWARE ERROR";
        if (Serial) Serial.println("[GalaxyTeleOp] START");
    }

    void loop() override {
        const uint32_t now = millis();
        const uint32_t elapsedMs = now - lastTick;
        lastTick = now;
        const bool stale = NRLComms::isInputStale();
        const bool pause = gamepad1.pressed(BTN_RB);
        const bool open = gamepad1.pressed(BTN_X);
        const bool close = gamepad1.pressed(BTN_A);
        const bool up = gamepad1.pressed(BTN_DPAD_UP);
        const bool down = gamepad1.pressed(BTN_DPAD_DOWN);
        const bool precision = gamepad1.pressed(BTN_LB);
        const float rawForward = gamepad1.leftY();
        const float rawTurn = gamepad1.rightX();
        const bool validAxes = std::isfinite(rawForward) && std::isfinite(rawTurn);
        const float forward = validAxes ? GalaxyMotion::axis(rawForward) : 0.0f;
        const float turn = validAxes ? GalaxyMotion::axis(rawTurn) : 0.0f;

        if (!ready) {
            drive.stop();
            state = "HARDWARE ERROR";
        } else if (stale || !validAxes || pause) {
            drive.stop();
            requireNeutral = true;
            state = stale ? "LINK LOST" : (pause ? "PAUSED" : "BAD INPUT");
            // Freeze servo targets; do not drop the arm during a brief pause.
        } else if (requireNeutral) {
            drive.stop();
            state = "RELEASE INPUTS";
            if (forward == 0 && turn == 0 && !open && !close && !up && !down)
                requireNeutral = false;
        } else {
            drive.setScale(precision ? GalaxySettings::PRECISION_SCALE : GalaxySettings::DRIVE_SCALE);
            if (forward == 0 && turn == 0) {
                drive.stop();
            } else {
                const auto input = GalaxyMotion::normalized(forward, turn);
                drive.drive(input.forward, input.turn);
            }
            const float nextGrip = GalaxyMotion::servoTarget(gripAngle, open, close,
                GalaxySettings::GRIP_OPEN, GalaxySettings::GRIP_CLOSED, elapsedMs);
            const float nextArm = GalaxyMotion::servoTarget(armAngle, up, down,
                GalaxySettings::ARM_UP, GalaxySettings::ARM_DOWN, elapsedMs);
            if (nextGrip != gripAngle) { gripAngle = nextGrip; gripper.setPosition(gripAngle); }
            if (nextArm != armAngle) { armAngle = nextArm; arm.setPosition(armAngle); }
            state = precision ? "PRECISION" : "RUNNING";
        }

        if (now - lastReport >= 250) {
            lastReport = now;
            telemetry.addData("program", "GALAXY TELEOP 4");
            telemetry.addData("status", state);
            telemetry.addData("exit", "TOP LEFT TOGGLE");
            telemetry.addData("grip target", gripAngle);
            telemetry.addData("arm target", armAngle);
            telemetry.addData("battery V", power.getBatteryVoltage());
            telemetry.addData("drive cap", precision ? GalaxySettings::PRECISION_SCALE : GalaxySettings::DRIVE_SCALE);
            telemetry.addData("SELECT", open ? "OPEN" : "UP");
            telemetry.addData("HOME", close ? "CLOSE" : "UP");
            telemetry.addData("arm input", up == down ? "HOLD" : (up ? "UP" : "DOWN"));
            if (Serial) Serial.printf("[GalaxyTeleOp] %s f=%.2f t=%.2f grip=%.1f arm=%.1f X=%u A=%u up=%u down=%u\n",
                state, forward, turn, gripAngle, armAngle, open, close, up, down);
        }
    }

    void stop() override {
        releaseOutputs();
        ready = false;
        requireNeutral = true;
        if (Serial) Serial.println("[GalaxyTeleOp] STOP: motors off, servos released");
    }
};

REGISTER_OPMODE(GalaxyTeleOp, "Galaxy TeleOp", TELEOP);
