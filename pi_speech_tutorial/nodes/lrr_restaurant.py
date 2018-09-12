#!/usr/bin/env python


import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8

from sound_play.libsoundplay import SoundClient

class gpsr:

	def __init__(self):
		print 2222
		rospy.on_shutdown(self.cleanup)
		self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
		self.wavepath = rospy.get_param("~wavepath", "")
		self.soundhandle=SoundClient()
		rospy.sleep(1)
		self.soundhandle.stopAll()
		rospy.sleep(10)
		self.soundhandle.say("ready",self.voice)
		rospy.sleep(5)
		self.l=0
		self.i=0
		self.j=0
		self.w=0
		self.h=0
		self.r=0
		self.fd=0
		self.myorder=''
		#{'drink':['green-tea','cafe-au-lait','iced-tea','grape-fruit-juice','strawberry-juice']}
		self.sp2nv=rospy.Publisher('speech2nav',String,queue_size=10)
		self.sp2img=rospy.Publisher('detectWave',String,queue_size=10)
		rospy.Subscriber('voice_infer',String,self.say_back)
		rospy.Subscriber('voice_service',String,self.say_final)
		rospy.Subscriber('img2voice',String,self.say_find)
		self.soundhandle.say("dear operator",self.voice)
		rospy.sleep(1.5)
		self.soundhandle.say("please say jack before your command",self.voice)
		rospy.sleep(6)
		self.soundhandle.say("now I am ready",self.voice)
		rospy.sleep(5)
		self.srt_turn('s')
		print 2345


	def  srt_turn(self,data):
		self.r=1
		self.sp2nv.publish("start")
	def say_start(self,msg):
		print 1234
		msg.data=msg.data.lower()
		print msg.data
		print 4444
		if msg.data.find('jack') > -1 :
			if self.r==1:
				if msg.data.find('green-tea') > -1 :
					self.r=2
					self.order='green-tea'
					self.soundhandle.say('I have taken your order       ',self.voice)
					rospy.sleep(3)
					self.soundhandle.say(self.order,self.voice)
					rospy.sleep(3)
					self.sp2nv.publish('order')

				elif msg.data.find('cafe-au-lait') > -1 :
					self.r=2
					self.myorder='cafe-au-lait'
					self.soundhandle.say('I have taken your order       ',self.voice)
					rospy.sleep(2.5)
					self.soundhandle.say(self.myorder,self.voice)
					rospy.sleep(2.5)
					self.sp2nv.publish('order')

				elif msg.data.find('iced-tea') > -1 :
					self.myorder='iced-tea'
					self.soundhandle.say('I have taken your order       ',self.voice)
					rospy.sleep(2.5)
					self.soundhandle.say(self.myorder,self.voice)
					rospy.sleep(2.5)
					self.r=2
					self.sp2nv.publish('order')

				elif msg.data.find('grape-fruit-juice') > -1 :
					self.myorder='grape-fruit-juice'
					self.soundhandle.say('I have taken your order       ',self.voice)
					rospy.sleep(2.5)
					self.soundhandle.say(self.myorder,self.voice)
					rospy.sleep(2.5)
					self.sp2nv.publish('order')
					self.r=2
				elif msg.data.find('strawberry-juice') > -1 :
					self.myorder='strawberry-juice'
					self.soundhandle.say('I have taken your order       ',self.voice)
					rospy.sleep(2.5)
					self.soundhandle.say(self.myorder,self.voice)
					rospy.sleep(2.5)
					self.sp2nv.publish('order')
					self.r=2
				elif msg.data.find('potato-chips') > -1 :
					self.myorder='potato-chips'
					self.soundhandle.say('I have taken your order       ',self.voice)
					rospy.sleep(2.5)
					self.soundhandle.say(self.myorder,self.voice)
					rospy.sleep(2.5)
					self.sp2nv.publish('order')
					self.r=2
				elif msg.data.find('potato-stick') > -1 :
					self.myorder='potato-stick'
					self.soundhandle.say('I have taken your order       ',self.voice)
					rospy.sleep(2.5)
					self.soundhandle.say(self.myorder,self.voice)
					rospy.sleep(2.5)
					self.sp2nv.publish('order')
					self.r=2
				elif msg.data.find('cookie') > -1 :
					self.myorder='cookie'
					self.soundhandle.say('I have taken your order       ',self.voice)
					rospy.sleep(2.5)
					self.soundhandle.say(self.myorder,self.voice)
					rospy.sleep(2.5)
					self.sp2nv.publish('order')
					self.r=2
				#rospy.Subscriber('voice_service',String,self.say_final)
			
			#else :
			#	self.myorder='green-tea'
			#	self.soundhandle.say('I have taken your order       '+self.myorder,self.voice)
			#	rospy.sleep(2.5)
			#	self.sp2nv.publish('order')
				#rospy.Subscriber('voice_service',String,self.say_final)
	def say_back(self,msg):
		print 22222
		msg.data=msg.data.lower()
		print msg.data
		if self.l==1:
			self.soundhandle.say('the bar is on the left',self.voice)
			rospy.sleep(5)
		if self.l==0:
			self.soundhandle.say('the bar is on the right',self.voice)
			rospy.sleep(5)
		self.sp2img.publish('wave')

	def say_find(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		if self.fd==0:
			self.fd=1
			self.soundhandle.say('I have arrived the table of the calling person',self.voice)
			rospy.sleep(3.5)
			rospy.sleep(2)
			self.soundhandle.say('I am looking at the waving person',self.voice)
			rospy.sleep(4)
			self.soundhandle.say('please say your order',self.voice)
			rospy.sleep(2)
			self.soundhandle.say("please say jack before your order",self.voice)
			rospy.sleep(7)
			self.r=1
			rospy.Subscriber('recognizer_output',String,self.say_start)

			
	def say_final(self,msg):
		if self.h == 0:
			self.h=1
			rospy.sleep(1)
			self.soundhandle.say('I have reached the   bar table',self.voice)
			rospy.sleep(4.5)
			self.soundhandle.say('the person wants      ',self.voice)
			rospy.sleep(2.5)
			self.soundhandle.say(self.myorder,self.voice)
			rospy.sleep(2.5)


	def cleanup(self):
		rospy.loginfo("Shutting down gpsr node...")


if __name__=="__main__":
	rospy.init_node('gpsr')
	try:
		gpsr()
		rospy.spin()
	except:
		pass


