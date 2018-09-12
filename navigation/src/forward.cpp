#include <ros/ros.h>
#include <std_msgs/String.h>
#include <kobuki_msgs/MotorPower.h>
#include <signal.h>
#include <geometry_msgs/Twist.h>
#include <tf/transform_listener.h>
#include <nav_msgs/Odometry.h>
#include <string.h>
#include <cmath>
const double pi = 3.141592653;
using namespace std;
ros::Publisher cmd_vel_pub;

void forward_robot(double forward_distance, double forward_time)
{
  geometry_msgs::Twist vel;
  int rate = 10;
  ros::Rate loop_rate(rate);
  vel.linear.x = forward_distance / forward_time;
  int count = int(forward_time * rate);
  for (int i = 0; i < count; i++)
    {
      cmd_vel_pub.publish(vel);
      loop_rate.sleep();
    }
  vel.linear.x = 0.0;
  cmd_vel_pub.publish(vel);
  sleep(1.5);
}

int main (int argc, char** argv)
{
  ros::init (argc, argv, "Forward");
  ros::NodeHandle nh;
  cmd_vel_pub = nh.advertise<geometry_msgs::Twist>("/mobile_base_controller/cmd_vel", 1);
  ros::spin();
  return 0;
}
