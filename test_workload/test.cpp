#include <vector>
#include <iostream>

using namespace std;

int main(){
  vector<int> a;
  vector<int> b;
  
  a.push_back(1);
  a.push_back(2);

  cout << a.size();
  b = a;
  a.clear();
  cout << b.size();
  return 0;
}
