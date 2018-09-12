#include <ros/ros.h>
#include <nav_msgs/Odometry.h>
#include "boost/thread/mutex.hpp"
#include "boost/thread/thread.hpp"
#include "ros/console.h"
#include <std_msgs/String.h>
#include <geometry_msgs/Twist.h>  // for velocity commands  
#include <geometry_msgs/TwistStamped.h>  // for velocity commands  
  
#include <nav_msgs/Odometry.h>  
#include "tf/LinearMath/Matrix3x3.h"  
#include "geometry_msgs/Quaternion.h"

#define PI 3.1415926535897932384626433832795
#define DEG2RAD(DEG) ( (PI) * (DEG) / 180.0 )//Coverts angles to radians

using namespace std;
const double rotate_velocity = 1.5;
const double forward_velocity = 0.1;
const double time_unit = 0.0001;
typedef struct D2Position  
{  
   double  x;  
   double  y;  
   double  theta;   
} pos;
class ExpClassm3
{
	public:
		ExpClassm3();
		D2Position start;
		D2Position curr;

	private:
		void ssCallback(const std_msgs::String::ConstPtr& msg);
		void odomCallback(const nav_msgs::Odometry::ConstPtr& msg);
		void publish();
		double angleWrap(double angle);
		ros::NodeHandle ph_,nh_;
		ros::Publisher vel_pub_;
		ros::Subscriber ss_sub_;
		ros::Subscriber odom_sub_;

		boost::mutex publish_mutex_;
		ros::Timer timer_;
		
		int command;
		int loop_time;
		int loop_counter;
		bool isstart;
};

ExpClassm3::ExpClassm3()
{
    isstart = 0;
	command = -1;
	
	loop_time = int(DEG2RAD(90)/(time_unit*rotate_velocity));
	loop_counter = 0;
	cout<<"deg2rad(90): "<<DEG2RAD(90)<<endl;
	cout<<"loop_time: "<<loop_time<<endl;
	cout<<"time_unit: "<<time_unit<<endl;
	cout<<"rotate_velocity: "<<rotate_velocity<<endl;
	cout<<"total_rad: "<<time_unit*rotate_velocity*loop_time<<endl;
	//vel_pub_ = ph_.advertise<geometry_msgs::Twist>("/cmd_vel_mux/input/safety_controller", 100, true);
	vel_pub_ = ph_.advertise<geometry_msgs::Twist>("/mobile_base/commands/velocity", 1);
	ss_sub_ = nh_.subscribe<std_msgs::String>("socket2topic", 1, &ExpClassm3::ssCallback, this);
	odom_sub_ = nh_.subscribe("/odom", 1000, &ExpClassm3::odomCallback,this);
	timer_ = nh_.createTimer(ros::Duration(time_unit), boost::bind(&ExpClassm3::publish, this));
}
double ExpClassm3::angleWrap(double angle)  
{  
    if (angle>=PI)  
        while (angle >= PI)  
        { angle = angle-2*PI;}  
    else if (angle < -1.0*PI)  
        while (angle < -1.0*PI)  
        { angle = angle+2*PI;}  
  return angle;  
}  
void ExpClassm3::odomCallback(const nav_msgs::Odometry::ConstPtr& msg)  
{ 
    geometry_msgs::Quaternion orientation = msg->pose.pose.orientation;  
    tf::Matrix3x3 mat(tf::Quaternion(orientation.x, orientation.y, orientation.z, orientation.w));  
    double yaw, pitch, roll;  
    mat.getEulerYPR(yaw, pitch, roll);  
    curr.x = msg->pose.pose.position.x;  
    curr.y = msg->pose.pose.position.y;  
    curr.theta = yaw; 
    switch (command)
    {
        case 1:
            command = 11;
            //isstart = 1;
            break;
        case 2:
            command = 21;
            //isstart = 1;
            break;
        case 3:
            command = 31;
            isstart = 1;
            break;
        case 4:
            command = 41;
            isstart = 1;
            break;
        case 11:
            publish();
            break;
        case 21:
            publish();
            break;
        case 31:
            publish();
            break;
        case 41:
            publish();
            break;
        case 0:
            publish();
            break;
        default:
            publish();
            break;
    }
}
void ExpClassm3::ssCallback(const std_msgs::String::ConstPtr& msg)
{ 
	char cmd = 0;
	string value = msg->data;
	cmd = value[0];
	switch(cmd)
	{
		case 'f':   
	        cout<<"Forward"<<endl; 
			command = 1;
			break;
		case 'b':   
			cout<<"Back"<<endl; 
			command = 2;
			break;
		case 'l': 
		    cout<<"Turn Left"<<endl;
			command = 3;
			break;
		case 'r':
		    cout<<"Turn Right"<<endl;
			command = 4;
			break;
		case 's':
	        cout<<"Stop"<<endl; 
			command = 0;
			break;
		default:
			command = 0;
			break;
	}
}

void ExpClassm3::publish()
{
	geometry_msgs::Twist vel = *new geometry_msgs::Twist;
	boost::mutex::scoped_lock lock(publish_mutex_);
	switch(command){
	    case 0:
	        vel_pub_.publish(vel);
	        break;
	    case 11:
			vel.angular.z = 0;
			vel.linear.x = forward_velocity;
			vel_pub_.publish(vel);
			command = 11;
			break;
		case 21:
			vel.angular.z = 0;
			vel.linear.x = 0-forward_velocity;
			vel_pub_.publish(vel);
			command = 21;
			break;
		case 31:  
		    if(isstart)
		    {
		        start.x = curr.x;
                start.y = curr.y;
                start.theta = curr.theta;
                isstart = 0;
		    }       
		    cout << "theta: " <<abs(angleWrap(curr.theta - start.theta)) << endl;
		    if (angleWrap(curr.theta - start.theta)< PI/2 )  
            {      
			    vel.angular.z = rotate_velocity; 
			    vel.linear.x = 0;
			    vel.linear.y = 0;
			    vel.linear.z = 0;
			    vel_pub_.publish(vel);
			    command = 31;
			}
			else
			{
			    vel_pub_.publish(*new geometry_msgs::Twist);
			    command = 0;
			}
			break;
		case 41: 
		    if(isstart)
		    {
		        start.x = curr.x;
                start.y = curr.y;
                start.theta = curr.theta;
                isstart = 0;
		    } 
			cout << "theta: " <<abs(angleWrap(curr.theta - start.theta)) << endl;
		    if ( abs(angleWrap(curr.theta - start.theta)) < PI/2 )  
            {      
			    vel.angular.z = 0 - rotate_velocity; 
			    vel.linear.x = 0;
			    vel.linear.y = 0;
			    vel.linear.z = 0;
			    vel_pub_.publish(vel);
			    command = 41;
			}
			else
			{
			    vel_pub_.publish(*new geometry_msgs::Twist);
			    command = 0;
			}
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
