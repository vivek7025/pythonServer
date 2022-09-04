#imports for firebase
import time
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db
import re
from nerModel import getMessageToPersonName, getNameAndContent, getReadRecenetPersonName


import intent_check


pattern_time_remm = r"\bat"
pattern_content_remm = r"\bto"
pattern_tag_bk = r"\bas"
pattern_call = r"\bcall"
pattern_message1 = r"\bto"
pattern_message2 = r"\bmessage"
pattern_message3 = r"\btext"


class outputObject:
    action = ""
    callName = ""


class convoSessionSpecific:
    def __init__(self, s_type = "",s_content = "",s_intent = "",s_slotNumber = "", s_slot1 = "",s_slot2 = "",s_slot3 = ""
                 ,s_slot4 = "",s_ask = "", s_askForSlot = "",s_content2 = "",s_content3 = "", s_action = "",s_output = "",s_status = ""):
        self.s_type = s_type
        self.s_content = s_content
        self.s_intent = s_intent
        self.s_slotNumber = s_slotNumber
        self.s_slot1 = s_slot1
        self.s_slot2 = s_slot2
        self.s_slot3 = s_slot3
        self.s_slot4 = s_slot4
        self.s_ask = s_ask
        self.s_askForSlot = s_askForSlot
        self.s_content2 = s_content2;
        self.s_content3 = s_content3;
        self.s_action = s_action
        self.s_output = s_output
        self.s_status = s_status


def getTagNameBook(sentence):
    list = re.split(pattern_tag_bk, sentence)
    if (isinstance(list, type(None))):
        return sentence
    else:
        list_vl = list[1]
    return list_vl


def getCallName(sentence):
    toPerson = getMessageToPersonName(sentence)
    print("person name" +toPerson)

    # list = re.split(pattern_call,sentence)
    # if (isinstance(list, type(None))):
    #     return sentence
    # else:
    #     list_vl = list[1]
    return toPerson


def contentFind(sentence):
    list = re.split(pattern_content_remm, sentence)
    try:
        list_vl = list[1]
        list2 = re.split(pattern_time_remm, list_vl)
        list2_vl = list2[0]
        return list2_vl
    except IndexError:
        list = "ask"
        return list


def timeFind(sentence):
    # if(sentence == "no"):
    #     return sentence
    # else:
    #     list_vl = "ask"
    #     return list_vl
    y = re.search(pattern_time_remm, sentence)
    if (isinstance(y, type(None))):
        list_vl = "ask"
    else:
        content_end = y.start()
        time_start_pos = y.end()
        time_end_pos = len(sentence)
        list = re.split(pattern_time_remm, sentence)
        list_vl = list[1]
        # list2 = re.split(pattern_time_remm, list_vl)
        # list2_vl = list2[0]
    return list_vl


def getMessageToPerson(invoke_info):
    toPerson = getNameAndContent(invoke_info)
    return toPerson


def getMessageContent(messageToPerson,sentence):
    list = re.split(messageToPerson,sentence)
    try:
        list_vl = list[2]
    except IndexError:
        cnt = re.split(r"\bthat",sentence)
        try:
            cntvl = cnt[1]
            list_vl = cntvl
        except:
            list_vl = "ask"
    return list_vl


def getPlaceofWeather(invoke_info):
    pass


def getWeatherReport(placeofWeather):
    pass


class BotAction:
    def __init__(self):
        self.val = "nul"

    def run_bot(self, sessionInfo):
        x = intent_check.checkIntent()
        rt_value = x.checkIntent(sessionInfo.s_content)
        ob = outputObject()
        print(rt_value)
        if (rt_value == "call"):
            sessionInfo.s_slotNumber = 1
            specificConvo = self.actRquest(sessionInfo)
            return specificConvo
        elif (rt_value == "callrecent"):
            self.actRquest(sessionInfo)
        elif (rt_value == "callmissed"):
            ob = self.actRquest(sessionInfo)
            return ob
        elif (rt_value == "message"):
            ob = self.actRquest(sessionInfo)
            return ob
        elif (rt_value == "askmessagerecent"):
            ob = self.actRquest(sessionInfo)
            return ob
        elif (rt_value == "askmessageunread"):
            ob = self.actRquest(sessionInfo)
            return ob
        elif (rt_value == "reminder"):
            ob = self.actRquest(sessionInfo)
            return ob
        elif (rt_value == "alarm"):
            ob = self.actRquest(sessionInfo)
            return ob
        elif (rt_value == "time"):
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            print("Current Time =", current_time)
            convObjct = convoSessionSpecific(s_output=current_time)
            return convObjct
        elif (rt_value != "n"):
            return rt_value

    def ask(self,toAsk):
        print(toAsk)
        vl = "at 6"
        inserter2 = db.reference('Tag4_sysinpt')
        inserter2.set(toAsk)

        inserter1 = db.reference('Tag2_trig')
        inserter1.set("recv")

        while True:
            flag1 = db.reference('Tag2_trig')
            print(flag1.get())
            print("inside ask")
            checker1 = flag1.get()

            if (checker1 == "snd"):
                receiver1 = db.reference('Tag3_usinpt')
                print(receiver1.get())
                sentence = receiver1.get()
                flag1.set("nul")
                if sentence == "quit":
                    break

                return sentence
        return vl

    def actRquest(self,sessionInfo):
        buff = "nul";
        ob = outputObject()
        if (sessionInfo.s_content == "open"):
            userId = db.reference('currentUsId')
            print(userId.get())
            usId = userId.get()
            # userName = doc_ob.name
            vl = "HEY "
            invokeActInsert = db.reference('Tag4_sysinpt')
            invokeActInsert.set(vl)

            invoketrig = db.reference('Tag2_trig')
            invoketrig.set("recv")
        else:
            rt_value = sessionInfo.s_intent
            if (rt_value == "call"):
                callName = getCallName(sessionInfo.s_content)
                if callName == "ask":
                    content2 = sessionInfo.s_content2
                    if(content2 == ""):
                        session_return = convoSessionSpecific(s_type="specificConvo",s_content=sessionInfo.s_content,s_intent=sessionInfo.s_intent,s_ask = "who would you like to call?"
                                                              ,s_askForSlot = "s_content2"
                                                              ,s_status="running")
                        return session_return
                    else:
                        callName = getCallName(content2)
                        session_return = convoSessionSpecific(s_type="specificConvo",s_content=sessionInfo.s_content,s_intent=sessionInfo.s_intent, s_action="call", s_slot1=callName,
                                                              s_ask="no", s_status="done")
                        return session_return
                else:
                    session_return = convoSessionSpecific(s_type="specificConvo",s_content=sessionInfo.s_content,s_action = "call", s_slot1 = callName,s_intent=sessionInfo.s_intent,
                                                          s_ask = "no",s_status="done")
                    return session_return
            elif (rt_value == "callrecent"):
                session_return = convoSessionSpecific(s_type="specificConvo", s_content=sessionInfo.s_content,
                                                      s_action="callrecent", s_intent=sessionInfo.s_intent,
                                                      s_ask="no", s_status="done")
                return session_return
            elif (rt_value == "callmissed"):
                session_return = convoSessionSpecific(s_type="specificConvo", s_content=sessionInfo.s_content,
                                                      s_action="callmissed", s_intent=sessionInfo.s_intent,
                                                      s_ask="no", s_status="done")
                return session_return
            elif (rt_value == "message"):
                messageToPerson = getMessageToPerson(sessionInfo.s_content)
                # content
                content2 = ""
                if messageToPerson == "ask":
                    content2 = sessionInfo.s_content2
                    if (content2 == ""):
                        session_return = convoSessionSpecific(s_type="specificConvo", s_content=sessionInfo.s_content,
                                                              s_intent=sessionInfo.s_intent,
                                                              s_ask="who do you want to send it to?"
                                                              , s_askForSlot="s_content2"
                                                              , s_status="running")
                        return session_return
                    else:
                        messageToPerson = getMessageToPerson(content2)
                messageContent = getMessageContent(messageToPerson,sessionInfo.s_content)
                print("out of if " + messageContent)
                if messageContent == "ask":
                    content3 = sessionInfo.s_content3
                    if content3 == "":
                        session_return = convoSessionSpecific(s_type="specificConvo", s_content=sessionInfo.s_content,
                                                              s_intent=sessionInfo.s_intent,
                                                              s_content2=content2,
                                                              s_slot1=messageToPerson,
                                                              s_ask="what do you want to sent?",
                                                              s_askForSlot="s_content3",
                                                              s_status="running")
                        return session_return
                    else:
                        session_return = convoSessionSpecific(s_type="specificConvo", s_content=sessionInfo.s_content,
                                                              s_intent=sessionInfo.s_intent,
                                                              s_content2=content2,
                                                              s_content3=content3,
                                                              s_slot1=messageToPerson,
                                                              s_slot2=content3,
                                                              s_action="message",
                                                              s_ask="no",
                                                              s_askForSlot="conformation",
                                                              s_status="done")
                        # "your message is ready to sent"
                        return session_return
                session_return = convoSessionSpecific(s_type="specificConvo", s_content=sessionInfo.s_content,
                                                      s_intent=sessionInfo.s_intent,
                                                      s_slot1=messageToPerson,
                                                      s_slot2=messageContent,
                                                      s_action="message",
                                                      s_ask="no",
                                                      s_askForSlot="conformation",
                                                      s_status="done")
                return session_return
            elif (rt_value == "askmessagerecent"):
                nameTocheck = getReadRecenetPersonName(sessionInfo.s_content)
                if (nameTocheck == "ask"):
                    vl = "askmessagerecent"
                else:
                    vl = "readmessageperson"
                session_return = convoSessionSpecific(s_type="specificConvo", s_content=sessionInfo.s_content,
                                                      s_action=vl,
                                                      s_slot1=nameTocheck,
                                                      s_intent=sessionInfo.s_intent,
                                                      s_ask="no", s_status="done")
                return session_return
            elif (rt_value == "askmessageunread"):
                nameTocheck = getReadRecenetPersonName(sessionInfo.s_content)
                if (nameTocheck == "ask"):
                    vl = "readmessagecheck"
                else:
                    vl = "readmessagecheckperson"
                session_return = convoSessionSpecific(s_type="specificConvo", s_content=sessionInfo.s_content,
                                                      s_action=vl,
                                                      s_slot1=nameTocheck,
                                                      s_intent=sessionInfo.s_intent,
                                                      s_ask="no", s_status="done")
                return session_return
            elif (rt_value == "reminder"):
                content = "content"
                timeR = "time"
                content2 = ""
                content = contentFind(sessionInfo.s_content)
                if (content == "ask"):
                    content2 = sessionInfo.s_content2
                    if (content2 == ""):
                        session_return = convoSessionSpecific(s_type="specificConvo", s_content=sessionInfo.s_content,
                                                              s_intent=sessionInfo.s_intent,
                                                              s_ask="what do you want to be reminded about",
                                                              s_askForSlot="s_content2"
                                                              , s_status="running")
                        return session_return
                    else:
                        content = content2
                timeR = timeFind(sessionInfo.s_content)
                if timeR == "ask":
                    content3 = sessionInfo.s_content3
                    if (content3 == ""):
                        session_return = convoSessionSpecific(s_type="specificConvo",
                                                              s_content=sessionInfo.s_content,
                                                              s_intent=sessionInfo.s_intent,
                                                              s_slot1=content,
                                                              s_content2=content2,
                                                              s_ask="at what time you want to get reminded?",
                                                              s_askForSlot="s_content3"
                                                              , s_status="running")
                        return session_return
                    else:
                        print("inside 3rd in " + content2)
                        timeR = timeFind(content3)
                        print(content3)
                        if timeR == "ask":
                            sessionSpecific = convoSessionSpecific()
                            sessionSpecific.s_content = content3
                            sessionSpecific.s_status = "new"
                            sessionNewIntent = self.run_bot(sessionSpecific)
                            returnAnswer = sessionNewIntent.s_output
                            session_return = convoSessionSpecific(s_type="specificConvo",
                                                                  s_content=sessionInfo.s_content,
                                                                  s_intent=sessionInfo.s_intent,
                                                                  s_slot1=content,
                                                                  s_content2= sessionInfo.s_content2,
                                                                  s_ask=returnAnswer + "    By the way at what time you want to get reminded?",
                                                                  s_askForSlot="s_content3"
                                                                  , s_status="running")
                            return session_return
                        else:
                            output = "your reminder for " + content + " at " + timeR + " is set "
                            session_return = convoSessionSpecific(s_type="specificConvo",
                                                                  s_content=sessionInfo.s_content,
                                                                  s_intent=sessionInfo.s_intent,
                                                                  s_slot1=content,
                                                                  s_slot2=timeR,
                                                                  s_action="remind",
                                                                  s_askForSlot="s_slot2",
                                                                  s_output=output,
                                                                  s_ask="no",
                                                                  s_status="done")
                            return session_return
                output = "your reminder for " + content + " at " + timeR + " is set "
                session_return = convoSessionSpecific(s_type="specificConvo",
                                                      s_content=sessionInfo.s_content,
                                                      s_intent=sessionInfo.s_intent,
                                                      s_slot1=content,
                                                      s_slot2=timeR,
                                                      s_action="remind",
                                                      s_askForSlot="s_slot2",
                                                      s_output=output,
                                                      s_ask="no",
                                                      s_status="done")
                return session_return
