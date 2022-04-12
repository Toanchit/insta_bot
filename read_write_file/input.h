#ifndef _INPUT_H
#define _INPUT_H

#include<iostream>
#include "util.h"
#include<string>
using namespace std;
class input : public util
{
public:
	input() {};
public:
	bool inputValue();
	std::string getFileWithTypeString();
private:
	std:: string fileTypeString = "";
};

#endif