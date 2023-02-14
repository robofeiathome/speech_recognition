#!/usr/bin/env python3

import sys
import rospy
import time
from gsr_ros.msg import *
from gsr_ros.srv import *

class Client_recog():
    def __init__(self):
        rospy.init_node('ClientSpeech')
        self.PATH = rospy.get_param('~PATH2')
        #print self.PATH
        self.choice = []

        filea = open(str(self.PATH+'beacon.txt'),'r')
        self.beacon = []
        for i in filea:
            self.beacon.append(i.replace('\n',''))
        filea.close()

        self.create_choices('beacon',self.beacon)

        filea = open(str(self.PATH+'placements.txt'),'r')
        self.locations = []
        for i in filea:
            self.locations.append(i.replace('\n',''))
        filea.close()

        self.create_choices('placement',self.locations)

        filea = open(str(self.PATH+'rooms.txt'),'r')
        self.rooms = []
        for i in filea:
            self.rooms.append(i.replace('\n',''))
        filea.close()

        self.create_choices('room',self.rooms)

        self.objects = []
        filea = open(str(self.PATH+'objects.txt'),'r')
        for i in filea:
            self.objects.append(i.replace('\n',''))
        filea.close()

        self.create_choices('object',self.objects)

        self.create_choices('adja',['biggest','smallest','heaviest','lightest'])
        self.create_choices('adjr',['heavier','smaller','bigger','lighter'])
        self.create_choices('gesture',['waving',"raising their left arm",'raising their right arm','pointing to the left','pointing to the right'])
        self.create_choices('gprsng',['male or female','man or woman','boy or girl'])
        self.create_choices('gprsn',['male','female','man','woman','boy','girl'])
        self.create_choices('color',['red','blue','white','black','green','yellow'])
        self.create_choices('category',["toiletries","fruits","snacks","food","drinks","cutlery","tableware","containers"])
        self.create_choices('posppl',['sitting','standing','lying','sitting or lying down','standing or lying down','standing or sitting'])
        self.create_choices('posprs',['sitting','standing','lying'])
        self.create_choices('people',['men','women','boys','girls','male','female','children','adults','elders'])

        #print self.choice 

        self.spec = []
        filea = open(str(self.PATH+'spec.txt'),'r')
        for i in filea:
            self.spec.append(i.replace('\n',''))
        filea.close()

        self.execute()

    def create_choices(self,ID,LiVal):
        x = gsr_ros.msg._Opcs.Opcs()
        x.id = ID
        x.values = LiVal
        self.choice.append(x)
        

    def execute(self):
        rospy.wait_for_service('Recognition')
        rospy.loginfo("Please wait 10 seconds")
        time.sleep(10)
        rospy.loginfo("I am ready")
        time.sleep(3)
        while True:
            try:
                #try:
                #    raw_input('next? just press enter: ')
                #except KeyboardInterrupt:
                #    exit()
                recog = rospy.ServiceProxy('Recognition', Start)
                resp1 = recog(self.spec, self.choice)
                print resp1
            except rospy.ServiceException, e:
                print "Service call failed: %s"%e
            except KeyboardInterrupt:
                exit()
            time.sleep(5)


if __name__ == "__main__":
    Client_recog()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.logginfo("Keyboard interrupted... Bye")