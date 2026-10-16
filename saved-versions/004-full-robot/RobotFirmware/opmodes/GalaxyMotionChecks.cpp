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
static_assert(near(travel(0, 90, 100, 10), 10), "One second opens by 10 degrees");
static_assert(near(travel(90, 0, 100, 10), 80), "One second closes by 10 degrees");
static_assert(near(travel(0, 90, 900, 10), 90), "Full gripper travel takes nine seconds");
static_assert(near(travel(90, 135, 450, 10), 135), "Arm rises 45 degrees in 4.5 seconds");
static_assert(near(travel(90, 45, 450, 10), 45), "Arm lowers 45 degrees in 4.5 seconds");
static_assert(near(travel(90, 45, 1000, 10), 45), "Holding cannot pass the endpoint");
static_assert(near(GalaxyMotion::approach(89.95f, 90, 10), 90), "Do not overshoot");
static_assert(near(GalaxyMotion::approach(20, 90, 3000), 21), "Long pause has no catch-up jump");
static_assert(GalaxyMotion::servoTarget(30, false, false, 90, 0, 100) == 30,
              "Released controls hold position");
static_assert(GalaxyMotion::servoTarget(30, true, true, 90, 0, 100) == 30,
              "Opposing controls hold position");
static_assert(GalaxyMotion::axis(0.05f) == 0 && GalaxyMotion::axis(-0.05f) == 0,
              "Joystick noise does not drive");
static_assert(GalaxyMotion::axis(1) == 1 && GalaxyMotion::axis(-2) == -1,
              "Preserve full travel and clamp out-of-range inputs");
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
