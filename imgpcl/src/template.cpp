#include <ros/ros.h>    
#include <image_transport/image_transport.h>    
#include <cv_bridge/cv_bridge.h>    
#include <sensor_msgs/image_encodings.h>    
#include <opencv2/imgproc/imgproc.hpp>    
    #include <opencv2/core/core.hpp>          
          
    #include <opencv2/opencv.hpp>        
     
    #include <iostream>        
    #include<string>        
    #include <sstream>      
#include <opencv2/highgui/highgui.hpp>    
#include "opencv2/video/tracking.hpp"    
#include <geometry_msgs/Twist.h>    
#include <std_msgs/Float32.h>    
#include <std_msgs/UInt8.h>    
  
using namespace cv;    
using namespace std;    
  
//Store all constants for image encodings in the enc namespace to be used later.    
namespace enc = sensor_msgs::image_encodings;    
  
stringstream sss;        
static string ImgInfo="/home/isi/2017_ws/src/imgpcl/template/PotatoChips.jpg";//如果用语音把1.jpg去掉  
void MTemplate(Mat src);  
/////////////////////////////////////////////////////从语音获取图像的名字。  
/*void imgInfoCallback(const std_msgs::String::ConstPtr & msg)   
{   
    ROS_INFO("From SPEECH, I heard: [%s]",msg->data.c_str());   
    sss.clear();       
    sss<<ImgInfo;       
    sss<<msg->data.c_str();       
    sss<<".jpg";       
    sss>>ImgInfo;   
  
} */  
//This function is called everytime a new image is published    
void imageCallback(const sensor_msgs::ImageConstPtr& original_image)    
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
    MTemplate(cv_ptr->image);    
}    
  
void MTemplate(Mat src)  
{  
    Mat templ;      
    Mat result;    
    int match_method=0;    
    templ=imread(ImgInfo,1);   
        int result_cols =  src.cols - templ.cols + 1;    
        int result_rows = src.rows - templ.rows + 1;    
    
        result.create( result_cols, result_rows, CV_32FC1 );    
    
        matchTemplate( src, templ, result, match_method );    
        normalize( result, result, 0, 1, NORM_MINMAX, -1, Mat() );    
    
        /// 通过函数 minMaxLoc 定位最匹配的位置    
        double minVal; double maxVal; Point minLoc; Point maxLoc;    
        Point matchLoc;    
    
        minMaxLoc( result, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );    
    
        /// 对于方法 SQDIFF 和 SQDIFF_NORMED, 越小的数值代表更高的匹配结果. 而对于其他方法, 数值越大匹配越好    
        if( match_method  == CV_TM_SQDIFF || match_method == CV_TM_SQDIFF_NORMED )    
        {   
            matchLoc = minLoc;   
        }    
        else    
        {  
           matchLoc = maxLoc;   
        }    
    
        /// 最终结果    
        rectangle( src, matchLoc, Point( matchLoc.x + templ.cols , matchLoc.y + templ.rows ), Scalar::all(0), 2, 8, 0 );    
     //   rectangle( result, matchLoc, Point( matchLoc.x + templ.cols , matchLoc.y + templ.rows ), Scalar::all(0), 2, 8, 0 );    
        cout<<"目标的中心坐标 ( "<<matchLoc.x + templ.cols/2<<" , ("<<matchLoc.y + templ.rows<<" )"<<endl;    
        imshow("当前视频",src);   
        imshow("视频",result);   
         waitKey(1);  
}  
  
/**  
* This is ROS node to track the destination image  
*/    
int main(int argc, char **argv)    
{    
  
ros::init(argc, argv, "image_processor");    
ROS_INFO("-----------------");    
  
ros::NodeHandle nh;    
//Create an ImageTransport instance, initializing it with our NodeHandle.    
image_transport::ImageTransport it(nh);    
  
//OpenCV HighGUI call to create a display window on start-up.    
  
namedWindow( "CamShift Demo", 0 );    
  
  
image_transport::Subscriber sub = it.subscribe("camera/rgb/image_raw", 1, imageCallback);  
///////////////////////////////////////////////////////////////////////////////  
//ros::Subscriber imgInfo         = nh.subscribe("final_recognizer_begin", 1, imgInfoCallback);//接收来自语音部分的话题    
   
destroyWindow("CamShift Demo");    
  
  
/**  
* In this application all user callbacks will be called from within the ros::spin() call.  
* ros::spin() will not return until the node has been shutdown, either through a call  
* to ros::shutdown() or a Ctrl-C.  
*/    
ros::spin();    
  
//ROS_INFO is the replacement for printf/cout.    
ROS_INFO("tutorialROSOpenCV::main.cpp::No error.");    
}
