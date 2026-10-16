#include "GalaxyMotion.h"

// Compile-time behavioral checks exercise the same functions used by TeleOp.
// No hardware is actuated and no extra OpMode is registered by this file.
namespace {
constexpr bool near(float a, float b) { return GalaxyMotion::absValue(a - b) < 0.002f; }
constexpr float travel(float start, float target, unsigned ticks, uint32_t tickMs) {
    for (unsigned i = 0; i < ticks; ++i)
        start = GalaxyMotion::approach(start, target, tickMs);
    return start;
}
static_assert(near(travel(15, 90, 50, 10), 60), "Half a second opens by 45 degrees");
static_assert(near(travel(90, 15, 50, 10), 45), "Half a second closes by 45 degrees");
static_assert(travel(15, 90, 83, 10) < 90 && near(travel(15, 90, 84, 10), 90),
              "75-degree gripper travel takes about 0.84 seconds");
static_assert(near(travel(90, GalaxySettings::ARM_UP, 50, 10), 45),
              "Arm up decreases angle to 45 in half a second");
static_assert(near(travel(90, GalaxySettings::ARM_DOWN, 50, 10), 135),
              "Arm down increases angle to 135 in half a second");
static_assert(GalaxyMotion::servoTarget(90, true, false,
              GalaxySettings::ARM_UP, GalaxySettings::ARM_DOWN, 10) < 90 &&
              GalaxyMotion::servoTarget(90, false, true,
              GalaxySettings::ARM_UP, GalaxySettings::ARM_DOWN, 10) > 90,
              "Up and down buttons use the corrected physical arm directions");
static_assert(near(travel(90, 45, 1000, 10), 45), "Holding cannot pass the endpoint");
static_assert(near(GalaxyMotion::approach(89.95f, 90, 10), 90), "Do not overshoot");
static_assert(near(GalaxyMotion::approach(20, 90, 3000), 29), "Long pause has no catch-up jump");
static_assert(GalaxyMotion::servoTarget(30, false, false, 90, 0, 100) == 30,
              "Released controls hold position");
static_assert(GalaxyMotion::servoTarget(30, true, true, 90, 0, 100) == 30,
              "Opposing controls hold position");
static_assert(GalaxyMotion::axis(0.05f) == 0 && GalaxyMotion::axis(-0.05f) == 0,
              "Joystick noise does not drive");
static_assert(GalaxyMotion::axis(1) == 1 && GalaxyMotion::axis(-2) == -1,
              "Preserve full travel and clamp out-of-range inputs");
static_assert(GalaxyMotion::steeringAxis(-0.5f) > 0 &&
              GalaxyMotion::steeringAxis(0.5f) < 0 &&
              GalaxyMotion::steeringAxis(0.05f) == 0,
              "Reverse steering on both sides while retaining neutral deadband");
constexpr auto diagonal = GalaxyMotion::normalized(1, 1);
static_assert(diagonal.forward + diagonal.turn == 1,
              "Combined full forward and turn respect the motor power cap");
static_assert(GalaxySettings::DRIVE_SCALE > 0 && GalaxySettings::DRIVE_SCALE <= 1,
              "Drive scale must be in range");
static_assert(GalaxySettings::PRECISION_SCALE > 0 &&
              GalaxySettings::PRECISION_SCALE <= GalaxySettings::DRIVE_SCALE,
              "Precision mode must be no faster than normal drive");
static_assert(GalaxySettings::STICK_DEADBAND >= 0 && GalaxySettings::STICK_DEADBAND < 1,
              "Deadband must leave joystick travel");
static_assert(GalaxySettings::GRIP_CLOSED >= 0 && GalaxySettings::GRIP_OPEN <= 180 &&
              GalaxySettings::GRIP_CLOSED <= GalaxySettings::GRIP_START &&
              GalaxySettings::GRIP_START <= GalaxySettings::GRIP_OPEN,
              "Gripper startup must be inside its trial limits");
static_assert(GalaxySettings::ARM_UP >= 0 && GalaxySettings::ARM_UP <= 180 &&
              GalaxySettings::ARM_DOWN >= 0 && GalaxySettings::ARM_DOWN <= 180 &&
              GalaxySettings::ARM_START >= 0 && GalaxySettings::ARM_START <= 180,
              "Arm angles must be supported servo commands");
}
