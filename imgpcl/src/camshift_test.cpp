//Includes all the headers necessary to use the most common public pieces of the ROS system.    
    #include <ros/ros.h>    
    //Use image_transport for publishing and subscribing to images in ROS    
    #include <image_transport/image_transport.h>    
    //Use cv_bridge to convert between ROS and OpenCV Image formats    
    #include <cv_bridge/cv_bridge.h>    
    //Include some useful constants for image encoding. Refer to: http://www.ros.org/doc/api/sensor_msgs/html/namespacesensor__msgs_1_1image__encodings.html for more info.    
    #include <sensor_msgs/image_encodings.h>    
    //Include headers for OpenCV Image processing    
    #include <opencv2/imgproc/imgproc.hpp>    
    //Include headers for OpenCV GUI handling    
    #include <opencv2/highgui/highgui.hpp>    
    #include "opencv2/video/tracking.hpp"    
    #include <geometry_msgs/Twist.h>    
    #include <std_msgs/Float32.h>    
    #include <std_msgs/UInt8.h>    
        
    using namespace cv;    
    using namespace std;    
        
    //Store all constants for image encodings in the enc namespace to be used later.    
    namespace enc = sensor_msgs::image_encodings;    
  
    int trackObject = -1;    
    bool showHist = true;    
    static Point origin;    
    static Rect selection;    
    int vmin = 30, vmax = 256, smin = 60;    
    Mat image;    
    //static int imgWidth, imgHeight;    
    static int initDestArea = 1; //Initialized to 1 to avoid DIV by 0 errors    

    static ros::Publisher robotAngleVar;    
   
    static ros::Publisher imagePrStatePub;    
    static ros::Publisher destAreaPub;    
        
    void camShift(Mat inImg);    
     static string ImgInfo="/home/isi/2017_ws/src/imgpcl/template/PotatoChips.jpg";   
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
        camShift(cv_ptr->image);    
    }    
        
    void camShift(Mat inImg)    
    {    
      static Rect trackWindow;    
      static int hsize = 16;    
      static float hranges[] = {0,180};    
      static const float* phranges = hranges;    
      static Mat frame, hsv, hue, mask, hist, histimg = Mat::zeros(200, 320, CV_8UC3), backproj;    
      static bool paused = false;    
      RotatedRect trackBox;    
      std_msgs::UInt8 state;    
        
      //If the image processing is not paused    
      if( !paused )    
      {    
        //cap >> frame;    
        if( inImg.empty() )    
        {    
          ROS_INFO("Camera image empty");    
          return;//break;    
        }    
      }    
        
      //Use the input image as the reference    
      //Only a shallow copy, so relatively fast    
      image = inImg;    
        
      if(!paused)    
      {    
          //Convert the colour space to HSV    
          cvtColor(image, hsv, CV_BGR2HSV);    
        
          //If the destination coordinates have been received, then start the tracking    
          //trackObject is set when the destination coordinates have been received    
          if( trackObject )    
          {    
           //   int _vmin = vmin, _vmax = vmax;    
              
              int _vmin = vmin, _vmax = vmax;    
        
              inRange(hsv, Scalar(0, smin, MIN(_vmin,_vmax)),    
                      Scalar(180, 256, MAX(_vmin, _vmax)), mask);    
              int ch[] = {0, 0};    
              hue.create(hsv.size(), hsv.depth());    
              mixChannels(&hsv, 1, &hue, 1, ch, 1);   
              Mat templ=imread(ImgInfo,1); 
                 selection=Rect(0,0,templ.cols-1,templ.rows-1);
              //Do the following steps only for the first time    
              if( trackObject < 0 )    
              {    
  
                  //Publish that we have started tracking    
                  std_msgs::UInt8 state;//    
                  state.data = 1;//    
                  imagePrStatePub.publish(state);//    

                  //Set the Region of interest and the mask for it    
                  Mat roi(hue, selection), maskroi(mask, selection);    
                  //Calculate the histogram of this    
                  calcHist(&roi, 1, 0, maskroi, hist, 1, &hsize, &phranges);    
                  normalize(hist, hist, 0, 255, CV_MINMAX);    
        
                  trackWindow = selection;    
                  trackObject = 1;    
      
                  histimg = Scalar::all(0);    
                  int binW = histimg.cols / hsize;    
                  Mat buf(1, hsize, CV_8UC3);    
                  for( int i = 0; i < hsize; i++ )    
                      buf.at<Vec3b>(i) = Vec3b(saturate_cast<uchar>(i*180./hsize), 255, 255);    
                  cvtColor(buf, buf, CV_HSV2BGR);    
        
                  for( int i = 0; i < hsize; i++ )    
                  {    
                      int val = saturate_cast<int>(hist.at<float>(i)*histimg.rows/255);    
                      rectangle( histimg, Point(i*binW,histimg.rows),    
                                 Point((i+1)*binW,histimg.rows - val),    
                                 Scalar(buf.at<Vec3b>(i)), -1, 8 );    
                  }    
                    ROS_INFO("--------------///---");    
              }    
        
              calcBackProject(&hue, 1, 0, hist, backproj, &phranges);    
              backproj &= mask;    
                ROS_INFO("--------------///---");    
              trackBox = CamShift(backproj, trackWindow,    
                                  TermCriteria( CV_TERMCRIT_EPS | CV_TERMCRIT_ITER, 10, 1 ));    
              ellipse( image, trackBox, Scalar(0,0,255), 3, CV_AA );    
          }    
      }     
      imshow( "CamShift Demo", image );    
    //  imshow( "Histogram", histimg );    
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
        
        std_msgs::UInt8 state;    
        
        //OpenCV HighGUI call to create a display window on start-up.    
        namedWindow( "Histogram", 0 );    
        namedWindow( "CamShift Demo", 0 );    
   
        image_transport::Subscriber sub = it.subscribe("camera/rgb/image_raw", 1, imageCallback); //style="background-color: rgb(255, 255, 0);"//Kinect Topic</span>    
        //ros::Subscriber camInfo  = nh.subscribe("camera/rgb/camera_info", 1, camInfoCallback);// style="background-color: rgb(255, 255, 0);"//Kinect Topic</span>    
       // ros::Subscriber destCoord       = nh.subscribe("dest_coord", 1, destCoordCallback);    
        
        robotAngleVar   = nh.advertise<std_msgs::Float32>("robot_angle", 100);    
        imagePrStatePub = nh.advertise<std_msgs::UInt8>("improc_state", 10);    
        destAreaPub     = nh.advertise<std_msgs::Float32>("dest_area", 10);    
        
        state.data = 0;    
        imagePrStatePub.publish(state);    
        
        //OpenCV HighGUI call to destroy a display window on shut-down.    
        //destroyWindow(WINDOW);    
        destroyWindow("Histogram");    
        destroyWindow("CamShift Demo");      
        ros::spin();    
        
        //ROS_INFO is the replacement for printf/cout.    
        ROS_INFO("tutorialROSOpenCV::main.cpp::No error.");    
    }    
