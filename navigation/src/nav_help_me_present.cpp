#include<ros/ros.h>
#include<iostream>
#include<std_msgs/String.h>
#include<string.h>

#include<geometry_msgs/Pose.h>
#include<geometry_msgs/PoseWithCovariance.h>
#include<geometry_msgs/PoseWithCovarianceStamped.h>
#include<geometry_msgs/Twist.h>
#include<geometry_msgs/Quaternion.h>

#include<move_base_msgs/MoveBaseGoal.h>
#include<move_base_msgs/MoveBaseAction.h>

#include<actionlib/client/simple_action_client.h>
#include <stdlib.h>
#include<cstdlib>
using namespace std;

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;
bool go = false;
bool follow=true;    // 是否在跟人
bool bcarry=true;
int step=0;

std_msgs::String sound_flag; //语音控制标志
std_msgs::String send_flag;
geometry_msgs::PoseWithCovariance  car_pose;
geometry_msgs::Pose goal_pose;//目标位置

//定义不同房间位置的坐标点
geometry_msgs::Pose start;
geometry_msgs::Pose livingroom;
geometry_msgs::Pose kitchen;
geometry_msgs::Pose bedroom;
geometry_msgs::Pose entrance;
geometry_msgs::Pose balcony;

ros::Publisher nav_pub;
ros::Publisher cmd_vel_pub;
ros::Publisher return_pub;

ros::Subscriber follow_sub;
ros::Subscriber car_sub;    //记住汽车位置
ros::Subscriber move_sub;
ros::Subscriber guide_sub;

void carlocationCallback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg);
void followCallback(const std_msgs::String::ConstPtr& msg);
void guideCallback(const std_msgs::String::ConstPtr& msg);

void followCallback(const std_msgs::String::ConstPtr& msg)
{
  if(msg->data == "follow_stop")
    {
      follow=false;
    }
}

void carlocationCallback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg)
{
  //在停止follow的情况下，调用该回调函数
  if(follow==false)
    {
      car_pose=msg->pose;
      send_flag.data = "grasp";
      nav_pub.publish(send_flag);

      cout<<"The robot has followed operator to the car location!"<<endl;
      cout<<"Ready to grasp the bag"<<endl;
      follow=true;
    }
}

//移动到目标点并返回汽车位置的回调函数,从语音话题 voice2bring
void moveCallback(const std_msgs::String::ConstPtr& msg)
{
  if(msg->data == "livingroom")
    {
      goal_pose = livingroom;
    }
  if(msg->data == "kitchen")
    {
      goal_pose = kitchen;
    }
  if(msg->data == "bedroom")
    {
      goal_pose = bedroom;
    }
  if(msg->data == "entrance")
    {
      goal_pose = entrance;
    }
  if(msg->data == "balcony")
    {
      goal_pose = balcony;
    }
  if(msg->data == "start")
    {
      goal_pose = start;
    }
  go = true;
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
  
  livingroom.position.x = 4.61094318635;
  livingroom.position.y = -5.7900828837;
  livingroom.position.z = 0;
  livingroom.orientation.x = 0;
  livingroom.orientation.y = 0;
  livingroom.orientation.z =  -0.453356884826;
  livingroom.orientation.w = 0.891329083437;

  kitchen.position.x = 1.79688547929;
  kitchen.position.y = -4.10143858799;
  kitchen.position.z = 0;
  kitchen.orientation.x = 0;
  kitchen.orientation.y = 0;
  kitchen.orientation.z =  -0.626843106691;
  kitchen.orientation.w = 0.779145506047;

  bedroom.position.x = -2.17600159314;
  bedroom.position.y = -5.16267245955;
  bedroom.position.z = 0;
  bedroom.orientation.x = 0;
  bedroom.orientation.y = 0;
  bedroom.orientation.z = -0.643078494121;
  bedroom.orientation.w = 0.765800267954;

  entrance.position.x = -3.29158934257;
  entrance.position.y = -2.38559560347;
  entrance.position.z = 0;
  entrance.orientation.x = 0;
  entrance.orientation.y = 0;
  entrance.orientation.z = -0.343712794037;
  entrance.orientation.w = 0.939074818753;

  balcony.position.x = 5.86481434825;
  balcony.position.y = 1.15879049876;
  balcony.position.z = 0;
  balcony.orientation.x = 0;
  balcony.orientation.y = 0;
  balcony.orientation.z = -0.599652156702;
  balcony.orientation.w = 0.800260764353;
}

void guideCallback(const std_msgs::String::ConstPtr& msg)
{
  if(msg->data == "instruction_over")
    {
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
  nav_pub = myNode.advertise<std_msgs::String>("nav2image", 1);

  ros::Subscriber car_sub = myNode.subscribe("/amcl_pose", 100, carlocationCallback);
  ros::Subscriber follow_sub = myNode.subscribe("/ifFollowme", 1, followCallback);
  ros::Subscriber move_sub = myNode.subscribe("/voice2bring", 1, moveCallback);
  ros::Subscriber guide_sub = myNode.subscribe("/voice2guide", 1, guideCallback);

  MoveBaseClient  mc_("move_base", true);
  move_base_msgs::MoveBaseGoal naviGoal;
  while(ros::ok())
    {
      if(go==true)
        {
          if(step==1){
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


            if(mc_.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
              {
                cout<<"Move to the gate....";
              }
            step = 0;
          }
          if(step==2){

            //naviGoal.target_pose.header.frame_id = "map";
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
                cout<<"Yes! The robot has moved to the goal,ready to release the grocery!"<<endl;
                std_msgs::String send;
                send_flag.data = "release";
                nav_pub.publish(send_flag);
                cout<<"I have sent the release signal to arm!"<<endl;

              }
            step = 0;
          }
	    }
      ros::spinOnce();
    }
  return 0;
}
