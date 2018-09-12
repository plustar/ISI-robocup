#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include "boost/thread/mutex.hpp"
#include "boost/thread/thread.hpp"
#include "ros/console.h"
#include <std_msgs/String.h>

#define PI 3.1415926
#define DEG2RAD(DEG) ( (PI) * (DEG) / 180.0 )//Coverts angles to radians

using namespace std;
const double rotate_velocity = 1;
const double forward_velocity = 0.1;
const double time_unit = 0.05;

class ExpClassm3
{
	public:
		ExpClassm3();

	private:
		void ssCallback(const std_msgs::String::ConstPtr& msg);
		void publish();
//		void timectrl();

		ros::NodeHandle ph_,nh_;

		ros::Publisher vel_pub_;
		ros::Subscriber ss_sub_;

		geometry_msgs::Twist last_published_;
		boost::mutex publish_mutex_;
		ros::Timer timer_;
//		ros::Timer ctimer_;
		int rotate_mark;
		int loop_time;
		int loop_counter;
};

ExpClassm3::ExpClassm3()
{
	rotate_mark = 0;
	loop_time = int(DEG2RAD(90)/(time_unit*rotate_velocity));
	loop_counter = 0;
	cout<<"deg2rad(90): "<<DEG2RAD(90)<<endl;
	cout<<"loop_time: "<<loop_time<<endl;
	cout<<"time_unit: "<<time_unit<<endl;
	cout<<"rotate_velocity: "<<rotate_velocity<<endl;
	cout<<"total_rad: "<<time_unit*rotate_velocity*loop_time<<endl;
	vel_pub_ = ph_.advertise<geometry_msgs::Twist>("/cmd_vel_mux/input/safety_controller", 100, true);
	//vel_pub_ = ph_.advertise<geometry_msgs::Twist>("/mobile_base/commands/velocity", 1);
	ss_sub_ = nh_.subscribe<std_msgs::String>("socket2topic", 100, &ExpClassm3::ssCallback, this);
	timer_ = nh_.createTimer(ros::Duration(time_unit), boost::bind(&ExpClassm3::publish, this));
//	ctimer_ = nh_.createTimer(ros::Duration(10), boost::bind(&ExpClassm3::timectrl, this));

}

void ExpClassm3::ssCallback(const std_msgs::String::ConstPtr& msg)
{ 
	char cmd = 0;
	string value = msg->data;
	cmd = value[0];
	geometry_msgs::Twist vel;
	switch(cmd)
	{
		case 'f':   
			cout<<"Forward"<<endl; 
			vel.angular.z = 0;
			vel.linear.x = forward_velocity;
			rotate_mark = 0;
			
			break;
		case 'b':   
			cout<<"Back"<<endl; 
			vel.angular.z = 0;
			vel.linear.x = 0-forward_velocity;
			rotate_mark = 0;
			break;
		case 'l': 
			cout<<"Turn Left"<<endl;              
			vel.angular.z = rotate_velocity; 
			vel.linear.x = 0;
			rotate_mark = 1;
			break;
		case 'r':
			cout<<"Turn Right"<<endl; 
			vel.angular.z = 0-rotate_velocity;
			vel.linear.x = 0;
			rotate_mark = 1;
			break;
		case 's':
			cout<<"Stop"<<endl; 
			vel.angular.z = 0;
			vel.linear.x = 0;
			rotate_mark = 0;
			break;
		default:
			vel.angular.z = 0;
			vel.linear.x = 0;
			rotate_mark = 3;
			break;
	}
	last_published_ = vel;
}

void ExpClassm3::publish()
{
	boost::mutex::scoped_lock lock(publish_mutex_);
	switch (rotate_mark) {
		case 0:
			vel_pub_.publish(last_published_);
			//cout << "case 0" << endl;
			break;
		case 1:
			//vel_pub_.publish(last_published_);
			cout << "case 1" << endl;
			rotate_mark = 2;
			break;
		case 2:
			loop_counter += 1;
			vel_pub_.publish(last_published_);
			cout << "loop counter:" << loop_counter <<" loop_time:"<< loop_time <<endl;
			if(loop_counter == loop_time)
			{
				loop_counter = 1;
				rotate_mark = 3;
				vel_pub_.publish(*new geometry_msgs::Twist);
			}
			break;
		case 3:
			loop_counter += 1;
			vel_pub_.publish(last_published_);
			cout << "loop counter:" << loop_counter <<" loop_time:"<< loop_time <<endl;
			if(loop_counter == loop_time)
			{
				loop_counter = 1;
				rotate_mark = 4;
				vel_pub_.publish(*new geometry_msgs::Twist);
			}
			break;
		case 4:
		    vel_pub_.publish(*new geometry_msgs::Twist);
		    break;
		default:
			vel_pub_.publish(*new geometry_msgs::Twist);
			break;
	}

}
int main(int argc, char** argv)
{
	ros::init(argc, argv, "exp_c");
	ExpClassm3 expm3;

	ros::spin();
	return 0;
}
