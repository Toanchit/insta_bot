#ifndef _HANDLE_H
#define _HANDLE_H

#include <string>
#include <iostream>
#include <algorithm> 
#include <vector>
#include "util.h"
enum state
{
	HASTAG_STATE,
	SOURCE_STATE
};
using namespace std;
class handle : public util
{
public:
	handle() {};
	void replaceElement();
	void splitElement(string file);
	void makeOutput();
	void makeUnique(vector<string>& sour);
private:
	int currentState = HASTAG_STATE;
	vector<string> general;
	vector<string> source;
	vector<string> hastag;
};
#endif // !_HANDLE_H
