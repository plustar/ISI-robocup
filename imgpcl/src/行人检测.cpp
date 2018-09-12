
///////////////////////////////////////////////////////////////////////////////////seconde example--people dection from pic
#include <iostream>
#include <opencv2/opencv.hpp>


int main(int argc, char** argv)
{
  cv::Mat image = cv::imread("/home/kris/catkin_ws/src/imgpcl/src/pedestrian_377.bmp");
  if (image.empty())
  {
    std::cout << "read image failed" << std::endl;
  }


  // 1. ¶¨ÒåHOG¶ÔÏó
  cv::HOGDescriptor hog; // ²ÉÓÃÄ¬ÈÏ²ÎÊý

  // 2. ÉèÖÃSVM·ÖÀàÆ÷
  hog.setSVMDetector(cv::HOGDescriptor::getDefaultPeopleDetector());   // ²ÉÓÃÒÑ¾­ÑµÁ·ºÃµÄÐÐÈË¼ì²â·ÖÀàÆ÷

  // 3. ÔÚ²âÊÔÍ¼ÏñÉÏ¼ì²âÐÐÈËÇøÓò
  std::vector<cv::Rect> regions, found_filtered;
  hog.detectMultiScale(image, regions, 0.1, cv::Size(4, 4), cv::Size(0, 0), 1.05, 1);

  size_t i, j;
  for (i = 0; i < regions.size(); i++)
  {
    cv::Rect r = regions[i];

    //ÏÂÃæµÄÕâ¸öforÓï¾äÊÇÕÒ³öËùÓÐÃ»ÓÐÇ¶Ì×µÄ¾ØÐÎ¿òr,²¢·ÅÈëfound_filteredÖÐ,Èç¹ûÓÐÇ¶Ì×µÄ
    //»°,ÔòÈ¡ÍâÃæ×î´óµÄÄÇ¸ö¾ØÐÎ¿ò·ÅÈëfound_filteredÖÐ
    for (j = 0; j <regions.size(); j++)
    if (j != i && (r&regions[j]) == r)
      break;
    if (j == regions.size())
      found_filtered.push_back(r);
  }

  //ÔÚÍ¼Æ¬imgÉÏ»­³ö¾ØÐÎ¿ò,ÒòÎªhog¼ì²â³öµÄ¾ØÐÎ¿ò±ÈÊµ¼ÊÈËÌå¿òÒªÉÔÎ¢´óÐ©,ËùÒÔÕâÀïÐèÒª
  //×öÒ»Ð©µ÷Õû
  for (i = 0; i <found_filtered.size(); i++)
  {
    cv::Rect r = found_filtered[i];
    r.x += cvRound(r.width*0.1);
    r.width = cvRound(r.width*0.8);
    r.y += cvRound(r.height*0.07);
    r.height = cvRound(r.height*0.8);
    rectangle(image, r.tl(), r.br(), cv::Scalar(255, 0, 0), 3);
  }


  // ÏÔÊ¾
  //for (size_t i = 0; i < regions.size(); i++)
  //{
  //  cv::rectangle(image, regions[i], cv::Scalar(0, 0, 255), 2);
  //}

  cv::imshow("hog", image);
  cv::waitKey(0);

  return 0;
}
// ///////////////////////////////////////////////////////////////////////////////third example -face dection from camera
//  #include "opencv2/objdetect/objdetect.hpp"  
//  #include "opencv2/highgui/highgui.hpp"  
//  #include "opencv2/imgproc/imgproc.hpp"  
  
//  #include <iostream>  
//  #include <stdio.h>  
// #include <opencv2/core/core.hpp>   
//  using namespace std;  
//  using namespace cv;  
  
//  // Function Headers   
//  void detectAndDisplay( Mat frame );  
  
//  // Global variables   
//  String face_cascade_name = "/home/kris/catkin_ws/src/imgpcl/src/haarcascade_frontalface_alt.xml";  
//  String eyes_cascade_name = "/home/kris/catkin_ws/src/imgpcl/src/haarcascade_eye_tree_eyeglasses.xml";  
//  CascadeClassifier face_cascade;  
//  CascadeClassifier eyes_cascade;  
//  string window_name = "Capture - Face detection";  
//  RNG rng(12345);  
  
//  // @function main   
//  int main( int argc, const char** argv )  
//  {  
  
//   // CvCapture* capture;  
//    Mat frame;  
  
//    //-- 1. Load the cascades  
//    if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };  
//    if( !eyes_cascade.load( eyes_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };  
  
//    //-- 2. Read the video stream  
//    CvCapture* capture=cvCaptureFromCAM(0);  
//    //capture = cvCaptureFromCAM( -1 );  
//    if( capture )  
//    {  
//      while( true )  
//      {  
//    frame = cvQueryFrame( capture );  
  
//    //-- 3. Apply the classifier to the frame  
//        if( !frame.empty() )  
//        { detectAndDisplay( frame ); }  
//        else  
//        { printf(" --(!) No captured frame -- Break!"); break; }  
  
//        int c = waitKey(10);  
//        if( (char)c == 'c' ) { break; }  
//       }  
//    }  
//    return 0;  
//  }  
  
// // @function detectAndDisplay   
// void detectAndDisplay( Mat frame )  
// {  
//   std::vector<Rect> faces;  
//   Mat frame_gray;  
  
//   cvtColor( frame, frame_gray, CV_BGR2GRAY );  
//   equalizeHist( frame_gray, frame_gray );  
  
//   //-- Detect faces  
//   face_cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, Size(30, 30) );  
  
//   for( size_t i = 0; i < faces.size(); i++ )  
//   {  
//     Point center( faces[i].x + faces[i].width*0.5, faces[i].y + faces[i].height*0.5 );  
//     ellipse( frame, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 2, 8, 0 );  
  
//     Mat faceROI = frame_gray( faces[i] );  
//     std::vector<Rect> eyes;  
  
//     //-- In each face, detect eyes  
//     eyes_cascade.detectMultiScale( faceROI, eyes, 1.1, 2, 0 |CV_HAAR_SCALE_IMAGE, Size(30, 30) );  
  
//     for( size_t j = 0; j < eyes.size(); j++ )  
//      {  
//        Point center( faces[i].x + eyes[j].x + eyes[j].width*0.5, faces[i].y + eyes[j].y + eyes[j].height*0.5 );  
//        int radius = cvRound( (eyes[j].width + eyes[j].height)*0.25 );  
//        circle( frame, center, radius, Scalar( 255, 0, 0 ), 4, 8, 0 );  
//      }  
//   }  
//   //-- Show what you got  
//   imshow( window_name, frame );  
//  } 
/*///////////////////////////////////////////////////////////////////////////////////fourth example--people dection from pic & publish topic
#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>
#include <iostream>
#include <opencv2/opencv.hpp>
    

int main(int argc, char** argv)
{

  cv::Mat image = cv::imread("/home/kris/catkin_ws/src/imgpcl/src/10.jpg");
  if (image.empty())
  {
    std::cout << "read image failed" << std::endl;
  }


  // 1. ¶¨ÒåHOG¶ÔÏó
  cv::HOGDescriptor hog; // ²ÉÓÃÄ¬ÈÏ²ÎÊý

  // 2. ÉèÖÃSVM·ÖÀàÆ÷
  hog.setSVMDetector(cv::HOGDescriptor::getDefaultPeopleDetector());   // ²ÉÓÃÒÑ¾­ÑµÁ·ºÃµÄÐÐÈË¼ì²â·ÖÀàÆ÷

  // 3. ÔÚ²âÊÔÍ¼ÏñÉÏ¼ì²âÐÐÈËÇøÓò
  std::vector<cv::Rect> regions, found_filtered;
  hog.detectMultiScale(image, regions, 0, cv::Size(8, 8), cv::Size(32, 32), 1.05, 1);

  size_t i, j;
  for (i = 0; i < regions.size(); i++)
  {
    cv::Rect r = regions[i];

    //ÏÂÃæµÄÕâ¸öforÓï¾äÊÇÕÒ³öËùÓÐÃ»ÓÐÇ¶Ì×µÄ¾ØÐÎ¿òr,²¢·ÅÈëfound_filteredÖÐ,Èç¹ûÓÐÇ¶Ì×µÄ
    //»°,ÔòÈ¡ÍâÃæ×î´óµÄÄÇ¸ö¾ØÐÎ¿ò·ÅÈëfound_filteredÖÐ
    for (j = 0; j <regions.size(); j++)
    if (j != i && (r&regions[j]) == r)
      break;
    if (j == regions.size())
      found_filtered.push_back(r);
  }

  //ÔÚÍ¼Æ¬imgÉÏ»­³ö¾ØÐÎ¿ò,ÒòÎªhog¼ì²â³öµÄ¾ØÐÎ¿ò±ÈÊµ¼ÊÈËÌå¿òÒªÉÔÎ¢´óÐ©,ËùÒÔÕâÀïÐèÒª
  //×öÒ»Ð©µ÷Õû
  for (i = 0; i <found_filtered.size(); i++)
  {
    cv::Rect r = found_filtered[i];
    r.x += cvRound(r.width*0.1);
    r.width = cvRound(r.width*0.8);
    r.y += cvRound(r.height*0.07);
    r.height = cvRound(r.height*0.8);
    rectangle(image, r.tl(), r.br(), cv::Scalar(0, 255, 0), 3);
  }
  ros::init(argc, argv, "talker");
  ros::NodeHandle n;
  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
  ros::Rate loop_rate(10);
  int count = 0;  
  while (ros::ok())
  {
    std_msgs::String msg;
    std::stringstream ss; 
    ss << "people number : " <<found_filtered.size();
    msg.data = ss.str();
    ROS_INFO("%s", msg.data.c_str());
    chatter_pub.publish(msg);
    ros::spinOnce();
    loop_rate.sleep();
    ++count;
  }

  // ÏÔÊ¾
  //for (size_t i = 0; i < regions.size(); i++)
  //{
  //  cv::rectangle(image, regions[i], cv::Scalar(0, 0, 255), 2);
  //}

  cv::imshow("hog", image);
  cv::waitKey(0);

  return 0;
}*/
////////////////////////////////////////////////////////////////////////////// third example  ----face dection from pic
/*#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
 #include "opencv2/objdetect/objdetect.hpp"  
 #include <opencv2/core/core.hpp> 
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

 using namespace std;  
using namespace cv;
void detectAndDisplay( Mat frame ); 
/// 全局变量
Mat src, dst, tmp;
char* window_name = "Pyramids Demo";
 String face_cascade_name = "/home/kris/catkin_ws/src/imgpcl/src/haarcascade_frontalface_alt.xml";  
 String eyes_cascade_name = "/home/kris/catkin_ws/src/imgpcl/src/haarcascade_eye_tree_eyeglasses.xml";  
 CascadeClassifier face_cascade;  
 CascadeClassifier eyes_cascade;  
 //string window_name = "Capture - Face detection";  
 RNG rng(12345);  

int main( int argc, char** argv )
{
   if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };  
   if( !eyes_cascade.load( eyes_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };  
  /// 指示说明
  printf( "\n Zoom In-Out demo  \n " );
  printf( "------------------ \n" );
  printf( " * [u] -> Zoom in  \n" );
  printf( " * [d] -> Zoom out \n" );
  printf( " * [ESC] -> Close program \n \n" );

  /// 测试图像 - 尺寸必须能被 2^{n} 整除
  src = imread( "/home/kris/catkin_ws/src/imgpcl/src/5.jpg" );
  if( !src.data )
    { printf(" No data! -- Exiting the program \n");
      return -1; }

  tmp = src;
  dst = tmp;

  /// 创建显示窗口
  namedWindow( window_name, CV_WINDOW_AUTOSIZE );
  imshow( window_name, dst );

  /// 循环
  while( true )
  {
    int c;
    c = waitKey(10);

    if( (char)c == 5 )
      { break; }
    if( (char)c == 'u' )
      { pyrUp( tmp, dst, Size( tmp.cols*2, tmp.rows*2 ) );
        printf( "** Zoom In: Image x 2 \n" );
      }
    else if( (char)c == 'd' )
     { pyrDown( tmp, dst, Size( tmp.cols/2, tmp.rows/2 ) );
       printf( "** Zoom Out: Image / 2 \n" );
     }
      detectAndDisplay( dst );
    //imshow( window_name, dst );
    tmp = dst;
  }
  return 0;
}

// @function detectAndDisplay   
void detectAndDisplay( Mat frame )  
{  
  std::vector<Rect> faces;  
  Mat frame_gray;  
  
  cvtColor( frame, frame_gray, CV_BGR2GRAY );  
  equalizeHist( frame_gray, frame_gray );  
  
  //-- Detect faces  
  face_cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, Size(30, 30) );  
  
  for( size_t i = 0; i < faces.size(); i++ )  
  {  
    Point center( faces[i].x + faces[i].width*0.5, faces[i].y + faces[i].height*0.5 );  
    ellipse( frame, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 2, 8, 0 );  
  
    Mat faceROI = frame_gray( faces[i] );  
    std::vector<Rect> eyes;  
  
    //-- In each face, detect eyes  
    eyes_cascade.detectMultiScale( faceROI, eyes, 1.1, 2, 0 |CV_HAAR_SCALE_IMAGE, Size(30, 30) );  
  
    for( size_t j = 0; j < eyes.size(); j++ )  
     {  
       Point center( faces[i].x + eyes[j].x + eyes[j].width*0.5, faces[i].y + eyes[j].y + eyes[j].height*0.5 );  
       int radius = cvRound( (eyes[j].width + eyes[j].height)*0.25 );  
       circle( frame, center, radius, Scalar( 255, 0, 0 ), 4, 8, 0 );  
     }  
  }  
  //-- Show what you got  
  imshow( window_name, frame );  
 }  */
