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
    #include<string>        
    #include <sstream>    
    using namespace cv;    
    using namespace std;    
        
    //Store all constants for image encodings in the enc namespace to be used later.      
    namespace enc = sensor_msgs::image_encodings;      
    void imgprocess(Mat inImg);    
    Mat image1;    
    static int imgWidth, imgHeight;    
    int objWidth=150;  
    int objHeight=250;  
    //char *output_file = "/home/hsn/catkin_ws/src/rosopencv";    
        
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
        imgprocess(cv_ptr->image);    
        
    }           
    void imgprocess(Mat inImg)    
    {    
        if( inImg.empty() )    
        {    
          ROS_INFO("Camera image empty");    
          return;//break;    
        }    
        //rectangle(inImg, Point(inImg.cols/2-objWidth/2-2,inImg.rows/2-objHeight/2-2),Point(inImg.cols/2+objWidth/2+2,inImg.rows/2+objHeight/2+2),Scalar(0,0,255), 1, 8 );  //画矩形   
    //画线  
    	Point a = Point (0,inImg.rows/2);  
   	 //参数为：承载的图像、起始点、结束点、颜色、粗细、线型  
    	line(inImg,Point (0,inImg.rows/2),Point (inImg.cols,inImg.rows/2),Scalar(255,0,0));  
    	
        imshow("imgprocess", inImg);//显示图片    
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
        
          strs="/home/isi/2017_ws/src/imgpcl/";    
          sss.clear();        
          sss<<strs;        
          sss<<image_num;        
          sss<<".jpg";        
          sss>>strs;        
          imwrite(strs,inImg);//保存图片  
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
        ros::init(argc, argv, "calibratePrimeArm");    
        ROS_INFO("-----------------");    
            
        ros::NodeHandle nh;    
        
        image_transport::ImageTransport it(nh);    
        
        image_transport::Subscriber sub = it.subscribe("camera/rgb/image_raw", 1, imageCallback);    
        ros::Subscriber camInfo         = nh.subscribe("camera/rgb/camera_info", 1, camInfoCallback);    
        
        ros::spin();    
        
        //ROS_INFO is the replacement for printf/cout.    
        ROS_INFO("tutorialROSOpenCV::main.cpp::No error.");    
    }    
