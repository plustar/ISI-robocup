5.1 Manipulation and object recognition

# 直接说出来接收到的消息，不涉及识别，运行的是 manipulation_sp.py

$ cd 2017_ws
$ source devel/setup.bash
$ roslaunch pi_speech_tutorial manipulation_sp.launch 





5.2   navigation

#  运行的节点是 nav_follow.py
#  节点名字：navsp
#  词库： nav_follow文件夹



 cd 2017_ws
 source devel/setup.bash
 roslaunch pi_speech_tutorial navigation.launch

# 加载词库
 pocketsphinx_continuous -inmic yes -dict /home/isi/2017_ws/src/pi_speech_tutorial/nav_follow/nav_follow.dic -lm /home/isi/2017_ws/src/pi_speech_tutorial/nav_follow/nav_follow.lm


5.3   person recognition


#  不用加载词库，自己启动
#  运行的是 person_recog.py节点

$ cd 2017_ws
$ source devel/setup.bash
$ roslaunch pi_speech_tutorial person_recog.launch

5.4  speech recognition

# 待完善




5.6

# 在general.py  general_executor.py上改动
# launch 文件   general.launch
# 词库  general_corpus文件夹，需要更新









