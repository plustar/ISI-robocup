#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8
 
def talker():
    pub = rospy.Publisher('recognizer_output', String, queue_size=10)
#    pub = rospy.Publisher('final_recognizer_begin', String, queue_size=10)
#    pub4 = rospy.Publisher('final_speakout', String, queue_size=10)
    pub1 = rospy.Publisher('nav_output', String, queue_size=10)
    pub2 = rospy.Publisher('gpsr_mstype', Int8, queue_size=10)
    pub3 = rospy.Publisher('gpsr_mission', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(0.2) # 10hz
    while not rospy.is_shutdown():
        hello_str = "kamerider german-count"
#	hello_str = "pepsi"
# kamerider-yes
# kamerider-no
        pub.publish(hello_str)
#	pub1.publish("arrive")
#	pub2.publish(0)
#	pub3.publish("time")
#	pub4.publish('pear')
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
