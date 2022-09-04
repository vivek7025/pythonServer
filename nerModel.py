import spacy


def getMessageToPersonName(input):
    nlp = spacy.load("new_model3")
    doc = nlp(input)
    try:
        toMessagePerson = doc.ents[0].text
    except IndexError:
        toMessagePerson = "ask"
    return toMessagePerson
    # print(toMessagePerson)
# getMessageToPersonName("read the last message from alen j")


def getReadRecenetPersonName(input):
    nlp = spacy.load("new_model3")
    doc = nlp(input)
    try:
        toMessagePerson = doc.ents[0].text
    except IndexError:
        toMessagePerson = "ask"
    return toMessagePerson
    # print(toMessagePerson)

# getMessageToPersonName("read the last message from alen j")


def getLocationName(input):
    # nlp = spacy.load("en_core_web_sm")
    nlp = spacy.load("new_model")
    doc = nlp(input)
    placeName = "ask"
    for ent in doc.ents:
        if(ent.label_ == "GPE"):
            placeName = ent.text
            print(placeName)
        print(ent.text, ent.label_, ent.start, ent.end)
    # print(placeName)
    # toMessagePerson = doc.ents[0].text
    # return toMessagePerson

# getLocationName("call vijay")


def getNameAndContent(input):
    nlp = spacy.load("new_model2")
    doc = nlp(input)
    try:
        personName = doc.ents[0].text
    except IndexError:
        personName = "ask"
    print("name extracted : " + personName)
    return personName

def messageandnameExtraction(input):
    nlp = spacy.load("new_model2")
    doc = nlp(input)
    try:
        personName = doc.ents[0].text
    except IndexError:
        personName = "ask"
    try:
        content = doc.ents[1].text
    except IndexError:
        content = "ask"
    print("name extracted : " + personName)
    print("content extracted : " + content)
    return personName

# getNameAndContent("remind me to help hari at 9:00")