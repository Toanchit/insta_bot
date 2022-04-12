// read_write_file.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "input.h"
#include "handle.h"
using namespace std;
int main()
{
    std::cout << "Hello World!\n";
    input test1;
    handle handl1;
    while (1)
    {
        if (!test1.inputValue())
        {
            continue;
        }
        handl1.splitElement(test1.getFileWithTypeString());
        handl1.replaceElement();


    }
}

