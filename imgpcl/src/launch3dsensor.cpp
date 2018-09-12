#include <ros/ros.h> 
#include <std_msgs/String.h>
#include <iostream>

using namespace std;
void armCallback(const std_msgs::String::ConstPtr& msg)
{
    if(msg->data == "go")
    {
         system("roslaunch /home/isi/3dsensor.launch"); 
         cout<<"launch 3dsensor.launch\n";
    }   
}
int main(int argc, char **argv) 
{   	   
	ros::init(argc, argv, "launch");
	ros::NodeHandle nh_;
    ros::Subscriber launch_sub = nh_.subscribe("/arm2image", 5, armCallback);
	ros::spin();
	return 0;
}
