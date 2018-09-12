#!/usr/bin/env python

"""
    talkback.py - Say back what is heard by the pocketsphinx recognizer.
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
import datetime
import re
import time
from std_msgs.msg import String
from std_msgs.msg import Int8
from std_msgs.msg import UInt8
import roslaunch
import os

from sound_play.libsoundplay import SoundClient
isokay = 0
isnum = 0

class TalkBack:

	def __init__(self):
		
		rospy.on_shutdown(self.cleanup)
		#self.voice = rospy.get_param("~voice", "voice_don_diphone")
		self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
		self.wavepath = rospy.get_param("~wavepath", "")

		self.pub = rospy.Publisher('isfinish', String, queue_size=20)
		# Create the sound client object
		self.soundhandle = SoundClient() 
		rospy.sleep(1)
		self.soundhandle.stopAll()
		rospy.sleep(1)
		self.finished = 0
		self.start = ''
		self.mstype_out1 = 5
		self.mission_out1 = ''
		self.i = 0
		self.h = 0
		self.say_objnum=''
		rospy.loginfo("To deal with the mission...")
		self.package = "voice"
		self.executable = "talker"
		self.node = roslaunch.core.Node(self.package, self.executable)
		self.launch = roslaunch.scriptapi.ROSLaunch()
		self.launch.start()
		self.gpsr_name = rospy.Publisher('gpsr_name', String, queue_size=10)
		self.gpsr_missiontype1 = rospy.Publisher('gpsr_mstype_out', Int8, queue_size = 10)
		self.gpsr_mission1 = rospy.Publisher('gpsr_mission_out', String, queue_size=10)

		rospy.Subscriber('nav_output', String, self.control)
		rospy.Subscriber('gpsr_mstype', Int8, self.mstype_out)
		rospy.Subscriber('gpsr_mission', String, self.mission_out)
		rospy.Subscriber('gpsr_mstype_out', Int8, self.mstype_out)
		rospy.Subscriber('gpsr_mission_out', String, self.mission_out)
		rospy.Subscriber('recognizer/output', String, self.say_grasp)
		rospy.Subscriber('det_obj_num', String, self.say_num)

	def mstype_out(self, msg):
		self.mstype_out1 = msg.data
#		print self.mstype_out1
		self.gpsr_missiontype1.publish(self.mstype_out1)
	def mission_out(self, msg):
		msg.data = msg.data.lower()
		self.mission_out1 = msg.data
		if self.i == 0:
		    self.gpsr_mission1.publish(self.mission_out1)
	def say_grasp(self,msg):
		msg.data = msg.data.lower()
		self.soundhandle.say(msg.data, self.voice)
	def control(self, msg):
		msg.data = msg.data.lower()

		if msg.data.find('arrive') > -1:
			#rospy.Subscriber('gpsr_mstype_out', Int8, self.dispatch)
			#rospy.sleep(10)
			#self.soundhandle.say('here you are', self.voice)
			rospy.Subscriber('recognizer_output', String, self.finish_mission)

			rospy.sleep(3)

#		self.process.stop()
#		print self.i
		if self.i == 0:
			os.system("rosnode kill /gpsr")
			self.i = 1  		                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
	def dispatch(self, msg):
		if self.h == 0:
			if(msg.data == 0):
				rospy.Subscriber('gpsr_mission_out', String, self.inform)
			elif(msg.data == 1):
				self.i = 1
				self.soundhandle.say("dear operator",self.voice)
				rospy.sleep(2)
				self.soundhandle.say("i am ready for your question", self.voice)
				rospy.sleep(3)
				print 555
				rospy.Subscriber('gpsr_mission', String, self.ans_a_question)
			elif(msg.data == 2):
				rospy.Subscriber('gpsr_mission_out', String, self.ask_a_question)
			self.h = 1
#		self.gpsr_mstype_out = 5
	
	
	def finish_mission(self,msg):
		msg.data = msg.data.lower()
		global isnum
		global isokay
		if isokay == 0:
			if msg.data.find('kamerider-okay') > -1:
				isnum = 1
				isokay = 1
				self.soundhandle.say("Okay,here you are", self.voice)
				rospy.sleep(1)
				self.pub.publish('finish')
		if isnum == 1 and isokay == 1:
			if msg.data.find('objects') > -1 or msg.data.find('how-many') > -1:
				self.soundhandle.say('there are' + self.say_objnum+ 'objects',self.voice)
				
	def say_num(self,msg):
		
		msg.data = msg.data.lower()
		global isnum
		self.say_objnum=msg.data
		isnum = 0
	
	def inform(self, msg):
		msg.data = msg.data.lower()
		if msg.data.find('time') > -1:
			curtime = time.strftime("%H:%M %p", time.localtime())
			self.soundhandle.say("it is " + curtime, self.voice)
			rospy.sleep(5)

		if msg.data.find('day') > -1:
			timetuple = time.localtime()
			self.soundhandle.say("today is "+ self.week[timetuple[6]], self.voice)
			rospy.sleep(5)
				
		if msg.data.find('date') > -1:
			timetuple = time.localtime()
			_year = time.strftime("%Y", timetuple)
			_month = self.month[timetuple[1]]	
			_day = time.strftime("%d", timetuple)
			self.soundhandle.say("today is "+ _month + " the " + _day + "th " + _year, self.voice)
			rospy.sleep(10)
		
		if msg.data.find('name') > -1:
			self.soundhandle.say("my name is kamerider", self.voice)
			rospy.sleep(5)

		if msg.data.find('team-name') > -1:
			self.soundhandle.say("my team's name is kamerider", self.voice)
			rospy.sleep(5)
		
		os.system("rosnode kill /talkback")
		
	def answer_a_question(self, msg):
		msg.data = msg.data.lower()
		if msg.data.find('kamerider') > -1:
			if msg.data.find('german-count') > -1 or msg.data.find('invented the zeppelin') > -1 or msg.data.find('invented the the zeppelin') > -1 or msg.data.find('invented zeppelin') > -1 :
				self.soundhandle.say('Count von Zeppelin invented the zeppelin', self.voice)
				rospy.sleep(4)
			else :
				self.soundhandle.say('Dear opreater', self.voice)
				rospy.sleep(1.5)
				self.soundhandle.say('Please repeat your question louder and slower', self.voice)
				rospy.sleep(3)
			msg.data = ''
		os.system("rosnode kill /talkback")

	def ask_a_question(self, msg):
		msg.data = msg.data.lower()
		if msg.data.find('name') > -1:
			self.soundhandle.say("what is your name", self.voice) 
			rospy.sleep(5)
			rospy.Subscriber('recognizer_output', String, self.lis_to_ans)
		
	
	def get_keyword(self, data):
		for (temp, keywords) in self.names.iteritems():
			for word in keywords:
				if data.find(word) > -1:
					return word
			return 'None'

	def lis_to_ans(self, msg):
		msg.data = msg.data.lower()
		keyword = self.get_keyword(msg.data)
		if keyword != 'None':
			self.soundhandle.say("Hello " + keyword, self.voice)
			rospy.sleep(10)
			print 1
			self.temp_pub = rospy.Publisher('information', String, queue_size=20)
			keyword = self.get_keyword(msg.data)
			self.temp_pub.publish(keyword)
			keyword = 'None'
			os.system("rosnode kill /talkback")	
			os.system("rosnode kill /soundplay_node")	
			os.system("rosnode kill /talker")
			os.system("rosnode kill /server2topic")		
	def cleanup(self):
		rospy.loginfo("Shutting down talkback node...")

	#def control(self, msg):
	#	if msg.data.find('arrive') > -1:
	#		TalkBack()
if __name__=="__main__":	
	rospy.init_node('talkback')
	try:
	#rospy.Subscriber('nav_output', String, self.control) 
		TalkBack()
		rospy.spin()
	except:
		pass

