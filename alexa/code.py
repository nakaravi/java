# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_slot_value
from ask_sdk_model.ui import SimpleCard

from ask_sdk_model import Response
import boto3
import pandas as pd
from openpyxl import Workbook,load_workbook
from io import BytesIO
import json
import sys
import random
import requests
import util


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

question = 0
score = 0
data = []
dataAll = ""
questionsFltr = []
questions = []
certificate = ""
level = ""
questionsForAttempt = 3 #************init 3 questions
profileName = ""
lastIntent = ""
messages = {}
trend = ""              #***** current conversation
findLevel = ""          #***** find level from level var
findCerti = ""          #***** find certificate from certificate var

# class LaunchRequestHandler(AbstractRequestHandler):
#     """Handler for Skill Launch."""
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool

#         return ask_utils.is_request_type("LaunchRequest")(handler_input)

#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         speak_output = "Welcome, you can say Hello or Help. Which would you like to try?"

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)
    def get_user_info(access_token):
        amazonProfileURL = 'https://api.amazon.com/user/profile?access_token='
        r = requests.get(url=amazonProfileURL+access_token)
        if r.status_code == 200:
            return r.json()
        else:
            return False
    
            
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        level = ""
        certificate = ""
        lastIntent = "LaunchRequest"
        speak_output= ""
        profilename = util.get_profile_name(handler_input)
        dataAll = util.load_data()
        data = util.load_questions()
        messages = util.load_messages()
        if profilename == 'Dude':
            speak_output = random.sample(messages["profile"], 1)[0]
        else:
            speak_output = random.sample(messages["launch"], 1)[0].replace("<<profilename>>", profilename)
        attr = handler_input.attributes_manager.session_attributes
        attr["questionsForAttempt"] = messages["questionsForAttempt"]
        attr["question"]            = 0
        attr["score"]               = 0
        attr["lastspeech"]          = speak_output
        attr["lastintent"]          = "LaunchRequest"
        attr["messages"]            = messages
        attr["certificate"]         = ""
        attr["level"]               = ""
        attr["questions"]           = []
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Which certification and level would you like your questions from?")
                # .ask(speak_output)
                .response
        )
class ProfileIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("ProfileIntent")(handler_input)
            
    def handle(self, handler_input):
        profilename = get_slot_value(handler_input=handler_input, slot_name="name")
        perm = get_slot_value(handler_input=handler_input, slot_name="permissions")
        attr = handler_input.attributes_manager.session_attributes
        messages = attr["messages"]
        speak_output = ""
        if (profilename is not None):
            attr["profile_name"] = profilename
            speak_output = random.sample(messages["launch"], 1)[0].replace("<<profilename>>", profilename)
        if (perm is not None):
            speak_output = random.sample(messages["permissions"], 1)[0]
            if perm == 'done':
                profilename = util.get_profile_name(handler_input)
                speak_output = random.sample(messages["launch"], 1)[0].replace("<<profilename>>", profilename)
            elif perm == "nothing" or perm == "its ok" or perm == "do not share" or perm == "not now" or perm == "don't want":
                speak_output = random.sample(messages["permissions_denied"], 1)[0]
        attr["lastintent"] = "ProfileIntent"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Which certification and level would you like your questions from?")
                # .ask(speak_output)
                .response
        )

class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # accesstoken = str(handler_input.request_envelope.context.system.api_access_token)
        # endpoint = "https://api.eu.amazonalexa.com/v2/accounts/~current/settings/Profile.name"
        # api_access_token = "Bearer " + str(accesstoken)
        # headers = {"Authorization": api_access_token}
        # r = requests.get(endpoint, headers=headers)
        # email = r.json()
        
        profilename = util.get_profile_name(handler_input)
        messages = util.load_messages()
        
        attr = handler_input.attributes_manager.session_attributes
        attr["messages"]            = messages
        attr["questionsForAttempt"] = messages["questionsForAttempt"]
        attr["question"]            = 0
        attr["score"]               = 0
        attr["lastintent"]          = "HelloWorldIntent"
        attr["level"]               = ""
        speak_output                = ""
        
        certificate = get_slot_value(handler_input=handler_input, slot_name="certificate")
        if profilename == 'Dude':
            speak_output = random.sample(messages["profile"], 1)[0]
        else:
            if (certificate is not None):
                speak_output = 'Hello, ' + str(profilename) + '! Welcome to juniper network practice assessment on ' + certificate + '. I will also need your level of expertise. Would you like the questions from Associate or Specialist levels?'
            else:
                speak_output = random.sample(messages["launch"], 1)[0].replace("<<profilename>>", profilename)

        attr["certificate"] = certificate if (certificate is not None) else ""
        attr["lastspeech"] = speak_output
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(" Which level of questions would you like? Say Associate, Specialist, Professional and Expert level. ")
                .response
        )

class CertificateIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CertificateIntent")(handler_input)

    def handle(self, handler_input):
        
        attr                = handler_input.attributes_manager.session_attributes
        lastIntent          = attr["lastintent"]
        messages            = attr["messages"]
        questionsForAttempt = attr["questionsForAttempt"]
        speak_output        = ""
        certificate         = ""
        level               = attr["level"]
        question            = 0
        # check illegal entry for this intent ****************************************
        if (lastIntent == "AnswerIntent" or lastIntent=="StartQuizIntent") and questionsForAttempt > question:
            speak_output = random.sample(messages["answer_msg"], 1)[0]
        if lastIntent == "LevelNCertificate" and len(level)>0 and len(certificate)>0:
            speak_output = random.sample(messages["start"], 1)[0]
        else:
            certificate = get_slot_value(handler_input=handler_input, slot_name="certificate")
            if certificate is not None and util.find_level(certificate, handler_input):
                level = certificate
            if util.find_certificate(certificate, handler_input):
                if len(level) == 0:
                    speak_output = " Which level of questions would you like? Say Associate, Specialist, Professional and Expert level"
                else:
                    # """ *************** filter master data with cetificate and filter """
                    if len(level) > 0 and len(certificate)>0:
                        q = util.filter_certificate_n_level(certificate, level, handler_input)
                        attr = handler_input.attributes_manager.session_attributes
                        questions = attr["questions"]
                        messages = attr["messages"]
                        certificate = attr["certificate"]
                        level = attr["level"]
                        questionsForAttempt = messages["questionsForAttempt"]
                        speak_output = "Great! The Practice Assessment consists of " + str(questionsForAttempt) + " multiple Choice questions. I will read each question along with its four suitable answers. Select the most appropriate answer to the question. Say start when you are ready."
                        if len(q)>0:
                            speak_output = random.sample(messages["level"],1)[0].replace("<<questioncount>>", str(questionsForAttempt)).replace("<<certificate>>", str(certificate)).replace("<<level>>", str(level))
                        else:
                            speak_output = random.sample(messages["not_enough_questions"],1)[0].replace("<<certificate>>", str(certificate)).replace("<<level>>", str(level))
                    else:
                        speak_output =" Which certification and level would you like your questions from?"
            else:
                speak_output = random.sample(messages["wrong_level_certificate"], 1)[0]
        attr["certificate"] = certificate
        attr["lastintent"] = "CertificateIntent"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class LevelIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("LevelIntent")(handler_input)

    def handle(self, handler_input):
        
        level = ""
        attr = handler_input.attributes_manager.session_attributes
        questions = []
        lastIntent = attr["lastintent"] if "lastintent" in attr else ""
        messages = attr["messages"] if "messages" in attr else util.load_messages()
        questionsForAttempt = attr["questionsForAttempt"] if "questionsForAttempt" in attr else 3
        certificate = attr["certificate"] if "certificate" in attr else ""
        question = attr["question"] if "question" in attr else 0
        
        # check illegal entry for this intent ****************************************

        if (lastIntent == "AnswerIntent" or lastIntent=="StartQuizIntent") and int(questionsForAttempt) > int(question):
            speak_output = random.sample(messages["answer_msg"], 1)[0]
        if (lastIntent == "LevelNCertificate" or lastIntent == "CertificateIntent") and len(level)>0 and len(certificate)>0:
            speak_output = random.sample(messages["start"], 1)[0]
        else:
            level = get_slot_value(handler_input=handler_input, slot_name="level")
            
            
            
            
            # """ *************** filter master data with cetificate and filter """
            if util.find_level(level, handler_input):
                #******************* check single entry to both level and certificate 
                if len(certificate)==0 and util.find_certificate(level, handler_input):
                    certificate = level
                if len(level) > 0 and len(certificate)>0:
                    q = util.filter_certificate_n_level(certificate, level, handler_input)
                    attr = handler_input.attributes_manager.session_attributes
                    certificate = attr["certificate"]
                    questionsForAttempt = attr["questionsForAttempt"]
                    level = attr["level"]
                    questions = attr["questions"]
                    if len(q)>0:
                        speak_output = random.sample(messages["level"],1)[0].replace("<<questioncount>>", str(questionsForAttempt)).replace("<<certificate>>", str(certificate)).replace("<<level>>", str(level))
                    else:
                        speak_output = random.sample(messages["not_enough_questions"],1)[0].replace("<<certificate>>", str(certificate)).replace("<<level>>", str(level))
                else:
                    if len(certificate) == 0:
                        speak_output =" Which certification track would you like your questions from?"
                    else:
                        speak_output =" Which level would you like your questions from?"
            else:
                speak_output = random.sample(messages["wrong_level_certificate"], 1)[0]
                
        attr["level"] = level
        attr["lastintent"] = "LevelIntent"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(" Say start when you are ready.")
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )



class LevelNCertificateHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("LevelNCertificate")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        certificate = ""
        level = ""
        attr = handler_input.attributes_manager.session_attributes
        messages = attr["messages"] if attr["messages"] else util.load_messages()
        lastIntent = attr["lastintent"] if (attr and attr["lastintent"]) else ""
        questionsForAttempt = messages["questionsForAttempt"] #attr["questionsForAttempt"] if attr["questionsForAttempt"] else 3
        question = attr["question"] if attr["question"] else 0
        
        #***************** check illegal entry
        if ((lastIntent == "AnswerIntent" or lastIntent=="StartQuizIntent") and questionsForAttempt > (question+1)):
            speak_output = random.sample(messages["answer_msg"], 1)[0]
        else:
            # """ **********************get slots of certificate and level ********************* """
            certificate = get_slot_value(handler_input=handler_input, slot_name="certificate")
            level       = get_slot_value(handler_input=handler_input, slot_name="level")
            speak_output = ""
            if len(certificate)>0 and len(level)>0:
                attr = handler_input.attributes_manager.session_attributes
                attr["questionsForAttempt"] = messages["questionsForAttempt"]
                q = util.filter_certificate_n_level(certificate, level, handler_input)
                attr = handler_input.attributes_manager.session_attributes
                questionsForAttempt = attr["questionsForAttempt"] if attr["questionsForAttempt"] else 3
                question = attr["question"] if attr["question"] else 0
                if len(q)>0:
                    speak_output = random.sample(messages["level"],1)[0].replace("<<questioncount>>", str(questionsForAttempt)).replace("<<certificate>>", str(certificate)).replace("<<level>>", str(level))
                else:
                    speak_output = random.sample(messages["not_enough_questions"],1)[0].replace("<<certificate>>", str(certificate)).replace("<<level>>", str(level))
            else:
                speak_output = "Which certification and level would you like your questions from?" 
            
        
        attr = handler_input.attributes_manager.session_attributes
        attr["lastspeech"]  = speak_output
        attr["lastintent"]  = "LevelNCertificate"
        attr["certificate"] = certificate
        attr["level"]       = level
        attr["question"]    = 0 
        attr["score"]       = 0
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(random.sample(messages["answer_msg"], 1)[0])
                .response
        )

class StartQuizIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StartQuizIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        score = 0 
        question = 0
        
        # ******************random questions *****************
        attr = handler_input.attributes_manager.session_attributes
        questions   = attr["questions"]
        messages    = attr["messages"]
        question    = 0
        certificate = attr["certificate"]
        level       = attr["level"]
        lastintent  = attr["lastintent"]
        
        attr["questions"] = questions
        if(questions is not None and len(questions) > 0):
            so = random.sample(messages["questioncounter"], 1)[0].replace("<<questioncounter>>", str(question + 1))
            speak_output = "<speak><p>" + so + "  <break time='1s'/></p><p>" 
            speak_output += questions[question]['QUESTIONS'] + " <break time='1s'/></p><p>"
            speak_output += "Option A: " + questions[question]['OPTION 1'] + " Option B: "  + questions[question]['OPTION 2']+ "  Option C: "  + questions[question]['OPTION 3'] + "  Option D: " + questions[question]['OPTION 4']
            speak_output += "</p>"
            speak_output += random.sample(messages["answer_msg"], 1)[0] + " </speak>"
        else:
            if lastintent == "SpecificQuesionsIntent" or lastintent=="LaunchRequest" or lastintent=="ProfileIntent":
                speak_output = "Which certification track and level do you prefer to start with?"
            else:
                speak_output = "Ahh ! We dont have enough questions at this moment from " + certificate + "  " + level + "  Would you like to select another certification track and level.  "
        
        attr                = handler_input.attributes_manager.session_attributes
        attr["lastspeech"]  = speak_output
        attr["lastintent"]  = "StartQuizIntent"
        attr["question"]    = 0
        attr["score"]       = score
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(random.sample(messages["answer_msg"], 1)[0])
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class AnswerIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("AnswerIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = ""
        ans = []    # user answer
        attr = handler_input.attributes_manager.session_attributes
        questions = attr["questions"]
        messages = attr["messages"]
        certificate = attr["certificate"]
        level = attr["level"]
        question = attr["question"]
        score = attr["score"]
        lastintent = attr["lastintent"]
        speak_output = str(len(questions))
        slot = get_slot_value(handler_input=handler_input, slot_name="answer")
        
        if lastintent=="AnswerIntent" and len(questions) ==0:
            speak_output =  random.sample(messages["levelNcertificate"], 1)[0]
            return ( 
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )
        if (slot is None):
            speak_output = random.sample(messages["answer_msg"], 1)[0]
        else:
            slot = slot.replace(" ","").replace(".", "").replace("a","1").replace("b","2").replace("c","3").replace("d","4").replace("A","1").replace("B","2").replace("C","3").replace("D","4")
            
            if len(slot)>1:
                ans = [slot[i:i+1] for i in range(0, len(str(slot)))]
            else:
                ans.append(slot)
            
            crctAns = str(questions[question]["Correct Answer"]).split(",")
            ansCount = 0
            # speak_output = str(slot) + ',' + str(len(ans)) + ',' + str(len(crctAns)
            for i in crctAns:
                for j in ans:
                    if int(i) == int(j):
                        ansCount += 1
            speak_output = ""
            # speak_output = str(question) + str(len(crctAns)) + str(len(ans)) + "---"+ str(ansCount)+"::"
            if int(question) == (len(questions)-1): #******* attended all the questions 
                
                if(len(crctAns) == len(ans)):
                    if ansCount == len(crctAns):
                        score = score + 1
                        speak_output += random.sample(messages["correctans"], 1)[0] + " "
                    else:
                        speak_output += random.sample(messages["wrongans"], 1)[0] + " "
                        speak_output += " " + questions[question]['Answer Explanation'] + " <break time=\"1s\"/>"
                else:
                    speak_output += random.sample(messages["wrongans"], 1)[0] + " "
                    speak_output += " " + questions[question]['Answer Explanation'] + " <break time=\"1s\"/>"
                
                # # Check all questions are Correct or not **********************************
                if int(score) == len(questions):
                    speak_output +=  random.sample(messages["completed"],1)[0].replace("<<certificate>>", str(certificate)).replace("<<level>>", str(level))
                    # .replace("<<score>>", str(score)).replace("<<questions>>", str(len(questions)))
                else:
                    speak_output += random.sample(messages["wronglycompleted"],1)[0].replace("<<certificate>>", str(certificate)).replace("<<level>>", str(level))
                attr["questions"] = []
                # attr["question"] = 0
                # speak_output = random.sample(messages["correctans"], 1)[0] + str(len(crctAns)) +" == " + str(len(ans)) + "," + str(question) + "," + str(len(questions))
                return ( 
                    handler_input.response_builder
                        .speak(speak_output)
                        .ask(speak_output)
                        .response
                )
            else:
                if(len(crctAns) == len(ans)):
                    if ansCount == len(crctAns):
                        score = score + 1
                        speak_output = str(random.sample(messages["correctans"], 1)[0])
                    else:
                        speak_output = str(random.sample(messages["wrongans"], 1)[0])
                        speak_output += " " + questions[question]['Answer Explanation'] + " <break time=\"1s\"/>"
                else:
                    speak_output += str(random.sample(messages["wrongans"], 1)[0])
                    speak_output += " " + questions[question]['Answer Explanation'] + " <break time=\"1s\"/>"
                question = question + 1
                
                speak_output += random.sample(messages["questioncounter"], 1)[0].replace("<<questioncounter>>", str(question + 1)) 
                speak_output += questions[question]['QUESTIONS']  + " Option A: " + questions[question]['OPTION 1'] + " Option B: "  + questions[question]['OPTION 2']+ " Option C: "  + questions[question]['OPTION 3'] + " Option D: " + questions[question]['OPTION 4']
        
        attr["lastspeech"]  = speak_output
        attr["lastintent"]  = "AnswerIntent"
        attr["score"]       = score
        attr["question"]    = question
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        speak_output = attr["lastspeech"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ReciteIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ReciteIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = ""
        recite = get_slot_value(handler_input=handler_input, slot_name="recite")
        option = get_slot_value(handler_input=handler_input, slot_name="answer")
        
        attr = handler_input.attributes_manager.session_attributes
        questions = attr["questions"]
        messages = attr["messages"]
        question = attr["question"]
        lastIntent = attr["lastintent"]
        if (option is not None):
            option = option.replace(" ","").replace(".", "").replace("1","a").replace("2","b").replace("3","c").replace("4","d").replace("A","a").replace("B","b").replace("C","c").replace("D","d")
        else:
            option = "z"
        if recite == "question":
            speak_output = questions[question]['QUESTIONS']
            speak_output += random.sample(messages["answer_msg"], 1)[0]
        elif recite == "option":
            
            if option.lower() == 'a' or option == '1' or option == 'first':
                speak_output = " Option A: " + questions[question]['OPTION 1']
            elif option.lower() == 'b' or option == '2' or option == 'second':
                speak_output = " Option B: " + questions[question]['OPTION 2']
            elif option.lower() == 'c' or option == '3' or option == 'third':
                speak_output = " Option C: " + questions[question]['OPTION 3']
            elif option.lower() == 'd' or option == '4' or option == 'fourth':
                speak_output = " Option D: " + questions[question]['OPTION 4']
            else:
                speak_output =  " Option A: " + questions[question]['OPTION 1'] + "  Option B: "  + questions[question]['OPTION 2']+ "  Option C: "  + questions[question]['OPTION 3'] + "  Option D: " + questions[question]['OPTION 4']
            speak_output += random.sample(messages["answer_msg"], 1)[0]
        elif recite == 'explanation':
            speak_output = questions[question]['Answer Explanation'] 
        elif recite == 'again':
            if lastIntent == "LaunchRequest":
                speak_output = random.sample(messages["levelNcertificate"], 1)[0]
        else:
            speak_output = random.sample(messages["answer_msg"], 1)[0]
        # speak_output += str(question)
        attr["lastintent"] = "ReciteIntent"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ReAttemptIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ReAttemptIntent")(handler_input) or ask_utils.is_intent_name("ResumeIntent")(handler_input)

    def handle(self, handler_input):
        attr                = handler_input.attributes_manager.session_attributes
        questions           = attr["questions"] if "questions" in attr else []
        messages            = attr["messages"] if "messages" in attr else util.load_messages()
        score               = attr["score"] if "score" in attr else 0
        question            = attr["question"] if "question" in attr else 0
        questionsForAttempt = attr["questionsForAttempt"] if "questionsForAttempt" in attr else 3
        certificate         = attr["certificate"] if "certificate" in attr else ""
        level               = attr["level"] if "level" in attr else ""
        lastIntent          = attr["lastintent"] if "lastintent" in attr else ""
        profile_name        = attr["profile_name"] if "profile_name" in attr else "User"
        
        attempt = get_slot_value(handler_input=handler_input, slot_name="attempt")
        speak_output = ""
        reprompt = ""
        #************************continue the same certificate and level with random questions 
        if attempt == 'continue':
            speak_output = random.sample(messages["reattempt"], 1)[0]
            reprompt = speak_output
        elif attempt == 'practice later' or attempt == 'later':
            speak_output = random.sample(messages["thanks"], 1)[0]
            reprompt = speak_output
            handler_input.attributes_manager.session_attributes = {}
        elif attempt == 'retry' or attempt == "same" or attempt == "something" or attempt == "different":     
            # speak_output = str(question) + "," + str(questionsForAttempt) + "," + str(int(question) >= (int(questionsForAttempt)-1))
            if int(question) >= (int(questionsForAttempt)-1):
                q = util.filter_certificate_n_level(certificate, level, handler_input)
                questions = q 
                question = 0 
                score = 0 
                speak_output = random.sample(messages["questioncounter"], 1)[0].replace("<<questioncounter>>", str(question + 1))
                speak_output += " <break time='1s'/>" 
                speak_output += questions[question]['QUESTIONS'] + " <break time='1s'/>"
                speak_output += " Option A: " + questions[question]['OPTION 1'] + "  Option B: "  + questions[question]['OPTION 2']+ "  Option C: "  + questions[question]['OPTION 3'] + "  Option D: " + questions[question]['OPTION 4']
                reprompt    = speak_output    
                attr        = handler_input.attributes_manager.session_attributes
                attr["questions"] = questions
                attr["question"] = 0
            else:
                attr["questions"] = questions
                attr["score"] = score
                attr["question"] = question
                speak_output = random.sample(messages["answer_msg"], 1)[0]
        elif attempt == 'yes' or attempt == 'ok':
            if lastIntent == "ReattemptIntent":
                profile_name = handler_input.attributes_manager.session_attributes["profile_name"]
                speak_output = "Thank you " + str(profile_name)+ ", " + str(random.sample(messages["thanks"], 1)[0])
                reprompt = speak_output
                handler_input.attributes_manager.session_attributes = {}
            elif int(question) > 0 and (int(questionsForAttempt)-1) > int(question) and (len(questions)>0):
                speak_output = random.sample(messages["questioncounter"], 1)[0].replace("<<questioncounter>>", str(question + 1))
                speak_output += " <break time='1s'/>" 
                speak_output += questions[question]['QUESTIONS'] + " <break time='1s'/>"
                speak_output += " Option A: " + questions[question]['OPTION 1'] + "  Option B: "  + questions[question]['OPTION 2']+ "  Option C: "  + questions[question]['OPTION 3'] + "  Option D: " + questions[question]['OPTION 4']
                reprompt = speak_output
            else:
                if len(level) == 0 and len(certificate) == 0:
                    speak_output = "Which certification and level would you like your question from?"
                    reprompt = speak_output
                elif len(level) == 0:
                    speak_output = "Which level would you like your question from?"
                    attr["certificate"] = ""
                    reprompt = speak_output
                else:
                    speak_output = "Which certification would you like your question from?"
                    reprompt = speak_output
                    attr["level"] = ""
                    attr["certificate"] = ""
        else:
            if lastIntent == "ReattemptIntent":
                profile_name = handler_input.attributes_manager.session_attributes["profile_name"]
                speak_output = "Thank you " + str(profile_name)+ ", " + str(random.sample(messages["thanks"], 1)[0])
                speak_output = random.sample(messages["stop"], 1)[0]
                reprompt = speak_output
                handler_input.attributes_manager.session_attributes = {}
            else:
                speak_output = random.sample(messages["no"], 1)[0]
                reprompt = speak_output #"Which certification track and level do you prefer?"
                questions = []
                handler_input.attributes_manager.session_attributes = {}
                # attr                        = handler_input.attributes_manager.session_attributes
                
        attr                        = handler_input.attributes_manager.session_attributes
        attr["lastintent"]          = "ReattemptIntent"
        attr["profile_name"]        = profile_name
        attr["messages"]            = messages
        attr["question"]            = 0 
        attr["questions"]           = questions
        attr["questionsForAttempt"] = messages["questionsForAttempt"] 
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )


class SpecificQuesionsIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SpecificQuesionsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        score = 0 
        question = 0
        questions = []
        questionsForAttempt = get_slot_value(handler_input=handler_input, slot_name="noOfQuestions")
        level = get_slot_value(handler_input=handler_input, slot_name="level")
        certificate = get_slot_value(handler_input=handler_input, slot_name="certificate")
        speak_output = "" # str(certificate) + " " + str(level)  +" "+str(questionsForAttempt) 
        attr        = handler_input.attributes_manager.session_attributes
        messages    = attr["messages"]
        if ((level is None) and (certificate is None)):
            speak_output = random.sample(messages["levelNcertificate"], 1)[0]
        elif (level is None) and (certificate is not None):
            if util.find_certificate(certificate, handler_input):
                if level is None and util.find_level(certificate, handler_input):
                    level = certificate
            else:
                speak_output = random.sample(messages["wrong_level_certificate"], 1)[0]
        elif ((level is not None) and (certificate is None) and (questionsForAttempt is not None)):
            if util.find_level(level, handler_input):
                #******************* check single entry to both level and certificate 
                if certificate is None and util.find_certificate(level, handler_input):
                    certificate = level

                # if len(level) > 0 and len(certificate)>0:
                #     q = util.filter_certificate_n_level(certificate, level, handler_input)
                #     attr = handler_input.attributes_manager.session_attributes
                #     certificate = attr["certificate"]
                #     questionsForAttempt = attr["questionsForAttempt"]
                #     level = attr["level"]
                #     questions = attr["questions"]
                #     if len(q)>0:
                #         speak_output = random.sample(messages["level"],1)[0].replace("<<questioncount>>", str(questionsForAttempt)).replace("<<certificate>>", str(certificate)).replace("<<level>>", str(level))
                #     else:
                #         speak_output = random.sample(messages["not_enough_questions"],1)[0].replace("<<certificate>>", str(certificate)).replace("<<level>>", str(level))
            else:
                speak_output = random.sample(messages["wrong_level_certificate"], 1)[0]
        
        if len(level)>0 and len(certificate) > 0 and questionsForAttempt is not None:# and int(questionsForAttempt) > 0:
            attr = handler_input.attributes_manager.session_attributes
            questionsForAttempt = int(questionsForAttempt)
            attr["questionsForAttempt"] = questionsForAttempt
            attr["level"] = level
            attr["certificate"] = certificate
            attr["question"] = question
            q = util.filter_certificate_n_level(certificate, level, handler_input)
            
            attr1 = handler_input.attributes_manager.session_attributes
            questions = attr1["questions"]
            messages = attr1["messages"]
            
            speak_output = str(len(questions))
            speak_output = "Great ! Getting question for you. <break time='1s'/>Here is your Question…<break time='1s'/>"
            speak_output += questions[question]['QUESTIONS'] + " <break time='1s'/>"
            speak_output += " Option A: " + questions[question]['OPTION 1'] + " Option B: "  + questions[question]['OPTION 2']+ "  Option C: "  + questions[question]['OPTION 3'] + "  Option D: " + questions[question]['OPTION 4']
            speak_output += random.sample(messages["answer_msg"], 1)[0]
            
        elif len(level) > 0 and len(certificate) > 0:
            q                   = util.filter_certificate_n_level(certificate, level, handler_input)
            attr                = handler_input.attributes_manager.session_attributes
            questions           = attr["questions"]
            messages            = attr["messages"]
            attr["level"]       = level
            attr["certificate"] = certificate
            questionsForAttempt = int(attr["questionsForAttempt"])
            if len(q)>0:
                speak_output = random.sample(messages["level"],1)[0].replace("<<questioncount>>", str(questionsForAttempt)).replace("<<certificate>>", str(certificate)).replace("<<level>>", str(level))
            else:
                speak_output = "Ahh ! We dont have enough questions at this moment from " + certificate + "  " + level + "  Would you like to select another certification track and level. "
        else:
            speak_output = "Select another certification track and level."
        attr1 = handler_input.attributes_manager.session_attributes
        attr1["lastspeech"] = speak_output
        attr1["lastintent"] = "SpecificQuesionsIntent"
        attr1["question"]   = question
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(random.sample(messages["answer_msg"], 1)[0])
                .response
        )

class CommonIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("CommonIntent")(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        slot = get_slot_value(handler_input=handler_input, slot_name="common")
        if slot == 'practice':
            speak_output = "I am sorry I can’t help you. We can try again later."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "In this skill we can help you in Practice Juniper certification questions. To hear available Certificate track or level of experties. Say Certificate tracks or Levels. "

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        
        attr = handler_input.attributes_manager.session_attributes
        lastIntent = attr["lastintent"] if "lastintent" in attr else ""
        messages = attr["messages"] if "messages" in attr else ""
        
        if lastIntent == "StartQuizIntent" or lastIntent == "SpecificQuesionsIntent":
            speech = random.sample(messages["answer_msg_sorry"], 1)[0]
            reprompt = random.sample(messages["answer_msg_sorry"], 1)[0]
        elif lastIntent == "LevelNCertificate":
            speech = random.sample(messages["start"], 1)[0]
            reprompt = random.sample(messages["start"], 1)[0]
        elif lastIntent == "LaunchRequest":
            speech = random.sample(messages["unwanted_input"], 1)[0]
            #"Sorry, I don’t understand this. Say Automation and DevOps; Cloud, Data Center; Design; Enterprise Routing and Switching; Mist AI; Security; and Service Provider Routing and Switching. Which certification and level would you like your questions from?"
            reprompt = "Which level and Certificate do you prefer?"
        elif(lastIntent == 'AnswerIntent'):
            if attr["question"] == 0:
                speech = random.sample(messages["noinput"], 1)[0]
                reprompt = speech 
            else:
                speech = random.sample(messages["answer_msg"], 1)[0]
                reprompt = " What would you like to do? Say yes or no."
        else:
            speech = "Sorry, in this skill I can help you in practice assessment questions. Do you want to continue? say continue or practice later."
            reprompt = " What would you like to do? Say yes or no."
        lastIntent = ""
        attr["lastintent"] = "FallbackIntent"
        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ProfileIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())

sb.add_request_handler(CertificateIntentHandler())
sb.add_request_handler(LevelIntentHandler())
sb.add_request_handler(LevelNCertificateHandler())
sb.add_request_handler(StartQuizIntentHandler())
sb.add_request_handler(AnswerIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(ReciteIntentHandler())
sb.add_request_handler(ReAttemptIntentHandler())
sb.add_request_handler(SpecificQuesionsIntentHandler())
sb.add_request_handler(CommonIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())


lambda_handler = sb.lambda_handler()
