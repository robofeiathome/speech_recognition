#!/usr/bin/env python3

import sys
import rospy
import time
from gsr_ros.msg import *
from gsr_ros.srv import *

class Gpsr_recog():
    def __init__(self):
        rospy.init_node('GPSR_client')
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

        self.names = []
        filea = open(str(self.PATH+'name.txt'),'r')
        for i in filea:
            self.names.append(i.replace('\n',''))
        filea.close()

        self.create_choices('name',self.names)

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
        self.create_choices('vbbring',['bring','give'])
        self.create_choices('vbtake',['bring','take'])
        self.create_choices('vbdeliver',['bring','give','deliver'])
        self.create_choices('vbplace',['put','place'])
        self.create_choices('vbfind',['find','locate','look for'])
        self.create_choices('vbgopl',['go','navigate'])
        self.create_choices('vbspeak',['tell','say'])
        self.create_choices('whattosay',['something about yourself','the time','what day is today','what day is tomorrow', 
            "your team's name", "your team's country", "your team's affiliation", 'the day of the week', 'the day of the month',
            'a joke'])
        self.create_choices('vbfollow',['follow'])
        self.create_choices('pron',['her','him','it'])
        self.create_choices('vbguide',['guide','escort','take','lead','accompany'])

        #print self.choice 

        self.spec = []
        filea = open(str(self.PATH+'gpsr_spec.txt'),'r')
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
        rospy.loginfo("Starting GPSR. Please wait 10 seconds")
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
                #resp1 = recog(self.spec, self.choice)
                resp1 = recog('',[])
                print resp1
            except rospy.ServiceException, e:
                print "Service call failed: %s"%e
            except KeyboardInterrupt:
                exit()
            time.sleep(5)


if __name__ == "__main__":
    Gpsr_recog()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.logginfo("Keyboard interrupted... Bye")