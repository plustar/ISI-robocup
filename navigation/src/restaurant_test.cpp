#include<ros/ros.h>
#include<iostream>
#include<std_msgs/String.h>
//navigation中需要使用的位姿信息头文件
#include<geometry_msgs/Pose.h>
#include<geometry_msgs/Point.h>
#include<actionlib_msgs/GoalID.h>
#include<nav_msgs/Odometry.h>
#include<geometry_msgs/PoseWithCovariance.h>
#include<geometry_msgs/PoseWithCovarianceStamped.h>
#include<geometry_msgs/Twist.h>
#include<geometry_msgs/Quaternion.h>
#include<kobuki_msgs/DigitalInputEvent.h>
#include<kobuki_msgs/ButtonEvent.h>
#include<kobuki_msgs/MotorPower.h>
//move_base头文件
#include<move_base_msgs/MoveBaseGoal.h>
#include<move_base_msgs/MoveBaseAction.h>
//actionlib头文件
#include<actionlib/client/simple_action_client.h>
#include<cstdlib>
using namespace std;
typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient; //简化类型书写为MoveBaseClient
bool estop_in=false;   //急停开关标志 低电平为输入，高电平为信号判断
bool backtobar = false;
bool backtoclient1 = false;
bool backtoclient2 = false;
bool receivePose = false;
bool towardGoal = false;
int locationnum=0; //标志位置序号

std_msgs::String sound_flag;
geometry_msgs::Twist vel; //控制机器人速度
geometry_msgs::Pose bar_pose;
geometry_msgs::Pose table1_pose;
geometry_msgs::Pose table2_pose;
geometry_msgs::Pose current_goal;
geometry_msgs::Pose viewpoint[4];

int ViewPoint = -1;
bool towardViewPoint = false;

ros::Publisher sound_pub;
ros::Publisher motor_power_pub;
ros::Publisher nav2img_pub;
ros::Publisher wave_pub;
ros::Publisher move_base_cancel_pub;

ros::Subscriber button_sub;
ros::Subscriber sound_sub;//订阅语音消息以记住bar以及tables的位置
ros::Subscriber location_sub;//订阅/odom话题
ros::Subscriber image_sub;
ros::Subscriber imagestr_sub;
ros::Subscriber soundimg_sub;

void initData();
void soundCallback(const std_msgs::String::ConstPtr& msg);
void locationCallback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg);
void DigitalInputEventCallback(const kobuki_msgs::DigitalInputEvent::ConstPtr& msg);
void imageCallback(const geometry_msgs::Point &point);
void imagestrCallback(const std_msgs::String::ConstPtr& msg);
void waveCallback(const std_msgs::String::ConstPtr& msg);

void initData()
{
  viewpoint[0].position.x = 2;
  viewpoint[0].position.y = 0;
  viewpoint[0].position.z = 0;
  viewpoint[0].orientation.x = 0;
  viewpoint[0].orientation.y = 0;
  viewpoint[0].orientation.z = 0;
  viewpoint[0].orientation.w = 1;
  viewpoint[1].position.x = 3;
  viewpoint[1].position.y = 0;
  viewpoint[1].position.z = 0;
  viewpoint[1].orientation.x = 0;
  viewpoint[1].orientation.y = 0;
  viewpoint[1].orientation.z = 0;
  viewpoint[1].orientation.w = 1;
  viewpoint[2].position.x = 0;
  viewpoint[2].position.y = -2;
  viewpoint[2].position.z = 0;
  viewpoint[2].orientation.x = 0;
  viewpoint[2].orientation.y = 0;
  viewpoint[2].orientation.z = 0;
  viewpoint[2].orientation.w = 1;
  viewpoint[3].position.x = -3;
  viewpoint[3].position.y = 0;
  viewpoint[3].position.z = 0;
  viewpoint[3].orientation.x = 0;
  viewpoint[3].orientation.y = 0;
  viewpoint[3].orientation.z = 0;
  viewpoint[3].orientation.w = 1;
}
//主函数
int main(int argc, char** argv)
{
  ros::init(argc, argv, "restaurant_test");
  ros::NodeHandle myNode;
  initData();
  ROS_INFO("Welcome to Restaurant!");
    
  
  motor_power_pub = myNode.advertise<kobuki_msgs::MotorPower>("/mobile_base/commands/motor_power",1);
  move_base_cancel_pub = myNode.advertise<actionlib_msgs::GoalID>("move_base/cancel",1);
  button_sub = myNode.subscribe("/mobile_base/events/digital_input",1,DigitalInputEventCallback);
  
  
  
  nav2img_pub = myNode.advertise<std_msgs::String>("nav2img", 1);
  wave_pub = myNode.advertise<std_msgs::String>("detectWave", 1);
  sound_pub = myNode.advertise<std_msgs::String>("voice_service", 1);
  
  
  image_sub = myNode.subscribe("/img2nav", 1, imageCallback);
  //imagei_sub = myNode.subscribe("/img2navi", 1, imagestrCallback);
  sound_sub = myNode.subscribe("/speech2nav", 1, soundCallback);
  soundimg_sub = myNode.subscribe("/detectWave", 1, waveCallback);
  location_sub = myNode.subscribe("/amcl_pose", 100, locationCallback);
  
  MoveBaseClient mc_("move_base", true); //建立导航客户端
  move_base_msgs::MoveBaseGoal naviGoal; //导航目标点

  while(ros::ok())
    {
      ros::spinOnce();
      if(towardViewPoint)
        {
          std_msgs::String stop;
          stop.data = "stopvel";
          wave_pub.publish(stop);
          naviGoal.target_pose.header.stamp = ros::Time::now();
          naviGoal.target_pose.pose = geometry_msgs::Pose(viewpoint[ViewPoint]);
          naviGoal.target_pose.header.frame_id = "base_link";
          while(!mc_.waitForServer(ros::Duration(5.0)))
            {
              ROS_INFO("Waiting for the server...");
            }
          mc_.sendGoal(naviGoal);
          mc_.waitForResult(ros::Duration(20.0));
          if(mc_.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
            {
              std::cout<<"Reach the ViewPoint ["<<ViewPoint<<"]"<<std::endl;
              std_msgs::String send_flag;
              send_flag.data = "wave";
              wave_pub.publish(send_flag);
              ROS_INFO("I have sent the message I have reached the ViewPoint!");
              towardViewPoint = false;
            }
          continue;
        }
      if(towardGoal)
        {
          std_msgs::String stop;
          stop.data = "stopvel";
          wave_pub.publish(stop);
          current_goal.position.x -= 0.5;
          current_goal.position.x += 0.5;
          naviGoal.target_pose.header.stamp = ros::Time::now();
          naviGoal.target_pose.pose = geometry_msgs::Pose(current_goal);
          naviGoal.target_pose.header.frame_id = "base_link";
          while(!mc_.waitForServer(ros::Duration(5.0)))
            {
              ROS_INFO("Waiting for the server...");
            }
          mc_.sendGoal(naviGoal);
          mc_.waitForResult(ros::Duration(20.0));
          ROS_INFO("Arrive nearby.");
          std_msgs::String send_flag;
          send_flag.data = "wave";
          nav2img_pub.publish(send_flag);
          ROS_INFO("I have sent the message to face to the person!");
          towardGoal = false;
          continue;
        }
      if(backtobar)
        {
          naviGoal.target_pose.header.stamp = ros::Time::now();
          naviGoal.target_pose.pose = geometry_msgs::Pose(bar_pose);
          naviGoal.target_pose.header.frame_id = "map";
          while(!mc_.waitForServer(ros::Duration(5.0)))
            {
              ROS_INFO("Waiting for the server...");
            }
          mc_.sendGoal(naviGoal);
          mc_.waitForResult(ros::Duration(20.0));
          if(mc_.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
            {
              ROS_INFO("Reach the bar.");
              std_msgs::String send_flag;
              send_flag.data = "reachbar";
              sound_pub.publish(send_flag);
              ROS_INFO("I have sent the message I have reached the bar!");
              backtobar = false;
            }
          continue;
        }
      if(backtoclient1)
        {
          naviGoal.target_pose.header.stamp = ros::Time::now();
          naviGoal.target_pose.pose = geometry_msgs::Pose(table1_pose);
          naviGoal.target_pose.header.frame_id = "map";
          while(!mc_.waitForServer(ros::Duration(5.0)))
            {
              ROS_INFO("Waiting for the server...");
            }
          mc_.sendGoal(naviGoal);
          mc_.waitForResult(ros::Duration(20.0));
          if(mc_.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
            {
              ROS_INFO("Reach the client1.");
              std_msgs::String send_flag;
              send_flag.data = "reachclient1";
              sound_pub.publish(send_flag);
              ROS_INFO("I have sent the message I have reached the client1!");
              backtoclient1 = false;
            }
          continue;
        }
      if(backtoclient2)
        {
          naviGoal.target_pose.header.stamp = ros::Time::now();
          naviGoal.target_pose.pose = geometry_msgs::Pose(table2_pose);
          naviGoal.target_pose.header.frame_id = "map";
          while(!mc_.waitForServer(ros::Duration(5.0)))
            {
              ROS_INFO("Waiting for the server...");
            }
          mc_.sendGoal(naviGoal);
          mc_.waitForResult(ros::Duration(20.0));
          if(mc_.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
            {
              ROS_INFO("Reach the client2.");
              std_msgs::String send_flag;
              sound_flag.data = "reachclient2";
              sound_pub.publish(sound_flag);
              ROS_INFO("I have sent the message I have reached the client2!");
              backtoclient2 = false;
            }
          continue;
        }
    }
  return 0;
}
void waveCallback(const std_msgs::String::ConstPtr& msg)
{
  if(msg->data == "wave")
    receivePose = true;
}
void soundCallback(const std_msgs::String::ConstPtr& msg)
{
	
  if(msg->data == "start")
    {
      locationnum=1;
      ROS_INFO("I am at the bar");
    }
  if(msg->data == "order1")
    {
      locationnum=2;
      ROS_INFO("I am beside the client1");
      receivePose = false;
    }
    
  if(msg->data == "order2")
    {
      locationnum=3;
      ROS_INFO("I am beside the client2");
      receivePose = false;
    }
  if(msg->data == "backorder1")
    {
      backtoclient1 = true;
      ROS_INFO("I am toward the client1");
    }
  if(msg->data == "backorder2")
    {
      backtoclient2 = true;
      ROS_INFO("I am toward the client2");
    }
  if(msg->data == "backtobar")
    {
      backtobar = true;
      ROS_INFO("I am toward the bar");
    }
}
void locationCallback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg)
{
  if(locationnum == 1)
    {
      bar_pose = msg->pose.pose;
      locationnum = 0;
    }
  if(locationnum == 2)
    {
      table1_pose = msg->pose.pose;
      locationnum = 0;
    }
  if(locationnum == 3)
    {
      table2_pose = msg->pose.pose;
      locationnum = 0;
    }
}

void imageCallback(const geometry_msgs::Point &point)
{
  if(receivePose)
    {
      receivePose = false;
      current_goal.position.x = point.x;
      current_goal.position.y = point.y;
      current_goal.orientation.w = 1;
      towardGoal = true;
    }
}
void imagestrCallback(const std_msgs::String::ConstPtr &msg)
{
  if(msg->data == "nextviewpoint")
    {
      ViewPoint++;
      if(ViewPoint < 4)
        towardViewPoint = true;
    }
}
// 激光和急停开关回调函数
void DigitalInputEventCallback(const kobuki_msgs::DigitalInputEvent::ConstPtr& msg)
{
  cout<<"DigitalInputEventCallback"<<endl;
  estop_in = msg->values[2];
  cout<<"msg value:"<<estop_in;
  if(estop_in)
    {
      kobuki_msgs::MotorPower offcmd;
      offcmd.state = kobuki_msgs::MotorPower::OFF;
      motor_power_pub.publish(offcmd);
      actionlib_msgs::GoalID cancelcmd;
      move_base_cancel_pub.publish(cancelcmd);
    }
};
