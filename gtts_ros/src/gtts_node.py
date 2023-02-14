#!/usr/bin/env python3

import os
import rospy
import actionlib

from gtts import gTTS
from std_msgs.msg import String

import gtts_ros.msg

class GTTS_ROS:
    """docstring for GTTS_ROS"""

    # create messages that are used to publish feedback/result
    _feedback = gtts_ros.msg.TalkFeedback()
    _result = gtts_ros.msg.TalkResult()

    def __init__(self):
        self.online = rospy.get_param('~ONLINE')
        self._action_name = "gtts_ros"
        self._as = actionlib.SimpleActionServer(self._action_name, gtts_ros.msg.TalkAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
        rospy.loginfo('Ready to talk.')

    def execute_cb(self, goal):
        # helper variables
        r = rospy.Rate(1)
        success = True

        # publish the feedback
        rospy.loginfo('%s: Executing' % self._action_name)
        self._feedback.feedback = "Executing"
        self._as.publish_feedback(self._feedback)

        #
        # if self.online == False:
        #     os.system("./flite/bin/flite -voice slt '"+goal.phrase+"' /tmp/flite.wav && play /tmp/flite.wav")
        # else:    
        # tts = gTTS(text=goal.phrase.decode('utf-8'), lang='pt', tld='com.br')
        # tts = gTTS(text=goal.phrase.decode('utf-8'), lang='en', tld='co.uk')
        tts = gTTS(text=goal.phrase, lang='en', tld='co.uk')
        tts.save("talk.mp3")
        # os.system("mpg321 talk.mp3/ -g 100 >/dev/null 2>&1")
        os.system("ffplay talk.mp3 -autoexit -nodisp")

        # publish the result
        rospy.loginfo('%s: Succeeded' % self._action_name)
        self._result.result = "Succeeded"
        self._as.set_succeeded(self._result)

if __name__ == "__main__":
    rospy.init_node('gtts_ros', anonymous=True)
    GTTS_ROS()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
