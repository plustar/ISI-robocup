#include <ros/ros.h>
#include <std_msgs/String.h>

#include <stdlib.h>
#include <string>
#include <stdio.h>
#include <signal.h>
using namespace std;
static void sig_int(int num)
{
	if(num == 2)
	{
		exit(0);
	}
}
//  receive       s    f    l    r   b   h   y
//array number    0    1    2    3   4   5   6
//    [s]    0   s/0  f/2  l/2  r/2 b/2 h/1 s/0
//    [sh]   1   s/1  f/1  l/1  r/1 b/1 s/1 y/0
// [f,l,r,b] 2   s/0  f/2  l/2  r/2 b/2 s/0 s/0
int msgC[3][7][2]={
	{{0,0},{1,2},{2,2},{3,2},{4,2},{5,1},{0,0}},
	{{0,1},{1,1},{2,1},{3,1},{4,1},{0,1},{6,0}},
	{{0,0},{1,2},{2,2},{3,2},{4,2},{0,0},{0,0}}
};
int currentR = 0;
char currentC = 's';
char constchar[] = {'s','f','l','r','b','h','y'};
int Getnum(char strcp)
{
	for(int i = 0; i < strlen(constchar); i++)
	{
		if(constchar[i] == strcp)
			return i;
	}
	return -1;		
}
char readMsgC(string msg, int &row)
{
	int index = Getnum(msg.c_str()[0]);
	if(index != -1)
	{
		row = msgC[row][index][2];
		return constchar[msgC[row][index][1]];
	}
	else 
		return constchar[0];
}
void sortmsg(const std_msgs::String::ConstPtr& msg_)
{
    string msg = msg_->data;
    currentC = readMsgC(msg, currentR);
}
int main(int argc, char** argv)
{
	ros::init(argc, argv, "sortTopic");
	ros::NodeHandle nh_;
	ros::Subscriber topic_sub;
	ros::Publisher topic_pub;
	topic_sub = nh_.subscribe<std_msgs::String>("sortmsg",10,&sortmsg);
	topic_pub = nh_.advertise<std_msgs::String>("socket2topic", 1);
	
	while(1)
	{
	    ros::spinOnce();
	    std_msgs::String msg;
	    msg.data = currentC;
	    topic_pub.publish(msg);
	}
	return 0;
}
