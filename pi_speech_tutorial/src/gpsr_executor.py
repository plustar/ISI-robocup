#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#上句表示程序中可以有中文，包括注释
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
import roslaunch
import os

from sound_play.libsoundplay import SoundClient


class TalkBack:
      
    	def __init__(self):
		self.month = ['january','february','march','april','may','june','july','august','september','october','november','december']
		self.week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
		self.names ={'name':['alex','angel','eve','jamie','jane','liza','melissa','tracy','robin','sophia','alex','angel','edward','homer','jamie','john','kevin','kurt']}
        	rospy.on_shutdown(self.cleanup)
        	#self.voice = rospy.get_param("~voice", "voice_don_diphone")
		self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
       		self.wavepath = rospy.get_param("~wavepath", "")
        
		self.pub = rospy.Publisher('mission_complete', String, queue_size=20)
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
        	rospy.loginfo("To deal with the mission...")
		self.package = "voice"
		self.executable = "talker"
		self.node = roslaunch.core.Node(self.package, self.executable)
		self.launch = roslaunch.scriptapi.ROSLaunch()
		self.launch.start()
#		self.process = launch.launch(node)
#		print self.process.is_alive()
        # self.open_object_name = rospy.Publisher('open_object_name', String, queue_size=10)
        # rospy.init_node('command', anonymous=True)
        # Subscribe to the recognizer output
        # rospy.Subscriber('speech_recognition_start', String, self.start)
		self.gpsr_name = rospy.Publisher('gpsr_name', String, queue_size=10)
		self.gpsr_missiontype1 = rospy.Publisher('gpsr_mstype_out', Int8, queue_size = 10)
		self.gpsr_mission1 = rospy.Publisher('gpsr_mission_out', String, queue_size=10)
		rospy.Subscriber('nav_output', String, self.control)
		rospy.Subscriber('gpsr_mstype', Int8, self.mstype_out)
		rospy.Subscriber('gpsr_mission', String, self.mission_out)
		rospy.Subscriber('gpsr_mstype_out', Int8, self.mstype_out)
		rospy.Subscriber('gpsr_mission_out', String, self.mission_out)
	def mstype_out(self, msg):
		self.mstype_out1 = msg.data
#		print self.mstype_out1
		self.gpsr_missiontype1.publish(self.mstype_out1)
	def mission_out(self, msg):
		msg.data = msg.data.lower()
		self.mission_out1 = msg.data
		if self.i == 0:
			self.gpsr_mission1.publish(self.mission_out1)
	def control(self, msg):
		msg.data = msg.data.lower()
		if msg.data.find('arrive') > -1:
			rospy.Subscriber('gpsr_mstype_out', Int8, self.dispatch)
#		self.process.stop()
#		print self.i
		if self.i == 0:
			os.system("rosnode kill /talkback_gpsr")#开始执行任务之后，关闭talkback_gpsr.py,即不再跟人对话
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
				#rospy.Subscriber('gpsr_mission', String, self.ans_a_question)
				rospy.Subscriber('recognizer_output', String, self.answer_a_question)
			elif(msg.data == 2):
				rospy.Subscriber('gpsr_mission_out', String, self.ask_a_question)
			self.h = 1
#		self.gpsr_mstype_out = 5
			
		#回答问题
	def inform(self, msg):
		msg.data = msg.data.lower()
		if msg.data.find('time') > -1:
			curtime = time.strftime("%H:%M %p", time.localtime())
			self.soundhandle.say("it is "+ curtime, self.voice)
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
			elif msg.data.find('first-president') > -1 or msg.data.find('the-usa') > -1 : 
				self.soundhandle.say('george washington was the first president of america', self.voice)
				rospy.sleep(4)
			elif msg.data.find('titanic built') > -1 or msg.data.find('titanic-built') > -1 or msg.data.find('in which city') > -1 :
				self.soundhandle.say('titanic was builted in belfast', self.voice)
				rospy.sleep(4)
			elif msg.data.find('queen-victoria') > -1 or msg.data.find('how-many-children') > -1 :
				self.soundhandle.say('she had nine children', self.voice)
				rospy.sleep(4)
			elif msg.data.find('french-king') > -1 or msg.data.find('the-sun-king') > -1 :
				self.soundhandle.say('louis fourteen was called the sun king', self.voice)
				rospy.sleep(4)
			elif msg.data.find('in england') > -1 or msg.data.find('in the england') > -1 or msg.data.find('northern-frontier') > -1 or msg.data.find('roman-empire') > -1 : 
				self.soundhandle.say('the hadrians wall was the northern frontier of the england', self.voice)
				rospy.sleep(4)
			elif msg.data.find('former-name') > -1 or msg.data.find('new-york') > -1 : 
				self.soundhandle.say('the former name of new york was new amsterdam', self.voice)
				rospy.sleep(4)
			elif msg.data.find('another-name') > -1 or msg.data.find('study of fosslis') > -1 or msg.data.find('study the fosslis') > -1 or msg.data.find('study-of-the-fosslis') > -1 : 
				self.soundhandle.say('the another name for the study of fossils is paleontology', self.voice)
				rospy.sleep(4)
			elif msg.data.find('dragonflies') > -1 or msg.data.find('prefer-to-eat') > -1 : 
				self.soundhandle.say('dragonfilies prefer to eat mosquitoes', self.voice)
				rospy.sleep(4)	
			elif msg.data.find('cannot-fly') > -1 or msg.data.find('but can jump') > -1 : 
				self.soundhandle.say('they are fleas', self.voice)
				rospy.sleep(4)
			elif msg.data.find('european-bison') > -1 : 
				self.soundhandle.say('the name of the european bison is wisent', self.voice)
				rospy.sleep(4)
			elif msg.data.find('called a fish') > -1 or msg.data.find('called fish') > -1 or msg.data.find('called the fish') > -1 or msg.data.find('snake-like') > -1 : 
				self.soundhandle.say('eel fish is called a fish with a snake-like body', self.voice)
				rospy.sleep(4)
			elif msg.data.find('which-plant') > -1 or msg.data.find('canadian-flag') > -1 : 
				self.soundhandle.say('maple plant does the canadian-flag contain', self.voice)
				rospy.sleep(4)
			elif msg.data.find('house-number') > -1 or msg.data.find('simpsons') > -1 : 
				self.soundhandle.say('the house number of the simpsons is seven hundred and forty-two', self.voice)
				rospy.sleep(4)
			elif msg.data.find('in computing') > -1 or msg.data.find('ram short') > -1 or msg.data.find('ram the short') > -1 or msg.data.find('short-for') > -1 : 
				self.soundhandle.say('the random access memory is short for ram', self.voice)
				rospy.sleep(4)
			elif msg.data.find('which-hemisphere') > -1 or msg.data.find('the-most-dinosaur') > -1 or msg.data.find('dinosaur-skeletons') > -1 : 
				self.soundhandle.say('most dinosaur skeletons have been found in the northern hemisphere', self.voice)
				rospy.sleep(4)
			elif msg.data.find('color-is-cobalt') > -1 or msg.data.find('cobalt') > -1 : 
				self.soundhandle.say('the color of cobalt is blue', self.voice)
				rospy.sleep(4)
			elif msg.data.find('which device') > -1 or msg.data.find('use to look at') > -1 or msg.data.find('at-the-stars') > -1 or msg.data.find('at-stars') > -1 : 
				self.soundhandle.say('we also use telescope to look at the stars', self.voice)
				rospy.sleep(4)
			elif msg.data.find('light-intensity') > -1 : 
				self.soundhandle.say('candela also indicates the light intensity', self.voice)
				rospy.sleep(4)
			elif msg.data.find('first-american') > -1 : 
				self.soundhandle.say('alan shepard was the first american in space', self.voice)
				rospy.sleep(4)
			elif msg.data.find('steam-engine') > -1 : 
				self.soundhandle.say('james watt was the inventor of the steam engine', self.voice)
				rospy.sleep(4)
			elif msg.data.find('henry-mill') > -1 : 
				self.soundhandle.say('the typewriter was invented by henry mill', self.voice)
				rospy.sleep(4)
			elif msg.data.find('lightest') > -1 or msg.data.find('existing-metal') > -1 : 
				self.soundhandle.say('aluminium is the lightest existing metal', self.voice)
				rospy.sleep(4)
			elif msg.data.find('primary-colors') > -1 : 
		       		self.soundhandle.say('they are blue yellow and red', self.voice)
				rospy.sleep(4)
			elif msg.data.find('planet') > -1 or msg.data.find('nearest-the-sun') > -1 : 
				self.soundhandle.say('the planet nearest-the-sun is mercury', self.voice)
				rospy.sleep(4)
			elif msg.data.find('great-wall') > -1 : 
				self.soundhandle.say('it is six thousand two hundred fifty-nine kilometers', self.voice)
				rospy.sleep(4)
			elif msg.data.find('largest-number') > -1 or msg.data.find('five-digits') > -1 : 
				self.soundhandle.say('the largest number of five digits is ninty-nine thousand nine hundred and ninty-nine', self.voice)
				rospy.sleep(4)
			elif msg.data.find('new-zealand') > -1 or msg.data.find('on-the-flag') > -1 or msg.data.find('on flag') > -1 or msg.data.find('on the the flag') > -1 : 
				self.soundhandle.say('there are four stars on the flag of new zealand', self.voice)
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

