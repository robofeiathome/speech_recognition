#!/usr/bin/env python3

from gsr_ros.msg import *
from gsr_ros.srv import *
import rospy
import numpy
import speech_recognition as sr
from difflib import SequenceMatcher
import datetime
import sys
import os
import time

class Recognition_server():

	def __init__(self):
		rospy.init_node('SpeechRecognition')
		self.API = rospy.get_param('~API')
		self.Key1 = rospy.get_param('~KEY1')
		self.Key2 = rospy.get_param('~KEY2')
		self.PATH = rospy.get_param('~PATH')
		self.r = sr.Recognizer()
		self.s = rospy.Service('Recognition', Start, self.recognition)
		rospy.loginfo("Ready to recognize")
		rospy.spin()

	def recognition(self,req):
		chosen_one = ""
		similar = 0.0
		spec = ''
		choice = []
		with sr.Microphone() as source:
			self.r.adjust_for_ambient_noise(source, duration=2)
			time.sleep(2)
			os.system('ogg123 '+self.PATH+'/drip.ogg')
			time.sleep(1)
			print("Say something!")
			#audio = r.listen(source) Listen is a method where the computer will stop listening when there is silence
			#audio = r.record(source,duration=7) Record is a method where the duration is how many seconds must the computer record the voice
			audio = self.r.record(source,duration=7)
		
		recog = self.API_Recognition(audio)
		print recog
		if recog == 'Error while processing the audio' or SequenceMatcher(None, recog, "API error; x").ratio() >= 0.75:
			spec = recog
			resp = []
			x = gsr_ros.msg._Opcs.Opcs()
			resp.append(x)
		elif req.spec == '' and len(req.choices) == 0:
			spec = recog
			resp = []
			x = gsr_ros.msg._Opcs.Opcs()
			resp.append(x)
		else:
			p = self.Spec_calc(recog,req.spec)
			if p == 'Where is the <placement> located':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('Where is the <beacon> located',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'Where is the <beacon> located'
					resp = b
			elif p == 'Where is the <beacon> located':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('Where is the <placement> located',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'Where is the <placement> located'
					resp = b

			elif p == 'In which room is the <placement>':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('In which room is the <beacon>',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'In which room is the <beacon>'
					resp = b					
			
			elif p == 'In which room is the <beacon>':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('In which room is the <placement>',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'In which room is the <placement>'
					resp = b



			elif p == 'How many <placement> are in the <room>':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('How many <beacon> are in the <room>',recog,req.choices,True)
				pc,c = self.Choices_Calc('How many objects are in the <placement>',recog,req.choices,True)
				pd,d = self.Choices_Calc('How many <category> are in the <placement>',recog,req.choices,True)
				if pa >= pb and pa >= pc and pa >= pd:
					print 'maior pa'
					maior = pa
				if pb >= pa and pb >= pc and pb >= pd:
					print 'maior pb'
					maior = pb
				if pc >= pa and pc >= pb and pc >= pd:
					print 'maior pc'
					maior = pc
				if pd >= pa and pd >= pb and pd >= pc:
					print 'maior pd'
					maior = pd
				
				if maior == pb:
					spec = 	'How many <beacon> are in the <room>'
					resp = b
				elif maior == pc:
					spec = 'How many objects are in the <placement>'
					resp = c
				elif maior == pd:
					spec = 'How many <category> are in the <placement>'
					resp = d
				else:
					spec = p
					resp = a


			elif p == 'How many <beacon> are in the <room>':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('How many <placement> are in the <room>',recog,req.choices,True)
				pc,c = self.Choices_Calc('How many objects are in the <placement>',recog,req.choices,True)
				pd,d = self.Choices_Calc('How many <category> are in the <placement>',recog,req.choices,True)
				maior = 0.0
				#print pa, pb, pc, pd
				if pa >= pb and pa >= pc and pa >= pd:
					print 'maior pa'
					maior = pa
				if pb >= pa and pb >= pc and pb >= pd:
					print 'maior pb'
					maior = pb
				if pc >= pa and pc >= pb and pc >= pd:
					print 'maior pc'
					maior = pc
				if pd >= pa and pd >= pb and pd >= pc:
					print 'maior pd'
					maior = pd
				
				if maior == pb:
					spec = 	'How many <placement> are in the <room>'
					resp = b
				elif maior == pc:
					spec = 'How many objects are in the <placement>'
					resp = c
				elif maior == pd:
					spec = 'How many <category> are in the <placement>'
					resp = d
				else:
					spec = p
					resp = a

			elif p == 'How many objects are in the <placement>':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('How many <placement> are in the <room>',recog,req.choices,True)
				pc,c = self.Choices_Calc('How many <beacon> are in the <room>',recog,req.choices,True)
				pd,d = self.Choices_Calc('How many <category> are in the <placement>',recog,req.choices,True)
				maior = 0.0
				#print pa, pb, pc, pd
				if pa >= pb and pa >= pc and pa >= pd:
					print 'maior pa'
					maior = pa
				if pb >= pa and pb >= pc and pb >= pd:
					print 'maior pb'
					maior = pb
				if pc >= pa and pc >= pb and pc >= pd:
					print 'maior pc'
					maior = pc
				if pd >= pa and pd >= pb and pd >= pc:
					print 'maior pd'
					maior = pd
				
				if maior == pb:
					spec = 	'How many <placement> are in the <room>'
					resp = b
				elif maior == pc:
					spec = 'How many <beacon> are in the <room>'
					resp = c
				elif maior == pd:
					spec = 'How many <category> are in the <placement>'
					resp = d
				else:
					spec = p
					resp = a
				

			elif p == 'How many <category> are in the <placement>':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('How many <placement> are in the <room>',recog,req.choices,True)
				pc,c = self.Choices_Calc('How many <beacon> are in the <room>',recog,req.choices,True)
				pd,d = self.Choices_Calc('How many objects are in the <placement>',recog,req.choices,True)
				maior = 0.0
				#print pa, pb, pc, pd
				if pa >= pb and pa >= pc and pa >= pd:
					print 'maior pa'
					maior = pa
				if pb >= pa and pb >= pc and pb >= pd:
					print 'maior pb'
					maior = pb
				if pc >= pa and pc >= pb and pc >= pd:
					print 'maior pc'
					maior = pc
				if pd >= pa and pd >= pb and pd >= pc:
					print 'maior pd'
					maior = pd
				
				if maior == pb:
					spec = 	'How many <placement> are in the <room>'
					resp = b
				elif maior == pc:
					spec = 'How many <beacon> are in the <room>'
					resp = c
				elif maior == pd:
					spec = 'How many objects are in the <placement>'
					resp = d
				else:
					spec = p
					resp = a	




			elif p == 'How many people in the crowd are <gesture>':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('How many people in the crowd are <posppl>',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'How many people in the crowd are <posppl>'
					resp = b
			
			elif p == 'How many people in the crowd are <posppl>':
				a = self.Choices_Calc(p,recog,req.choices,True)
				b = self.Choices_Calc('How many people in the crowd are <gesture>',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'How many people in the crowd are <gesture>'
					resp = b

			elif p == 'Tell me if the person <gesture> was a <gprsn>':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('Tell me if the person <posprs> was a <gprsn>',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'Tell me if the person <posprs> was a <gprsn>'
					resp = b

			elif p == 'Tell me if the person <posprs> was a <gprsn>':
				a = self.Choices_Calc(p,recog,req.choices,True)
				b = self.Choices_Calc('Tell me if the person <gesture> was a <gprsn>',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'Tell me if the person <gesture> was a <gprsn>'
					resp = b


			elif p == 'Where can I find the <object>':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('Where can I find the <category>',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'Where can I find the <category>'
					resp = b
			elif p == 'Where can I find the <category>':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('Where can I find the <object>',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'Where can I find the <object>'
					resp = b

			elif p == 'Which is the <adja> object':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('Which is the <adja> <category>',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'Which is the <adja> <category>'
					resp = b
			elif p == 'Which is the <adja> <category>':
				pa,a = self.Choices_Calc(p,recog,req.choices,True)
				pb,b = self.Choices_Calc('Which is the <adja> object',recog,req.choices,True)
				if pa > pb:
					spec = p
					resp = a
				else:
					spec = 'Which is the <adja> object'
					resp = b
			else:
				spec = p
				resp = self.Choices_Calc(p,recog,req.choices)

		print spec
		print resp 

		return StartResponse(spec,resp)

	def Choices_Calc(self,spec,phrase,Choices,Percentage=False):
		s = spec.split()
		p = phrase.split()
		resp = []
		i = 0
		Sim_Rate = 0.0
		interm = ''
		newPhrase = spec
		for xs in s:
			if xs[0] == '<':
				for N in Choices:
					if N.id == xs[1:-1]:
						Sim_Rate = 0.0
						for v in N.values:
							if SequenceMatcher(None, p[i], v).ratio() > Sim_Rate:
								Sim_Rate = SequenceMatcher(None, p[i], v).ratio()
								interm = v
						x = gsr_ros.msg._Opcs.Opcs()
						x.id = str(N.id)
						x.values = [str(interm)]
						newPhrase = newPhrase.replace(N.id,interm)
						resp.append(x)
					
			i = i+1
		if Percentage == True:
			return SequenceMatcher(None, newPhrase, phrase).ratio(),resp
		else:
			return resp
		


	def Spec_calc(self,phrase,Spec):
		Sim_Rate = 0.0
		Near_phrase = ''
		plist = []
		for i in Spec:
			tempVal = SequenceMatcher(None, phrase, i).ratio()
			if tempVal > Sim_Rate:
				Sim_Rate = tempVal
				Near_phrase = i
				#print Sim_Rate
				#print Near_phrase
			#elif (tempVal - Sim_Rate)*-1 < 0.15 and tempVal > 0.60:
			#	print 'entered'
			#	plist.append(i)
		#if len(plist) > 0:
		#	return plist
		#else:
		return Near_phrase


	def API_Recognition(self,audio):
		try:
			if self.API == 'Google':
				return self.r.recognize_google(audio)
			if self.API == 'Sphinx':
				return self.r.recognize_sphinx(audio)
			if self.API == 'Wit':
				return self.r.recognize_wit(audio,self.Key1,self.Key2)['_text']
			if self.API == 'Houndify':
				return self.r.recognize_houndify(audio,self.Key1,self.Key2)
		
		except sr.UnknownValueError:
			return 'Error while processing the audio'

		except sr.RequestError as e:
			return str("API error; {0}".format(e))


if __name__ == "__main__":
	Recognition_server()