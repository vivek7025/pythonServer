import json

from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

import intent_check
import nlu_convo
from spyc import getTrainingSetReady, getTrainingSetReady2


class outputObject:
    action = ""
    callName = ""


class inputObject:
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
    s_slot2 = ""
    s_slot3 = ""
    s_slot4 = ""
    s_ask = ""
    s_askForSlot = ""
    s_content2 = ""
    s_content3 = ""
    s_action = ""
    s_output = ""
    s_status = ""


specific_intent = ["reminder","call","callrecent","callmissed","open cam","alarm","calreminder","askWeather","askNews","askmessagerecent"
    ,"askmessageunread","time","message"]


def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2

        # If x is greater, ignore left half
        if arr[mid] < x:
            low = mid + 1

        # If x is smaller, ignore right half
        elif arr[mid] > x:
            high = mid - 1

        # means x is present at mid
        else:
            return mid
    # If we reach here, then the element was not present
    return -1


def createJsonObject(sessionInfo):
    if sessionInfo.s_type == "nomralConvo":
        return_json = {
            "s_type" : sessionInfo.s_type,
            "s_content" : sessionInfo.s_content,
            "s_intent" : sessionInfo.s_intent,
            "s_output" : sessionInfo.s_output,
            "s_status" : sessionInfo.s_status
        }
        return return_json
    elif sessionInfo.s_type == "specificConvo":
        return_json = {
            "s_type": sessionInfo.s_type,
            "s_content": sessionInfo.s_content,
            "s_intent": sessionInfo.s_intent,
            "s_output": sessionInfo.s_output,
            "s_status": sessionInfo.s_status,
            "s_slotNumber": sessionInfo.s_slotNumber,
            "s_slot1": sessionInfo.s_slot1,
            "s_slot2": sessionInfo.s_slot2,
            "s_slot3": sessionInfo.s_slot3,
            "s_slot4": sessionInfo.s_slot4,
            "s_ask": sessionInfo.s_ask,
            "s_askForSlot": sessionInfo.s_askForSlot,
            "s_content2" : sessionInfo.s_content2,
            "s_content3": sessionInfo.s_content3,
            "s_action": sessionInfo.s_action,
        }
        return return_json


app = Flask(__name__)
api = Api(app)

# names = {"vivek": {"age": 21, "gender": "male"},
#         "rahul" : {"age": 25, "gender": "male"}}

# class HelloWorld(Resource):
#     def get(self, name):
#         return names[name]

#     def post(self):
#         return {"data": "posted"}    

# api.add_resource(HelloWorld, "/helloworld/<string:name>")

videos_put_args = reqparse.RequestParser()
videos_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
videos_put_args.add_argument("views", type=int, help="Views of the video", required=True)
videos_put_args.add_argument("likes", type=int, help="likes on the video", required=True)

videos = {}

def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Video id is not valid....")

def abort_if_video_exist(video_id):
    if video_id in videos:
        abort(409, message="Video already exist with that ID...")        

class Video(Resource):
    def get(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        return videos[video_id]

    def put(self, video_id):
        abort_if_video_exist(video_id)
        args = videos_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201 

    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204


class Bot(Resource):
    def get(self, sentence):
        x = intent_check.checkIntent()
        voiceBot = nlu_convo.voice_bot()
        rt_value = x.checkIntent(sentence)
        result = binary_search(specific_intent, rt_value)

        if result != -1:
            return
        else:
            sessionNormal = convoSessionNormal()
            sessionNormal.s_content = sentence
            sessionNormal.s_type = "nomralConvo"
            sessionNormal.s_intent = rt_value
            sessionNormal.s_status = "completed"
            sessionNormal.s_output = rt_value
            return_json = createJsonObject(sessionNormal)
            return return_json


class Bot2(Resource):
    def get(self, sentence):
        # voiceBot = nlu_convo.voice_bot()
        # return_value = outputObject()
        # return_value = voiceBot.run_bot(sentence)
        # return_dic = {
        #     "action": return_value.action,
        #     "callName": return_value.callName
        # }
        returnData = sentence
        return returnData


@app.route('/getjs', methods = ['POST'])
def getjs():
    vl = request.get_json()
    print(len(vl))
    # getTrainingSetReady(vl)
    getTrainingSetReady2(vl)
    return_dic = "good"
    return return_dic
    # return slot1


@app.route('/getQa', methods = ['POST'])
def getQa():
    x = intent_check.checkIntent()
    inputJson = request.get_json()
    intent = inputJson['s_intent']
    s_type = inputJson['s_type']
    if(intent == "message"):
        slot1 = inputJson['s_slot1']
        slot2 = inputJson['s_slot2']
        anw = inputJson['s_qa']
        rt_value = x.checkIntent(anw)
        if rt_value == "yes":
            return_dic = {
                "s_type": s_type,
                "s_ask": "no",
                "s_action" : "message",
                "s_slot1" : slot1,
                "s_slot2" : slot2
            }
            return return_dic


@app.route('/getInput', methods = ['POST'])
def getInput():
    x = intent_check.checkIntent()
    voiceBot = nlu_convo.voice_bot()
    inputJson = request.get_json()
    statusSession = inputJson['s_status']
    if statusSession == "running":
        sessionSpecific = convoSessionSpecific()
        sessionSpecific.s_type = inputJson['s_type']
        print("2nd input type " +sessionSpecific.s_type)
        sessionSpecific.s_content = inputJson['s_content']
        print("content 1 "+inputJson['s_content'])
        sessionSpecific.s_intent = inputJson['s_intent']
        sessionSpecific.s_slotNumber = inputJson['s_slotNumber']
        sessionSpecific.s_slot1 = inputJson['s_slot1']
        sessionSpecific.s_slot2 = inputJson['s_slot2']
        sessionSpecific.s_slot3 = inputJson['s_slot3']
        sessionSpecific.s_slot4 = inputJson['s_slot4']
        sessionSpecific.s_ask = inputJson['s_ask']
        sessionSpecific.s_askForSlot = inputJson['s_askForSlot']
        sessionSpecific.s_content2 = inputJson['s_content2']
        print("content 2 " + inputJson['s_content2'])
        sessionSpecific.s_content3 = inputJson['s_content3']
        print("content 3 " + inputJson['s_content3'])
        sessionSpecific.s_action = inputJson['s_action']
        sessionSpecific.s_output = inputJson['s_output']
        sessionSpecific.s_status = inputJson['s_status']
        return_value = voiceBot.run_bot(sessionSpecific)
        return_json = createJsonObject(return_value)
        print("came till main" +return_value.s_type)
        return return_json
    else:
        rt_value = x.checkIntent(inputJson['s_content'])
        if rt_value in specific_intent:
            sessionSpecific = convoSessionSpecific()
            sessionSpecific.s_content = inputJson['s_content']
            sessionSpecific.s_type = "specificConvo"
            sessionSpecific.s_intent = rt_value
            sessionSpecific.s_status = "running"
            print(inputJson['s_content'])
            return_value = voiceBot.run_bot(sessionSpecific)
            return_json = createJsonObject(return_value)
            return return_json
        else:
            sessionNormal = convoSessionNormal()
            sessionNormal.s_content = inputJson['s_content']
            print("inside normal " + inputJson['s_content'])
            sessionNormal.s_type = "nomralConvo"
            sessionNormal.s_intent = rt_value
            sessionNormal.s_status = "completed"
            sessionNormal.s_output = rt_value
            return_json = createJsonObject(sessionNormal)
            return return_json


api.add_resource(Video, "/video/<int:video_id>")
api.add_resource(Bot, "/bot/<string:sentence>")
api.add_resource(Bot2, "/bot2/<string:sentence>")



if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
    # app.run(debug=True)