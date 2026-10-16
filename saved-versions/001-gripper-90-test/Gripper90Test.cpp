#include "NRL.h"

// Calibration step: 90 degrees is a trial command, not a measured open pose.
// Keep the normal 0..180 pulse mapping; changing minAngle/maxAngle would
// rescale that mapping rather than simply limit this test's travel.
class Gripper90Test : public NRLOpMode {
    HexaServo gripper{{ .signalPin = SERVO_1, .startAngle = 90.0f }};
    bool begun = false;
    bool holding = false;
    bool failed = false;

public:
    void init() override {
        HexaDCMotor::stopAll();
        // Defer begin(): it immediately commands startAngle. INIT and START
        // must leave the gripper uncommanded until a fresh X press.
    }

    void loop() override {
        // A takes priority if both buttons are pressed. This releases servo 1;
        // it deliberately does not guess an uncalibrated closed position.
        if (gamepad1.pressed(BTN_A)) {
            if (holding) gripper.detach();
            holding = false;
        } else if (gamepad1.justPressed(BTN_X)) {
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

        telemetry.addData("gripper", failed ? "INIT FAILED" :
                          (holding ? "HOLDING 90" : "RELEASED"));
        telemetry.addData("controls", "X=90 A=release");
    }

    void stop() override {
        if (begun) gripper.detach();
        holding = false;
        HexaDCMotor::stopAll();
    }
};

REGISTER_OPMODE(Gripper90Test, "Gripper 90 Test", TELEOP);
