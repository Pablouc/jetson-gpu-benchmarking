#include <stdlib.h>
#include <fstream>
#include <iostream>
#include <stdio.h>
#include <termio.h>
#include <unistd.h>
#include <time.h>
using namespace std;
int main(){
 ifstream gpuPowerFile;
 int totalCount=0;
 int sumofPower=0;
 char input=0;
 time_t start=time(NULL);
 while(true){
   string str;
   int power=0;
   int voltage=0;
   int val;
   gpuPowerFile.open("/sys/bus/i2c/drivers/ina3221x/1-0040/iio:device0/in_power0_input");


   gpuPowerFile>>str;
   val=atoi(str.c_str());
   cout<<"GPU Power:"<<val<<"mW"<<endl;
   power+=val;
   str.clear();
  
   gpuPowerFile.close();
   
   cout<<"Total Power:"<<power<<"mW"<<endl;
   sumofPower+=power;
   totalCount++;
   cout<<"AveragePower: "<<sumofPower/totalCount<<endl;
   time_t end=time(NULL);
   cout<<"Time: "<<(double)(end-start)<<endl;
   sleep(1);
 }
}