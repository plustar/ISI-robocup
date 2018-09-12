#!/usr/bin/env python
# -*- coding: utf-8 -*-

# types of Questions
#	define Type A : Go to PLACE_A, find a person,and finish a mission             word_count <= 3

#		Type B : Go to PLACE_A, find an OBJECT and take it to the PLACE_B       word_count <= 3

#		Type C : Bring an OBJECT and give it to the PERSON in the PLACE_A and finish a mission    word_count <= 4


"""
	talkback.py - Say back what is heard by the pocketsphinx recognizer.
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

		# Intiate Dicts for storing msgs 
		self.temp = {'mission' : '', 'object': '', 'src_loc' : '', 'dst_loc' : '', 'target' : ''}   # store the words recognized each time
		self.command = {'mission' : '', 'object' : '', 'src_loc' : '', 'dst_loc' : '', 'target' : ''} # store the final command 
		self.needupdate = {'mission' : 1, 'object' : 1, 'src_loc' : 1, 'dst_loc' : 1, 'target' : 1}   # mark the words which need update
		
		self.i = 0   	# for loop
		self.index = 0  # for loop
		self.temp_echo = ''
		self.mission_type = -1  # -1: no mission;     to differentiate the type of missions
					#  0: inform, 
					#  1: answer, 
					#  2: ask
		self.first_recog = 1 # to mark if it is the first time to start regonition or correcting mistakes
		self.yes = -1 # to mark if the recognition is finished
		self.pos = 0  # to find two locations, [CAUTION]need initialiaztion later! 
		self.srcloc=0
		self.dstloc=0
		self.object=0
		self.mission=0
		self.name=0

		self.keywords_to_temp_mission = {'mission': ['name','time','question']}
		self.keywords_to_temp_object = {'object': ['coke','crackers']}
		self.keywords_to_temp_location = {'location': ['bedroom','side-table','dinner-table','livingroom','door']}
		self.keywords_to_temp_target ={'name':['alex','tracy','person']}
		self.mission = {'name': 'ask her for his name and tell it to you',
				'time':'tell him the time',
				'question':'answer him a question',
				}
		self.ifhas_word = 0
		self.ifokay=0
		self.start_recog = 0 
		self.repeat_data = '' 

		# Create the sound client object
		self.soundhandle = SoundClient() 
		rospy.sleep(1)
		self.soundhandle.stopAll()
		# Announce that we are ready for input
		rospy.sleep(1) 
		self.soundhandle.say("Ready", self.voice)
		rospy.sleep(2) 

		# Initiate Publishers 
		self.gpsr_srclocation = rospy.Publisher('gpsr_srclocation', String, queue_size=10)
		self.gpsr_dstlocation = rospy.Publisher('gpsr_dstlocation', String, queue_size=10) 
		self.gpsr_name = rospy.Publisher('gpsr_name', String, queue_size=10)
		self.gpsr_missiontype = rospy.Publisher('gpsr_mstype', Int8, queue_size = 10)
		self.gpsr_mission = rospy.Publisher('gpsr_mission', String, queue_size=10)
		self.gpsr_object = rospy.Publisher('gpsr_object',String,queue_size=10)               
		self.gpsr_begin = rospy.Publisher('gpsr_begin', String, queue_size=10)

			# Subscribe to the recognizer output
		rospy.Subscriber('recognizer_output', String, self.talk_back) 

	def get_temp_mission(self, data):      # mission
		for (temp, keywords) in self.keywords_to_temp_mission.iteritems():
			for word in keywords:  
				if data.find(word) > -1:
					return word
		return ''

	#str.split(str="",num=string.count(str))     通过指定分割符对字符串进行切片
	#str 是指定的分割符，默认所有的空字符，换行符(\n),制表符(\t)等
	#num  是指定的分割次数
	#返回分割后的字符串列表

	#range函数 http://www.cnblogs.com/buro79xxd/archive/2011/05/23/2054493.html

	def get_temp_location(self, data):
		word_list = data.split()
		for index in range(self.pos,len(word_list)):
			for (temp, keywords) in self.keywords_to_temp_location.iteritems():
				for word in keywords:
					if word_list[index] == word:
						self.pos = index + 1
						return word
		return ''

	def get_temp_target(self, data):
		for (temp, keywords) in self.keywords_to_temp_target.iteritems():
			for word in keywords:
				if data.find(word) > -1:
					return word
		return ''

	def get_temp_object(self, data):
		for (temp, keywords) in self.keywords_to_temp_object.iteritems(): 
			for word in keywords:
				if data.find(word) > -1:
					return word
		return ''


	def delete_none(self,data):
		for k in range(len(data)):
			if data[k]== '':
				del data[k]

	def form_the_question(self, word_count):
		if self.start_recog == 1 :
			print word_count
			print self.temp['src_loc']
			print self.temp['object']
			print self.temp['dst_loc']
			if word_count == 0:
				self.question='sorry i did not get it'
			if  word_count > 0  and self.srcloc == 0 :
				
				if self.temp['src_loc'] =='':
					self.question='1sorry i did not get it'
				elif self.temp['src_loc'] !='':
					self.repeat_data='2do you want me to go to the '+self.command['src_loc']
					self.ifhas_word = 1
					if self.yes == 0:
						self.question='3please repeat your command'	
						self.yes = -1	
					elif self.yes == 1:
						self.command['src_loc']=self.temp['src_loc']
						self.yes = -1
						self.srcloc=1
				self.ifhas_word = 0
			if word_count > 0 and self.srcloc == 1 and self.target==0 and self.mission== 0 and self.object==0 and self.dstloc==0:
				
				if self.temp['target'] =='' and self.temp['object'] =='' and self.temp['dst_loc']=='' and self.temp['mission']=='':
					self.question='1sorry i did not get other message, please repeat the command'
				if self.temp['target'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' to find '+self.temp['target']
					self.ifhas_word = 1
					if self.yes == 0:
						self.question='3please repeat your command'	
						self.yes = -1	
					elif self.yes == 1:
						self.command['target']=self.temp['target']
						self.yes = -1
						self.target=1
				if self.temp['object'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' to find '+self.temp['object']
					self.ifhas_word = 1
					if self.yes == 0:	
						self.question='3please repeat your command'	
						self.yes = -1
					elif self.yes == 1:
						self.command['object']=self.temp['object']
						self.yes = -1
						self.object=1	
				if self.temp['dst_loc'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' to give a object to '+self.temp['dst_loc']
					self.ifhas_word = 1
					if self.yes == 0:	
						self.question='3please repeat your command'	
						self.yes = -1	
					elif self.yes == 1:
						self.command['dst_loc']=self.temp['dst_loc']
						self.yes = -1
						self.dstloc=1	
				if self.temp['mission'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' and '+self.mission[ self.command['mission'] ]
					self.ifhas_word = 1
					if self.yes == 0:
						self.question='3please repeat your command'	
						self.yes = -1	
					elif self.yes == 1:
						self.command['mission']=self.temp['mission']
						self.yes = -1
						self.mission=1	
				self.ifhas_word =0	
			if word_count > 0 and self.srcloc == 1 and self.target ==1 and self.mission== 0 and self.object==0 and self.dstloc==0:
				if self.temp['mission']=='' or self.temp['object'] =='':
					self.question='1sorry i did not get other message, please repeat the command'
				if self.temp['mission'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' and '+self.mission[ self.command['mission'] ]
					self.ifhas_word = 1
					if self.yes == 0:	
						self.question='3please repeat your command'	
						self.yes = -1
					elif self.yes == 1:
						self.command['mission']=self.temp['mission']
						self.yes = -1
						self.mission=1
				if self.temp['object'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' to give '+self.temp['object']+' to '+self.temp['target']
					self.ifhas_word = 1
					if self.yes == 0:	
						self.question='3please repeat your command'
						self.yes = -1
					elif self.yes == 1:
						self.command['object']=self.temp['object']
						self.yes = -1
						self.object=1
				self.ifhas_word =0
			if word_count > 0 and self.srcloc == 1 and self.object ==1 and self.target==0 and self.mission== 0 and self.dstloc==0:
				if self.temp['dst_loc']=='' or self.temp['target'] =='':
					self.question='1sorry i did not get other message, please repeat the command'
				if self.temp['dst_loc'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' to give a ' + self.command['object'] + ' to '+self.temp['dst_loc']
					self.ifhas_word = 1
					if self.yes == 0:
						self.question='3please repeat your command'
						self.yes = -1
					elif self.yes == 1:
						self.command['dst_loc']=self.temp['dst_loc']
						self.yes = -1
						self.dstloc=1
						####################################################################
				if self.temp['target'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' to give a '+ self.command['object'] + ' to '+self.temp['target']
					self.ifhas_word = 1
					if self.yes == 0:
						self.question='3please repeat your command'
						self.yes = -1
					elif self.yes == 1:
						self.command['target']=self.temp['target']
						self.yes = -1
						self.target=1
				self.ifhas_word =0
			if word_count > 0 and self.srcloc == 1 and self.dstloc ==1 and self.target==0 and self.mission== 0 and self.object==0:
				if self.temp['object'] =='':
					self.question='1sorry i did not get the object name, please repeat the command'
				if self.temp['object'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' to give '+self.temp['object']+' to '+self.command['dst_loc']
					self.ifhas_word = 1
					if self.yes == 0:
						self.question='3please repeat your command'
						self.yes = -1
					elif self.yes == 1:
						self.command['object']=self.temp['object']
						self.yes = -1
						self.object=1
				self.ifhas_word =0
						###############################################
			if word_count > 0 and self.srcloc == 1 and self.mission ==1 and self.dstloc ==0 and self.target==0 and self.object==0:
				if self.temp['object']=='' or self.temp['target'] =='':
					self.question='1sorry i did not get other message, please repeat the command'
				if self.temp['target'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' to find '+ self.temp['target'] + ' and '+self.mission[ self.command['mission'] ]
					self.ifhas_word = 1
					if self.yes == 0:
						self.question='3please repeat your command'	
						self.yes = -1
					elif self.yes == 1:
						self.command['target']=self.temp['target']
						self.yes = -1
						self.target=1
				if self.temp['object'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' to give '+self.temp['object']+' to a person and '+self.mission[ self.command['mission'] ]
					self.ifhas_word = 1
					if self.yes == 0:
						self.question='3please repeat your command'	
						self.yes = -1
					elif self.yes == 1:
						self.command['object']=self.temp['object']
						self.yes = -1
						self.object=1
				self.ifhas_word =0
			if word_count > 0 and self.srcloc==1 and self.mission ==1 and self.object==1 and self.dstloc ==0 and self.target==0:			
				if self.temp['target'] =='':
					self.question='1sorry i did not get the person name, please repeat the command'
				if self.temp['target'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' bring a '+ self.temp['object'] +' to '+self.temp['target'] + ' and '+self.mission[ self.command['mission'] ]
					self.ifhas_word = 1
					if self.yes == 0:
						self.question='3please repeat your command'
						self.yes = -1
					elif self.yes == 1:
						self.command['target']=self.temp['target']
						self.yes = -1
						self.target=1
				self.ifhas_word =0
						#################################
			if word_count > 0 and self.srcloc==1 and self.mission ==1 and self.target==1 and self.dstloc ==0 and self.object==0:	
				if self.temp['object'] =='':
					self.question='shall I bring some object, please repeat the command'
					self.ifhas_word =1
					if self.yes == 0:
						self.question='OK'	#####################没有拿物体
						self.yes = -1
					elif self.yes == 1:
						self.question='3please repeat your command'
						self.yes = -1
						self.object=1
				if self.temp['object'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' to bring '+self.temp['object']+' to '+self.command['target'] +' and ' +self.mission[ self.command['mission'] ]
					self.ifhas_word = 1
					if self.yes == 0:
						self.question='3please repeat your command'
						self.yes = -1
					elif self.yes == 1:
						self.command['object']=self.temp['object']
						self.yes = -1
						self.object=1
				self.ifhas_word =0
						#################################
			if word_count > 0 and self.srcloc==1 and self.object==1 and self.target==1 and self.mission ==0 and self.dstloc ==0:
				if self.temp['mission']=='':
					self.question='1sorry i did not the mission, please repeat the command'
				if self.temp['mission'] !='':
					self.repeat_data='4do you want me to go to the '+self.command['src_loc']+' find '+self.command['target']+ ' and ' + self.mission[ self.temp['mission'] ]
					self.ifhas_word = 1
					if self.yes == 0:
						self.question='3please repeat your command'
						self.yes = -1
					elif self.yes == 1:
						self.command['mission']=self.temp['mission']
						self.yes = -1
						self.mission=1
				self.ifhas_word =0
			if word_count > 0 and self.srcloc == 1 and self.object ==1 and self.dstloc == 1:
			if word_count > 0 and self.srcloc == 1 and self.target ==1 and self.mission == 1:
			if word_count > 0 and self.srcloc == 1 and self.target ==1 and self.object == 1 and self.mission == 1:	
			if self.repeat_data != '':
				self.soundhandle.say(self.repeat_data,self.voice)
				print self.repeat_data
				#self.first_recog = 1
				rospy.sleep(5)
				rospy.sleep(5)
				self.soundhandle.say('please say my name before this answer',self.voice)
				rospy.sleep(5)
				rospy.sleep(3)
				self.makesure = 1
			else: 
				self.soundhandle.say(self.question,self.voice)
				print self.question
				rospy.sleep(7)
				rospy.sleep(5)
			self.start_recog = 0
			self.repeat_data = '' 

	def talk_back(self, msg):
		# Print the recognized words on the screen  
		msg.data = msg.data.lower()
		print msg.data

		self.repeat_data = ''  
		
		if msg.data.find('kamerider') > -1:# recognize 'kamerider'
			self.start_recog = 1   
		#else: 
		if self.ifhas_word == 1
			if msg.data.find('kamerider-yes') > -1: # recognized "kamerider yes"
				#self.start_recog = 0 
				#for (key,value) in self.command.items(): 
				#	print key+':'
				#	print self.command[key] + '\n'

				self.gpsr_begin.publish('start')
			
				self.gpsr_dstlocation.publish(self.command['dst_loc'])
				self.gpsr_srclocation.publish(self.command['src_loc'])
				self.gpsr_mission.publish(self.command['mission'])
				self.gpsr_name.publish(self.command['target'])
				self.gpsr_object.publish(self.command['object'])
				self.gpsr_missiontype.publish(self.mission_type)
				self.yes = 1
				for (key,value) in self.temp.items(): 
					self.temp[key] = ''
					self.command[key] = ''
				self.soundhandle.say('ok i will follow the command', self.voice)
				rospy.sleep(6)

			if msg.data.find('kamerider-no') > -1 : # recognized "kamerider no"  
				###########################################################################

				###########################################################################
				self.start_recog = 0 
				self.soundhandle.say('sorry could you please repeat the question louder and slower',self.voice)
				rospy.sleep(6)
				self.first_recog = 1
				self.yes = 0
				for (key,value) in self.needupdate.items():
					self.needupdate[key] = 1
		

		if self.start_recog == 1 and self.finished != 1:
			# Give the feedback if it recognizes message succesfully
			self.temp['src_loc'] = self.get_temp_location(msg.data)
			self.temp['dst_loc'] = self.get_temp_location(msg.data)
			self.temp['mission'] = self.get_temp_mission(msg.data)
			self.temp['target'] = self.get_temp_target(msg.data)
			self.temp['object'] = self.get_temp_object(msg.data) 
			word_count = 0
			self.pos = 0
			if (msg.data.find('tell') > -1):
				self.mission_type = 0
			if (msg.data.find('answer') > -1):
				self.mission_type = 1
			if (msg.data.find('ask') > -1):
				self.mission_type = 2
	
			for (key,word) in self.temp.items():
				print key + ":"
				self.temp_echo = self.temp[key] + "\n"
				print self.temp_echo	
				if self.temp[key] != '':
					print 'aaaa'
					print self.first_recog
					if self.first_recog == 1:
						print 'nnnnnnn'
						self.needupdate[key] = 1
						

						word_count = word_count + 1
						print word_count
				# store valid commands in self.command

			if self.first_recog == 1:# the first time to start recognition
			
				self.first_recog = 0   # next time is not the first time to recognize
				self.form_the_question(word_count)
			else: # if not the first time to start recognition
				for (key,word) in self.temp.items():
					if self.needupdate[key] == 1:
						self.command[key] = self.temp[key]  # update commands
						self.needupdate[key] = 0
				#######################################

				self.form_the_question(word_count)
				#######################################
		#	print "on"
	
	def cleanup(self):
		rospy.loginfo("Shutting down gpsr node...")

if __name__=="__main__":
	rospy.init_node('gpsr')
	try:
		gpsr()
		rospy.spin()
	except:
		pass


