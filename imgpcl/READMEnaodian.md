#final
############################
#脑电控制机械臂抓取
#机械臂
cd 2017_ws
source devel/setup.bash
sudo dmesg -c
sudo chmod 666 /dev/ttyUSB0
roslaunch arm_2017 ed_arm_final.launch
#图像
cd 2017_ws
source devel/setup.bash
roslaunch imgpcl naodian.launch
单独运行需要：
rostopic pub  socket2topic_nd  std_msgs/String -- a

# 运行语音部分的步骤
# 运行的是 gpsr_detect_object.py  以及  talkback_gpsr2.py
# 词库 dect_corpus 文件夹
# 直接说出来接收到的消息，不涉及识别，运行的是 manipulation_sp.py

cd 2017_ws
source devel/setup.bash
roslaunch pi_speech_tutorial manipulation_sp.launch     
#
