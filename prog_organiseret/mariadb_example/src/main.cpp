#include <iostream>
#include <mariadb/mysql.h>

int main() {
    MYSQL* conn = mysql_init(nullptr);

    if (!conn) {
        std::cout << "mysql_init failed\n";
        return 1;
    }

    std::string username;
    std::cout << "Enter username: ";
    std::cin >> username;

    std::string password;
    std::cout << "Enter password: ";
    std::cin >> password;

    if (!mysql_real_connect(conn, "localhost", username.c_str(), password.c_str(), nullptr, 0, nullptr, 0)) {
        std::cout << "Connection failed: " << mysql_error(conn) << "\n";
        mysql_close(conn);
        return 1;
    }

    std::cout << "Forbundet til MariaDB\n";
    std::cout << "Server version: " << mysql_get_server_info(conn) << "\n";
    std::cout << "Client version: " << mysql_get_client_info() << "\n";
    std::cout << "Host info: " << mysql_get_host_info(conn) << "\n";
    std::cout << "Protocol info: " << mysql_get_proto_info(conn) << "\n";
    std::cout << "Server status: " << mysql_stat(conn) << "\n";

    mysql_close(conn);
    return 0;
}
