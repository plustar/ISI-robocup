#include <moveit/move_group_interface/move_group.h>
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float64.h>
#include "boost/thread/mutex.hpp"
#include "boost/thread/thread.hpp"
#include "ros/console.h"
#include "time.h"

using namespace std;
void miCallback(const std_msgs::String::ConstPtr& msg);

int fetch_mark = 0;
bool fetched = false;
int main(int argc, char** argv)
{
	ros::init(argc, argv, "movebottle");
	moveit::planning_interface::MoveGroup group_arm("arm");
	moveit::planning_interface::MoveGroup group_gripper("gripper");
	string reference_frame = "arm_base_link";
	group_arm.setStartStateToCurrentState();
    group_arm.setPoseReferenceFrame(reference_frame);
    group_arm.setEndEffectorLink("gripper_active_finger_link");
    string end_effector_link = group_arm.getEndEffectorLink();
    string end_effector = group_arm.getEndEffector();
    cout<<"end_effector: "<<end_effector<<" end_effector_link: "<<end_effector_link<<endl;
/*	geometry_msgs::PoseStamped target_pose;
	target_pose.header.frame_id = reference_frame;
	target_pose.header.stamp = ros::Time::now();
	target_pose.pose.position.x = 0.20;
    target_pose.pose.position.y = 0.2;
    target_pose.pose.position.z = 0.2;
    target_pose.pose.orientation.x = 0.0;
    target_pose.pose.orientation.y = 0.0;
    target_pose.pose.orientation.z = 0.0;
    target_pose.pose.orientation.w = 1.0;
 */   
    group_arm.setPositionTarget(0,0,0,end_effector_link);
    moveit::planning_interface::MoveGroup::Plan plan;
    group_arm.plan(plan);
    group_arm.execute(plan);
    sleep(1);
	ros::spin();
	return 0;
}

