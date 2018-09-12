# pi_speech_tutorial
# 运行语音部分的步骤
GPSR:
cd 2017_ws
source devel/setup.bash
roslaunch pi_speech_tutorial gpsr_object_dec.launch

pocketsphinx_continuous -inmic yes -dict /home/isi/2017_ws/src/pi_speech_tutorial/dect_corpus/corpus.dic -lm /home/isi/2017_ws/src/pi_speech_tutorial/dect_corpus/corpus.lm

storing:????????????


人脸识别：
cd 2017_ws
source devel/setup.bash
roslaunch pi_speech_tutorial recog.launch
问题：
Inbound TCP/IP connection failed: connection from sender terminated before handshake header received. 0 bytes were received. Please check sender for additional details.




navigation:

cd 2017_ws
source devel/setup.bash
roslaunch pi_speech_tutorial navigation.launch


新终端：

pocketsphinx_continuous -inmic yes -dict /home/isi/2017_ws/src/pi_speech_tutorial/nav_follow/nav_follow.dic -lm /home/isi/2017_ws/src/pi_speech_tutorial/nav_follow/nav_follow.lm


EEgpsr:

cd 2017_ws
source devel/setup.bash
roslaunch pi_speech_tutorial EEgpsr.launch


新终端：

pocketsphinx_continuous -inmic yes -dict /home/isi/2017_ws/src/pi_speech_tutorial/nav_follow/nav_follow.dic -lm /home/isi/2017_ws/src/pi_speech_tutorial/nav_follow/nav_follow.lm


#help_me_carry
navigation:

cd 2017_ws
source devel/setup.bash
roslaunch pi_speech_tutorial nav_help.launch


新终端：

pocketsphinx_continuous -inmic yes -dict /home/isi/2017_ws/src/pi_speech_tutorial/nav_follow/nav_help.dic -lm /home/isi/2017_ws/src/pi_speech_tutorial/nav_follow/nav_help.lm

单独启动:
rostopic pub Point std_msgs/String -- b

