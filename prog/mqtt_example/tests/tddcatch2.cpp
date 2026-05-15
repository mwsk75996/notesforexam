#include <catch2/catch_test_macros.hpp>

#include <iomanip>
#include <sstream>
#include <string>

namespace {

std::string buildPayload(int id, double tempC, const std::string& timestamp) {
    std::ostringstream out;
    out << "ID " << id
        << " - Temp " << std::fixed << std::setprecision(1) << tempC << " C"
        << " - " << timestamp;
    return out.str();
}

bool isTemperatureValid(double tempC) {
    return tempC >= 10.0 && tempC <= 30.0;
}

} // namespace

TEST_CASE("Publisher payload gets expected structure", "[publisher]") {
    const auto msg = buildPayload(42, 23.4, "27-02-2026 12:00:00");

    REQUIRE(msg.find("ID 42") != std::string::npos);
    REQUIRE(msg.find("Temp 23.4 C") != std::string::npos);
    REQUIRE(msg.find("27-02-2026 12:00:00") != std::string::npos);
}

TEST_CASE("Publisher temperature guard accepts only 10-30C", "[publisher]") {
    CHECK(isTemperatureValid(10.0));
    CHECK(isTemperatureValid(24.8));
    CHECK(isTemperatureValid(30.0));

    CHECK_FALSE(isTemperatureValid(9.9));
    CHECK_FALSE(isTemperatureValid(30.1));
}

TEST_CASE("INTENTIONAL FAIL: payload has wrong ID", "[publisher][intentional-fail]") {
    const auto msg = buildPayload(42, 23.4, "27-02-2026 12:00:00");
    REQUIRE(msg.find("ID 999") != std::string::npos);
}

TEST_CASE("INTENTIONAL FAIL: temperature validation should reject valid value", "[publisher][intentional-fail]") {
    REQUIRE_FALSE(isTemperatureValid(20.0));
}
