#include <iostream>
#include <mariadb/mysql.h>

int main() {
    MYSQL* conn = mysql_init(nullptr);

    if (!conn) {
        std::cerr << "mysql_init failed\n";
        return 1;
    }

    mysql_close(conn);
    std::cout << "MariaDB client smoke test passed\n";
    return 0;
}
