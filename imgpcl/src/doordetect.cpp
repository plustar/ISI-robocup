#include <ros/ros.h>
#include <iostream>
#include <std_msgs/String.h>
// PCL 的相关的头文件
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/io/png_io.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
//滤波的头文件
#include <pcl/filters/voxel_grid.h>
#include <string>
#include "algorithm"

using namespace std;

class DetectDoor
{
	public:
	ros::NodeHandle nh;   //声明节点的名称
	ros::Subscriber image_sub;
	ros::Publisher door_pub;
	bool _enable;
	int pprevious;
	int previous;
	int current;

	DetectDoor(ros::NodeHandle &nh):nh(nh)
	{
	_enable = 1;
	}
	~DetectDoor(){}

	void init()
	{
	cout<<"INIT..........................."<<endl;
	door_pub = nh.advertise<std_msgs::String> ("/doorstate", 1);
	image_sub = nh.subscribe<sensor_msgs::PointCloud2> ("/camera/depth_registered/points", 10, &DetectDoor::cloud_Cb, this);
	current = 0;
	previous = 0;
	pprevious = 0;
	}

	void cloud_Cb (const sensor_msgs::PointCloud2ConstPtr& input)  //特别注意的是这里面形参的数据格式
	{
		if(_enable == 1)
		{
			// 声明存储原始数据与滤波后的数据的点云的 格式
			pcl::PCLPointCloud2* cloud = new pcl::PCLPointCloud2;    //原始的点云的数据格式
			pcl::PCLPointCloud2ConstPtr cloudPtr(cloud);
			pcl::PCLPointCloud2 cloud_filtered;     //存储滤波后的数据格式

			// 转化为PCL中的点云的数据格式
			pcl_conversions::toPCL(*input, *cloud);

			int i = 0;
			int sum = 0;
			int count = 0;
			for(vector<pcl::uint8_t>::iterator it = cloud->data.begin();it!=cloud->data.end(); ++it, ++i)
			{
				if((i%cloud->width<cloud->width*2/3)&&(i%cloud->width>cloud->width*1/3))
				{
					if((i>cloud->width*cloud->height*1/3)&&(i<cloud->width*cloud->height*2/3))
					{
						sum+=*it;
						count++;
					}
				}
			}
			cout<<" sum: "<<sum<<" count: "<<count<<endl;
			pprevious = previous;
			previous = current;
			current = sum / count;
			cout<<" current: "<<current<<endl;
			if((current < (int((pprevious + previous) / 2) + 1)) && pprevious != 0)
			{
				std_msgs::String str;
				str.data = "opened";
				door_pub.publish(str);
				cout<<"The door has been opened"<<endl;
				_enable = 0;
			}
		}
	}
};

int main (int argc, char** argv)
{
	// 初始化 ROS节点
	ros::init (argc, argv, "doordetect");
	cout<<"main....................."<<endl;
	ros::NodeHandle nh("~");
	DetectDoor door(nh);
	door.init();
	ros::spin ();
	//exit(0);
	return 0;
}
