#include "handle.h" 
#include <fstream>
using namespace std;
void handle::replaceElement()
{
	makeUnique(source);
}
void handle::makeUnique(vector<string>& sour)
{
	sort(sour.begin(), sour.end());
	std::unique(sour.begin(), sour.end());
	//source.resize(std::distance(source.begin(), it));
	cout << "source after make unique" << endl;
	for (auto i : sour)
	{
		cout << i << endl;
	}
}
void handle::splitElement(string file)
{
	size_t p = file.find(" ");
	if (p == string::npos)
	{
		cout << "There is no value" << endl;
		return;
	}
	string temp;
	cout << "split for each string" << endl;
	do
	{
		temp = file.substr(0, p);
		file.erase(0, p + 1);
		if (!temp.compare("hastag") || !temp.compare(":"))
		{
			continue;
		}
		if (!temp.compare("\nsource"))
		{
			currentState = SOURCE_STATE;
			continue;
		}
		switch (currentState)
		{
		case HASTAG_STATE:
		{
			hastag.push_back(temp);
			break;
		}
		case SOURCE_STATE:
		{
			source.push_back(temp);
			break;
		}
		default:
			break;
		}
	} while (((p = file.find(" ")) != string::npos));
	cout << "list hastag la: " << endl;
	for (auto x : hastag)
	{
		cout << x << endl;
	}
	cout << "list source la: " << endl;
	for (auto x : source)
	{
		cout << x << endl;
	}
}
void handle::makeOutput()
{
	string address1;
	cout << "Output will be saved in folder: " << endl;
	getline(cin, address1);
	ofstream sour;
	sour.open(addCondition(address1, "source.txt"), ios::out | ios::ate);
	if (!sour.is_open())
	{
		cout << "Can not open file source.txt";
	}
	for (auto i : source)
	{
		sour << i << ",";
	}
	sour.close();
}