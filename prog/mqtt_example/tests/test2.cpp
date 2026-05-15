#include <catch2/catch_test_macros.hpp>

#include <string>

namespace {

bool shouldSubscribe(const std::string& topic, int qos) {
    return !topic.empty() && qos >= 0 && qos <= 2;
}

bool looksLikePublisherPayload(const std::string& message) {
    return message.find("ID ") != std::string::npos &&
           message.find(" - Temp ") != std::string::npos &&
           message.find(" C - ") != std::string::npos;
}

} // namespace

TEST_CASE("Subscriber config validation is sane", "[subscriber]") {
    CHECK(shouldSubscribe("test", 1));
    CHECK(shouldSubscribe("sensor/room1", 0));

    CHECK_FALSE(shouldSubscribe("", 1));
    CHECK_FALSE(shouldSubscribe("test", -1));
    CHECK_FALSE(shouldSubscribe("test", 3));
}

TEST_CASE("Subscriber recognizes publisher message pattern", "[subscriber]") {
    const std::string ok = "ID 9001 - Temp 21.3 C - 27-02-2026 12:34:56";
    const std::string bad = "hello world";

    CHECK(looksLikePublisherPayload(ok));
    CHECK_FALSE(looksLikePublisherPayload(bad));
}
