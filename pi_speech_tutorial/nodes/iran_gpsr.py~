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

import roslib; roslib.load_manifest('speech')
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8

from sound_play.libsoundplay import SoundClient

class gpsr:
      
    def __init__(self):

    rospy.on_shutdown(self.cleanup)
    self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")//说话人
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
    self.keywords_to_temp_object = {'object': ['sprite','hype','chocolate-milk','coca','tooth-paste','noodle','pringles','sweet-corn','biscuits','spray','shampoo','digestive', 'hand-wash-liquid','fanta','banana','nutella','apple', 'ketchup','orange','compote','bag','tray','cappuccino', 'shaving-foam','coffee-mate',
'snack','water']}

    self.keywords_to_temp_people_locations = {'location': ['bed','bedroom','dinning-room','dinning-room-sofa','tv','sofa','trash-bin','shelf','living-room','hanger','hallway','kitchen']}
#fridgelivingroom','bar','on-the-sofa','in-the-bedroom','on-the-bed','in-the-hallway']}

    self.keywords_to_temp_object_locations = {'location': ['shelf','side-board','dresser','sink','stove','bar','side-table','cabinet','dinner-table','dinning-room-table','couch-table']}
    self.keywords_to_temp_names ={'name':['michael','jessica','christopher','ashley','matthew','brittany','joshua','amanda','danial','samantha','david','sarah','andrew','stephanie', 'james','jennifer','justin','elizabeth','joseph','lauren','mee','person']}
	self.mission = {'name': 'ask him for his name and tell it to you',
			'time':'tell him the time',
			'question':'answer him a question',
			'your-name':'tell him my name',
			'your-team':'tell him the name of our team',
			'date':'tell him what is the date today',
			'what-day': 'tell him what day is it today',
			'the-name':'ask him for the persons name and tell it to you',
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
    def get_temp_object_src_locations(self, data):
	    word_list = data.split()
	    for index in range(self.pos,len(word_list)):
                for (temp, keywords) in self.keywords_to_temp_object_locations.iteritems():
                	for word in keywords:
                 	   if word_list[index] == word:
			    self.pos = index + 1
		            return word
            return 'None'
    def get_temp_object_dst_locations(self, data):
	    word_list = data.split()
	    for index in range(self.pos,len(word_list)):
                for (temp, keywords) in self.keywords_to_temp_object_locations.iteritems():
                	for word in keywords:
                 	   if word_list[index] == word:
			    self.pos = index + 1
		            return word
            return 'None'
    def get_temp_people_locations(self, data):
	    word_list = data.split()
	    for index in range(self.pos,len(word_list)):
                for (temp, keywords) in self.keywords_to_temp_people_locations.iteritems():
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
        if self.start_recog == 1:#识别到'kamerader'
		    if word_count > 2 :          # type C or D
		        if self.command['dst_object_loc'] != '' and self.command['src_object_loc']==self.command['dst_object_loc']
		            self.command['dst_object_loc']=''
		        if self.command['dst_object_loc'] != '' and (self.command['src_object_loc'] != '' or if self.command['object'] != ''):#至少识别两种词汇，认为把物体从某处移动到某处
                    if self.command['src_object_loc'] != '':
		                if self.command['object'] != ''
                            self.repeat_data = 'did you ask me to go to the' + self.command['src_object_loc'] + 'to find ' + self.command['object'] + 'and take it to the ' + self.command['src_object_loc']
                        if self.command['object'] == ''
                            self.question = 'sorry what do you want me to find in the'+ self.command['src_loc'] + 'and take it to the ' + self.command['src_object_loc']
                    if self.command['src_object_loc'] == '':
                        if self.command['object'] != ''
                            self.repeat_data = 'sorry where should i go to find the' + self.command['object'] + 'and take it to the ' + self.command['src_object_loc']
                else:
                    if self.command['object'] == ''
                        if self.command['people_loc'] != '':#至少识别到两种词汇
                            if self.command['target'] != ''
                                if self.command['mission'] != '':
                                    self.repeat_data = 'did you ask me to go to the' + self.command['people_loc'] + 'to find ' + self.command['target'] + ' and ' + self.mission[ self.command['mission'] ]
                                if self.command['mission'] == '':
                                    self.question = 'sorry what do you want me to do with the person'
                            if self.command['target'] == ''
                                if self.command['mission'] != '':
                                    self.question = 'sorry whom should I go to and ' + self.mission[ self.command['mission'] ]
                        if self.command['people_loc'] == '':
                            if self.command['target'] != ''
                                if self.command['mission'] != '':
                                    self.question = 'sorry where should i go to find a' + self.command['target']
                                if self.command['mission'] == '':
                                    self.question = 'sorry where should i go to find a' + self.command['target'] + 'and what do you want me to do with the person'
                    if self.command['object'] != ''
                        if self.command['people_loc'] != '':
                            if self.command['target'] != '':
                                if self.command['mission'] != '':
                                    if self.command['src_object_loc'] != '':
                                    self.repeat_data = 'did you ask me to go to the' self.command['src_object_loc'] + ' to grasp ' +  self.command['object']  + 'and give it to ' + self.command['target'] + self.command['people_loc'] ' and ' + self.mission[ self.command['mission'] ]
                                    if self.command['src_object_loc'] == '':
                                        self.question = 'sorry where should i go to find a' + self.command['object']
                                if self.command['mission'] == '':
                                    if self.command['src_object_loc'] != '':
                                        self.question = 'sorry what do you want me to do with the person'
                                    if self.command['src_object_loc'] == '':
                                        self.question = 'sorry where should i go to find a' + self.command['object'] + ' and what do you want me to do with the person ' 
                            if self.command['target'] == '': 
                                if self.command['mission'] != '':
                                    if self.command['src_object_loc'] != '':
                                        self.question = ' sorry whom should I go to '
                                    if self.command['src_object_loc'] == '':
                                        self.question = 'sorry where should i go to find a' + self.command['object'] + 'and whom should I go to '
                                if self.command['mission'] == '':
                                    if self.command['src_object_loc'] != '':
                                        self.question = 'sorry whom should I go to and what do you want me to do with the person'
                                    if self.command['src_object_loc'] == '':
                                        self.question = 'sorry where should i go to find a' + self.command['object'] + ' and whom should I go to and what do you want me to do with the person ' 
                                        
                        if self.command['people_loc'] == '':
                            if self.command['target'] != '':
                                if self.command['mission'] != '':
                                    if self.command['src_object_loc'] != '':
                                        self.question = 'sorry where should i go to find ' + self.command['target']
                                    if self.command['src_object_loc'] == '':
                                        self.question = 'sorry where should i go to find a' + self.command['object'] + ' and where should i go to find ' + self.command['target']
                                if self.command['mission'] == '':
                                    if self.command['src_object_loc'] != '':
                                        self.question = 'sorry what do you want me to do with the person' + ' and where should i go to find '+' + self.command['target']
                                    if self.command['src_object_loc'] == '':
                                        self.question = 'sorry where should i go to find a ' + self.command['object'] + ' and where should i go to find ' + self.command['target'] + ' and what do you want me to do with ' + self.command['target']
                            if self.command['target'] == '': 
                                if self.command['mission'] != '':
                                    if self.command['src_object_loc'] != '':
                                        self.question = ' sorry where should i go and and whom should i find '
                                    if self.command['src_object_loc'] == '':
                                        self.question = ' sorry where should i go to find a' + self.command['object'] + ' and where should i go and and whom should i find'
                                if self.command['mission'] == '':
                                    if self.command['src_object_loc'] != '':
                                        self.question = 'sorry where should i go and and whom should i find, and what do you want me to do with the person'                                   
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
		self.temp['people_loc'] = self.get_temp_people_locations(msg.data)
    	self.temp['src_object_loc'] = self.get_temp_object_src_locations(msg.data)
    	self.temp['dst_object_loc'] = self.get_temp_object_dst_locations(msg.data)	
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
        rospy.loginfo("Shutting down general node...")

if __name__=="__main__":
    rospy.init_node('general')
    try:
        gpsr()
        rospy.spin()
    except:
        pass


