/***********************************************************
Author: Zheng Haosi
Date: 3/30/2017
Abstract: Code for Help-me-carry task
************************************************************/
//标准头文件
#include<ros/ros.h>
#include<iostream>
#include<std_msgs/String.h>
#include<string.h>
//navigation中需要使用的位姿信息头文件
#include<geometry_msgs/Pose.h>
#include<geometry_msgs/Point.h>
#include<geometry_msgs/PoseWithCovariance.h>
#include<geometry_msgs/PoseWithCovarianceStamped.h>
#include<geometry_msgs/Twist.h>
#include<geometry_msgs/Quaternion.h>
#include <kobuki_msgs/DigitalInputEvent.h>
#include <kobuki_msgs/ButtonEvent.h>
//move_base头文件
#include<move_base_msgs/MoveBaseGoal.h>
#include<move_base_msgs/MoveBaseAction.h>
//actionlib头文件
#include<actionlib/client/simple_action_client.h>
#include <stdlib.h>
#include<cstdlib>
using namespace std;
//定义的全局变量
typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient; //简化类型书写为MoveBaseClient
bool go = false;
bool stop = false;
bool bfollow=true;    // 是否在跟人
bool bcarry=true;
bool bguide=false;   //是否开始引导人
int step=2;

geometry_msgs::Twist vel; //控制机器人速度
std_msgs::String sound_flag; //语音控制标志
std_msgs::String send_flag;
geometry_msgs::PoseWithCovariance  car_pose;
geometry_msgs::Pose goal_pose;//目标位置

//定义不同房间位置的坐标点
geometry_msgs::Pose livingroom;
geometry_msgs::Pose kitchen;
geometry_msgs::Pose bedroom;
geometry_msgs::Pose entrance;
geometry_msgs::Pose balcony;
geometry_msgs::Pose start;

ros::Publisher nav_pub;
ros::Publisher cmd_vel_pub;
ros::Publisher return_pub;


ros::Subscriber follow_sub;
ros::Subscriber car_sub;    //记住汽车位置
ros::Subscriber move_sub;
ros::Subscriber guide_sub;
ros::Subscriber button_sub;

void DigitalInputEventCallback(const kobuki_msgs::DigitalInputEvent::ConstPtr& msg);
void carlocationCallback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg);
void followCallback(const std_msgs::String::ConstPtr& msg);
void guideCallback(const std_msgs::String::ConstPtr& msg);

//语音控制“stop following me”
void followCallback(const std_msgs::String::ConstPtr& msg)
{
	if(msg->data == "follow_stop")
    {
		bfollow=false;
	}
}

void initplace()
{
  start.position.x = 1.8315198099;
  start.position.y = -2.70883212347;
  start.position.z = 0;
  start.orientation.x = 0;
  start.orientation.y = 0;
  start.orientation.z =  -0.993983728736;
  start.orientation.w = 0.10952783668;
  
  door.position.x = -4.49198569005;
  door.position.y = -1.70812927225;
  door.position.z = 0;
  door.orientation.x = 0;
  door.orientation.y = 0;
  door.orientation.z = -0.397227183417;
  door.orientation.w = 0.10952783668;
  
  livingroom.position.x = 4.61094318635;
  livingroom.position.y = -5.7900828837;
  livingroom.position.z = 0;
  livingroom.orientation.x = 0;
  livingroom.orientation.y = 0;
  livingroom.orientation.z =  -0.453356884826;
  livingroom.orientation.w = 0.891329083437;

  kitchen.position.x = 1.77283289516;
  kitchen.position.y = -4.05372810971;
  kitchen.position.z = 0;
  kitchen.orientation.x = 0;
  kitchen.orientation.y = 0;
  kitchen.orientation.z =  -0.636697410912;
  kitchen.orientation.w = 0.771113744487;

  bedroom.position.x = -2.21886371669;
  bedroom.position.y = -5.29413074921;
  bedroom.position.z = 0;
  bedroom.orientation.x = 0;
  bedroom.orientation.y = 0;
  bedroom.orientation.z = -0.650948613053;
  bedroom.orientation.w = 0.759121797319;

  entrance.position.x = -3.29376092612;
  entrance.position.y = -2.52392025721;
  entrance.position.z = 0;
  entrance.orientation.x = 0;
  entrance.orientation.y = 0;
  entrance.orientation.z = -0.379128067642;
  entrance.orientation.w = 0.925344210727;

  balcony.position.x = 2.98617397856;
  balcony.position.y = -1.49467780406;
  balcony.position.z = 0;
  balcony.orientation.x = 0;
  balcony.orientation.y = 0;
  balcony.orientation.z = 0.492294159753;
  balcony.orientation.w = 0.870428894438;
}

void carlocationCallback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg)
{
    //在停止follow的情况下，调用该回调函数
    if(bfollow==false)
    {
		car_pose=msg->pose;//定义此时AMCL中的汽车位置 ,car_pose.pose才是geometry_msgs::Pose类型
		send_flag.data = "grasp";
		nav_pub.publish(send_flag);

		cout<<"The robot has followed operator to the car location!"<<endl;
		cout<<"Ready to grasp the bag"<<endl;
		bfollow=true;
	}
}

//移动到目标点并返回汽车位置的回调函数,从语音话题 voice2bring
void moveCallback(const std_msgs::String::ConstPtr& msg)
{
  if(msg->data == "door")
    {
      goal_pose = door;
      go = true;
    }
  if(msg->data == "livingroom")
    {
      goal_pose = livingroom;
      go = true;
    }
  if(msg->data == "kitchen")
    {
      goal_pose = kitchen;
      go = true;
    }
  if(msg->data == "bedroom")
    {
      goal_pose = bedroom;
      go = true;
    }
  if(msg->data == "entrance")
    {
      goal_pose = entrance;
      go = true;
    }
  if(msg->data == "balcony")
    {
      goal_pose = balcony;
      go = true;
    }
  if(msg->data == "start")
    {
      goal_pose = start;
      go = true;
    }
}

void guideCallback(const std_msgs::String::ConstPtr& msg)
{
    if(msg->data == "instruction_over")
    {
		bguide=true;
		step=3;
	}
}
//主函数
int main(int argc, char** argv)
{
	ros::init(argc, argv, "navi_demo");
	ros::NodeHandle myNode;
	cout<<"Welcome to Help-me-carry!"<<endl;

  initplace();

	return_pub= myNode.advertise<std_msgs::String>("nav2speech", 1);
	nav_pub = myNode.advertise<std_msgs::String>("nav2image", 10);

	ros::Subscriber car_sub = myNode.subscribe("/amcl_pose", 100, carlocationCallback);//订阅amcl包中的amcl_pose话题
	ros::Subscriber follow_sub = myNode.subscribe("/ifFollowme", 1, followCallback);
	ros::Subscriber move_sub = myNode.subscribe("/voice2bring", 1, moveCallback);
	ros::Subscriber guide_sub = myNode.subscribe("/voice2guide", 1, guideCallback);

	MoveBaseClient  mc_("move_base", true); //建立导航客户端
	move_base_msgs::MoveBaseGoal naviGoal; //导航目标点
	while(ros::ok())
	{
		if((go==true)  && (stop==false))
		{
			if(step==1)
			{

				if(bcarry)
				{
					naviGoal.target_pose.header.frame_id = "map";
					naviGoal.target_pose.header.stamp = ros::Time::now();
					naviGoal.target_pose.pose = geometry_msgs::Pose(door);

					while(!mc_.waitForServer(ros::Duration(5.0)))
					{
						//等待服务初始化
						cout<<"Waiting for the server..."<<endl;
					}
					mc_.sendGoal(naviGoal);
					mc_.waitForResult(ros::Duration(20.0));

					if(mc_.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
					{
						cout<<"Move to the gate....";
						step=2;
					}
				}
			}
			if(step==2)
			{

				//naviGoal.target_pose.header.frame_id = "map";
				if(bcarry)
				{
					naviGoal.target_pose.header.frame_id = "map";
					naviGoal.target_pose.header.stamp = ros::Time::now();
					naviGoal.target_pose.pose = geometry_msgs::Pose(goal_pose);

					while(!mc_.waitForServer(ros::Duration(5.0)))
					{
						//等待服务初始化
						cout<<"Waiting for the server..."<<endl;
					}
					mc_.sendGoal(naviGoal);
					mc_.waitForResult(ros::Duration(20.0));

					//导航反馈直至到达目标点
					if(mc_.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
					{
						cout<<"Yes! The robot has moved to the goal,ready to realse the grocery!"<<endl;
						send_flag.data = "release";
						nav_pub.publish(send_flag);
						cout<<"I have sent the release signal to arm!"<<endl;

						bcarry=false;
						//sleep(15);

					}
				}
			}
			if(bguide==true)
			{
				if(step==3)
				{
					cout<<"Returning ... "<<endl;
					naviGoal.target_pose.header.frame_id = "map";
					naviGoal.target_pose.header.stamp = ros::Time::now();
					naviGoal.target_pose.pose = geometry_msgs::Pose(door);
					while(!mc_.waitForServer(ros::Duration(5.0)))
					{
						//等待服务初始化
						cout<<"Waiting for the server..."<<endl;
					}
					mc_.sendGoal(naviGoal);
					mc_.waitForResult(ros::Duration(20.0));

					if(mc_.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
					{
						std_msgs::String door_flag;
						door_flag.data = "open_door";
						return_pub.publish(door_flag);
						sleep(15);
						naviGoal.target_pose.header.frame_id = "map";
						naviGoal.target_pose.header.stamp = ros::Time::now();
						naviGoal.target_pose.pose = geometry_msgs::Pose(car_pose.pose);
						while(!mc_.waitForServer(ros::Duration(5.0)))
						{
							//等待服务初始化
							cout<<"Waiting for the server..."<<endl;
						}
						mc_.sendGoal(naviGoal);
						mc_.waitForResult(ros::Duration(20.0));

						if(mc_.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
						{
							sound_flag.data = "arrived";
							return_pub.publish(sound_flag);
							cout<<"Yes! The robot has come back to the car!"<<endl;
							go=false;
						}

					}
				}
			}
		}
		ros::spinOnce();
	}
	return 0;
}
};
