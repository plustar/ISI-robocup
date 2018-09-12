#include <moveit/move_group_interface/move_group.h>
#include <ros/ros.h>
#include <std_msgs/String.h>
#include "boost/thread/mutex.hpp"
#include "boost/thread/thread.hpp"
#include "ros/console.h"

using namespace std;
void miCallback(const std_msgs::String::ConstPtr& msg);

int fetch_mark = 0;
bool fetched = false;

int main(int argc, char** argv)
{
	ros::init(argc, argv, "movebottle");
	ros::NodeHandle nh_;
	ros::Subscriber mi_sub_ = nh_.subscribe<std_msgs::String>("socket2topic",1000,&miCallback);
	moveit::planning_interface::MoveGroup group_arm("arm");
	//moveit::planning_interface::MoveGroup group_arm("arm");
	group_arm.setNamedTarget("start_pose");
	group_arm.asyncMove();
	while(ros::ok())
	{

		switch(fetch_mark)
		{
			case 0:
				break;
			case 1:
				group_arm.setNamedTarget("hold_pose");
				group_arm.asyncMove();
				break;
			case 2:
				group_arm.setNamedTarget("set_pose");
				group_arm.asyncMove();
				fetch_mark = 3;
				sleep(1);
				break;
			case 3:
				group_arm.setNamedTarget("start_pose");
				group_arm.asyncMove();
				fetch_mark = 0;
				fetched = false;
				break;
			default:
				break;
		}
		ros::spinOnce();
	}
}
void miCallback(const std_msgs::String::ConstPtr& msg)
{
	char cmd = 0;
	string value = msg->data;
	cmd = value[0];
	switch(cmd)
	{
		case 'h':
			if(!fetched)
			{
				cout<<"\tfetch bottle\n";
				fetch_mark = 1;
				fetched = true;
				break;

			}		
			break;
		case 'y':
			if(fetch_mark == 1)
			{
				cout<<"\trelease bottle\n";
				fetch_mark = 2;
				break;
			}
		default:
			break;
	} 
}

