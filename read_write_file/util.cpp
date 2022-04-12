#include "util.h"

using namespace std;
string util::addCondition(string address1, string address2)
{
	string result;
	for (int32_t i = 0; i < address1.length(); i++)
	{
		if (address1[i] == ' \ ')
		{
			result.append("\\");
		}
		else
		{
			result.push_back(address1[i]);
		}
	}
	result.append("\\");
	result.append(address2);
	cout << result << endl;
	return result;
}