import json
import spacy
import random
from spacy.training import Example
from spacy.util import minibatch


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def save_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def train_spacy(data, iterations):
    TRAIN_DATA = data
    nlp = spacy.blank("en")
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe("ner", last=True)
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        # TRAIN_DATA =  # your data
        random.shuffle(TRAIN_DATA)
        losses = {}
        for batch in minibatch(TRAIN_DATA, size=8):
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], drop=0.35, sgd=optimizer, losses=losses)
            print(losses)
    return (nlp)


# TRAIN_DATA = load_data("train.json")
# nlp = train_spacy(TRAIN_DATA, 30)
# nlp.to_disk("new_model")


def makeIntent(names,sentence_call,ent_start_call,sentence_message,ent_start_message_name1,sentence_message2,ent_start_message_name2,
               sentence_message3,ent_start_message_name3,sentence_messageContinue,addOnValue,data):
    data_final = []
    for name in names: #for call
        ent_end = ent_start_call+len(name)
        sentence_in = sentence_call+name
        ent_label = 'PERSON'
        data_value =[
                sentence_in,
                {'entities': [
                    [
                        ent_start_call, ent_end, ent_label
                    ]
                ]}
            ]
        data.append(data_value)

    for name in names: #for message1
        length_name = len(name)
        ent_end_name1 = ent_start_message_name1+length_name
        sentence_in1 = sentence_message +name +sentence_messageContinue
        ent_start_message_content1 = ent_end_name1 + addOnValue
        ent_end_message_content1 = ent_start_message_content1 + len(sentence_messageContinue) - 6
        ent_label = 'PERSON'
        ent_label2 = 'CONTENT'
        data_value =[
                sentence_in1,
                {'entities': [
                    [
                        ent_start_message_name1, ent_end_name1, ent_label
                    ],
                    [
                        ent_start_message_content1, ent_end_message_content1, ent_label2
                    ]
                ]}
            ]
        data.append(data_value)
    for name in names: #for message2
        ent_end_name2 = ent_start_message_name2 + len(name)
        sentence_in1 = sentence_message2 +name +sentence_messageContinue
        ent_start_message_content1 = ent_end_name2 + addOnValue
        ent_end_message_content1 = ent_start_message_content1 + len(sentence_messageContinue) - 6
        ent_label = 'PERSON'
        ent_label2 = 'CONTENT'
        data_value = [
            sentence_in1,
            {'entities': [
                [
                    ent_start_message_name2, ent_end_name2, ent_label
                ],
                [
                    ent_start_message_content1, ent_end_message_content1, ent_label2
                ]
            ]}
        ]
        data.append(data_value)
    for name in names: #for message3
        ent_end_name3 = ent_start_message_name3 + len(name)
        sentence_in1 = sentence_message3 + name + sentence_messageContinue
        ent_start_message_content1 = ent_end_name3 + addOnValue
        ent_end_message_content1 = ent_start_message_content1 + len(sentence_messageContinue) - 6
        ent_label = 'PERSON'
        ent_label2 = 'CONTENT'
        data_value = [
            sentence_in1,
            {'entities': [
                [
                    ent_start_message_name3, ent_end_name3, ent_label
                ],
                [
                    ent_start_message_content1, ent_end_message_content1, ent_label2
                ]
            ]}
        ]
        data.append(data_value)
    python_obj = json.dumps(data)
    data_json = json.loads(python_obj)
    # print(data_json[len(data_json - 1)])
    with open('train2.json', 'w') as json_file:
        json.dump(data_json, json_file)
    TRAIN_DATA = load_data("train2.json")
    nlp = train_spacy(TRAIN_DATA, 30)
    nlp.to_disk("new_model2")


def makeModel2(names,sentence1,ent_start1,sentence2,ent_start2,sentence3,ent_start3,sentence4,ent_start4,sentence5,ent_start5,sentence6,
               ent_start6,sentence7,ent_start7,sentence8,ent_start8,sentence9,ent_start9,sentence10,ent_start10,data):
    for name in names:  # for call
        sentence_in1 = sentence1 + name
        ent_end1 = ent_start1 + len(name)
        sentence_in2 = sentence2 + name
        ent_end2 = ent_start2 + len(name)
        sentence_in3 = sentence3 + name
        ent_end3 = ent_start3 + len(name)
        sentence_in4 = sentence4 + name
        ent_end4 = ent_start4 + len(name)
        sentence_in5 = sentence5 + name
        ent_end5 = ent_start5 + len(name)
        sentence_in6 = sentence6 + name
        ent_end6 = ent_start6 + len(name)
        sentence_in7 = sentence7 + name
        ent_end7 = ent_start7 + len(name)
        sentence_in8 = sentence8 + name
        ent_end8 = ent_start8 + len(name)
        sentence_in9 = sentence9 + name
        ent_end9 = ent_start9 + len(name)
        sentence_in10 = sentence10 + name
        ent_end10 = ent_start10 + len(name)
        ent_label = 'PERSON'
        data_value1 = [
            sentence_in1,
            {'entities': [
                [
                    ent_start1, ent_end1, ent_label
                ]
            ]}
        ]
        data_value2 = [
            sentence_in2,
            {'entities': [
                [
                    ent_start2, ent_end2, ent_label
                ]
            ]}
        ]
        data_value3 = [
            sentence_in3,
            {'entities': [
                [
                    ent_start3, ent_end3, ent_label
                ]
            ]}
        ]
        data_value4 = [
            sentence_in4,
            {'entities': [
                [
                    ent_start4, ent_end4, ent_label
                ]
            ]}
        ]
        data_value5 = [
            sentence_in5,
            {'entities': [
                [
                    ent_start5, ent_end5, ent_label
                ]
            ]}
        ]
        data_value6 = [
            sentence_in6,
            {'entities': [
                [
                    ent_start6, ent_end6, ent_label
                ]
            ]}
        ]
        data_value7 = [
            sentence_in7,
            {'entities': [
                [
                    ent_start7, ent_end7, ent_label
                ]
            ]}
        ]
        data_value8 = [
            sentence_in8,
            {'entities': [
                [
                    ent_start8, ent_end8, ent_label
                ]
            ]}
        ]
        data_value9 = [
            sentence_in9,
            {'entities': [
                [
                    ent_start9, ent_end9, ent_label
                ]
            ]}
        ]
        data_value10 = [
            sentence_in10,
            {'entities': [
                [
                    ent_start10, ent_end10, ent_label
                ]
            ]}
        ]
        data.append(data_value1)
        data.append(data_value2)
        data.append(data_value3)
        data.append(data_value4)
        data.append(data_value5)
        data.append(data_value6)
        data.append(data_value7)
        data.append(data_value8)
        data.append(data_value9)
        data.append(data_value10)

    python_obj = json.dumps(data)
    data_json = json.loads(python_obj)
        # print(data_json[len(data_json - 1)])
    with open('train3.json', 'w') as json_file:
        json.dump(data_json, json_file)
    TRAIN_DATA = load_data("train3.json")
    nlp = train_spacy(TRAIN_DATA, 30)
    nlp.to_disk("new_model3")


def getTrainingSetReady2(names):
    # with open('Ner train/data_set.json', 'r') as f:
    with open('train3.json', 'r') as f:
      data = json.load(f)
    sentence1 = "read the last message from "
    ent_start1 = 27
    sentence2 = "read the recent message of "
    ent_start2 = 27
    sentence3 = "read message of "
    ent_start3 = 16
    sentence4 = "how many unread messages are there from "
    ent_start4 = 40
    sentence5 = "is there any unread messages of "
    ent_start5 = 32
    sentence6 = "count the unread messages from "
    ent_start6 =  31
    sentence7 = "Call "
    ent_start7 = 5
    sentence8 = "Send a message to "
    ent_start8 = 18
    sentence9 = "Text "
    ent_start9 = 5
    sentence10 = "Text message "
    ent_start10 = 13
    makeModel2(names,sentence1,ent_start1,sentence2,ent_start2,sentence3,ent_start3,sentence4,ent_start4,sentence5,ent_start5,
               sentence6,ent_start6,sentence7,ent_start7,sentence8,ent_start8,sentence9,ent_start9,sentence10,ent_start10,data)


def getTrainingSetReady(names):
    with open('Ner train/data_set.json', 'r') as f:
      data = json.load(f)
    print(data[0])
    sentence_call = 'Call '
    sentence_message = 'Send a message to '
    ent_start_message_name1 = 18
    sentence_message2 = 'Text '
    ent_start_message_name2 = 5
    sentence_message3 ='Text message '
    ent_start_message_name3 = 13
    sentence_messageContinue = ' that the door is closed'
    addOnValue = 6 #name entity stop + 6
    # names = ['vivek','vijay','amma','chithra','sunil']
    ent_start_call = 5
    makeIntent(names,sentence_call,ent_start_call,sentence_message,ent_start_message_name1,sentence_message2,ent_start_message_name2,
               sentence_message3,ent_start_message_name3,sentence_messageContinue,addOnValue,data)

# TRAIN_DATA = load_data("annotations.json")
# print(TRAIN_DATA[0])

# test = "Text message Rahul the door is closed"
# nlp = spacy.load("ano")
# doc = nlp(test)
# for ent in doc.ents:
#     print(ent.text, ent.label)