#pragma once
#include <stdint.h>
#include "GalaxySettings.h"

namespace GalaxyMotion {
constexpr float absValue(float value) { return value < 0 ? -value : value; }
constexpr float clamp(float value, float low, float high) {
    return value < low ? low : (value > high ? high : value);
}
constexpr float axis(float value) {
    value = clamp(value, -1.0f, 1.0f);
    const float magnitude = absValue(value);
    if (magnitude <= GalaxySettings::STICK_DEADBAND) return 0.0f;
    const float scaled = (magnitude - GalaxySettings::STICK_DEADBAND) /
                         (1.0f - GalaxySettings::STICK_DEADBAND);
    return value < 0 ? -scaled : scaled;
}

struct DriveInput { float forward; float turn; };
constexpr DriveInput normalized(float forward, float turn) {
    const float sum = absValue(forward) + absValue(turn);
    return sum > 1.0f ? DriveInput{forward / sum, turn / sum}
                     : DriveInput{forward, turn};
}

constexpr float approach(float current, float target, uint32_t elapsedMs) {
    const uint32_t boundedMs = elapsedMs > 100 ? 100 : elapsedMs;
    const float step = GalaxySettings::SERVO_DEGREES_PER_SECOND * boundedMs / 1000.0f;
    return current < target ? (current + step < target ? current + step : target)
                           : (current - step > target ? current - step : target);
}

constexpr float servoTarget(float current, bool positive, bool negative,
                            float positiveEnd, float negativeEnd, uint32_t elapsedMs) {
    // Opposing buttons cancel; releasing both holds the last command.
    if (positive == negative) return current;
    return approach(current, positive ? positiveEnd : negativeEnd, elapsedMs);
}
}
