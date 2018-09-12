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
 #include "opencv2/objdetect/objdetect.hpp"  

 #include <iostream>  
 #include <stdio.h>  
#include <opencv2/core/core.hpp>   
#include <string>        
#include <sstream>    
using namespace cv;    
using namespace std;    
    
//Store all constants for image encodings in the enc namespace to be used later.      
namespace enc = sensor_msgs::image_encodings;      
void image_socket(Mat inImg);    
void detectAndDisplay( Mat frame );  
Mat image1;    
static int imgWidth, imgHeight;    
int objWidth=50;  
int objHeight=200;  
String face_cascade_name = "/home/kris/catkin_ws/src/imgpcl/src/haarcascade_frontalface_alt.xml";  
 String eyes_cascade_name = "/home/kris/catkin_ws/src/imgpcl/src/haarcascade_eye_tree_eyeglasses.xml";  
  CascadeClassifier face_cascade; 
 
 
 string window_name = "Capture - Face detection";  
 RNG rng(12345);  
//char *output_file = "/home/shuning/catkin_ws/src/rosopencv";    
    
//This function is called everytime a new image_info message is published    
void camInfoCallback(const sensor_msgs::CameraInfo & camInfoMsg)    
{    
  //Store the image width for calculation of angle    
  imgWidth = camInfoMsg.width;    
  imgHeight = camInfoMsg.height;    
}    
    
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
    image_socket(cv_ptr->image); 
    //detectAndDisplay(cv_ptr->image); 
    
}    

void detectAndDisplay( Mat frame )  
{  
  std::vector<Rect> faces;  
  Mat frame_gray;  
  
  cvtColor( frame, frame_gray, CV_BGR2GRAY );  
  equalizeHist( frame_gray, frame_gray );  
  
  //-- Detect faces  
  face_cascade.detectMultiScale( frame_gray, faces, 1.1, 3, 0|CV_HAAR_SCALE_IMAGE, Size(30, 30) );  
//   参数1：image--待检测图片，一般为灰度图像加快检测速度；

// 参数2：objects--被检测物体的矩形框向量组；
// 参数3：scaleFactor--表示在前后两次相继的扫描中，搜索窗口的比例系数。默认为1.1即每次搜索窗口依次扩大10%;
// 参数4：minNeighbors--表示构成检测目标的相邻矩形的最小个数(默认为3个)。
//         如果组成检测目标的小矩形的个数和小于 min_neighbors - 1 都会被排除。
//         如果min_neighbors 为 0, 则函数不做任何操作就返回所有的被检候选矩形框，
//         这种设定值一般用在用户自定义对检测结果的组合程序上；
// 参数5：flags--要么使用默认值，要么使用CV_HAAR_DO_CANNY_PRUNING，如果设置为

//         CV_HAAR_DO_CANNY_PRUNING，那么函数将会使用Canny边缘检测来排除边缘过多或过少的区域，

//         因此这些区域通常不会是人脸所在区域；
// 参数6、7：minSize和maxSize用来限制得到的目标区域的范围。
imshow( "face", frame );
  for( size_t i = 0; i < faces.size(); i++ )  
  {  
    ROS_INFO("--------!!!!!!!---------");  
    Point center( faces[i].x + faces[i].width*0.5, faces[i].y + faces[i].height*0.5 );  

    ellipse( frame, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 2, 8, 0 );  
  }  
  //-- Show what you got  
         waitKey(10);  
       
 }     

void image_socket(Mat inImg)    
{    

    if( inImg.empty() )    
    {    
      ROS_INFO("Camera image empty");    
      return;//break;    
    }  
          std::vector<Rect> faces;  
      Mat frame_gray; 
        cvtColor( inImg, frame_gray, CV_BGR2GRAY );  
       equalizeHist( frame_gray, frame_gray ); 
       face_cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, Size(30, 30) ); 
  for( size_t i = 0; i < faces.size(); i++ )  
  {  
    Point center( faces[i].x + faces[i].width*0.5, faces[i].y + faces[i].height*0.5 );  
    if(faces[i].width*faces[i].height>=3000){
      cout<<faces[i].width*faces[i].height<<"=====";
      //ellipse( inImg, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 2, 8, 0 );   
    }
  }
    

    //rectangle(inImg, Point(inImg.cols/2-objWidth/2-2,inImg.rows/2-objHeight/2-2),Point(inImg.cols/2+objWidth/2+2,inImg.rows/2+objHeight/2+2),Scalar(0,0,255), 1, 8 );  //画矩形    
    imshow("image_socket", inImg);//显示图片    
    stringstream sss;        
    string strs;    
    static int image_num = 1;    
    char c = (char)waitKey(1);    
    
    if( c == 27 )    
      ROS_INFO("Exit boss");//break;    
    switch(c)    
    {    
      case 'p':    
      //resize(inImg,image1,Size(imgWidth/6,imgHeight/6),0,0,CV_INTER_LINEAR);      
      //image1=inImg(Rect(inImg.cols/2-objWidth/2,inImg.rows/2-objHeight/2,objWidth,objHeight ));  
      for( size_t i = 0; i < faces.size(); i++ )  
  {  
    if(faces[i].width*faces[i].height>=3000)
     image1=inImg(Rect(faces[i].x,faces[i].y,faces[i].width,faces[i].height ));
  }  

      strs="/home/kris/catkin_ws/src/imgpcl/";    
      sss.clear();        
      sss<<strs;        
      sss<<image_num;       
      sss<<".jpg";        
      sss>>strs;        
      imwrite(strs,image1);//保存图片  
      cout<<image_num<<"images have saved!"<<endl;  
      image_num++;    
      break;    
  default:    
      break;    
  }    
    
}    
    
    
/** 
* This is ROS node to track the destination image 
*/    
int main(int argc, char **argv)    
{    
  face_cascade.load( face_cascade_name );
    ros::init(argc, argv, "image_socket");    
    ROS_INFO("-----------------");    
        
    ros::NodeHandle nh;    
    
    image_transport::ImageTransport it(nh);    
    
    image_transport::Subscriber sub = it.subscribe("camera/rgb/image_raw", 1, imageCallback);    
    ros::Subscriber camInfo         = nh.subscribe("camera/rgb/camera_info", 1, camInfoCallback);    
    
    ros::spin();    
    
    //ROS_INFO is the replacement for printf/cout.    
    ROS_INFO("tutorialROSOpenCV::main.cpp::No error.");    
}