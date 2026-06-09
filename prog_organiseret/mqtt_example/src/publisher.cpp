#include <atomic>
#include <chrono>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <thread>

#include "mqtt/async_client.h"

using namespace std;

const string DFLT_SERVER_URI{"mqtt://localhost:1883"};

const string TOPIC{"test"};
const int QOS = 1;

const auto TIMEOUT = chrono::seconds(10);

/*
 * make_payload:
 * 1) Generates a random sensor ID (1000-9999).
 * 2) Generates a random temperature in Celsius (10.0-30.0).
 * 3) Reads the current local time.
 * 4) Formats everything into one payload string:
 *    ID <id> - Temp <temp> C - <dd-mm-yyyy hh:mm:ss>
 */
string make_payload(mt19937& rng) {
    uniform_int_distribution<int> id_dist(1, 3);
    uniform_real_distribution<double> temp_dist(10.0, 100.0);

    const auto now = chrono::system_clock::now();
    const time_t raw_time = chrono::system_clock::to_time_t(now);
    tm local_tm{};
    localtime_r(&raw_time, &local_tm);

    ostringstream out;
    out << "ID " << id_dist(rng)
        << " - Temp " << fixed << setprecision(1) << temp_dist(rng) << " C"
        << " - " << put_time(&local_tm, "%d-%m-%Y %H:%M:%S");
    return out.str();
}

/*
 * main:
 * 1) Reads broker URI from command line or uses default localhost URI.
 * 2) Creates MQTT async client and connects to broker.
 * 3) Publishes an intro message and then 5 generated payload messages.
 * 4) Waits for publish completion and disconnects cleanly.
 * 5) Prints and returns error code if MQTT throws an exception.
 */
int main(int argc, char* argv[]){
    string serverURI = (argc > 1) ? string(argv[1]) : DFLT_SERVER_URI;

    cout << "Connecting to the MQTT server at " << serverURI << "..." << endl;
    mqtt::async_client cli(serverURI, "");

    cout << "  .... OK" << endl;

    try {
        cout << "\nConnecting..." << endl;
        cli.connect()->wait();
        cout << "  ... OK" << endl;

        cout << "\nPublishing messages..." << endl;

        mqtt::topic top(cli, TOPIC, QOS);
        mqtt::token_ptr tok;
        random_device rd;
        mt19937 rng(rd());

        top.publish("EXAMPLE PAYLOADS INCOMMING");
        for (int i = 0; i < 10; ++i) {
            const string payload = make_payload(rng);
            cout << "  -> " << payload << endl;
            tok = top.publish(payload);
            this_thread::sleep_for(chrono::milliseconds(500));
        }
        tok->wait_for(TIMEOUT);
        cout << "  ... OK" << endl;

        cout << "\nDisconnecting..." << endl;
        cli.disconnect()->wait();
        cout << "  ... OK" << endl;
    }
    catch (const mqtt::exception& exc) {
        cerr << exc << endl;
        return 1;
    }
    return 0;
}
