__author__ = 'yiqibai'
#encoding=utf-8


import re
import jieba



'''contains the basic data type and operation'''


#TODO: Load stop words
stopkey=[line.strip().decode('utf-8') for line in open('./stopword.txt').readlines()]
p = [u'。',u'!',u'',u'?',u'！']
# sp = "u'。'|u'!'|u'?'"
sp = "。|？|！"



#TODO:_____________________
class Sentences(object):
    '''
    :argument
        self.sent : text
        self.words : segment text
        self.title : title
        self.category : category
        self.lldawords : llda words contains in sentences
        self.connectwords: connected words with other sentences
    '''
    def __init__(self, sentences, title, category, id):
        self.sent = sentences
        self.title = title
        # self.words = segmet(sentences)
        self.category = category
        self.id = id
        self.lldawords = None
        self.connectwords = None



#TODO: ____________________
class Document(object):
    '''
    :argument
        self.text : news text
        self.title : news title
        self.category : news category
    '''
    def __init__(self, text, title, category):
        self.title = title
        self.category = category
        self.text = spliter1(text, sp)
        self.sentences = splitSentences(self.text, title, category)



def splitSentences(text, title, category):
    sentences = []
    for i in range(len(text)):
        sentence = text[i]
        if len(sentence) > 3:
            sentObj = Sentences(sentence, title, category, i)
            sentences.append(sentObj)
    return sentences



#TODO: seg text
def segmet(Str):
    '''
    :argument
        Str : string
    :return
        set of token
    '''
    tre = ur'[\u4e00-\u9fff]+'
    rstr = ''.join(re.findall(tre, Str))
    tokenset = set(jieba.cut(rstr))
    tokens = [w for w in tokenset if len(w) > 1]
    return set(tokens) - set(stopkey)



def spliter(s, p):
    result = []
    w = ""
    for c in s:
        c = c.strip()
        if len(c) < 1:
            continue
        if c not in p:
            w += c
        else:
            w += c
            result.append(w)
            w = ""
    if w != "":
        result.append(w)

    text = []
    for i in range(len(result)):
        if len(result[i]) > 3:
            text.append(str(i) + "  " + result[i])
    return text


def spliter1(s, sp):
    st = re.split(sp, s)
    nst = filter(lambda x: len(x) > 0, st)
    return nst



#


