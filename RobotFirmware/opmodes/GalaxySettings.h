#pragma once

// All mechanical calibration choices are here. Verify these on the robot.
namespace GalaxySettings {
// The production SDK exposes two drive channels. This assumes the four
// sockets group the front/rear motors by side; physical mapping is unverified.
constexpr bool LEFT_REVERSED = false;
constexpr bool RIGHT_REVERSED = true;
constexpr float DRIVE_SCALE = 0.85f;
constexpr float PRECISION_SCALE = 0.40f;
constexpr float DRIVE_RAMP_PER_TICK = 0.04f;
constexpr float STICK_DEADBAND = 0.08f;

// Servo 1: trial positions, not measured mechanical limits.
constexpr float GRIP_CLOSED = 0.0f;
constexpr float GRIP_OPEN = 90.0f;
constexpr float GRIP_START = 90.0f;

// Servo 4: 45 degrees either side of a trial 90-degree neutral position.
// Swap UP and DOWN if the mechanical direction is reversed.
constexpr float ARM_DOWN = 45.0f;
constexpr float ARM_UP = 135.0f;
constexpr float ARM_START = 90.0f;
constexpr float SERVO_DEGREES_PER_SECOND = 20.0f;
}
