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
		
		rospy.sleep(3)
		rospy.Subscriber('Point',String,self.nav_sp)
		self.pub = rospy.Publisher('ifFollowme', String, queue_size=15)
		self.if_followme=0
		self.if_stop=0
	def nav_sp(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		if msg.data.find('a') > -1:
			self.soundhandle.say("I am moving now",self.voice)
		#if msg.data.find('b') > -1:
			#self.soundhandle.say("I have arrived the start loction,waiting for your command",self.voice)
			#rospy.sleep(10)
		if msg.data.find('move') > -1:
			self.soundhandle.say("I see a man,Please move away",self.voice)
		if msg.data.find('c') >-1:
			self.soundhandle.say("I have arrived the waypoint two",self.voice)
		if msg.data.find('b')>-1:
			self.soundhandle.say("I have arrived the start location",self.voice)
			rospy.sleep(3)
			self.soundhandle.say("waiting for your command",self.voice)
			rospy.sleep(2.7)
			#self.soundhandle.say("Please stand in front of  me",self.voice)
			#rospy.sleep(4)
			#self.soundhandle.say("Dear operator",self.voice)
			#rospy.sleep(2)
			#self.soundhandle.say("if you say kamerider follow me",self.voice)
			#rospy.sleep(3)
			#self.soundhandle.say("I will start to follow you",self.voice)
			#rospy.sleep(3)
			#self.soundhandle.say("If you say kamerider stop",self.voice)
			#rospy.sleep(3)
			#self.soundhandle.say("I will stop doing it",self.voice)
			#rospy.sleep(2.7)
			rospy.Subscriber('recognizer_output',String,self.follow)
			
	def follow(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		#if msg.data.find('kamerider') > -1:
		if msg.data.find('follow-me') > -1 and self.if_followme ==0 :
			self.soundhandle.say('okay i will follw you',self.voice)
			rospy.sleep(3)
			self.pub.publish('follow_start')
			rospy.Subscriber('follow2voice',String,self.follow_adj)
			self.if_followme=1
		if self.if_followme ==1 and self.if_stop==0:
			if msg.data.find('stop-follow-me') > -1 or msg.data.find('stop') > -1:
				self.soundhandle.say('okay i will stop and remember this car location',self.voice)
				rospy.sleep(10)
				self.pub.publish('follow_stop')
				self.if_stop=1
		if self.if_stop==1:
			if msg.data.find('shelf') > -1 :
				self.pubbring.publish('shelf')
				self.soundhandle.say('i will bring to shelf',self.voice)
				rospy.sleep(3)
				print "shelf"

			elif msg.data.find('side-board') > -1 :
				self.pubbring.publish('side board')
				self.soundhandle.say('i will bring to side board',self.voice)				
				rospy.sleep(3)
				print "side board"

			elif msg.data.find('dresser') > -1 :
				self.pubbring.publish('dresser')
				self.soundhandle.say('i will bring to dresser',self.voice)
				rospy.sleep(3)
				print "dresser"

			elif msg.data.find('sink') > -1 :
				self.pubbring.publish('sink')
				self.soundhandle.say('i will bring to sink',self.voice)				
				rospy.sleep(3)
				print "sink"
			elif msg.data.find('bar') > -1 :
				self.pubbring.publish('bar')
				self.soundhandle.say('i will bring to bar',self.voice)
				rospy.sleep(3)
				print "bar"

			elif msg.data.find('side-table') > -1 :
				self.pubbring.publish('side table')
				self.soundhandle.say('i will bring to side table',self.voice)
				rospy.sleep(3)
				print "side table"

			elif msg.data.find('cabinet') > -1 :
				self.pubbring.publish('cabinet')
				self.soundhandle.say('i will bring to cabinet',self.voice)
				rospy.sleep(3)
				print "cabinet"

			elif msg.data.find('dinner-table') > -1 :
				self.pubbring.publish('dinner table')
				self.soundhandle.say('i will bring to dinner table',self.voice)
				rospy.sleep(3)
				print "dinner table"

			elif msg.data.find('dinning-room-table') > -1 :
				self.pubbring.publish('dinning room table')
				self.soundhandle.say('i will bring to dinning room table',self.voice)
				rospy.sleep(3)
				print "dinning room table"

			elif msg.data.find('couch-table') > -1 :
				self.pubbring.publish('couch table')
				self.soundhandle.say('i will bring to couch table',self.voice)
				rospy.sleep(3)
				print "couch table"

			elif msg.data.find('stove') > -1 :
				self.pubbring.publish('stove')
				self.soundhandle.say('i will bring to stove',self.voice)				
				rospy.sleep(3)
				print "stove"			
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



















