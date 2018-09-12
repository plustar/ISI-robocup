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
        if msg.data.find('kamerider') > -1 and msg.data.find('table') > -1:

            self.soundhandle.say('ok i will follow the command',self.voice)

            rospy.sleep(3)
            self.gpsr_begin.publish('start')
            self.gpsr_srclocation.publish('table')
            self.gpsr_dstlocation.publish('sofa')
            self.gpsr_mission.publish('')
            self.gpsr_name.publish('')
            self.gpsr_object.publish('green-tea')
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


