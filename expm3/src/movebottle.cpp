#include <moveit/move_group_interface/move_group.h>
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float64.h>
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
	ros::Publisher gripper_pub = nh_.advertise<std_msgs::Float64>("/gripper_joint/command", 1);
	moveit::planning_interface::MoveGroup group_arm("arm");
	std_msgs::Float64 open,close;
    open.data = -0.2;
    close.data = 0;
	//moveit::planning_interface::MoveGroup group_gripper("gripper");
	group_arm.setNamedTarget("start_pose");
	group_arm.asyncMove();
	sleep(3);
	//group_gripper.setNamedTarget("gripper_close");
	//group_gripper.asyncMove();

	while(ros::ok())
	{

		switch(fetch_mark)
		{
			case 0:
				break;
			case 1:
				//group_gripper.setNamedTarget("gripper_open");
				//group_gripper.asyncMove();
				gripper_pub.publish(open);
				group_arm.setNamedTarget("hold_pose");		
				group_arm.asyncMove();
				sleep(3);
                gripper_pub.publish(close);
				//group_gripper.setNamedTarget("gripper_close");
				//group_gripper.asyncMove();
				fetch_mark = 0;
				break;
			case 2:
				group_arm.setNamedTarget("set_pose");
				group_arm.asyncMove();
				sleep(3);
				gripper_pub.publish(open);
				//group_gripper.setNamedTarget("gripper_open");
				//group_gripper.asyncMove();
				sleep(5);
				
				group_arm.setNamedTarget("start_pose");
				group_arm.asyncMove();
				gripper_pub.publish(close);
				//group_gripper.setNamedTarget("gripper_close");
				//group_gripper.asyncMove();
				fetch_mark = 0;
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
	cout<<"miCallback"<<endl;
	switch(cmd)
	{
		case 'h':

				cout<<"\tfetch bottle\n";
				fetch_mark = 1;
			break;
		case 'y':
				cout<<"\trelease bottle\n";
				fetch_mark = 2;
				break;
		default:
			break;
	} 
}

