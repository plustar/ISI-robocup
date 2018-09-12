#!/usr/bin/env python
#coding:UTF-8
#上句表示程序中可以有中文，包括注释
"""
    talkback.py - Say back what is heard by the pocketsphinx recognizer.
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String
from std_msgs.msg import Char
#from std_msgs.msg import Int8

from sound_play.libsoundplay import SoundClient

class gpsr:
      
    def __init__(self):

        rospy.on_shutdown(self.cleanup)
        #self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
	self.voice = rospy.get_param("~voice", "voice_don_diphone") 
        self.wavepath = rospy.get_param("~wavepath", "")
	
	# Intiate Dicts for storing msgs 
#        self.temp = {'mission' : '', 'object': '', 'src_loc' : '', 'dst_loc' : '', 'target' : ''}     # store the words recognized each time
	# 
        self.keywords_to_temp_temp = {'object': ['key','pepsi','nongfu-spring','green-tea','shuttlecock','cup']}
	
	self.speakout1 = ''

        self.soundhandle = SoundClient() 
        rospy.sleep(1)
        self.soundhandle.stopAll()
        rospy.sleep(1) 
        self.soundhandle.say("Ready", self.voice) 
        self.final_recognizer_begin = rospy.Publisher('final_recognizer_begin', String, queue_size=10)
#        self.final_detect_begin = rospy.Publisher('final_detect_begin', String, queue_size=10)
        rospy.Subscriber('recognizer_output', String, self.recognition)
	rospy.Subscriber('Answer', String, self.speakout)  

    def get_temp_temp(self, data):
        for (temp, keywords) in self.keywords_to_temp_temp.iteritems():
            for word in keywords:  
		if data.find(word) > -1:
			return word
            return ''

    def recognition(self, msg) :
	msg.data = msg.data.lower()
#	print msg.data
	if msg.data.find('kamerider') > -1:
		if msg.data.find('what-is-this') > -1 :
	#	or msg.data.find('what is')
			self.final_recognizer_begin.publish('w')
		self.object_name = self.get_temp_temp(msg.data)
		if self.object_name != '' :
			self.final_recognizer_begin.publish(self.object_name)
	      		self.soundhandle.say('Ok now I am ready to study', self.voice)
	       	rospy.sleep(2)
#说出接受到的内容
    def speakout(self, msg) :
	msg.data = msg.data.lower()
	if msg.data == 'ok' :
		self.soundhandle.say('now I have learned the answer', self.voice)
	else:
		self.speakout1 = 'this is an' + msg.data
		self.soundhandle.say(self.speakout1, self.voice)
		rospy.sleep(3)
		self.speakout1 = ''
	
    def cleanup(self):
        rospy.loginfo("Shutting down gpsr node...")

if __name__=="__main__":
    rospy.init_node('gpsr')
    try:
        gpsr()
        rospy.spin()
    except:
        pass

