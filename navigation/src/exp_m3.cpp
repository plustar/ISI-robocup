#include <ros/ros.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Twist.h>
#include <nav_msgs/Odometry.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>

#define PI 3.141592  
#define DEG2RAD(DEG) ( (PI) * (DEG) / 180.0 ) 

using namespace std;

//void MICallback(const std_msgs::String::ConstPtr& msg);
void JDCallback(const std_msgs::String::ConstPtr& msg);

//int MI_mark = 0;
int JD_mark = 0;

int main(int argc, char **argv) 
{   	   	
    ros::init(argc, argv, "expm3");
    ros::NodeHandle nh_;
    //ros::Subscriber MI_sub = nh_.subscribe("MItopic_nd",1000, &MICallback);
    ros::Subscriber JD_sub = nh_.subscribe("JDtopic",1000, &JDCallback);
    ros::Publisher odom_pub = nh_.advertise<nav_msgs::Odometry>("odom", 50);
    tf::TransformBroadcaster odom_broadcaster;
    
    double x = 0.0;
    double y = 0.0;
    double th = 0.0;

    double vx = 0.0;
    double vy = 0.0;
    double vth = 0.0;

    ros::Time current_time, last_time;
    current_time = ros::Time::now();
    last_time = ros::Time::now();
    
    ros::Rate r(10.0);
    while(nh_.ok())
    {
        ros::spinOnce();// check for incoming messages
        current_time = ros::Time::now();
        
        switch(JD_mark)
        {
            case 0:{        //stop
                vx = 0.0;
                vy = 0.0;
                vth = 0.0;
                break;
            }
            case 1:{        //forward
                vx = 0.1;
                vy = 0.0;
                vth = 0.0;
                break;
            }
            case 2:{        //left
                vx = 0.0;
                vy = 0.0;
                vth = 0.1;
                break;
            }
            case 3:{        //right
                vx = 0.0;
                vy = 0.0;
                vth = -0.1;
                break;
            }
        }
        
        //compute odometry in a typical way given the velocities of the robot
        double dt = (current_time - last_time).toSec();
        double delta_x = (vx * cos(th) - vy * sin(th)) * dt;
        double delta_y = (vx * sin(th) + vy * cos(th)) * dt;
        double delta_th = vth * dt;

        x += delta_x;
        y += delta_y;
        th += delta_th;
        
        //since all odometry is 6DOF we'll need a quaternion created from yaw
        geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(th);
        
        //first, we'll publish the transform over tf
        geometry_msgs::TransformStamped odom_trans;
        odom_trans.header.stamp = current_time;
        odom_trans.header.frame_id = "odom";
        odom_trans.child_frame_id = "base_link";
        
        odom_trans.transform.translation.x = x;
        odom_trans.transform.translation.y = y;
        odom_trans.transform.translation.z = 0.0;
        odom_trans.transform.rotation = odom_quat;
    
        //send the transform
        odom_broadcaster.sendTransform(odom_trans);
    
        //next, we'll publish the odometry message over ROS
        nav_msgs::Odometry odom;
        odom.header.stamp = current_time;
        odom.header.frame_id = "odom";
   
        //set the position
        odom.pose.pose.position.x = x;
        odom.pose.pose.position.y = y;
        odom.pose.pose.position.z = 0.0;
        odom.pose.pose.orientation = odom_quat;
   
        //set the velocity
        odom.child_frame_id = "base_link";
        odom.twist.twist.linear.x = vx;
        odom.twist.twist.linear.y = vy;
        odom.twist.twist.angular.z = vth;
   
        //publish the message
        odom_pub.publish(odom);
    
        last_time = current_time;
        r.sleep();
    }
	return 0;
}

void JDCallback(const std_msgs::String::ConstPtr& msg)
{
    char cmd = 0;
    string value = msg->data;
    cmd = value[0];
    
    switch(cmd)
    {
        case 'f':    
            cout<<"\tforward\n";
            JD_mark = 1;
            break;
        case 'l':              
            cout<<"\tturn left\n"; 
            JD_mark = 2;
            break;
        case 'r':
            cout<<"\tturn right\n";
            JD_mark = 3;
            break;
        case 's':
			cout<<"\tstop\n";
			JD_mark = 0;
			break;
		default:
		    JD_mark = 0;
		    break;
    }
}
    
