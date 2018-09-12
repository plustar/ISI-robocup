#!/usr/bin/env python

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
        self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
	#self.voice = rospy.get_param("~voice", "voice_don_diphone") 
        self.wavepath = rospy.get_param("~wavepath", "")
	
        self.keywords_to_temp_temp = {'table_number': ['table-one','table-two']}
		
	self.table_number = ''
	self.nav_arrive = ''

        self.soundhandle = SoundClient() 
        rospy.sleep(1)
        self.soundhandle.stopAll()
        rospy.sleep(1) 
        self.soundhandle.say("Ready", self.voice) 
#        self.final_detect_begin = rospy.Publisher('final_detect_begin', String, queue_size=10)
        rospy.Subscriber('recognizer_output', String, self.recognition)
        rospy.Subscriber('nav_arrive', String, self.arrive)  

    def get_temp_temp(self, data):
        for (temp, keywords) in self.keywords_to_temp_temp.iteritems():
            for word in keywords:  
		if data.find(word) > -1:
			return word
            return ''

    def arrive(self, msg) :
    	self.nav_arrive = msg.data

    def recognition(self, msg) :
	msg.data = msg.data.lower()
	self.table_number = self.get_temp_temp(msg.data)
	if self.nav_arrive == "arrive" :
		if msg.data.find('kamerider') > -1 :
			if self.table_number != '' :
				speakout = "ok this " + self.table_number
	       		else :
	       			speakout = "dear operator please repeat the table number"
			self.soundhandle.say(speakout, self.voice)
	       		rospy.sleep(2)	       			
	       		self.nav_arrive = ''
    def cleanup(self):
        rospy.loginfo("Shutting down gpsr node...")

if __name__=="__main__":
    rospy.init_node('gpsr')
    try:
        gpsr()
        rospy.spin()
    except:
        pass

