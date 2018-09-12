#include <ros/ros.h>
#include <iostream>
#include <std_msgs/String.h>
// PCL 的相关的头文件
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
//滤波的头文件
#include <pcl/filters/voxel_grid.h>
#include "algorithm"

using namespace std;

class DetectBar
{
public:
  ros::NodeHandle nh;   //声明节点的名称
  ros::Subscriber image_sub;
  ros::Subscriber turn_sub;
  ros::Publisher pub;

  double min_dist[2];
  int orient;
  bool _enable;

  DetectBar(ros::NodeHandle &nh):nh(nh)
  {
    orient = -1;
    _enable = 0;
  }
  ~DetectBar(){}
  
  void init()
  {
    pub = nh.advertise<std_msgs::String> ("/barplace", 1);
    image_sub = nh.subscribe ("/camera/depth/points", 1, &DetectBar::cloud_cb, this);
    turn_sub = nh.subscribe ("/turnleft", 1, &DetectBar::turnleft_cb, this);
  }
  void turnleft_cb (const std_msgs::String& msg)
  {
    ++orient;
    _enable = 1;
    cout << "turn_cb times:"<<orient<<"enable:"<<_enable<<endl;
  }


  void cloud_cb (const sensor_msgs::PointCloud2ConstPtr& input)  //特别注意的是这里面形参的数据格式
  {
    cout<<"cloud_cb"<<endl;
    if((orient == 0||orient == 2)&&_enable == 1)
      {
        // 声明存储原始数据与滤波后的数据的点云的 格式
        pcl::PCLPointCloud2* cloud = new pcl::PCLPointCloud2;    //原始的点云的数据格式
        pcl::PCLPointCloud2ConstPtr cloudPtr(cloud);
        pcl::PCLPointCloud2 cloud_filtered;     //存储滤波后的数据格式

        // 转化为PCL中的点云的数据格式
        pcl_conversions::toPCL(input, cloud);

      
        // 进行一个滤波处理
        pcl::VoxelGrid<pcl::PCLPointCloud2> sor;   //实例化滤波
        sor.setInputCloud (cloudPtr);     //设置输入的滤波
        sor.setLeafSize (0.1, 0.1, 0.1);   //设置体素网格的大小
        sor.filter (cloud_filtered);      //存储滤波后的点云

        int count = 0;
        double sum = 0;
        for(vector<pcl::uint8_t>::iterator it = cloud_filtered.data.begin();it!=cloud_filtered.data.end();++it)
          {
            count++;
          }
        int ucount = count/3;

        sort(cloud_filtered.data.begin(),cloud_filtered.data.end());

        for(vector<pcl::uint8_t>::iterator it = cloud_filtered.data.begin();it!=cloud_filtered.data.begin()+ucount;++it)
          {
            sum += *it;
          }
        sum = sum/ucount;
        min_dist[orient/2] = sum;
        cout << "cloud_cb orient " << orient << " sum " << sum << endl;
        sum = 0;
        _enable = 0;
      }
    if(orient == 3)
      {
        std_msgs::String str;
        cout<<"orient = = = = = = 3"<<endl;
        if(min_dist[0] < min_dist[1])
          {
            str.data = "left";
          }
        else
          {
            str.data = "right";
          }
        
        pub.publish(str);
        _enable = 0;
        ++orient;
      }

  }

};

int main (int argc, char** argv)
{
  // 初始化 ROS节点
  ros::init (argc, argv, "my_pcl_tutorial");
  ros::NodeHandle nh("~");
  DetectBar bar(nh);
  bar.init();
  ros::spin ();
  exit(0);
  return 0;
}


