#!/usr/bin/env python



"""
    play riddle game
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8

from sound_play.libsoundplay import SoundClient

class gpsr:

	def __init__(self):

		rospy.on_shutdown(self.cleanup)
		self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
		self.wavepath = rospy.get_param("~wavepath", "")

		# Create the sound client object
		self.soundhandle = SoundClient() 
		rospy.sleep( 1)
		self.soundhandle.stopAll()

		# Announce that we are ready for input
		rospy.sleep( 1) 
		self.soundhandle.say("Ready", self.voice)
		rospy.sleep(4) 

		self.i=0
		self.j=0
		self.crowd_num=''
		self.w=0
		self.female_num=''
		self.male_num=''
		self.wave_num=''

		self.riddle_turn = rospy.Publisher('riddle_turn', String, queue_size= 10)
		self.soundhandle.say('please say my name kamerider before each question',self.voice)
		rospy.sleep(4.5)
		self.soundhandle.say('hello,I want to play riddles',self.voice)
		rospy.sleep(3)


		self.riddle_turn.publish('turn_robot')

		rospy.Subscriber('human_num', String, self.h_num)
		rospy.Subscriber('female_num', String, self.f_num)
		rospy.Subscriber('male_num', String, self.m_num)
		rospy.Subscriber('recognizer_output', String, self.talk_back)


	def h_num(self,msg):
		msg.data=msg.data.lower()
		self.crowd_num=msg.data
		print "human number is " + msg.data
		self.soundhandle.say('human number is  '+msg.data,self.voice)
		rospy.sleep(4)

	def f_num(self,msg):
		msg.data=msg.data.lower()
		print "female number is " + msg.data
		self.female_num=msg.data
		self.soundhandle.say('female number is  '+msg.data,self.voice)
		rospy.sleep(4)

	def m_num(self,msg):
		msg.data=msg.data.lower()
		print 22222
		print "male number is " + msg.data
		self.male_num=msg.data
		self.soundhandle.say('male number is ' +msg.data,self.voice)
		rospy.sleep(4)
		self.soundhandle.say('who wants to play riddles with me',self.voice)
		rospy.sleep(3.5)
		self.soundhandle.say('please speak loudly and slowly',self.voice)
		rospy.sleep(3.5)
		self.w=1

	def talk_back(self, msg):
		msg.data = msg.data.lower()
		print msg.data
		if self.w==1:
			if  msg.data.find('kamerider') > -1:
				if msg.data.find('the-capital-of iran') > -1 or msg.data.find('capital iran') > -1: 
					self.soundhandle.say('the capital of IRAN is Tehran', self.voice)
					rospy.sleep(4)
					print 44444

				elif msg.data.find('your league-title') > -1:     # league title
					self.soundhandle.say('my league title is  at Home League', self.voice)
					rospy.sleep(4)
					
				elif msg.data.find('the-name-of  this-university') > -1 or msg.data.find('this-university') > -1 :     # league title
					self.soundhandle.say('mmei jo university', self.voice)
					rospy.sleep(4)
				elif msg.data.find('the-date') > -1 or msg.data.find('what-is-the-date') > -1 or msg.data.find('the-date today') > -1 or msg.data.find('date today') > -1:     # league title
					self.soundhandle.say('today is wednsday', self.voice)
					rospy.sleep(4)
				elif msg.data.find('this-event what-is') > -1 or msg.data.find('this-event') > -1:     # league title
					self.soundhandle.say('robo cup  at Home ', self.voice)
					rospy.sleep(4)
				
				elif msg.data.find('how-many-doors') > -1 or msg.data.find('how-many door') > -1 or msg.data.find('door this-room') > -1 or msg.data.find('how-many doors') > -1 or msg.data.find('doors this-room') > -1:     # league title
					self.soundhandle.say('three', self.voice)
					rospy.sleep(4)
				elif msg.data.find('dining-table') > -1 or msg.data.find('where-is dining') > -1 or msg.data.find('where-is dining-table') > -1:     # league title
					self.soundhandle.say('dining room', self.voice)
					rospy.sleep(4)
				elif msg.data.find('the-color-of') > -1 or msg.data.find('the-flooring') > -1 or msg.data.find('what-is color') > -1:     # league title
					self.soundhandle.say('my league title is  at Home League', self.voice)
					rospy.sleep(4)

				elif msg.data.find('people sitting') > -1 or msg.data.find('people-sitting') > -1:     # league title
					self.soundhandle.say('my league title is  at Home League', self.voice)
					rospy.sleep(4)
				elif msg.data.find('people wearing-spectacles') > -1 or msg.data.find('wearing-spectacles') > -1 or msg.data.find('people-wearing-spectacles') > -1:     # league title
					self.soundhandle.say('my league title is  at Home League', self.voice)
					rospy.sleep(4)
				elif msg.data.find('people wearing-cap') > -1 or msg.data.find('people-wearing-cap') > -1:     # league title
					self.soundhandle.say('my league title is  at Home League', self.voice)
					rospy.sleep(4)
				elif msg.data.find('object-available') > -1 or msg.data.find('object in-this-room') > -1 or msg.data.find('available in-this-room') > -1 or msg.data.find('in-this-room') > -1 or msg.data.find('object-available-in-this-room') > -1:     # league title
					self.soundhandle.say('my league title is  at Home League', self.voice)
					rospy.sleep(4)
				
				elif msg.data.find('the-color-of-cup' ) > -1 or msg.data.find('color-of-cup') > -1 or msg.data.find('the-color-of') > -1: 
					self.soundhandle.say('white', self.voice)
					rospy.sleep(4)
				elif msg.data.find('find drink') > -1 or msg.data.find('find-drink') > -1: 
					self.soundhandle.say('fridge', self.voice)
					rospy.sleep(4)
				elif msg.data.find('animal afraid-you') > -1 or msg.data.find('which-animal ') > -1 or msg.data.find('which animal afraid-you') > -1: 
					self.soundhandle.say('Lion can afraid me', self.voice)
					rospy.sleep(4)
				elif msg.data.find('the-country-of pizza') > -1 or msg.data.find('the-country-of-pizza') > -1 or msg.data.find('country pizza') > -1: 
					self.soundhandle.say('Italy ,is ,the ,contry ,of ,pizza', self.voice)
					rospy.sleep(5)
				elif msg.data.find('the-name-of  animal') > -1 or msg.data.find('heaviest-animal') > -1 : 
					print 23456
					self.soundhandle.say('the name of the heaviest animal is Elephant', self.voice)
					rospy.sleep(4)





	def cleanup(self):
		rospy.loginfo("Shutting down gpsr node...")

if __name__=="__main__":
	rospy.init_node('gpsr')
	try:
		gpsr()
		rospy.spin()
	except:
		pass



