#include <ros/ros.h>
#include <std_msgs/String.h>
#include <kobuki_msgs/MotorPower.h>
#include<geometry_msgs/Twist.h>
#include <signal.h>
#include <geometry_msgs/Twist.h>
#include <tf/transform_listener.h>
#include <nav_msgs/Odometry.h>
#include <string.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <kobuki_msgs/DigitalInputEvent.h>
#include <cmath>

ros::Publisher turn_pub;
ros::Publisher cmd_vel_pub;
const double pi = 3.141592653;
void turn_robot(double rotate_angle, double rotate_time)
{
  geometry_msgs::Twist vel;
  int rate = 50;
  ros::Rate loop_rate(rate);
  double angle = pi * rotate_angle / 180;
  vel.angular.z = angle / rotate_time;
  int count = int(angle * rate);
  for (int i = 0; i < count; i++)
  {
    cmd_vel_pub.publish(vel);
    loop_rate.sleep();
  }
  vel.angular.z = 0.0;
  cmd_vel_pub.publish(vel);
  sleep(1.5);
}

void turn_left()
{
  turn_robot(90, 1.5);
  std_msgs::String str;
  turn_pub.publish(str);
}

void detectaround()
{
  for(int i = 0; i < 4; ++i)
    {
      turn_left();
    }
}

int main (int argc, char** argv)
{
  ros::init (argc, argv, "DetectAround");
  ros::NodeHandle nh;
  turn_pub = nh.advertise<std_msgs::String>("/turnleft", 1);
  cmd_vel_pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel_mux/input/safety_controller", 1);
  turn_pub = nh.advertise<std_msgs::String>("/turnleft", 1);
  detectaround();
  ros::spin ();
  exit(0);
  return 0;
}
