
#include <iostream>

#include "helper.hpp"

void print_one_thing() {
    std::cout << "I printed one thing" << std::endl;
}

void print_many_things() {
    for (int i = 0; i < 10; i++) {
        std::cout << "i am printing the " << i << "'th time" << std::endl;
    }
}
