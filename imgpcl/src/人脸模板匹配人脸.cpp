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
#include "imgpcl/objectDetect.hpp"
using namespace std;
using namespace message_filters;
using namespace sensor_msgs;

typedef pcl::PointCloud<pcl::PointXYZRGBA> PointCloud;
typedef boost::shared_ptr<PointCloud> PointCloudPtr;
typedef boost::shared_ptr<const PointCloud> PointCloudConstPtr;
//实现时间同步性
typedef message_filters::sync_policies::ApproximateTime<sensor_msgs::Image, sensor_msgs::PointCloud2> MySyncPolicy;
typedef message_filters::sync_policies::ApproximateTime<sensor_msgs::Image, sensor_msgs::Image> MySyncPolicy2;
#define PI 3.14159
//#define TIME_MODE 1
struct PathPoint
{
    int state;
    float vel;
    float time;
};
vector<PathPoint> vppt;             //储存反馈调节时的调节参数

ros::Publisher pos_pub;             //发布pos位置信息
ros::Publisher voice_pub;           //向voice发消息
ros::Publisher move_pub;            //向navigation发消息，微调机器人
ros::Publisher nav_pub;             //向nav发消息，表明状态转移

const int temp_num = 3;             //需要改的地方------模板的个数
IplImage* tempImage[temp_num];      //模板图像
char object_name[temp_num][100];    //模板名称

char *window_name;                  //显示设置
CvFont font;
CvScalar textColor;
char text[200];

int state = 0;                     //状态标记，-1  --  什么都不做
                                    //0 - 开始检测，检测不到
                                    //1 - 检测，调整位置中
                                    //2 - 检测到，并且已调节好
//时间同步化好的回调函数，获取rgb图像和点云数据
void callback(const ImageConstPtr& image, const PointCloud2::ConstPtr& Callback_Points);

//物体识别程序，detection_method(1-单尺度，2-多尺度)， temp 多模板图像指针， temp_num-模板个数，res-返回的结果
//一般选2
bool objectRec(IplImage *image, int detection_method, IplImage** temp, int temp_num, objectRecT& res);

int main(int argc, char **argv)
{
	//-------------------------初始化全局变量------------------------------//
	cvInitFont(&font,CV_FONT_HERSHEY_PLAIN, 2, 2, 0, 1, CV_AA);  //initialize font
	textColor = CV_RGB(255,0,0);
	window_name = "detect";
	cvNamedWindow(window_name, 1);

	ifstream fin("/home/kris/catkin_ws/src/imgpcl/template/listzzk.txt");   //注意注意-------如果复制到其他地方，修改目录
	for(int i=0;i<temp_num;i++) //获取三个模板的直方图；
    {
        char name[100];
        fin>>name;
        char tempName[255];
        sprintf(tempName, "/home/kris/catkin_ws/src/imgpcl/template/%s", name);
        tempImage[i] = cvLoadImage(tempName);
        ROS_INFO("Load template: %s\n", tempName);

        name[strlen(name)-4] = '\0';
        strcpy(object_name[i], name);
    }

	//------------------------------初始化ros---------------------------------//
	ros::init(argc, argv, "objectdetect");
	ros::NodeHandle nh_;

    //三个话题的同步性，image_raw, depth/image, depth/points
    int global_subscriber_queue_size = 1;

    message_filters::Subscriber<sensor_msgs::Image> visual_sub_ (nh_, "/camera/rgb/image_raw", global_subscriber_queue_size);
   // message_filters::Subscriber<sensor_msgs::Image> depth_sub_(nh_, "/camera/depth/image", global_subscriber_queue_size);
    message_filters::Subscriber<sensor_msgs::PointCloud2> cloud_sub_(nh_, "/camera/depth/points", global_subscriber_queue_size);
    message_filters::Synchronizer<MySyncPolicy> sync_(MySyncPolicy(1),  visual_sub_, cloud_sub_);
    sync_.registerCallback(boost::bind(&callback, _1, _2));

	ros::spin();

	return 0;
}
bool objectRec(IplImage *image, int detection_method, IplImage** temp, int temp_num, objectRecT& res)
{
    static int image_num = 0;
	objectRecT *object_recs = new objectRecT[temp_num];
	bool return_value = false;
	for(int i=0; i<temp_num; i++)
	{
	    if(detection_method == 1)
        {
            //sidewindow+hue
            if( sWindowHueDetect(image, temp[i], object_recs[i], 0.6) )  //0.6 是相似度，可改（0是完全不相似，1是完全相似）
            {
                object_recs[i].flag = 1;
            }
            else
            {
                object_recs[i].flag = 0;
            }

        }
        else if(detection_method == 2)
        {
            //sidewindow+hue
            if( sWindowHueDetectP(image, temp[i], object_recs[i], 0.6) )
            {
                object_recs[i].flag = 1;
            }
            else
            {
                object_recs[i].flag = 0;
            }
        }
    }

    int object_label = -1;
    float sim = -1;
   	for(int i=0; i<temp_num; i++)
   	{
   	    if(sim < object_recs[i].similarity && object_recs[i].flag == 1)
   	    {
   	        sim = object_recs[i].similarity;
   	        object_label = i;
   	    }
   	}

   	if(object_label != -1)
   	{
   	    res.flag = 1;
   	    strcpy(res.name, object_name[object_label]);
   	    res.rc = object_recs[object_label].rc;
   	    res.similarity = object_recs[object_label].similarity;
   	    return_value = true;
   	}

	cvShowImage(window_name, image);
	cvWaitKey(100);

	return return_value;
}
void callback(const ImageConstPtr& image, const PointCloud2::ConstPtr& Callback_Points)
{

    //cout<<"synchronize...\n";
    if(state == -1 || state == 2)
        return;

    cout<<"state = "<<state<<"\n";
    //---------------获取彩色图像------------------//
    cv_bridge::CvImagePtr cv_ptr;
	try
	{
	   	cv_ptr = cv_bridge::toCvCopy(image, sensor_msgs::image_encodings::BGR8);
	}
	catch (cv_bridge::Exception& e)
	{
	     	ROS_ERROR("cv_bridge exception: %s", e.what());
	      	return;
	}
	IplImage ipl_imgColor = cv_ptr->image;
	IplImage *imgColor= cvCloneImage(&ipl_imgColor);
	//cvNamedWindow("color");
	//cvShowImage("color", imgColor);

	//---------------获得点云数据------------------//
    pcl::PointCloud<pcl::PointXYZ> points_xyz;
    pcl::fromROSMsg (*Callback_Points, points_xyz);

    objectRecT obj;
    object::pos p;
    bool is_find = false;
#ifdef TIME_MODE
    time_t t1 = time(NULL);
    tm* tt1 = localtime(&t1);
    cout<<"时间1 :  "<<tt1->tm_min<<":"<<tt1->tm_sec<<"\n";
#endif
    is_find = objectRec(imgColor, 1, tempImage, temp_num, obj);
#ifdef TIME_MODE
    time_t t2 = time(NULL);
    tm* tt2 = localtime(&t2);
    cout<<"时间2 :  "<<tt2->tm_min<<":"<<tt2->tm_sec<<"\n";
    cout<<"所需的时间 = "<<tt2->tm_min-tt1->tm_min<<":"<<tt2->tm_sec-tt1->tm_sec<<"\n";
#endif
    if(is_find)
    {
        //显示
        cvRectangle(imgColor, cvPoint(obj.rc.x, obj.rc.y), cvPoint(obj.rc.x+obj.rc.width-1, obj.rc.y+obj.rc.height-1), CV_RGB(0, 255, 0), 2, 8, 0);
   	    ROS_INFO("recognized results:  object = %s, similarity = %f\n", obj.name, obj.similarity);
   	    strcpy(text, obj.name);
   	    cvPutText(imgColor, text, cvPoint(obj.rc.x, obj.rc.y), &font, textColor);

   	    //转换为三维坐标
   	    ComputeClusterCenter(points_xyz, obj.rc, p);
   	    object::pos newp;
   	    ROS_INFO("Position: %f %f %f\n", p.x, p.y, p.z);

#ifdef TIME_MODE
        time_t t3 = time(NULL);
        tm* tt3 = localtime(&t3);
        cout<<"时间3 :  "<<tt3->tm_min<<":"<<tt3->tm_sec<<"\n";
#endif

   	}
   	else
   	{
   	    ROS_INFO("recognized results:  nothing\n");
   	    state = 0;
   	}
   	cvShowImage(window_name, imgColor);
	cvWaitKey(100);

    if(state == 0)  //检测不到的情况
    {
        cout<<" can not find any object\n";
    }
    if(state == 1)  //检测到需要调整
    {
        cout<<"robot is adjusting\n";
    }
    cvReleaseImage(&imgColor);

}

