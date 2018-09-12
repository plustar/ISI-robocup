//Includes all the headers necessary to use the most common public pieces of the ROS system.    
#include <ros/ros.h>
#include <string>        
#include <sstream> 
#include <vector>  
#include <list>  
#include <map>  
#include <stack> 
#include <iostream>  
#include <stdio.h>   
#include <opencv2/core/core.hpp>      
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
#include <opencv2/core/core.hpp>   
#include <opencv2/features2d/features2d.hpp>  
#include <opencv2/calib3d/calib3d.hpp> 
#include <std_msgs/String.h> 
#include "/home/plus/2017_ws/src/imgpcl/include/imgpcl/auto_tchar.h"
using namespace cv;    
using namespace std;    
    
//Store all constants for image encodings in the enc namespace to be used later.      
namespace enc = sensor_msgs::image_encodings;      
void image_socket(Mat inImg);    
void detectAndDisplay( Mat frame );  
Mat image1;    
static int imgWidth, imgHeight;   
string detect_begin = "";
String wave_man="no";
ros::Publisher chatter_waveman; 
int objx=0;  
int objy=0;  

String face_cascade_name = "/home/isi/2017_ws/src/imgpcl/src/haarcascade_frontalface_alt.xml";  
 String eyes_cascade_name = "/home/isi/2017_ws/src/imgpcl/src/haarcascade_eye_tree_eyeglasses.xml";  
  CascadeClassifier face_cascade; 
 
 
 string window_name = "Capture - Face detection";  
 RNG rng(12345);  
    //8邻接种子算法，并返回每块区域的边缘框  
void Seed_Filling(const cv::Mat& binImg, cv::Mat& labelImg, int& labelNum, int (&ymin)[20], int(&ymax)[20], int(&xmin)[20], int(&xmax)[20])   //种子填充法    
{  
    if (binImg.empty() ||  
        binImg.type() != CV_8UC1)  
    {  
        return;  
    }  
  
    labelImg.release();  
    binImg.convertTo(labelImg, CV_32SC1);  
    int label = 1;  
    int rows = binImg.rows - 1;  
    int cols = binImg.cols - 1;  
    for (int i = 1; i < rows - 1; i++)  
    {  
        int* data = labelImg.ptr<int>(i);  
        for (int j = 1; j < cols - 1; j++)  
        {  
            if (data[j] == 1)  
            {  
                std::stack<std::pair<int, int> > neighborPixels;  
                neighborPixels.push(std::pair<int, int>(j, i));     // 像素位置: <j,i>    
                ++label;  // 没有重复的团，开始新的标签   
                ymin[label] = i;  
                ymax[label] = i;  
                xmin[label] = j;  
                xmax[label] = j;  
                while (!neighborPixels.empty())  
                {  
                    std::pair<int, int> curPixel = neighborPixels.top(); //如果与上一行中一个团有重合区域，则将上一行的那个团的标号赋给它    
                    int curX = curPixel.first;  
                    int curY = curPixel.second;  
                    labelImg.at<int>(curY,curX) = label;  
  
                    neighborPixels.pop();  
  
                    if ((curX>0)&&(curY>0)&&(curX<(cols-1))&&(curY<(rows-1)))  
                    {   
                        if (labelImg.at<int>(curY - 1,curX) == 1)                     //上  
                        {  
                            neighborPixels.push(std::pair<int, int>(curX, curY - 1));  
                            //ymin[label] = curY - 1;  
                        }  
                        if (labelImg.at<int>( curY + 1,curX) == 1)                        //下  
                        {  
                            neighborPixels.push(std::pair<int, int>(curX, curY + 1));  
                            if ((curY+1)>ymax[label])  
                                ymax[label] = curY + 1;  
                        }  
                        if (labelImg.at<int>(curY,curX - 1) == 1)                     //左  
                        {  
                            neighborPixels.push(std::pair<int, int>(curX - 1, curY));  
                            if ((curX - 1)<xmin[label])  
                                xmin[label] = curX - 1;  
                        }  
                        if (labelImg.at<int>(curY,curX + 1) == 1)                     //右  
                        {  
                            neighborPixels.push(std::pair<int, int>(curX + 1, curY));  
                            if ((curX + 1)>xmax[label])  
                                xmax[label] = curX + 1;  
                        }  
                        if (labelImg.at<int>(curY - 1,curX-1) == 1)                   //左上  
                        {    
                            neighborPixels.push(std::pair<int, int>(curX - 1, curY - 1));  
                            //ymin[label] = curY - 1;  
                            if ((curX - 1)<xmin[label])  
                                xmin[label] = curX - 1;  
                        }  
                        if (labelImg.at<int>(curY + 1,curX+1) == 1)                   //右下  
                        {    
                            neighborPixels.push(std::pair<int, int>(curX+1, curY + 1));  
                            if ((curY + 1)>ymax[label])  
                                ymax[label] = curY + 1;  
                            if ((curX + 1)>xmax[label])  
                                xmax[label] = curX + 1;  
  
                        }  
                        if (labelImg.at<int>( curY + 1,curX - 1) == 1)                    //左下  
                        {   
                            neighborPixels.push(std::pair<int, int>(curX - 1, curY+1));  
                            if ((curY + 1)>ymax[label])  
                                ymax[label] = curY + 1;  
                            if ((curX - 1)<xmin[label])  
                                xmin[label] = curX - 1;  
                        }  
                        if (labelImg.at<int>( curY - 1,curX + 1) == 1)                    //右上  
                        {  
                            neighborPixels.push(std::pair<int, int>(curX + 1, curY-1));  
                            //ymin[label] = curY - 1;  
                            if ((curX + 1)>xmax[label])  
                                xmax[label] = curX + 1;  
  
                        }  
                    }  
                }  
            }  
        }  
    }  
    labelNum = label-1;  
  
}  
      
    class WatershedSegmenter 
{  
    private:  
        cv::Mat markers;  
    public:  
        void setMarkers(const cv::Mat& markerImage) {  
      
            // Convert to image of ints  
            markerImage.convertTo(markers, CV_32S);  
        }  
        cv::Mat process(const cv::Mat &image) {  
      
            // Apply watershed  
            cv::watershed(image, markers);  
            return markers;  
        }  
        // Return result in the form of an image  
        cv::Mat getSegmentation() {  
      
            cv::Mat tmp;  
            // all segment with label higher than 255  
            // will be assigned value 255  
            markers.convertTo(tmp, CV_8U);  
            return tmp;  
        }  
      
        // Return watershed in the form of an image  
        cv::Mat getWatersheds() {  
            cv::Mat tmp;  
            markers.convertTo(tmp, CV_8U,255, 255);  
            return tmp;  
        }  
};  
      
       
    
//This function is called everytime a new image_info message is published    
void camInfoCallback(const sensor_msgs::CameraInfo & camInfoMsg)    
{    
          //Store the image width for calculation of angle    
          imgWidth = camInfoMsg.width;    
          imgHeight = camInfoMsg.height;    
}    
  
void waveInfoCallback(const std_msgs::String::ConstPtr& msg)    
{    
  //Store the image width for calculation of angle    
  detect_begin= msg->data;    
  cout<<"waveInfoCallback  "<<detect_begin<<endl;
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

        detectAndDisplay(cv_ptr->image); 
    
}  


void detectAndDisplay( Mat frame )  
{   
  if(frame.empty()){
    ROS_INFO("camera image empty");
    return;
  }
  if(detect_begin=="stop"){
     ROS_INFO("stop detect wave");
    return;
  }
  if(detect_begin=="wave")
  {
        Mat binImage,tmp;  
        Mat Y, Cr, Cb;  
        vector<Mat> channels;  
        //模板图片，是Cr颜色通道的人手图像截图  
        Mat tmpl = imread("/home/isi/2017_ws/src/imgpcl/bwz.jpeg",CV_8UC1);  


        cvtColor(frame, binImage, CV_BGR2GRAY);  
        frame.copyTo(tmp);  
        cvtColor(tmp, tmp, CV_BGR2YCrCb);  
        split(tmp, channels);  
        Cr = channels.at(1);  
        Cb = channels.at(2);  

        //肤色检测，输出二值图像  
        for (int j = 1; j < Cr.rows - 1; j++)  
        {  
            uchar* currentCr = Cr.ptr< uchar>(j);  
            uchar* currentCb = Cb.ptr< uchar>(j);  
            uchar* current = binImage.ptr< uchar>(j);  
            for (int i = 1; i < Cb.cols - 1; i++)  
            {  
                if ((currentCr[i] > 140) && (currentCr[i] < 170)  &&(currentCb[i] > 77) && (currentCb[i] < 123))  
                    current[i] = 255;  
                else  
                    current[i] = 0;  
            }  
        }  
      
        //形态学处理  
        //dilate(binImage, binImage, Mat());  
        dilate(binImage, binImage, Mat());  
      
        //分水岭算法  
        cv::Mat fg;  
        cv::erode(binImage, fg, cv::Mat(), cv::Point(-1, -1), 6);  
        // Identify image pixels without objects  
        cv::Mat bg;  
        cv::dilate(binImage, bg, cv::Mat(), cv::Point(-1, -1), 6);  
        cv::threshold(bg, bg, 1, 128, cv::THRESH_BINARY_INV);  
        // Show markers image  
        cv::Mat markers(binImage.size(), CV_8U, cv::Scalar(0));  
        markers = fg + bg;  
        // Create watershed segmentation object  
        WatershedSegmenter segmenter;  
        segmenter.setMarkers(markers);  
        segmenter.process(frame);  
        Mat waterShed;  
        waterShed = segmenter.getWatersheds();  
        //imshow("watershed", waterShed);  
        //获得区域边框  
        threshold(waterShed, waterShed, 1, 1, THRESH_BINARY_INV);  
          
        //8向种子算法，给边框做标记  
        Mat labelImg;  
        int label, ymin[20], ymax[20], xmin[20], xmax[20];  
        Seed_Filling(waterShed, labelImg, label, ymin, ymax, xmin, xmax);  
      
        //根据标记，对每块候选区就行缩放，并与模板比较  
        Size dsize = Size(tmpl.cols, tmpl.rows);  
        float simi[20];  
        for (int i = 0; i < label; i++)  
        {  
            simi[i] = 1;  
            if (((xmax[2 + i] - xmin[2 + i])>50) && ((ymax[2 + i] - ymin[2 + i]) > 50))  
            {  
                //rectangle(frame, Point(xmin[2 + i], ymin[2 + i]), Point(xmax[2 + i], ymax[2 + i]), Scalar::all(255), 2, 8, 0);  
                Mat rROI = Mat(dsize, CV_8UC1);  
                resize(Cr(Rect(xmin[2 + i], ymin[2 + i], xmax[2 + i] - xmin[2 + i], ymax[2 + i] - ymin[2 + i])), rROI, dsize);  
                Mat result;  
                matchTemplate(rROI, tmpl, result, CV_TM_SQDIFF_NORMED);  
                simi[i] = result.ptr<float>(0)[0];  
                //cout << simi[i] << endl;  
            }  
        }  
          
        //统计一下区域中的肤色区域比例  
        float fuseratio[20];  
        for (int k = 0; k < label; k++)  
        {  
            fuseratio[k] = 1;  
            if (((xmax[2 + k] - xmin[2 + k])>50) && ((ymax[2 + k] - ymin[2 + k]) > 50))  
            {  
                int fusepoint=0;  
                for (int j = ymin[2+k]; j < ymax[2+k]; j++)  
                {  
                    uchar* current = binImage.ptr< uchar>(j);  
                    for (int i = xmin[2+k]; i < xmax[2+k]; i++)  
                    {  
                        if (current[i] == 255)  
                            fusepoint += 1;  
                    }  
                }  
                fuseratio[k] = float(fusepoint) / ((xmax[2 + k] - xmin[2 + k])*(ymax[2 + k] - ymin[2 + k]));  
                //cout << fuseratio[k] << endl;  
            }  
        }  
      
        //给符合阈值条件的位置画框  
        // for (int i = 0; i < label; i++)  
        // {  
        //     if ((simi[i]<0.03)&&(fuseratio[i]<0.55))  
        //         rectangle(frame, Point(xmin[2 + i], ymin[2 + i]), Point(xmax[2 + i], ymax[2 + i]), Scalar::all(255), 2, 8, 0);  
        // }  
          
        imshow("frame", frame);  
        Mat element5(5,5,CV_8U,cv::Scalar(1));
        //morphologyEx(binImage, binImage,cv::MORPH_CLOSE,element5,Point(-1,-1),1);
        //////////////////////////////////////////////////////////////////////////////////////change for better performer
        Mat element = getStructuringElement(MORPH_RECT, Size(15, 15));
        erode( binImage,binImage,element); //腐蚀
        medianBlur(binImage, binImage, 5);  
        dilate( binImage,binImage,element); //膨胀
        morphologyEx(binImage, binImage,cv::MORPH_CLOSE,element5,Point(-1,-1),1); 
        imshow("test", binImage);  
        vector<vector<Point> > contours;  
        vector<Vec4i> hierarchy;
        findContours(binImage, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);
        //drawContours(resultImage, contours, -1, Scalar(255, 0, 255));
        /// 多边形逼近轮廓 + 获取矩形和圆形边界框
        vector<vector<Point> > contours_poly( contours.size() );
        vector<Rect> boundRect( contours.size() );
        vector<Point2f>center( contours.size() );
        vector<float>radius( contours.size() );

        for( int i = 0; i < contours.size(); i++ )
           { approxPolyDP( Mat(contours[i]), contours_poly[i], 3, true );
             boundRect[i] = boundingRect( Mat(contours_poly[i]) );
             minEnclosingCircle( contours_poly[i], center[i], radius[i] );
           }

        //Detect faces  
        std::vector<Rect> faces;  
        Mat frame_gray;  
        cvtColor( frame, frame_gray, CV_BGR2GRAY );  
        equalizeHist( frame_gray, frame_gray ); 
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


        /// 画多边形轮廓 + 包围的矩形框 + 圆形框
       Mat drawing = Mat::zeros( binImage.size(), CV_8UC3 );
       cout<<"contours.size()"<<contours.size()<<endl;
       
       for( int i = 0; i< contours.size(); i++ )
       {
         Scalar color = Scalar( rng.uniform(0, 255), rng.uniform(0,255), rng.uniform(0,255) );
        //drawContours( drawing, contours_poly, i, color, 1, 8, vector<Vec4i>(), 0, Point() );
        double g_dConArea = contourArea(contours[i], true); 
        //rectangle( drawing, boundRect[i].tl(), boundRect[i].br(), color, 2, 8, 0 );
        //circle( drawing, center[i], (int)radius[i], color, 2, 8, 0 );
        cout<<"faces.size()"<<faces.size()<<endl;
        if(faces.size()==0)
        {
        
            objx=boundRect[0].x + boundRect[0].width*0.5;
            
        }
        for( size_t j = 0; j < faces.size(); j++ )  
        {
            ROS_INFO("--------!!!!!!!---------");  
            Point center( faces[j].x + faces[j].width*0.5, faces[j].y + faces[j].height*0.5 );  
            Point center1( boundRect[i].x + boundRect[i].width*0.5, boundRect[i].y + boundRect[i].height*0.5 );  

            //   rectangle( drawing, boundRect[i].tl(), boundRect[i].br(), color, 2, 8, 0 ); 
            if(g_dConArea<300&&(boundRect[i].y<faces[j].y)&&((boundRect[i].x<faces[j].x-5)||(boundRect[i].x>(faces[j].x+faces[j].width+5))))
                if (faces[i].contains(center1))
                    rectangle( drawing, boundRect[i].tl(), boundRect[i].br(), (0,0,255), 2, 8, 0 );
            objx=boundRect[i].x + boundRect[i].width*0.5;
            //ellipse( binImage, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 2, 8, 0 );  
            }  
        }
           if(objx==0)
            wave_man="no";
          else if(objx>260&&objx<380)
            wave_man="middle";
          else if(objx<320)
            wave_man="left";
          else
            wave_man="right";
          std_msgs::String msg1;
          std::stringstream ss1;
          ss1<<wave_man;
          msg1.data=ss1.str();
          chatter_waveman.publish(msg1);
        imshow("result", drawing);  
        // namedWindow( "Contours", CV_WINDOW_AUTOSIZE );
        // imshow( "Contours", drawing );
             waitKey(10);  
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
    
    image_transport::Subscriber sub = it.subscribe("camera1/rgb/image_raw", 1, imageCallback);    
    ros::Subscriber waveInfo_sub     = nh.subscribe("detectWave", 1, waveInfoCallback);
    ros::Subscriber camInfo         = nh.subscribe("camera1/rgb/camera_info", 1, camInfoCallback);   
    chatter_waveman = nh.advertise<std_msgs::String>("wave_detect", 1);
    
    ros::spin();    
    
    //ROS_INFO is the replacement for printf/cout.    
    ROS_INFO("tutorialROSOpenCV::main.cpp::No error.");    
}


