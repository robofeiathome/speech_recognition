#!/usr/bin/env python3

import rospy
from gsr_ros.msg import Opcs
from gsr_ros.srv import Start, StartResponse
import speech_recognition as sr
import jellyfish
from difflib import SequenceMatcher
import os
import time

class RecognitionServer:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('SpeechRecognition')
        
        # Retrieve parameters from the ROS server
        self.api = rospy.get_param('~API').lower()
        self.key1 = rospy.get_param('~KEY1')
        self.key2 = rospy.get_param('~KEY2')
        self.path = rospy.get_param('~PATH')
        
        # Initialize the speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Set up the recognition service
        self.service = rospy.Service('Recognition', Start, self.handle_recognition_request)
        
        # Log that the server is ready
        rospy.loginfo("Recognition server ready.")
        
        # Initialize an in-memory cache for storing recent recognition results
        self.cache = {}

    def handle_recognition_request(self, req):
        # Capture audio from the microphone
        with sr.Microphone(sample_rate=32000) as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            time.sleep(2)
            os.system(f'ogg123 {self.path}/beep.ogg >/dev/null 2>&1')  # Play a beep sound
            rospy.loginfo("Say something!")
            audio = self.recognizer.record(source, duration=7)

        # Save the captured audio as a WAV file
        with open(f"{self.path}/audio.wav", "wb") as f:
            f.write(audio.get_wav_data())

        # Recognize the captured audio
        recognized_text = self.recognize_audio(audio)

        # Check for specific commands or errors in the recognized text
        if recognized_text.startswith("how much is"):
            return StartResponse(spec=recognized_text, resp=[])

        if recognized_text.startswith("API error;") or "Error while processing the audio" in recognized_text:
            rospy.logwarn("API responded with an Error... Sorry")
            return StartResponse(spec='', resp=[])

        # Process the recognized text based on given specifications and choices
        if not req.spec or not req.choices:
            rospy.loginfo("No choices or specs provided. This is what was recognized:")
            return StartResponse(spec=recognized_text, resp=[])

        return self.process_recognized_text(recognized_text, req)

    def process_recognized_text(self, recognized_text, req):
        # Find specifications in the recognized text that are close to the provided specifications
        closest_specs = self.find_closest_specs(recognized_text, req.spec)
        
        # If only one specification matches closely, find the best choices for it
        if len(closest_specs) == 1:
            spec = closest_specs[0]
            resp = self.find_best_choices(spec, recognized_text, req.choices)
            return StartResponse(spec=spec, resp=resp)

        # If multiple specifications match, find the best match based on the provided choices
        best_match_spec = ""
        best_match_choices = []
        best_similarity = 0
        for spec in closest_specs:
            similarity, choices = self.find_best_choices(spec, recognized_text, req.choices, True)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match_spec = spec
                best_match_choices = choices

        return StartResponse(spec=best_match_spec, resp=best_match_choices)

    def find_best_choices(self, spec, recognized_text, choices, return_similarity=False):
        # Split the recognized text and specification into words
        spec_words = spec.split()
        recognized_words = recognized_text.split()
        selected_choices = []

        # Replace placeholders in the specification with the best matching choice
        new_phrase = spec
        for i, word in enumerate(spec_words):
            if word.startswith('<'):
                choice_id = word[1:-1]
                best_match = self.get_best_match_from_choices(choice_id, recognized_words, choices)
                choice = Opcs(id=str(choice_id), values=[str(best_match)])
                new_phrase = new_phrase.replace(choice_id, best_match)
                selected_choices.append(choice)

        # Return the choices with their similarity score if requested
        if return_similarity:
            similarity = SequenceMatcher(None, new_phrase, recognized_text).ratio()
            return similarity, selected_choices

        return selected_choices

    def get_best_match_from_choices(self, choice_id, recognized_words, choices):
        # Find the best matching word from the provided choices for a given placeholder
        best_match = ""
        best_similarity = 0
        for choice in choices:
            if choice.id == choice_id:
                for value in choice.values:
                    similarity = max([SequenceMatcher(None, word, value).ratio() for word in recognized_words])
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match = value

        return best_match

    def find_closest_specs(self, recognized_text, specs):
        # Find specifications that are close to the recognized text
        threshold_similarity = 0.6
        close_specs = []
        for spec in specs:
            similarity = jellyfish.jaro_winkler_similarity(recognized_text, spec)
            if similarity >= threshold_similarity:
                close_specs.append(spec)

        return close_specs

    def recognize_audio(self, audio):
        # Use caching to avoid processing the same audio multiple times
        audio_hash = hash(audio.get_wav_data())
        if audio_hash in self.cache:
            return self.cache[audio_hash]

        # Recognize the audio using the specified API
        try:
            if self.api == 'google':
                result = self.recognizer.recognize_google(audio)
            elif self.api == 'sphinx':
                result = self.recognizer.recognize_sphinx(audio)
            elif self.api == 'wit':
                result = self.recognizer.recognize_wit(audio, self.key1, self.key2)['_text']
            elif self.api == 'houndify':
                result = self.recognizer.recognize_houndify(audio, self.key1, self.key2)
            elif self.api == "deepspeech":
                result = os.popen(f"deepspeech --model {self.path}/models/output_graph.pbmm --trie {self.path}/models/trie --lm {self.path}/models/lm.binary --alphabet {self.path}/models/alphabet.txt --audio {self.path}/audio.wav").read().split('Running inference.')[1].strip()

            # Store the recognition result in the cache before returning
            self.cache[audio_hash] = result
            return result

        except sr.UnknownValueError:
            return 'Error while processing the audio'
        except sr.RequestError as e:
            return f"API error; {e}"

if __name__ == "__main__":
    RecognitionServer()
    rospy.spin()
