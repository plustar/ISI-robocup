#!/usr/bin/env python
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
		self.gpsr_begin = rospy.Publisher('/gpsr_begin', String, queue_size=10)

		# rospy.init_node('temp', anonymous=True)

		# Subscribe to the recognizer output
		rospy.Subscriber('recognizer_output', String, self.talkback)
	def talkback(self, msg):
		# Print the recognized words on the screen  
		rospy.loginfo(msg.data)
		msg.data = msg.data.lower()

		print msg.data
		#else:
		if msg.data.find('bedroom') > -1:

			self.soundhandle.say('ok i will go to the bedroom',self.voice)
			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('bedroom')
			self.gpsr_dstlocation.publish('bedroom')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('kitchen') > -1:

			self.soundhandle.say('ok i will go to the shelf',self.voice)
			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('kitchen')
			self.gpsr_dstlocation.publish('kitchen')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('dining-room') > -1:
			self.soundhandle.say('ok i will go to the dining room',self.voice)
			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('dining_room')
			self.gpsr_dstlocation.publish('dining_room')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('living-room') > -1:

			self.soundhandle.say('ok i will go to the living room',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('living_room')
			self.gpsr_dstlocation.publish('living_room')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('hallway') > -1:

			self.soundhandle.say('ok i will go to the living room',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('hallway')
			self.gpsr_dstlocation.publish('hallway')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('shelf') > -1:
			self.soundhandle.say('ok i will go to the shelf',self.voice)
			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('shelf')
			self.gpsr_dstlocation.publish('shelf')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('side-board') > -1:

			self.soundhandle.say('ok i will go to the sideboard',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('side_board')
			self.gpsr_dstlocation.publish('side_board')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('dresser') > -1:

			self.soundhandle.say('ok i will go to the dresser',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('dresser')
			self.gpsr_dstlocation.publish('dresser')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('sink') > -1:

			self.soundhandle.say('ok i will go to the sink',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('sink')
			self.gpsr_dstlocation.publish('sink')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('stove') > -1:

			self.soundhandle.say('ok i will go to the stove',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('stove')
			self.gpsr_dstlocation.publish('stove')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('bar') > -1:

			self.soundhandle.say('ok i will go to the bar',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('bar')
			self.gpsr_dstlocation.publish('bar')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('side-table') > -1:

			self.soundhandle.say('ok i will go to the sidetable',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('side_board')
			self.gpsr_dstlocation.publish('side_board')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('cabinet') > -1:

			self.soundhandle.say('ok i will go to the cabinet',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('cabinet')
			self.gpsr_dstlocation.publish('cabinet')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('dinner-table') > -1:

			self.soundhandle.say('ok i will go to the dinner table',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('dinner_table')
			self.gpsr_dstlocation.publish('dinner_table')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
			
		if msg.data.find('dinner-room-table') > -1:
			self.soundhandle.say('ok i will go to the dinner-room-table',self.voice)
			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('dinner_room_table')
			self.gpsr_dstlocation.publish('dinner_room_table')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
			
		if msg.data.find('couch-table') > -1:
			self.soundhandle.say('ok i will go to the couch table',self.voice)
			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('couch_table')
			self.gpsr_dstlocation.publish('couch_table')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('hanger') > -1:
			self.soundhandle.say('ok i will go to the hanger',self.voice)
			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('hanger')
			self.gpsr_dstlocation.publish('hanger')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('trash-bin') > -1:
			self.soundhandle.say('ok i will go to the trash bin',self.voice)
			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('trash_bin')
			self.gpsr_dstlocation.publish('trash_bin')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('bed') > -1:
			self.soundhandle.say('ok i will go to the bed',self.voice)
			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('bed')
			self.gpsr_dstlocation.publish('bed')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('dinner-room-sofa') > -1:

			self.soundhandle.say('ok i will go to the dinner room sofa',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('dinner_room_sofa')
			self.gpsr_dstlocation.publish('dinner_room_sofa')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('fridge') > -1:

			self.soundhandle.say('ok i will go to the fridge',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('fridge')
			self.gpsr_dstlocation.publish('fridge')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('sofa') > -1:

			self.soundhandle.say('ok i will go to the sofa',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('sofa')
			self.gpsr_dstlocation.publish('sofa')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('tv') > -1:
			self.soundhandle.say('ok i will go to the tv',self.voice)

			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('tv')
			self.gpsr_dstlocation.publish('tv')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
		if msg.data.find('desk') > -1:
			self.soundhandle.say('ok i will go to the desk',self.voice)
			rospy.sleep(5)
			self.gpsr_begin.publish('start')
			self.gpsr_srclocation.publish('desk')
			self.gpsr_dstlocation.publish('desk')
			self.gpsr_mission.publish('')
			self.gpsr_name.publish('')
			self.gpsr_object.publish('CoffeeMate')
			self.gpsr_missiontype.publish(-1)
			#self.start_recog = 0
			#self.first_recog = 1
	def cleanup(self):
		rospy.loginfo("Shutting down gpsr node...")

if __name__=="__main__":
	rospy.init_node('gpsr')
	try:
		gpsr()
		rospy.spin()
	except:
		pass


