#include "input.h" 
#include <fstream>
using namespace std;
bool input::inputValue()
{
	string address1,address2;
	cout << "input address of file : " << endl;
	getline(cin, address1);
	if (address1.length() == 0)
	{
		cout << "address error" << endl << "input address again" << endl;
		return false;
	}
	cout << "input name of file" << endl;
	getline(cin, address2);
	if (address2.length() == 0)
	{
		cout << "address error" << endl << "input address again" << endl;
		return false;
	}
	ifstream ip1(addCondition(address1,address2));
	if (!ip1.is_open())
	{
		cout << "error when input " << endl;
		return false;
	}
	while (!ip1.eof())
	{
		string temp;
		getline(ip1, temp);
		fileTypeString.append(temp + "\n");
	}
	return true;
};
string input::getFileWithTypeString()
{
	cout << fileTypeString << endl;
	return fileTypeString;
};