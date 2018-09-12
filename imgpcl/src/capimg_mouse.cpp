    #include <ros/ros.h>    
      
    #include <image_transport/image_transport.h>    
      
    #include <cv_bridge/cv_bridge.h>    
      
    #include <sensor_msgs/image_encodings.h>    
      
    #include <opencv2/imgproc/imgproc.hpp>    
      
    #include <opencv2/highgui/highgui.hpp>    
    #include "opencv2/video/tracking.hpp"    
    #include <geometry_msgs/Twist.h>    
    #include <std_msgs/Float32.h>    
    #include <std_msgs/UInt8.h>    
      
    using namespace cv;    
    using namespace std;    
      
    //Store all constants for image encodings in the enc namespace to be used later.    
    namespace enc = sensor_msgs::image_encodings;    
      
    bool selectObject = false;    
       
    static Point origin;    
    static Rect selection;    
      
    Mat image;     
    static int CapImgNum=0;  //采集图像个数   
      
    void ImgCapMouse(Mat inImg);    
      
    static void onMouse( int event, int x, int y, int, void* )    
    {    
        ROS_INFO("Mouse detected");    
        if( selectObject )    
        {    
            selection.x = MIN(x, origin.x);    
            selection.y = MIN(y, origin.y);    
            selection.width = std::abs(x - origin.x);    
            selection.height = std::abs(y - origin.y);    
               // rectangle(image, origin,Point(x,y),Scalar(0,0,255), 1, 8 );  //画矩形  
            selection &= Rect(0, 0, image.cols, image.rows);  //用于确保所选的矩形区域在图片范围内         
        }    
      
        switch( event )    
        {    
        case CV_EVENT_LBUTTONDOWN:    
            origin = Point(x,y);    
            selection = Rect(x,y,0,0);    
            selectObject = true;    
            break;    
        case CV_EVENT_LBUTTONUP:    
            selectObject = false;    
            if( selection.width > 0 && selection.height > 0 )    
            {  
              
                    //Mat img=image(Rect(selection.x,selection.y,selection.width,selection.height));  
            Mat img(image, selection);  
                    bitwise_not(img, img);    
                    CapImgNum++;   
                    stringstream sss;        
                    string name;    
                    name="/home/isi/2017_ws/src/imgpcl/";    
                    sss.clear();        
                    sss<<name;        
                    sss<<CapImgNum;        
                    sss<<".jpg";        
                    sss>>name;    
                cout<<name<<"\n";  
                imwrite(name, img);   
            }  
            break;    
        }    
      
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
        ImgCapMouse(cv_ptr->image);    
    }    
      
      
    void ImgCapMouse(Mat inImg)    
    {    
    static bool paused = false;    
      
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
      
      
    //Code to display an inverted image of the selected region    
    //Remove this in the fall validation expt TBD    
    if( selectObject && selection.width > 0 && selection.height > 0 )    
    {    
      Mat roi(image, selection);    
      bitwise_not(roi, roi);  //反转图像灰度，即求图像的负片.将图像中每点的灰度变成（255-gray），其中gray是当前点的灰度。  
    }    
       
      
    char c = (char)waitKey(1);    
    if( c == 27 )    
      ROS_INFO("Exit boss");//break;    
    switch(c)    
    {      
    case 'p':  //暂停检测或继续  
      paused = !paused;    
      break;    
    default:    
      break;    
    }    
    setMouseCallback( "ObjCap", onMouse, 0 );//     
    imshow( "ObjCap", image );    
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
      
    namedWindow( "ObjCap", 0 );    
      
      
    image_transport::Subscriber sub = it.subscribe("camera/rgb/image_raw", 1, imageCallback);  
    //OpenCV HighGUI call to destroy a display window on shut-down.    
    //destroyWindow(WINDOW);    
       
    destroyWindow("ObjCap");    
      
      
    /**  
    * In this application all user callbacks will be called from within the ros::spin() call.  
    * ros::spin() will not return until the node has been shutdown, either through a call  
    * to ros::shutdown() or a Ctrl-C.  
    */    
    ros::spin();    
      
    //ROS_INFO is the replacement for printf/cout.    
    ROS_INFO("tutorialROSOpenCV::main.cpp::No error.");    
    }    
