#!/usr/bin/env python

"""
    talkback.py - Say back what is heard by the pocketsphinx recognizer.
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
import datetime
import re
import time
from std_msgs.msg import String

from sound_play.libsoundplay import SoundClient

class TalkBack:
      
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.voice = rospy.get_param("~voice", "voice_don_diphone")
        self.wavepath = rospy.get_param("~wavepath", "")
        
#	self.open_object_name = rospy.Publisher('open_object_name', String, queue_size=10)
        # Create the sound client object
        self.soundhandle = SoundClient()
        rospy.sleep(1)
        self.soundhandle.stopAll()
#	self.ready = 0
        # Announce that we are ready for input
#       self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
#        rospy.sleep(1)
	self.soundhandle.say("Dear operater", self.voice)
	rospy.sleep(2)
	self.soundhandle.say("Please say my name kamerider before each question", self.voice)
	rospy.sleep(4)
	self.soundhandle.say("thank you", self.voice)
	rospy.sleep(1.3)
	self.soundhandle.say("Now I am ready for your question", self.voice)
	rospy.sleep(3)

        #rospy.loginfo("Say one of the navigation commands...")

        # self.open_object_name = rospy.Publisher('open_object_name', String, queue_size=10)
        # rospy.init_node('command', anonymous=True)

        # Subscribe to the recognizer output
        # rospy.Subscriber('speech_recognition_start', String, self.start)
	rospy.Subscriber('recognizer_output', String, self.recognition)
    def recognition(self, msg) :
	msg.data = msg.data.lower()
	print msg.data
	if msg.data.find('kamerider') > -1:
		self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
		rospy.sleep(1)
		if msg.data.find('german-count') > -1 or msg.data.find('invented the zeppelin') > -1 or msg.data.find('invented the the zeppelin') > -1 or msg.data.find('invented zeppelin') > -1 :
			print 555
	      		self.soundhandle.say('Count von Zeppelin invented the zeppelin', self.voice)
	       		rospy.sleep(4)
		elif msg.data.find('first-president') > -1 or msg.data.find('the-usa') > -1 : 
			self.soundhandle.say('george washington was the first president of america', self.voice)
			rospy.sleep(4)
		elif msg.data.find('titanic built') > -1 or msg.data.find('titanic-built') > -1 or msg.data.find('in which city') > -1 :
			self.soundhandle.say('titanic was builted in belfast', self.voice)
			rospy.sleep(4)
		elif msg.data.find('queen-victoria') > -1 or msg.data.find('how-many-children') > -1 :
			self.soundhandle.say('she had nine children', self.voice)
			rospy.sleep(4)
		elif msg.data.find('french-king') > -1 or msg.data.find('the-sun-king') > -1 :
			self.soundhandle.say('louis fourteen was called the sun king', self.voice)
			rospy.sleep(4)
		elif msg.data.find('in england') > -1 or msg.data.find('in the england') > -1 or msg.data.find('northern-frontier') > -1 or msg.data.find('roman-empire') > -1 : 
			self.soundhandle.say('the hadrians wall was the northern frontier of the england', self.voice)
			rospy.sleep(4)
		elif msg.data.find('former-name') > -1 or msg.data.find('new-york') > -1 : 
			self.soundhandle.say('the former name of new york was new amsterdam', self.voice)
			rospy.sleep(4)
		elif msg.data.find('another-name') > -1 or msg.data.find('study of fosslis') > -1 or msg.data.find('study the fosslis') > -1 or msg.data.find('study-of-the-fosslis') > -1 : 
			self.soundhandle.say('the another name for the study of fossils is paleontology', self.voice)
			rospy.sleep(4)
		elif msg.data.find('dragonflies') > -1 or msg.data.find('prefer-to-eat') > -1 : 
			self.soundhandle.say('dragonfilies prefer to eat mosquitoes', self.voice)
			rospy.sleep(4)	
		elif msg.data.find('cannot-fly') > -1 or msg.data.find('but can jump') > -1 : 
			self.soundhandle.say('they are fleas', self.voice)
			rospy.sleep(4)
		elif msg.data.find('european-bison') > -1 : 
			self.soundhandle.say('the name of the european bison is wisent', self.voice)
			rospy.sleep(4)
		elif msg.data.find('called a fish') > -1 or msg.data.find('called fish') > -1 or msg.data.find('called the fish') > -1 or msg.data.find('snake-like') > -1 : 
			self.soundhandle.say('eel fish is called a fish with a snake-like body', self.voice)
			rospy.sleep(4)
		elif msg.data.find('which-plant') > -1 or msg.data.find('canadian-flag') > -1 : 
			self.soundhandle.say('maple plant does the canadian-flag contain', self.voice)
			rospy.sleep(4)
		elif msg.data.find('house-number') > -1 or msg.data.find('simpsons') > -1 : 
			self.soundhandle.say('the house number of the simpsons is seven hundred and forty-two', self.voice)
			rospy.sleep(4)
		elif msg.data.find('in computing') > -1 or msg.data.find('ram short') > -1 or msg.data.find('ram the short') > -1 or msg.data.find('short-for') > -1 : 
			self.soundhandle.say('the random access memory is short for ram', self.voice)
			rospy.sleep(4)
		elif msg.data.find('which-hemisphere') > -1 or msg.data.find('the-most-dinosaur') > -1 or msg.data.find('dinosaur-skeletons') > -1 : 
			self.soundhandle.say('most dinosaur skeletons have been found in the northern hemisphere', self.voice)
			rospy.sleep(4)
		elif msg.data.find('color-is-cobalt') > -1 or msg.data.find('cobalt') > -1 : 
			self.soundhandle.say('the color of cobalt is blue', self.voice)
			rospy.sleep(4)
		elif msg.data.find('which device') > -1 or msg.data.find('use to look at') > -1 or msg.data.find('at-the-stars') > -1 or msg.data.find('at-stars') > -1 : 
			self.soundhandle.say('we also use telescope to look at the stars', self.voice)
			rospy.sleep(4)
		elif msg.data.find('light-intensity') > -1 : 
			self.soundhandle.say('candela also indicates the light intensity', self.voice)
			rospy.sleep(4)
		elif msg.data.find('first-american') > -1 : 
			self.soundhandle.say('alan shepard was the first american in space', self.voice)
			rospy.sleep(4)
		elif msg.data.find('steam-engine') > -1 : 
			self.soundhandle.say('james watt was the inventor of the steam engine', self.voice)
			rospy.sleep(4)
		elif msg.data.find('henry-mill') > -1 : 
			self.soundhandle.say('the typewriter was invented by henry mill', self.voice)
			rospy.sleep(4)
		elif msg.data.find('lightest') > -1 or msg.data.find('existing-metal') > -1 : 
			self.soundhandle.say('aluminium is the lightest existing metal', self.voice)
			rospy.sleep(4)
		elif msg.data.find('primary-colors') > -1 : 
               		self.soundhandle.say('they are blue yellow and red', self.voice)
			rospy.sleep(4)
		elif msg.data.find('planet') > -1 or msg.data.find('nearest-the-sun') > -1 : 
			self.soundhandle.say('the planet nearest-the-sun is mercury', self.voice)
			rospy.sleep(4)
		elif msg.data.find('great-wall') > -1 : 
			self.soundhandle.say('it is six thousand two hundred fifty-nine kilometers', self.voice)
			rospy.sleep(4)
		elif msg.data.find('largest-number') > -1 or msg.data.find('five-digits') > -1 : 
			self.soundhandle.say('the largest number of five digits is ninty-nine thousand nine hundred and ninty-nine', self.voice)
			rospy.sleep(4)
		elif msg.data.find('new-zealand') > -1 or msg.data.find('on-the-flag') > -1 or msg.data.find('on flag') > -1 or msg.data.find('on the the flag') > -1 : 
			self.soundhandle.say('there are four stars on the flag of new zealand', self.voice)
			rospy.sleep(4)
		else :
			print msg.data
			self.soundhandle.say('Dear opreater', self.voice)
			rospy.sleep(1.5)
			self.soundhandle.say('Please repeat your question louder and slower', self.voice)
			rospy.sleep(3)
		msg.data = ''
		self.soundhandle.say('now you can ask another question', self.voice)
		rospy.sleep(3)


    def cleanup(self):
        rospy.loginfo("Shutting down talkback node...")

if __name__=="__main__":
    rospy.init_node('talkback')
    try:
        TalkBack()
        rospy.spin()
    except:
        pass

