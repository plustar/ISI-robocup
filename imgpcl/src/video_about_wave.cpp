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
#include "auto_tchar.h"
#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <math.h>
#include <std_msgs/String.h>
using namespace cv;    
using namespace std;    

//Store all constants for image encodings in the enc namespace to be used later.      
namespace enc = sensor_msgs::image_encodings;      
void image_socket(Mat inImg);    
Mat image1;    
string detect_begin = "";
static int imgWidth, imgHeight;
ros::Publisher chatter_pub;
ros::Publisher chatter_waveman;

int woman_num=0;
int man_num=0;
int objWidth=50;  
int objHeight=200;  
int g_howManyPhotoForTraining = 260;
//脙驴赂枚脠脣脠隆鲁枚8脮脜脳梅脦陋脩碌脕路
int g_photoNumberOfOnePerson = 279;
//ORL脢媒戮脻驴芒脙驴赂枚脠脣10脮脜脥录脧帽
void detectAndDisplay(Mat frame); 
/// 全局变量
Mat src, dst, tmp;
const char* window_name = "Pyramids Demo";
 String face_cascade_name = "/home/kris/catkin_ws/src/imgpcl/src/haarcascade_frontalface_alt.xml";  
 String eyes_cascade_name = "/home/kris/catkin_ws/src/imgpcl/src/haarcascade_eye_tree_eyeglasses.xml";  
 const char* pic_path ="/home/kris/catkin_ws/src/imgpcl/people.jpg";
 String faces_num; 
  String wave_man; 
 CascadeClassifier face_cascade;  
 CascadeClassifier eyes_cascade;  
 //string window_name = "Capture - Face detection";  
 RNG rng(12345);  
   static int image_num = 1;  
   static int image_dec_num = 1;  
//char *output_file = "/home/shuning/catkin_ws/src/rosopencv";  
string n1;
string n2;
string n3;
string n4;
string n5;
//pHash算法
 string pHashValue(Mat &src)
 {
   Mat img ,dst;
   string rst(64,'\0');
   double dIdex[64];
   double mean = 0.0;
   int k = 0;
   if(src.channels()==3)
   {
     cvtColor(src,src,CV_BGR2GRAY);
     img = Mat_<double>(src);
   }   
   else
   {
     img = Mat_<double>(src);
   }     
   
        /* 第一步，缩放尺寸*/
   resize(img, img, Size(8,8));
        
        /* 第二步，离散余弦变换，DCT系数求取*/
   dct(img, dst); 

        /* 第三步，求取DCT系数均值（左上角8*8区块的DCT系数）*/
   for (int i = 0; i < 8; ++i) {
     for (int j = 0; j < 8; ++j) 
     {
       dIdex[k] = dst.at<double>(i, j);
       mean += dst.at<double>(i, j)/64;
       ++k;
     }
   }
        
        /* 第四步，计算哈希值。*/
   for (int i =0;i<64;++i)
   {
     if (dIdex[i]>=mean)
     {
       rst[i]='1';
     }
     else
     {
       rst[i]='0';
     }
   }
   return rst;
 }
 //均值Hash算法
 string HashValue(Mat &src)
 {
   string rst(64,'\0');
   Mat img;
   if(src.channels()==3)
     cvtColor(src,img,CV_BGR2GRAY);
  else
    img=src.clone();
       /*第一步，缩小尺寸。
         将图片缩小到8x8的尺寸，总共64个像素,去除图片的细节*/

        resize(img,img,Size(8,8));
  /* 第二步，简化色彩(Color Reduce)。
     将缩小后的图片，转为64级灰度。*/

  uchar *pData;
  for(int i=0;i<img.rows;i++)
  {
    pData = img.ptr<uchar>(i);
    for(int j=0;j<img.cols;j++)
    {
      pData[j]=pData[j]/4;        }
  }
  
        /* 第三步，计算平均值。
     计算所有64个像素的灰度平均值。*/
  int average = mean(img).val[0];
  
        /* 第四步，比较像素的灰度。
   将每个像素的灰度，与平均值进行比较。大于或等于平均值记为1,小于平均值记为0*/
  Mat mask= (img>=(uchar)average);
  
        /* 第五步，计算哈希值。*/
  int index = 0;
  for(int i=0;i<mask.rows;i++)
  {
    pData = mask.ptr<uchar>(i);
    for(int j=0;j<mask.cols;j++)
    {
      if(pData[j]==0)
        rst[index++]='0';
      else
        rst[index++]='1';
    }
  }
  return rst;
 }
    //汉明距离计算  
     int HanmingDistance(string &str1,string &str2)  
     {  
        if((str1.size()!=64)||(str2.size()!=64))  
            return -1;  
        int difference = 0;  
        for(int i=0;i<64;i++)  
        {  
            if(str1[i]!=str2[i])  
                difference++;  
        }  
        return difference;  
     }    
 static Mat norm_0_255(InputArray _src) {
  Mat src = _src.getMat();
  // 麓麓陆篓潞脥路碌禄脴脪禄赂枚鹿茅脪禄禄炉潞贸碌脛脥录脧帽戮脴脮贸:
  Mat dst;
  switch (src.channels()) {
  case1:
    cv::normalize(_src, dst, 0, 255, NORM_MINMAX, CV_8UC1);
    break;
  case3:
    cv::normalize(_src, dst, 0, 255, NORM_MINMAX, CV_8UC3);
    break;
  default:
    src.copyTo(dst);
    break;
  }
  return dst;
}   
void detectAndDisplay(Mat frame)  
{  
  std::vector<Rect> faces;  
  Mat frame_gray;   
     IplImage *pImg;
    Mat mat1; // mat1是临时变

    mat1=frame.clone();// 包括数据的深度复制，以防对mat数据的更改

    pImg=cvCreateImage(cvSize(frame.cols,frame.rows),8,3); //根据实际进行初始化

    pImg->imageData=(char*)mat1.data;
  cvtColor( frame, frame_gray, CV_BGR2GRAY );  
  equalizeHist( frame_gray, frame_gray );  
  
  //-- Detect faces  
  face_cascade.detectMultiScale( frame_gray, faces, 1.1, 3, 0|CV_HAAR_SCALE_IMAGE, Size(30, 30) );  
   //faces_num=faces.size();
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
  size_t people_num = 0;    
if(faces.size()==++people_num){
  faces_num="one";
}
else if(faces.size()==++people_num){
  faces_num="two";
}else if(faces.size()==++people_num){
  faces_num="three";
}else if(faces.size()==++people_num){
  faces_num="four";
}else if(faces.size()==++people_num){
  faces_num="five";
}else if(faces.size()==++people_num){
  faces_num="six";
}else if(faces.size()==++people_num){
  faces_num="seven";
}else if(faces.size()==++people_num){
  faces_num="eight";
}else if(faces.size()==++people_num){
  faces_num="nine";
}else if(faces.size()==++people_num){
  faces_num="ten";
}else
faces_num="none";
std_msgs::String msg;
    std::stringstream ss; 
    ss << "people number : " <<faces_num;
    msg.data = ss.str();
    ROS_INFO("%s", msg.data.c_str());
    chatter_pub.publish(msg);

  for( size_t i = 0; i < faces.size(); i++ )  
  {  
   // Point center( faces[i].x + faces[i].width*0.5, faces[i].y + faces[i].height*0.5 );  
   // ellipse( frame, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 2, 8, 0 );  
    CvPoint P1,P2;  
    P1.x=faces[i].x- faces[i].width-faces[i].width;  
    P1.y=faces[i].y+faces[i].height;  
    P2.x=faces[i].x + faces[i].width+faces[i].width+faces[i].width;  
    P2.y= faces[i].y + faces[i].height+ faces[i].height+ faces[i].height;  
     cvRectangle(pImg,P1 ,P2, CV_RGB(0, 255, 0), 2); //绿色画框  
    image1=frame(Rect(P1.x,P1.y,faces[i].width*5,faces[i].height*3));    
    Mat faceROI = image1;  
    stringstream sss;        
    string strs;      
       strs="/home/kris/catkin_ws/src/imgpcl/dec";    
      sss.clear();        
      sss<<strs;        
      sss<<image_dec_num;       
      sss<<".jpg";        
      sss>>strs;
       resize(faceROI,faceROI,Size(150,70),0,0,CV_INTER_LINEAR);             
      imwrite(strs,faceROI);//保存图片  
      cout<<image_num<<"images have saved!  ";  
      image_dec_num++; 
  }


  

   Mat imgMat(pImg, 1);  
   imwrite("/home/kris/catkin_ws/src/imgpcl/result.jpg",imgMat);
  //-- Show what you got  
  imshow( window_name, frame );  
 }  
void waveInfoCallback(const std_msgs::String::ConstPtr& msg)    
{    
  //Store the image width for calculation of angle    
  detect_begin= msg->data;    
  cout<<"waveInfoCallback  "<<detect_begin<<endl;
}    
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
    //cout<<"BBBBBBBBBBBBBBB"<<endl;
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
    
}    
    
void image_socket(Mat inImg)    
{    
  //cout<<"AAAAAAAAAAAAAAAA"<<endl;
  if( inImg.empty() )    
  {    
    ROS_INFO("Camera image empty");    
    return;//break;    
  }    
  //rectangle(inImg, Point(inImg.cols/2-objWidth/2-2,inImg.rows/2-objHeight/2-2),Point(inImg.cols/2+objWidth/2+2,inImg.rows/2+objHeight/2+2),Scalar(0,0,255), 1, 8 );  //画矩形    
  imshow("image_socket", inImg);//显示图片    
  stringstream sss;        
  string strs;    
       if(detect_begin=="wave")
       {
       cout<<"CCCCCCCCCCC"<<endl;
        //resize(inImg,image1,Size(imgWidth/6,imgHeight/6),0,0,CV_INTER_LINEAR);      
    image1=inImg(Rect(0,0,inImg.cols,inImg.rows ));    

    strs="/home/kris/catkin_ws/src/imgpcl/";    
    sss.clear();        
    sss<<strs;        
    sss<<image_num;       
    sss<<".jpg";        
    sss>>strs;     
    //resize(image1,image1,Size(150,70),0,0,CV_INTER_LINEAR);           
    imwrite(strs,image1);//保存图片  
    cout<<image_num<<"images have saved!"<<endl;  
    image_num++; 
       if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading\n"); };  
       if( !eyes_cascade.load( eyes_cascade_name ) ){ printf("--(!)Error loading\n"); };  
       detectAndDisplay(image1);  
  if(image_num>8)
  {
  cv::Mat Image1 = cv::imread("/home/kris/catkin_ws/src/imgpcl/dec1.jpg");
  cv::Mat Image2 = cv::imread("/home/kris/catkin_ws/src/imgpcl/dec2.jpg");
  cv::Mat Image3 = cv::imread("/home/kris/catkin_ws/src/imgpcl/dec3.jpg");
  cv::Mat Image4 = cv::imread("/home/kris/catkin_ws/src/imgpcl/dec4.jpg");
  cv::Mat Image5 = cv::imread("/home/kris/catkin_ws/src/imgpcl/dec5.jpg");
  resize(Image1,Image1,Size(92,112),0,0,CV_INTER_LINEAR);     
  resize(Image2,Image2,Size(92,112),0,0,CV_INTER_LINEAR);     
  resize(Image3,Image3,Size(92,112),0,0,CV_INTER_LINEAR);     
  resize(Image4,Image4,Size(92,112),0,0,CV_INTER_LINEAR);     
  resize(Image5,Image5,Size(92,112),0,0,CV_INTER_LINEAR);   
  n1=pHashValue(Image1);
  n2=pHashValue(Image2);
  n3=pHashValue(Image3);
  n4=pHashValue(Image4);
  n5=pHashValue(Image5);
  int wave_maybe=HanmingDistance(n1,n2)+HanmingDistance(n2,n3)+HanmingDistance(n3,n4)+HanmingDistance(n4,n5);
  cout<< wave_maybe <<endl;
  // n1=HashValue(image1);
  // n2=HashValue(image2);
  if(wave_maybe >30)
  wave_man="yes";
  else
  wave_man="no";
  ///////////////////////////////////////////////////////////
  std_msgs::String msg1;
  std::stringstream ss1; 
  ss1 << "dectct wave people " <<wave_man;
  msg1.data = ss1.str();
  ROS_INFO("%s", msg1.data.c_str());
  chatter_waveman.publish(msg1);
  }


  }
    
    



}    
    
    
/** 
* This is ROS node to track the destination image 
*/    
int main(int argc, char **argv)    
{    
    ros::init(argc, argv, "image_socket");    
    ROS_INFO("-----------------");    
    ros::NodeHandle nh;    
    image_transport::ImageTransport it(nh);    
    
    image_transport::Subscriber sub = it.subscribe("camera/rgb/image_raw", 1, imageCallback);    
    ros::Subscriber camInfo         = nh.subscribe("camera/rgb/camera_info", 1, camInfoCallback);
    ros::Subscriber waveInfo_sub     = nh.subscribe("detectWave", 1, waveInfoCallback);        
    chatter_pub = nh.advertise<std_msgs::String>("person_num", 1);
    chatter_waveman = nh.advertise<std_msgs::String>("wave_man", 1);

    //ROS_INFO is the replacement for printf/cout.    
    ROS_INFO("tutorialROSOpenCV::main.cpp::No error.");  
    ros::spin();
    return 0;  
}
// cv::Mat image1 = cv::imread("/home/kris/catkin_ws/src/imgpcl/33.png");
// cv::Mat image2 = cv::imread("/home/kris/catkin_ws/src/imgpcl/40.png");
//  n1=pHashValue(image1);
//  n2=pHashValue(image2);
//  cout<< HanmingDistance(n1,n2)<<endl;
//   n1=HashValue(image1);
//  n2=HashValue(image2);
//  cout<< HanmingDistance(n1,n2)<<endl;