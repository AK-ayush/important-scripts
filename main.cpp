#include <iostream>
#include <bits/stdc++.h>

using namespace std;

int findMissing(vector<int> adam, vector<int> alex){
  cout<<"here\n";
  int n = adam.size();
  int m = alex.size();
  if(m == 0)  return  adam[0];


  int l1, r1,mid1, l2, r2, mid2;
  l1 = 0, r1 = n-1;
  l2 = 0, r2 = m-1;
  
  while(l1 <= r1 && l2 <= r2){
    mid1 = (l1+r1)/2;
    mid2 = (l2+ r2)/2;

    if(mid1== mid2){
     if(adam[mid1] == alex[mid2]){  l1 = mid1+1;  l2 = mid2+1;}
     else {  r1 = mid1;  r2 = mid2;} 
     }
     else if (mid1 > mid2){
        if(mid2+1 < m && adam[mid1] == alex[mid2+1]) {  l1 = mid1+1;  l2 = mid2+1;}
        else {  r1 = mid1;  r2 = mid2;}  
     }
  }
  cout<<l1<<r1<<l2<<r2<<endl;
  return adam[l1];

}



int main()
{
   //cout << "Hello World" << endl; 
   vector<int> adam = {2, 3, 4, 5, 6};
   vector<int> alex = {2, 3, 4, 5};
   
   int ans = findMissing(adam, alex);
   
   cout<<ans<<endl;
   
   return 0;
}
