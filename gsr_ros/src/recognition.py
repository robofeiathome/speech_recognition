#!/usr/bin/env python3

from gsr_ros.msg import *
from gsr_ros.srv import *
import rospy
import numpy
import speech_recognition as sr
import jellyfish as jf
from difflib import SequenceMatcher
import datetime
import sys
import os
import time

class Recognition_server():

	def __init__(self):
		rospy.init_node('SpeechRecognition')
		self.API = rospy.get_param('~API')
		self.API = self.API.lower()
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
		resp = []
		choice = []

		with sr.Microphone(sample_rate=16000) as source:
			self.r.adjust_for_ambient_noise(source, duration=2)
			time.sleep(2)
			os.system('ogg123 '+self.PATH+'/beep.ogg >/dev/null 2>&1')
			#time.sleep(1)
			print("Say something!")
			#audio = r.listen(source) Listen is a method where the computer will stop listening when there is silence
			#audio = r.record(source,duration=7) Record is a method where the duration is how many seconds must the computer record the voice
			audio = self.r.record(source,duration=7)

		with open(self.PATH+"/audio.wav", "wb") as f:
			f.write(audio.get_wav_data())


		recog = self.API_Recognition(audio)

		#print 'len do choices '+str(req.choices)
		#print 'len do spec '+str(req.spec)
		print ('I heard: %s'%recog)

		z = recog.split()
		if z[:3] == ['how', 'much', 'is']:
			spec = recog
			resp = []
			return StartResponse(spec,resp)			

		if recog == 'Error while processing the audio' or SequenceMatcher(None, recog, "API error; x").ratio() >= 0.75:
			rospy.loginfo("API responded with and Error... Sorry")
			spec = ''
			resp = []
			# x = gsr_ros.msg._Opcs.Opcs()
			# resp.append(x)
			# return None

		elif req.spec == [''] or req.choices == '':
			rospy.loginfo("You gave me no choices nor specs, This is what I heard")
			spec = recog
			resp = []
			# x = gsr_ros.msg._Opcs.Opcs()
			# resp.append(x)

		elif req.choices == '':
			spec = ''
			closer = 0.0
			p = self.Spec_calc(recog,req.spec)
			if len(p) == 1:
				spec = p[0]
				resp = []
			else:
				for phrase in p:
					x = jf.jaro_winkler(unicode(recog),unicode(phrase))
					if x > closer:
						closer = x
						spec = phrase

				resp = []

		else:
			percao = 0.0
			chosen = ''
			p = self.Spec_calc(recog,req.spec)

			if len(p) == 1:
				rospy.loginfo("Entered with only one phrase")
				resp = self.Choices_Calc(p[0],recog,req.choices)
				spec = p[0]

			else:

				for ph in p:
					rospy.loginfo("Multiple phrase detected")
					Perc, Ch = self.Choices_Calc(ph,recog,req.choices,True)

					if Perc > percao:
						percao = Perc
						resp = Ch
						spec = ph


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
							if i < len(p):
								if SequenceMatcher(None, p[i], v).ratio() > Sim_Rate:
									Sim_Rate = SequenceMatcher(None, p[i], v).ratio()
									interm = v
							else :
								if SequenceMatcher(None, p[len(p)-1], v).ratio() > Sim_Rate:
									Sim_Rate = SequenceMatcher(None, p[len(p)-1], v).ratio()
									interm = v
						x = gsr_ros.msg._Opcs.Opcs()
						x.id = str(N.id)
						x.values = [str(interm)]
						newPhrase = newPhrase.replace(N.id,interm)
						resp.append(x)

			i = i+1
		if Percentage == True:
			return SequenceMatcher(None, newPhrase, phrase).ratio(), resp
		else:
			return resp



	def Spec_calc(self,phrase,Spec):

		Sim_Rate = 0.0
		Near_phrase = ''
		plist = []
		for i in Spec:
			#tempVal = SequenceMatcher(None, phrase, i).ratio()
			# tempVal = jf.jaro_winkler(unicode(phrase),unicode(i))
			tempVal = jf.jaro_winkler(phrase,i)
			if tempVal >= 0.6:
				plist.append(i)
		return  plist


	def API_Recognition(self,audio):

		try:
			if self.API == 'google':
				return self.r.recognize_google(audio)

			if self.API == 'sphinx':
				return self.r.recognize_sphinx(audio)

			if self.API == 'wit':
				return self.r.recognize_wit(audio,self.Key1,self.Key2)['_text']

			if self.API == 'houndify':
				return self.r.recognize_houndify(audio,self.Key1,self.Key2)

			if self.API == "deepspeech":
				x = os.popen("deepspeech --model "+self.PATH+"/models/output_graph.pbmm --trie "+self.PATH+"/models/trie --lm "+self.PATH+"/models/lm.binary --alphabet "+self.PATH+"/models/alphabet.txt --audio "+self.PATH+"/audio.wav").read()
 
				x = str(x.split('Running inference.'))
				print ("I understood: "+str(x))
				x = x[2:-4]
				return x

		except sr.UnknownValueError:
			return 'Error while processing the audio'

		except sr.RequestError as e:
			return str("API error; {0}".format(e))


if __name__ == "__main__":

	Recognition_server()
