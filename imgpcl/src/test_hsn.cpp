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
    #include <std_msgs/UInt8.h>   
      
    #include <sys/types.h>   
    #include <sys/socket.h>   
    #include <stdio.h>   
    #include <stdlib.h>   
    #include <string.h>   
    #include <sys/ioctl.h>   
    #include <unistd.h>   
    #include <netdb.h>   
    #include <netinet/in.h>     
    #include  <arpa/inet.h>    
    using namespace cv;  
    using namespace std;  
      
    //Store all constants for image encodings in the enc namespace to be used later.    
    namespace enc = sensor_msgs::image_encodings;   
       
    void image_socket(Mat inImg);  
    static Mat image1;  
    static int imgWidth, imgHeight;  
       
    static int image_num = 1;  
      
    #define PORT 30000   
    #define BUFFER_SIZE 20000  
    #define NAME_SIZE 20  
    char * servInetAddr = "127.0.0.1";    
    static int sockfd;  
    bool  ifcap_obj=0;
    bool ifapple=0;
    bool iforange=0;
    //static ros::Publisher capture;    
    //This function is called everytime a new image_info message is published  
    void camInfoCallback(const sensor_msgs::CameraInfo & camInfoMsg)  
    {  
      //Store the image width for calculation of angle  
      imgWidth = camInfoMsg.width;  
      imgHeight = camInfoMsg.height;  
    } 
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
    double get_avg_gray(Mat img)
    {
    Mat gray;
    cvtColor( img, gray, CV_BGR2GRAY );
    
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
      
    }  
      
    void image_socket(Mat inImg)  
    {  
       imshow("image_socket", inImg);//显示图片  
        if( inImg.empty() )  
        {  
            ROS_INFO("Camera image empty");  
            return;//break;  
        } 
        if(ifcap_obj)
        {
            resize(inImg,image1,Size(imgWidth/6,imgHeight/6),0,0,CV_INTER_LINEAR);  
          
            image1=image1(Rect(image1.cols/2-32,image1.rows/2-32, 64, 64));  
            stringstream sss;      
            string strs;  
            strs="/home/hsn/catkin_ws/src/rosopencv/";  
            sss.clear();      
            sss<<strs;      
            sss<<image_num;      
            sss<<".jpg";      
            sss>>strs;      
            //imwrite(strs,image1);//保存图片  
            cout<<image_num<<endl;  
            //reshape(
            uchar sendline[BUFFER_SIZE];  
            char recvline[NAME_SIZE];   
            char name[]="w";//"NongFuSpringwwwwwww";  
            int i;  
            int j;  
            i=0;
            Mat gray;
            cvtColor( img, gray, CV_BGR2GRAY );
            //将图像像素值存到sendline中  
            for (int r=0;r<image1.rows;r++)  
            {  
             for(int c=0;c<image1.cols;c++)  
             {  
                sendline[i]=image1.at<Vec3b>(r,c)[0];//green  
                i++;  
                sendline[i]=image1.at<Vec3b>(r,c)[1];//blue  
                i++;  
                sendline[i]=image1.at<Vec3b>(r,c)[2];//red  
                i++;  
             }  
            }  
          /*for(i=0;i<image1.total()*image1.channels();i++) 
          { 
              sendline[i]=image1.data[i];//此种方法服务器接受到的图像是乱码 
          }*/ 
          if(ifapple)
          {
               for(j=0;j<sizeof(name);j++,i++)  
              {  
                 sendline[i]=name[j];  
              } 
          }
        //  sprintf(sendline, "%%%%", image1.data,name);  
          int n;  
           //发送图像及名字到服务器  
           n = send(sockfd, sendline, image1.total()*image1.channels()+NAME_SIZE,0);    
          if (n < 0)   
         perror("ERROR writing to socket");  

          n = recv(sockfd, recvline, NAME_SIZE,MSG_WAITALL);   
          cout<< recvline<<endl;  
          cout<<n<<endl;  

          if(recvline=="none")
          {
            
          }
          if(recvline=="apple")
          {
            
          }
           // n = read(sockfd, recvline, MAXLINE);    
           // write(STDOUT_FILENO, recvline, n);   
         // n = write(sockfd,image1.data,image1.total()*image1.channels());  
          if(recvline=="orange")
          {
            
          }
          image_num++;  
          break; 
          }
          if() 
    }  
      default:  
          break;  
      }  
     //imshow("image", image1);//显示图片  
    //image1.release();  
    }  
      
    /** 
    * This is ROS node to track the destination image 
    */  
    int main(int argc, char **argv)  
    {  
        ros::init(argc, argv, "image_socket");  
        ROS_INFO("-----------------");  
          
        struct sockaddr_in serv_addr;     
    /*创建socket*/   
        if ((sockfd = socket(AF_INET,SOCK_STREAM,0)) == -1)   
        {   
          perror("Socket failed!\n");   
          exit(1);   
        }   
        printf("Socket id = %d\n",sockfd);   
    /*设置sockaddr_in 结构体中相关参数*/   
        serv_addr.sin_family = AF_INET;   
        serv_addr.sin_port = htons(PORT);   
        inet_pton(AF_INET, servInetAddr, &serv_addr.sin_addr);    
        bzero(&(serv_addr.sin_zero), 8);   
        /*调用connect 函数主动发起对服务器端的连接*/   
        if(connect(sockfd,(struct sockaddr *)&serv_addr, sizeof(serv_addr))== -1)   
        {   
            perror("Connect failed!\n");   
            exit(1);   
        }   
        printf("welcome\n");    
      
        ros::NodeHandle nh;  
        image_transport::ImageTransport it(nh);  
        ros::Subscriber sp_sub = nh.subscribe("/cap_obj", 1, spCallback);  //订阅voice的消息???????????
        ros::Subscriber sp_sub = nh.subscribe("/obj_name", 1, spCallback);  //订阅voice的消息
        image_transport::Subscriber sub = it.subscribe("camera/rgb/image_raw", 1, imageCallback);  
        ros::Subscriber camInfo         = nh.subscribe("camera/rgb/camera_info", 1, camInfoCallback);  
       
        ros::Rate loop_rate(10);  
      
        while (ros::ok())  
        {  
           ros::spinOnce();  
           loop_rate.sleep();  
        }  
      
        close(sockfd);  
        //ROS_INFO is the replacement for printf/cout.  
        ROS_INFO("No error.");  
    return 0;  
      
    }  
void spCallback(const std_msgs::String::ConstPtr& msg)
{
	//cout<<"spCallback()\n";
    ROS_INFO("spCallback received: %s\n", msg->data.c_str());
    if(msg->data == "cap_obj")
    {
        cout<<"received data :  cap_obj\n";
        ifcap_obj = 1;
    }
    else if(msg->data == "apple")
    {
        cout<<"received data :  apple\n";
        obj_name = "apple";
        ifapple=1;
    }
    else if(msg->data == "orange")
    {
        cout<<"received data :  orange\n";
        obj_name = "orange";
        iforange=1;
    }
    else 
    {
        cout<<"I heared other things:  "<<msg->data<<"\n";
    }
    //抓制定的物体，确定不同的标签
}
