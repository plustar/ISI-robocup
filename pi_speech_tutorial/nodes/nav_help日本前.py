#!/usr/bin/env python


"""
    navigation.py - Say back what is heard by the pocketsphinx recognizer.
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8

from sound_play.libsoundplay import SoundClient

class navsp:

	def __init__(self):

		rospy.on_shutdown(self.cleanup)
		self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
		self.wavepath = rospy.get_param("~wavepath", "")
		self.soundhandle=SoundClient()
		rospy.sleep(1)
		self.soundhandle.stopAll()
		rospy.sleep(1)
		self.soundhandle.say("ready",self.voice)

		rospy.sleep(2)
		#rospy.Subscriber('Point',String,self.nav_sp)
		self.pub = rospy.Publisher('ifFollowme', String, queue_size=15)
		self.loc_pub = rospy.Publisher('voice2bring', String, queue_size=15)
		self.srt_guide = rospy.Publisher('voice2guide', String, queue_size=15)

		rospy.Subscriber('follow2voice',String,self.follow_adj)
		rospy.Subscriber('found_person',String,self.askhelp)
		rospy.Subscriber('nav2speech',String,self.reachdst)
		rospy.Subscriber('img2voice',String,self.img_say)
		self.if_followme=0
		self.if_stop=0
		self.if_locpub=0
		self.soundhandle.say("please say jack before each question",self.voice)
		rospy.sleep(4)
		self.soundhandle.say("say stop following me when you arrive",self.voice)
		rospy.sleep(4)
		self.soundhandle.say("I am waiting for your command",self.voice)
		rospy.sleep(3.5)

		rospy.Subscriber('recognizer_output',String,self.follow)
	def askhelp(self,msg):
		msg.data=msg.data.lower()
		if msg.data.find("found_person") > -1:
			self.soundhandle.say(" new operator ",self.voice)
			rospy.sleep(2)
			self.soundhandle.say(" i have memorized you ",self.voice)
			rospy.sleep(3)
			self.soundhandle.say("please help me carry groceries into the house",self.voice)
			rospy.sleep(7)
			self.soundhandle.say(" now please follow me ",self.voice)
			rospy.sleep(2)
			self.soundhandle.say(" I am ready to start guiding ",self.voice)
			rospy.sleep(3)
			self.srt_guide.publish("instruction_over")
	def img_say(self,msg):
		msg.data=msg.data.lower()
		self.soundhanle.say(msg.data,self.voice)
		rospy.sleep(5)

	def reachdst(self,msg):
		msg.data=msg.data.lower()
		if msg.data.find('open_door') > -1:
			self.soundhandle.say("the door is closed ",self.voice)
			rospy.sleep(2)
			self.soundhandle.say(" please help me ",self.voice)
			rospy.sleep(2)
		if msg.data.find('arrived') > -1:
			self.soundhandle.say(" I have reached the destination ",self.voice)
			rospy.sleep(3)

	def follow(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		if msg.data.find('jack') > -1:
			rospy.sleep(0.4)
			if msg.data.find('follow-me') > -1 and self.if_followme ==0 :
				self.soundhandle.say('okay i will follw you',self.voice)
				rospy.sleep(3)
				self.pub.publish('follow_start')
				#rospy.Subscriber('follow2voice',String,self.follow_adj)
				self.if_followme=1
				msg.data=' '

		if self.if_followme ==1 and self.if_stop==0:
			if msg.data.find('jack') > -1 :
				rospy.sleep(0.4)
				if msg.data.find('stop-following-me') > -1 or msg.data.find('stop-following') > -1 or msg.data.find('stop') > -1 or msg.data.find('follow-me') > -1:
					self.soundhandle.say('okay i will stop and remember this car location',self.voice)
					rospy.sleep(5)
					self.pub.publish('follow_stop')
					self.if_stop=1
					#rospy.sleep(3)
					msg.data=' '

		if self.if_stop==1 and self.if_locpub==0:
			#rospy.sleep(3)
			msg.data=msg.data.lower()
			#rospy.sleep(2)
			if msg.data.find('jack') > -1 :
				rospy.sleep(0.4)
				if (msg.data.find('take to-kitchen') > -1 or msg.data.find('bring to-kitchen') > -1 or msg.data.find('to-kitchen') > -1) and  self.if_locpub==0:
					self.loc_pub.publish('kitchen')
					self.soundhandle.say('i will take to kitchen',self.voice)
					rospy.sleep(3.5)
					msg.data=' '
					print "kitchen"
					self.if_locpub=1
				if (msg.data.find('bedroom') > -1 or msg.data.find('bring bedroom') > -1 or msg.data.find('take bedroom') > -1) and self.if_locpub==0 :
					self.loc_pub.publish('bedroom')
					self.soundhandle.say('i will take to bedroom ',self.voice)
					rospy.sleep(3.5)
					msg.data=''
					print "bed room"
					self.if_locpub=1
				if (msg.data.find('the-living-room') > -1 or msg.data.find('living-room') > -1 or msg.data.find('to-living-room') > -1 or msg.data.find('to-the-living-room') > -1) and self.if_locpub==0:
					self.loc_pub.publish('living_room')
					self.soundhandle.say('i will take to living room ',self.voice)
					rospy.sleep(3.5)
					msg.data=' '
					print "living room"
					self.if_locpub=1

	def follow_adj(self,msg):
		msg.data=msg.data.lower()
		print msg.data

		if msg.data.find('nobody') > -1 : 
			self.soundhandle.say('I can not see anybody,Please stand in front of me',self.voice)
			rospy.sleep(5)

		if msg.data.find('far') > -1 : 
			self.soundhandle.say('I have lost you and I will have a new detection,Please stand still in front of me',self.voice)
			rospy.sleep(5)
		if msg.data.find('go_ahead') > -1 : 
			self.soundhandle.say('You are too far from me,Please go ahead',self.voice)
			rospy.sleep(5)
		if msg.data.find('go_left') > -1 : 
			self.soundhandle.say('please go left',self.voice)
			rospy.sleep(5)
		if msg.data.find('go_right') > -1 : 
			self.soundhandle.say('please go right',self.voice)
			rospy.sleep(5)
		if msg.data.find('passing') > -1 : 
			self.soundhandle.say('Someone is passing between us,I am waiting',self.voice)
			rospy.sleep(5)
		if msg.data.find('find') > -1 : 
			self.soundhandle.say('I will follow behind you again',self.voice)
			rospy.sleep(5)


	def cleanup(self):
		rospy.loginfo("shuting down navsp node ....")

if __name__=="__main__":
	rospy.init_node('navsp')
	try:
		navsp()
		rospy.spin()
	except:
		pass





