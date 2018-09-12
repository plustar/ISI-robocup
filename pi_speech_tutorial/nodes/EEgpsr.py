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
		rospy.sleep(2)
		self.soundhandle.say("ready",self.voice)

		rospy.sleep(3)
		rospy.Subscriber('Point',String,self.nav_sp)
		self.pub = rospy.Publisher('ifFollowme', String, queue_size=10)

		self.gpsr_srclocation = rospy.Publisher('gpsr_srclocation', String, queue_size=10)
		
		self.if_followme=0
		self.if_stop=0
		self.flag = 0
		self.if_followflag=0
		self.if_stopflag=0
		self.flaga = -1
		self.flagb = -1
		self.flag24 = 0
	def nav_sp(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		if msg.data.find('a') > -1 and self.flaga == -1:
			self.soundhandle.say("I am moving now",self.voice)
			self.flaga = 1
		if msg.data.find('b') > -1 and self.flagb == -1:
			rospy.sleep(2)
			self.flagb = 1
			#self.soundhandle.say("I have arrived the designated position",self.voice)
			rospy.sleep(2)
			self.soundhandle.say("waiting for your command",self.voice)
			rospy.sleep(5)
			rospy.Subscriber('recognizer_output',String,self.follow)
			rospy.Subscriber('recognizer_output', String, self.talkback)
			
		if msg.data.find('c') >-1:
			self.soundhandle.say("Please follow me,I will guide you",self.voice)
		#if msg.data.find('d')>-1:
			##self.soundhandle.say("I have arrived the third point",self.voice)
			##rospy.sleep(3)
			#self.soundhandle.say("waiting for your command",self.voice)
			#rospy.sleep(3)
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
			##rospy.Subscriber('recognizer_output',String,self.follow)
                if msg.data.find('back')>-1:
			self.soundhandle.say("I am back,waiting for your next command",self.voice)
	def follow(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		if ((msg.data.find('follow') > -1 or msg.data.find('follow-me') > -1) and self.if_followme ==0 and self.flagb == 1 ) :
			self.soundhandle.say('okay i will follw you',self.voice)
			rospy.sleep(3)
			self.pub.publish('follow_start')
			rospy.Subscriber('follow2voice',String,self.follow_adj)
			self.if_followme=1
			self.if_followflag=1
		if self.if_followme ==1 and self.if_stop==0:
			if  msg.data.find('stop') > -1:
				self.soundhandle.say('okay,follow stop',self.voice)
				rospy.sleep(3)
				self.pub.publish('follow_stop')
				self.if_stop=1
				self.soundhandle.say('Shall I go back',self.voice)
				rospy.sleep(3)
				self.flag = 1;
				self.if_followflag=0
		if self.flag == 1 and self.if_stopflag == 0:
			if msg.data.find('yes') > -1:
				self.soundhandle.say('ok I go back',self.voice)
				self.pub.publish('go_back')
				self.if_stopflag = 1
				print msg.data
				
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
			self.soundhandle.say('I have sensed you',self.voice)
			rospy.sleep(5)		
			
	def talkback(self, msg):
		# Print the recognized words on the screen  
		rospy.loginfo(msg.data)
		msg.data = msg.data.lower()

		print msg.data
		#else:
		if self.flagb == 1:
			if ((msg.data.find('bedroom') > -1 or msg.data.find('bed-room') > -1 or msg.data.find('bed room') > -1) and self.if_followflag !=1):
				self.soundhandle.say('ok i will go to the bedroom',self.voice)
				rospy.sleep(5)		
				self.gpsr_srclocation.publish('bedroom')
				self.flag24 = 1
			elif msg.data.find('desk') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the desk',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('desk')
				self.flag24 = 1
			elif msg.data.find('bed') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the bed',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('bed')
				self.flag24 = 1
			elif msg.data.find('kitchen') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the kitchen',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('kitchen')
				self.flag24 = 1
			elif msg.data.find('dining-room-sofa') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the dining room sofa',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('dinner_room_sofa')
				self.flag24 = 1
			elif msg.data.find('dining-room-table') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the dining-room-table',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('dinner_room_table')
				self.flag24 = 1
			elif msg.data.find('dining-room') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the dining room',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('dining_room')
				self.flag24 = 1
			elif ((msg.data.find('living-room') > -1 or msg.data.find('living') > -1) and self.if_followflag !=1):
				self.soundhandle.say('ok i will go to the living room',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('living_room')
				self.flag24 = 1
			elif msg.data.find('hallway') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the hallway',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('hallway')
				self.flag24 = 1
			elif msg.data.find('shelf') > -1 and self.if_followflag !=1:			#pronouns as selves
				self.soundhandle.say('ok i will go to the shelf',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('shelf')
				self.flag24 = 1
			elif ((msg.data.find('side-board') > -1 or msg.data.find('board') > -1) and self.if_followflag !=1) :
				self.soundhandle.say('ok i will go to the sideboard',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('side_board')
				self.flag24 = 1
			elif msg.data.find('dresser') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the dresser',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('dresser')
				self.flag24 = 1
			elif msg.data.find('sink') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the sink',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('sink')
				self.flag24 = 1
			elif msg.data.find('sofa') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the sofa',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('sofa')
				self.flag24 = 1
			elif msg.data.find('stove') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the stove',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('stove')
				self.flag24 = 1
			elif msg.data.find('bar') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the bar',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('bar')
				self.flag24 = 1
			elif msg.data.find('side-table') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the sidetable',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('side_board')
				self.flag24 = 1
			elif msg.data.find('cabinet') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the cabinet',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('cabinet')
				self.flag24 = 1
			elif ((msg.data.find('dinner-table') > -1 or msg.data.find('dinner') > -1) and self.if_followflag !=1):
				self.soundhandle.say('ok i will go to the dinner table',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('dinner_table')
				self.flag24 = 1				
			elif msg.data.find('couch-table') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the couch table',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('couch_table')
				self.flag24 = 1

			elif msg.data.find('hanger') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the hanger',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('hanger')
				self.flag24 = 1
			elif msg.data.find('trash-bin') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the trash bin',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('trash_bin')
				self.flag24 = 1
			elif msg.data.find('fridge') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the fridge',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('fridge')
				self.flag24 = 1
			elif msg.data.find('tv') > -1 and self.if_followflag !=1:
				self.soundhandle.say('ok i will go to the tv',self.voice)
				rospy.sleep(5)
				self.gpsr_srclocation.publish('tv')
				#self.start_recog = 0
				#self.first_recog = 1
				self.flag24 = 1
			else	:
				print msg.data
	
	def cleanup(self):
		rospy.loginfo("shuting down navsp node ....")

if __name__=="__main__":
	rospy.init_node('navsp')
	try:
		navsp()
		rospy.spin()
	except:
		pass

