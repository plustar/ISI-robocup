#education
############################
#speech

    #图像
        cd 2017_ws
        source devel/setup.bash
        roslaunch imgpcl gender2017.launch
        单独运行需要：
        rostopic pub /turn_robot std_msgs/String -- ok
#help me carry
    #图像
        cd 2017_ws
        source devel/setup.bash
        roslaunch imgpcl find_person2017.launch
        单独运行：
        roslaunch imgpcl find_person2017_full.launch
        rostopic pub /arm_released std_msgs/String -- find_person
    #机械臂
        cd 2017_ws
        source devel/setup.bash
        sudo dmesg -c
        sudo chmod 666 /dev/ttyUSB0
        roslaunch arm_2017 ed_arm_carry.launch
        单独运行：
        
#restaurant
    #机械臂
        cd 2017_ws
        source devel/setup.bash
        sudo dmesg -c
        sudo chmod 666 /dev/ttyUSB0
        roslaunch arm_2017 ed_arm_restaurant.launch
    #图像
        cd 2017_ws
        source devel/setup.bash
        roslaunch imgpcl ed_obj_restaurant.launch
        单独运行需要：
        rostopic pub /nav2image std_msgs/String -- reached_table
        rostopic pub /gpsr_object std_msgs/String -- potato-chips

    # 运行语音部分的步骤
        # 运行的是 gpsr_detect_object.py  以及  talkback_gpsr2.py
        # 词库 dect_corpus 文件夹
##########################################################################
#GPSR:
    #机械臂
    cd 2017_ws
    source devel/setup.bash
    sudo dmesg -c
    sudo chmod 666 /dev/ttyUSB0
    roslaunch arm_2017 arm_gpsr2017.launch
    #图像
    cd 2017_ws
    source devel/setup.bash
    roslaunch imgpcl obj_gpsr2017.launch
    单独运行需要：
    rostopic pub /nav2image std_msgs/String -- grasp
    rostopic pub /gpsr_object std_msgs/String -- green-tea

    # 运行语音部分的步骤
    # 运行的是 gpsr_detect_object.py  以及  talkback_gpsr2.py
    # 词库 dect_corpus 文件夹
    GPSR:
    cd 2017_ws
    source devel/setup.bash
    roslaunch pi_speech_tutorial gpsr_object_dec.launch 

    pocketsphinx_continuous -inmic yes -dict /home/isi/2017_ws/src/pi_speech_tutorial/dect_corpus/corpus.dic -lm /home/isi/2017_ws/src/pi_speech_tutorial/dect_corpus/corpus.lm
    
    
    
    #导航
    
#Storing:
    机械臂：
        cd 2017_ws
        source devel/setup.bash
        sudo dmesg -c
        sudo chmod 666 /dev/ttyUSB0
        roslaunch arm_2017 arm_storing2017.launch
    图像：
        cd 2017_ws
        source devel/setup.bash
        roslaunch imgpcl storing2017.launch

    运行： rostopic pub /nav2image std_msgs/String -- reached_table
#人脸：
cd 2017_ws
source devel/setup.bash
    训练：rosrun imgpcl gender_train
    针对：2016
        roslaunch imgpcl gender2016hsn.launch
        语音：
        cd 2017_ws
        source devel/setup.bash
        roslaunch pi_speech_tutorial recog.launch
    
    针对2017:无操作者识别
        roslaunch imgpcl gender2017.launch

类似错误：
[hog_followme-28] process has died [pid 10308, exit code -11, cmd /home/isi/2017_ws/devel/lib/imgpcl/hog_followme __name:=hog_followme __log:=/home/isi/.ros/log/cbf6be06-1615-11e7-a290-ac2b6eb423d2/hog_followme-28.log].
log file: /home/isi/.ros/log/cbf6be06-1615-11e7-a290-ac2b6eb423d2/hog_followme-28*.log
