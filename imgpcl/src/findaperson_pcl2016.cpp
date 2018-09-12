//Includes all the headers necessary to use the most common public pieces of the ROS system.    
#include <ros/ros.h>    
//Use image_transport for publishing and subscribing to images in ROS    
#include <image_transport/image_transport.h>    
//Use cv_bridge to convert between ROS and OpenCV Image formats    
#include <cv_bridge/cv_bridge.h>    

#include <sensor_msgs/image_encodings.h>    
//Include headers for OpenCV Image processing    
#include <opencv2/imgproc/imgproc.hpp>    
//Include headers for OpenCV GUI handling    
#include <opencv2/highgui/highgui.hpp>    
#include <string>        
#include <sstream>    
#include <stdio.h>
#include "imgpcl/auto_tchar.h"
#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <math.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Twist.h>
#include <vector>
#include <stdlib.h>
#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <imgpcl/pos.h>
#include <std_msgs/Int32.h> 
#include <std_msgs/String.h>
#include <geometry_msgs/Twist.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/ml/ml.hpp>
#include <opencv/cv.h>
//write txt
#include <fstream>  
#include <vector>
#include <float.h>//isnan 
//pcl
#include <sensor_msgs/PointCloud2.h>  
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl_ros/point_cloud.h>
#include <boost/foreach.hpp>
#include <pcl/visualization/cloud_viewer.h>
#include <pcl/io/io.h>
#include <pcl/io/pcd_io.h>
// time synchronize
#include <message_filters/subscriber.h>
#include <message_filters/time_synchronizer.h>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/CameraInfo.h>
#include <message_filters/sync_policies/approximate_time.h>
#include <ros/callback_queue.h>
#include <boost/bind.hpp>
#include <time.h>
#include "imgpcl/objdetect_test.hpp"
#include <std_msgs/UInt8.h>
using namespace std;
using namespace message_filters;
using namespace sensor_msgs;

typedef pcl::PointCloud<pcl::PointXYZRGBA> PointCloud;
typedef boost::shared_ptr<PointCloud> PointCloudPtr;
typedef boost::shared_ptr<const PointCloud> PointCloudConstPtr;
//实现时间同步性
typedef message_filters::sync_policies::ApproximateTime<sensor_msgs::Image, sensor_msgs::PointCloud2> MySyncPolicy;
typedef message_filters::sync_policies::ApproximateTime<sensor_msgs::Image, sensor_msgs::Image> MySyncPolicy2;
int system(const char *string); 
using namespace cv;    
using namespace std;    

//Store all constants for image encodings in the enc namespace to be used later.      
namespace enc = sensor_msgs::image_encodings; 
struct PathPoint
{
    int state;
    float vel;
    float time;
};
vector<PathPoint> vppt;             //储存反馈调节时的调节参数
void image_process(Mat inImg, pcl::PointCloud<pcl::PointXYZ> points_xyz); 
void spCallback(const std_msgs::String::ConstPtr& msg); 
void forward_robot(float x);
void turn_robot(float theta);
/// 全局变量

const char* window_name = "Find Person";
String face_cascade_name = "/home/isi/2017_ws/src/imgpcl/haarcascade_frontalface_alt.xml";  
//String eyes_cascade_name = "/home/isi/2017_ws/src/imgpcl/haarcascade_eye_tree_eyeglasses.xml";  
CascadeClassifier face_cascade;

ros::Publisher move_pub;            //向navigation发消息，微调机器人
ros::Publisher if_found_Pub;   //检测到物体的数量
ros::Publisher image2voice_Pub;  
 
std_msgs::String img2voiceP;
//ros::Publisher if;   
std_msgs::String if_found_P;
int state = -1;
//This function is called everytime a new image is published    
void Callback(const sensor_msgs::ImageConstPtr& original_image, const PointCloud2::ConstPtr& Callback_Points)    
{    
    //Convert from the ROS image message to a CvImage suitable for working with OpenCV for processing    
    cv_bridge::CvImagePtr cv_ptr;      
    try      
    {      
        //Always copy, returning a mutable CvImage      
        //OpenCV expects color images to use BGR channel order.      
        cv_ptr = cv_bridge::toCvCopy(original_image, enc::BGR8);      
    }      
    catch (cv_bridge::Exception& e) 
    {      
        //if there is an error during conversion, display it      
        ROS_ERROR("tutorialROSOpenCV::main.cpp::cv_bridge exception: %s", e.what());      
        return;
    }
    Mat img_color = cv_ptr->image;
    	//---------------获得点云数据------------------//
    pcl::PointCloud<pcl::PointXYZ> points_xyz;
    pcl::fromROSMsg (*Callback_Points, points_xyz);
    
    image_process(img_color, points_xyz);    
}
void image_process(Mat inImg, pcl::PointCloud<pcl::PointXYZ> points_xyz)    
{   

    if(state == -1 || state == 2)
        return;
    if( inImg.empty() )    
    {    
        ROS_INFO("Camera image empty");    
        return;//break;    
    } 
    if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading\n"); };  
    //if( !eyes_cascade.load( eyes_cascade_name ) ){ printf("--(!)Error loading\n"); };
    std::vector<Rect> faces;  
    Mat inImg_gray;
    cvtColor( inImg, inImg_gray, CV_BGR2GRAY );  
    equalizeHist( inImg_gray, inImg_gray );  
    //-- Detect faces  
    face_cascade.detectMultiScale( inImg_gray, faces, 1.1, 3, 0|CV_HAAR_SCALE_IMAGE, Size(30, 30) );  
    int human_num = faces.size();
    cout<<"human_num:"<<human_num<<endl;
    if(human_num == 0)
    {
        img2voiceP.data = "I find no people, I am finding";
        image2voice_Pub.publish(img2voiceP);//发送此时检测到的物体数量
        turn_robot(1.5);
        return;
    }
    if(human_num > 1)
    {
        img2voiceP.data = "There is more than one people!";
        image2voice_Pub.publish(img2voiceP);//发送此时检测到的物体数量 
        //return;
        return;
    }
    if(human_num == 1)
    {  
        Mat face = inImg_gray( faces[0] ); 
        rectangle(inImg,faces[0],Scalar(0,255,0),1);
        imgpcl::pos p;  
   	    //二维坐标转换为三维坐标，p为物体关于摄像头的坐标
   	    bool isfind_pcl = ComputeClusterCenter(points_xyz, faces[0], p);
        ROS_INFO("p: %f %f %f\n", p.x, p.y, p.z);
        if(!isfind_pcl)
        {
            ROS_INFO("NO PCL!!\n");
            return;
        }
        if(p.z > 2.5)
        {
            ROS_INFO("person too faraway!!\n");
            //state = 0;
            turn_robot(1.5);
            return;
        }
        int pos_x = 0;
        int pos_y = 0;
        pos_x = faces[0].x + faces[0].width ;
        pos_y = faces[0].y + faces[0].height;
        cout<<"pos_x"<<pos_x<<endl;
        cout<<"pos_y"<<pos_y<<endl;
        if(pos_x - 320 > 80)
            turn_robot(-0.8);
        if(pos_x - 320 < -80)
            turn_robot(0.8);
        if(pos_y > 110)
            forward_robot(0.2);
        if(abs(pos_x - 320) < 80 && pos_y < 110)
        {
            img2voiceP.data = "I have reached the person!";
            image2voice_Pub.publish(img2voiceP); 
            if_found_P.data = "found_person";
            if_found_Pub.publish(if_found_P);           
            state = 2;
        }
        //imwrite("/home/isi/2017_ws/src/imgpcl/person.jpg",frame);//保存图片    
        imshow( window_name, inImg );
        waitKey(5);
        //return true; 
    }
} 
void turn_robot(float theta)
{
    geometry_msgs::Twist vel;
    int count = 0;
    float time = 2;
    ros::Rate loop_rate(10);
    int num = time*10;
    PathPoint pt;
    //转90度
    //float theta = 5;
	//cout<<"theta:"<<theta<<endl;
	float theta2 = theta/time;
	vel.angular.z = theta2;    
    count = 0;
    num = time*10;
    while(count < num)
    {
        count++;
        move_pub.publish(vel);
        loop_rate.sleep();
    }
    pt.state = 0;
    pt.time = time;
    pt.vel = vel.angular.z;
    vppt.push_back(pt);
    vel.angular.z = 0.0;
    move_pub.publish(vel);
    cout<<"转弯\n";
    sleep(1);
}
void forward_robot(float x)
{
    geometry_msgs::Twist vel;
    int count = 0;
    float time = 3;
    vel.linear.x = x/time; 
    ros::Rate loop_rate(10);
    int num = time*10;
    //cout<<"armCallback1()\n";
    while(count < num)
    {
        count++;
        move_pub.publish(vel);
        loop_rate.sleep();
    }
    PathPoint pt;
    pt.state = 0;
    pt.time = time;
    pt.vel = vel.linear.x;
    vppt.push_back(pt);
    vel.linear.x = 0.0;
    move_pub.publish(vel);
    cout<<"直行\n";
    sleep(1);
}
void navCallback(const std_msgs::String::ConstPtr& msg)
{
	//cout<<"navCallback()\n";
    ROS_INFO("navCallback received: %s\n", msg->data.c_str());
    if(msg->data == "find_person")   //接受到navigation的消息，开始检测
    {
        state = 0;
    }
}   
/** 
* This is ROS node to track the destination image 
*/    
int main(int argc, char **argv)    
{    
    ros::init(argc, argv, "");    
    ROS_INFO("-----------------");
    ros::NodeHandle nh;
    move_pub = nh.advertise<geometry_msgs::Twist>("cmd_vel_mux/input/navi",1);  //移动
    if_found_Pub = nh.advertise<std_msgs::String>("found_person", 1);
    image2voice_Pub = nh.advertise<std_msgs::String>("img2voice", 1);
    image_transport::ImageTransport it(nh); 
   // image_transport::Subscriber sub = it.subscribe("camera1/rgb/image_raw", 1, imageCallback);
    int global_subscriber_queue_size = 1; 
    message_filters::Subscriber<sensor_msgs::Image> visual_sub_ (nh, "/camera1/rgb/image_raw", global_subscriber_queue_size);
    message_filters::Subscriber<sensor_msgs::PointCloud2> cloud_sub_(nh, "/camera1/depth/points", global_subscriber_queue_size);   
    message_filters::Synchronizer<MySyncPolicy> sync_(MySyncPolicy(1),  visual_sub_, cloud_sub_);
    sync_.registerCallback(boost::bind(&Callback, _1, _2));   
   // ros::Subscriber camInfo         = nh.subscribe("camera/rgb/camera_info", 1, camInfoCallback);    
    ros::Subscriber nav_sub = nh.subscribe("/nav2image", 1, navCallback);        //订阅navigation的消息
    ros::spin();
    //ROS_INFO is the replacement for printf/cout.    
    ROS_INFO("main_No error.");  
}
