#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#上句表示程序中可以有中文，包括注释
# types of Questions
# define Type A : Go to PLACE_A, find an OBJECT                 word_count <= 2
#	 Type B : Go find a PERSON, and finish a MISSION 	word_count <= 2
#	 Type C : Go to PLACE_A, find an OBJECT and take it to (a TARGET) (in PLACE_B)       word_count <= 4
#   	 Type D : Go to PLACE_A, find an OBJECT , take it to a TARGET(in PLACE_B) and finish a MISSION   word_count <= 4

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
	#self.voice = rospy.get_param("~voice", "voice_don_diphone") 
        self.wavepath = rospy.get_param("~wavepath", "")
	
	# Intiate Dicts for storing msgs 
        self.temp = {'mission' : '', 'object': '', 'src_loc' : '', 'dst_loc' : '', 'target' : ''}     # store the words recognized each time
	self.command = {'mission' : '', 'object' : '', 'src_loc' : '', 'dst_loc' : '', 'target' : ''} # store the final command 
	self.needupdate = {'mission' : 1, 'object' : 1, 'src_loc' : 1, 'dst_loc' : 1, 'target' : 1}   # mark the words which need update
	#self.place = ['',''] 
	self.i = 0   	# for loop
	self.index = 0  # for loop
	self.temp_echo = ''
	self.mission_type = -1  # -1: no mission;     to differentiate the type of missions
 				#  0: inform, 
				#  1: answer, 
				#  2: ask
	self.first_recog = 1 # to mark if it is the first time to start regonition or correcting mistakes
	self.finished = 0 # to mark if the recognition is finished
	self.pos = 0  # to find two locations, [CAUTION]need initialiaztion later! 
	#self.place2 = '' 
	#词与任务对应
        self.keywords_to_temp_temp = {'mission': ['name','time','question','your-name','your-team','date','what-day','his-name','her-name']}
        self.keywords_to_temp_object = {'object': ['cola','person']}
        self.keywords_to_temp_locations = {'location': ['in-the-kitchen','fridge','on-the-kitchen-table','kitchen-counter','cupboard','trashbin','in-the-livingroom','bar','on-the-couch-table','on-the-dinner-table','on-the-sofa','in-the-bedroom','on-the-desk','on-the-bed','in-the-hallway','on-the-bookcase','on-the-hallway-table','fridge']}
        self.keywords_to_temp_names ={'name':['alex','angel','eve','jamie','jane','liza','melissa','tracy','robin','sophia','alex','angel','edward','homer','jamie','john','kevin','kurt','mee','person']}
	self.mission = {'name': 'ask him for his name and tell it to you',
			'time':'tell him the time',
			'question':'answer him a question',
			'your-name':'tell him my name',
			'your-team':'tell him the name of our team',
			'date':'tell him what is the date today',
			'what-day': 'tell him what day is it today',
			'his-name':'ask him for his name and tell it to you',
			'her-name':'ask her for her name and tell it to you'
			}
	#self.catch = {'mission' : 0, 'object': 0, 'src_loc' : 0, 'dst_loc' : 0, 'target' : 0}
		


        # used to match the keywords recognized with a sentence the robot will say

        # Create the sound client object
	self.start_recog = 0 
	self.repeat_data = ''  
        self.soundhandle = SoundClient() 
        rospy.sleep(1)
        self.soundhandle.stopAll()
        # Announce that we are ready for input
        #self.soundhandle.playWave(self.wavepath + "R2D2a.wav")
	#self.soundhandle.playWave("../sound/R2D2a.wav")
        rospy.sleep(1) 
        self.soundhandle.say("Ready", self.voice)
	rospy.sleep(2) 
        # rospy.loginfo("Say one of the navigation temps...") 
	
	# Initiate Publishers 
        self.gpsr_srclocation = rospy.Publisher('gpsr_srclocation', String, queue_size=10)
	self.gpsr_dstlocation = rospy.Publisher('gpsr_dstlocation', String, queue_size=10) 
	self.gpsr_name = rospy.Publisher('gpsr_name', String, queue_size=10)
	self.gpsr_missiontype = rospy.Publisher('gpsr_mstype', Int8, queue_size = 10)
	self.gpsr_mission = rospy.Publisher('gpsr_mission', String, queue_size=10)
	self.gpsr_object = rospy.Publisher('gpsr_object',String,queue_size=10)               
	self.gpsr_begin = rospy.Publisher('gpsr_begin', String, queue_size=10)
	
        # rospy.init_node('temp', anonymous=True)
	#
        # Subscribe to the recognizer output
        rospy.Subscriber('recognizer_output', String, self.talk_back) 
#提取关键词
    def get_temp_temp(self, data):
        for (place, keywords) in self.keywords_to_temp_temp.iteritems():
            for word in keywords:  
		if data.find(word) > -1:
			return word
            return 'None'
    def get_temp_locations(self, data):
	word_list = data.split()
	for index in range(self.pos,len(word_list)):
            for (temp, keywords) in self.keywords_to_temp_locations.iteritems():
            	for word in keywords:
             	   if word_list[index] == word:
			self.pos = index + 1
		        return word
        return 'None'

    def get_temp_names(self, data):
        for (temp, keywords) in self.keywords_to_temp_names.iteritems():
            for word in keywords:
                if data.find(word) > -1:
                    return word
            return 'None'

    def get_temp_object(self, data):
        for (temp, keywords) in self.keywords_to_temp_object.iteritems(): 
            for word in keywords:
                if data.find(word) > -1:
                    return word
            return 'None'
        
    def delete_none(self,data):
         for k in range(len(data)): 
            if data[k]== 'None':
                del data[k]

    def form_the_question(self, word_count):#根据关键词复述问题
	if self.start_recog == 1 :#识别到'kamerader'
		if word_count > 2 :          # type C or D
			if self.command['mission'] != '':  # type D
				if self.command['src_loc'] == '' :
					self.question = 'sorry where should i go to find a' + self.command['object']
				elif self.command['object'] == '' :
					self.question = 'sorry what do you want me to find in the'+ self.command['src_loc']
				elif self.command['target'] == '' :
					self.question = 'sorry who is the' + self.command['object'] + 'prepared for' 	
				elif self.command['object'] == 'person':       # recognized all the keywords
				     self.repeat_data = 'did you ask me to go to the' + self.command['src_loc'] + 'to find a ' + self.command['target'] + 'and' + self.mission[ self.command['mission'] ]
				else :       # recognized all the keywords
				     self.repeat_data = 'did you ask me to go to the' + self.command['src_loc'] + 'to find a' + self.command['object'] + 'take it to' + self.command['target'] + 'and' + self.mission[ self.command['mission'] ]    
			elif self.command['dst_loc'] != '' :  # type C
				if self.command['src_loc'] == '' : 
					self.question = 'sorry where should i go to find a' + self.command['object']
				elif self.command['object'] == '' :
					self.question = 'sorry what do you want me to find in the'+ self.command['src_loc']
	 			else :
					self.repeat_data = 'did you ask me to go to the' + self.command['src_loc'] + 'to find a' + self.command['object'] + 'take it to the' + self.command['dst_loc']	
			else : 	     # dst_loc is missing or doesn't exist
				self.repeat_data = 'did you ask me to go to the' + self.command['src_loc'] + 'to find a' + self.command['object'] + 'take it to' + self.command['target']
			
		else :  		     # type A or B or C, D with missing points (word_count <= 2)
	#		print self.command['mission']		
			if (self.command['mission'] != ''):    # type B
				self.repeat_data = 'did you ask me to find a person and'+ self.mission[ self.command['mission'] ]
			else: 		     # type B with missing points or type A
				if self.command['object'] == 'person':
					self.question = 'sorry what do you want me to do with the person'
				else: 	     # type A
					if word_count == 0:
						self.question = 'sorry i did not get it could you please repeat the question louder and slower'
					elif self.command['src_loc'] == '' :
						self.question = 'sorry where should i go to find a' + self.command['object']
					elif self.command['object'] == '' :
						self.question = 'sorry what do you want me to find in the'+ self.command['src_loc']
					else :
						self.repeat_data = 'did you ask me to go to the' + self.command['src_loc'] + 'and find a' + self.command['object']
		self.start_recog = 0
	if self.repeat_data != 'None':
		self.soundhandle.say(self.repeat_data,self.voice)
		rospy.sleep(5)
		rospy.sleep(3)
		self.soundhandle.say('please say my name kamerider before this answer',self.voice)
		rospy.sleep(5)
		rospy.sleep(3)
        	self.makesure = 1
	else: 
		self.soundhandle.say(self.question,self.voice)
		rospy.sleep(7)
		rospy.sleep(5)

    def talk_back(self, msg):
        # Print the recognized words on the screen  
        rospy.loginfo(msg.data)
        msg.data = msg.data.lower()
	print msg.data
	
	self.repeat_data = 'None'  
	if msg.data.find('kamerider') > -1:	# recognize 'kamerider'
		self.start_recog = 1   
	#else: 
	if msg.data.find('kamerider-yes') > -1:  # recognized "kamerider yes"
			for (key,value) in self.command.items(): 
				print key+':'
				print self.command[key] + '\n'
			self.gpsr_begin.publish('start')
     			self.gpsr_srclocation.publish(self.command['src_loc'])
			self.gpsr_dstlocation.publish(self.command['dst_loc'])
			self.gpsr_mission.publish(self.command['mission'])
			self.gpsr_name.publish(self.command['target'])
			self.gpsr_object.publish(self.command['object'])
			self.gpsr_missiontype.publish(self.mission_type)
			self.finished = 1
			for (key,value) in self.temp.items(): 
				self.temp[key] = ''
				self.command[key] = ''
			self.soundhandle.say('ok i will follow the command', self.voice)
			#self.start_recog = 0   
			#self.first_recog = 1
	if msg.data.find('kamerider-no') > -1 : # recognized "kamerider no"  
			###########################################################################

			###########################################################################
			self.soundhandle.say('sorry could you please repeat the question louder and slower')
			#self.start_recog = 0
			self.first_recog = 1
			for (key,value) in self.needupdate.items():
				self.needupdate[key] = 1
#	else : self.start_recog = 1

	if self.start_recog == 1 and self.finished != 1:	
		# Give the feedback if it recognizes message succesfully
		self.temp['src_loc'] = self.get_temp_locations(msg.data)
        	self.temp['dst_loc'] = self.get_temp_locations(msg.data)		
		self.temp['mission'] = self.get_temp_temp(msg.data)
		self.temp['target'] = self.get_temp_names(msg.data)
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
		    if self.temp[key] != 'None':
			if self.first_recog == 1:
				self.needupdate[key] = 0
				self.command[key] = self.temp[key]  # bug
			word_count = word_count + 1
			   # store valid commands in self.command

		if self.first_recog == 1:	# the first time to start recognition
		# Calculate the num of words in valid temp words
			self.first_recog = 0   # next time is not the first time to recognize	
			self.form_the_question(word_count)
		else: # if not the first time to start recognition
			for (key,word) in self.temp.items():
				if self.needupdate[key] == 1 and self.temp[key] != 'None':
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


