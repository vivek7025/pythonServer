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


TRAIN_DATA = load_data("try.json")
nlp = train_spacy(TRAIN_DATA, 30)
nlp.to_disk("reminder_model")


def makeModel2(names,sentence1,ent_start1,sentence2,ent_start2,sentence3,ent_start3,sentence4,ent_start4,sentence5,ent_start5,sentence6,ent_start6,data):
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
        data.append(data_value1)
        data.append(data_value2)
        data.append(data_value3)
        data.append(data_value4)
        data.append(data_value5)
        data.append(data_value6)

    python_obj = json.dumps(data)
    data_json = json.loads(python_obj)
        # print(data_json[len(data_json - 1)])
    with open('train3.json', 'w') as json_file:
        json.dump(data_json, json_file)
    TRAIN_DATA = load_data("train3.json")
    nlp = train_spacy(TRAIN_DATA, 30)
    nlp.to_disk("new_model3")


def getTrainingSetReady2(names):
    with open('Ner train/data_set.json', 'r') as f:
      data = json.load(f)
    sentence1 = "send a message i will come late to "
    ent_start1 = 15
    sentence2 = "send a sms "
    ent_start2 = 11
    sentence3 = "send a message to "
    ent_start3 = 18
    sentence4 = "send a sms to "
    ent_start4 = 14
    sentence5 = "is there any unread messages of "
    ent_start5 = 32
    sentence6 = "count the unread messages from "
    ent_start6 =  31
    makeModel2(names,sentence1,ent_start1,sentence2,ent_start2,sentence3,ent_start3,sentence4,ent_start4,sentence5,ent_start5,
               sentence6,ent_start6,data)