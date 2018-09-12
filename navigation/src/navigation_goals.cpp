#include<ros/ros.h>
#include<iostream>
#include<std_msgs/String.h>
#include<string.h>

#include<geometry_msgs/Pose.h>
#include<geometry_msgs/Point.h>
#include<geometry_msgs/PoseWithCovariance.h>
#include<geometry_msgs/PoseWithCovarianceStamped.h>
#include<geometry_msgs/Twist.h>
#include<geometry_msgs/Quaternion.h>
#include <kobuki_msgs/DigitalInputEvent.h>
#include <kobuki_msgs/ButtonEvent.h>

#include<move_base_msgs/MoveBaseGoal.h>
#include<move_base_msgs/MoveBaseAction.h>

#include<actionlib/client/simple_action_client.h>
#include<cstdlib>
using namespace std;
typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient; //

geometry_msgs::Pose MyPose;

int main(int argc, char** argv)
{
  ros::init(argc, argv, "navi_goal");
  ros::NodeHandle myNode;
  MoveBaseClient  mc_("move_base", true);
  move_base_msgs::MoveBaseGoal naviGoal;
  MyPose.position.x = 2;
  MyPose.position.y = -0.5;
  MyPose.position.z = 0;
  MyPose.orientation.x = 0;
  MyPose.orientation.y = 0;
  MyPose.orientation.z = 0;
  MyPose.orientation.w = 1;
      naviGoal.target_pose.header.frame_id = "base_link";
      naviGoal.target_pose.header.stamp = ros::Time::now();
      naviGoal.target_pose.pose = geometry_msgs::Pose(MyPose);

      while(!mc_.waitForServer(ros::Duration(5.0)))
        {
          cout<<"Waiting for the server..."<<endl;
        }
      mc_.sendGoal(naviGoal);
      mc_.waitForResult(ros::Duration(20.0));

      if(mc_.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
        {
          cout<<"Move to the gate....";
        }

      ros::spinOnce();
  return 0;
}
