import re
import intent_check
import actionBot
from firebase_admin import db

#for Weather
import requests
from datetime import datetime
from geopy.geocoders import Nominatim

pattern_content_remm = r"\bto"
pattern_time_remm = r"\bat"

pattern_tag_bk = r"\bas"

regex = '^[0-9]+$'
pattern_call = r"\bcall"

bookmark_head1 = r"\bas"
bookmark_head2 = r"\blabel"
bookmark_head3 = r"\bname"


class outputObject:
    action = ""
    callName = ""


class convoSessionNormal:
    s_type = ""
    s_content = ""
    s_intent = ""
    s_output = ""
    s_status = ""


class convoSessionSpecific:
    s_type = ""
    s_content = ""
    s_intent = ""
    s_slotNumber = ""
    s_slot1 = ""
    s_slot2 = ""
    s_slot3 = ""
    s_slot4 = ""
    s_ask = ""
    s_askForSlot = ""
    s_action = ""
    s_output = ""
    s_status = ""


class Slots:
    def __init__(self):
        self.s_intent = "nul"
        self.s_num = 0
        self.s1 = "nul"
        self.s2 = "nul"


def requestD(toRqst):
    vl = "got"
    invokeActInsert = db.reference('invokebotaction')
    invokeActInsert.set(toRqst)

    invoketrig = db.reference('invokebottrig')
    invoketrig.set("recv")

    while True:
        flag1 = db.reference('locationSndtrig')
        print(flag1.get())
        checker1 = flag1.get()

        if (checker1 == "snd"):
            flag1.set("nul")
            return


def getPlaceofWeather(sentence):
    val = "ask"
    pattern_currentPlaceFind1 = r"\bnow"
    pattern_currentPlaceFind2 = r"\btoday"
    pattern_currentPlaceFind3 = r"\boutside"
    pattern_placeName = r"\bin"
    match1 = re.search(pattern_currentPlaceFind1, sentence)
    match2 = re.search(pattern_currentPlaceFind2, sentence)
    match3 = re.search(pattern_currentPlaceFind3, sentence)
    match01 = re.search(pattern_placeName, sentence)
    if(match1 != None or match2 != None or match3 != None):
        print("get current location")
        val = "getCurrent"
    elif(match01 != None):
        list = re.split(pattern_placeName, sentence)
        list_vl = list[1]
        val = list_vl
    return val


def getWeather(latitude,longitude):
    user_api = "f954bd7b19dc81b72034a0f76c0c24f7"
    # function to get placeofWeather
    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(
        longitude) + "&appid=" + str(user_api)
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    temp_city = ((api_data['main']['temp']) - 273.15)
    temp_city = round(temp_city)
    temp_cityString = str(temp_city)

    weatherOutput = "The current weather is " + temp_cityString + "degree celsius"

    return weatherOutput


def getWeatherReport(placeofWeather):
    if(placeofWeather == "getCurrent"):
        requestD(placeofWeather)
        lati = db.reference('locationLatitude')
        longi = db.reference('locationLongitude')
        print(lati.get())
        print(longi.get())
        latitude = lati.get()
        longitude = longi.get()
        result = getWeather(latitude,longitude)
        return result
    else:
        location = placeofWeather
        # Initialize Nominatim API
        geolocator = Nominatim(user_agent="MyApp")

        location_geo = geolocator.geocode(location)
        latitude = location_geo.latitude
        longitude = location_geo.longitude
        #
        lat = str(latitude)
        lon = str(longitude)
        result = getWeather(latitude, longitude)
        return result


class voice_bot:
    def __init__(self):
        self.val = "nul"

    def ask(self,toAsk):
        vl = "at 6"
        inserter2 = db.reference('Tag4_sysinpt')
        inserter2.set(toAsk)

        inserter1 = db.reference('Tag2_trig')
        inserter1.set("recv")

        while True:
            flag1 = db.reference('Tag2_trig')
            print(flag1.get())
            checker1 = flag1.get()

            if (checker1 == "snd"):
                receiver1 = db.reference('Tag3_usinpt')
                print(receiver1.get())
                sentence = receiver1.get()
                if sentence == "quit":
                    break

                return sentence
        return vl

    def slotFill(self,slotD,sentence):
        gd = "couldn't process the output"
        if (slotD == "askWeather"):
            placeofWeather = getPlaceofWeather(sentence)
            if (placeofWeather == "ask"):
                xer = self.ask("which place do you want to know")
                placeofWeather = getPlaceofWeather(xer)
            weatherReport = getWeatherReport(placeofWeather)
            return weatherReport
        elif (slotD == "time"):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            vl = "the current time is "+ current_time
            return vl
        return gd

    def run_bot(self,sessionInfo):
        rt_value = sessionInfo.s_intent
        ob = outputObject()
        print(rt_value)
        if(rt_value == "call"):
            sessionInfo.s_slotNumber = 1
            z = actionBot.BotAction()
            specificConvo = z.actRquest(sessionInfo)
            return specificConvo
        elif (rt_value == "callrecent"):
            z = actionBot.BotAction()
            specificConvo = z.actRquest(sessionInfo)
            return specificConvo
        elif (rt_value == "callmissed"):
            z = actionBot.BotAction()
            specificConvo = z.actRquest(sessionInfo)
            return specificConvo
        elif (rt_value == "message"):
            z = actionBot.BotAction()
            specificConvo = z.actRquest(sessionInfo)
            return specificConvo
        elif (rt_value == "askmessagerecent"):
            z = actionBot.BotAction()
            specificConvo = z.actRquest(sessionInfo)
            return specificConvo
        elif (rt_value == "askmessageunread"):
            z = actionBot.BotAction()
            ob = z.actRquest(sessionInfo)
            return ob
        elif (rt_value == "reminder"):
            sessionInfo.s_slotNumber = 2
            z = actionBot.BotAction()
            rt_value = z.actRquest(sessionInfo)
            return rt_value
        elif (rt_value != "n"):
            return rt_value

