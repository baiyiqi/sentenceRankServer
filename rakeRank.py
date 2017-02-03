__author__ = 'yiqibai'
#encoding=utf-8

import re
import operator
import jieba
import math
import dataType


#TODO: seg text
def segment(Str):
    '''
    :argument
        Str : string
    :return
        set of token
    '''
    tre = ur'[\u4e00-\u9fff]+'
    rstr = ''.join(re.findall(tre, Str))
    tokenset = jieba.cut(rstr)
    tokens = [w for w in tokenset if len(w.strip()) > 1]
    return tokens



def generate_fix_lenth_candidate_keywords(text, stopwords, length):
    phrase_list = []
    phrase = ""
    if length == -1:
        for i, w in enumerate(text):
            if len(w) == 0:
                continue
            if w not in stopwords:
                phrase += w + " "
            if i == len(text) - 1 or w in stopwords:
                phrase = phrase.strip()
                if len(phrase) > 0:
                    phrase_list.append(phrase)
                    phrase = ""

    else:
        counter = 0
        for i, w in enumerate(text):
            if len(w) == 0:
                continue
            if w not in stopwords:
                phrase += w + " "
                counter += 1
            if counter == length or i == len(text) - 1:
                phrase_list.append(phrase.strip())
                phrase = ""
                counter = 0
    return phrase_list


def load_stop_words(stop_word_file):
    stopkey=[line.strip().decode("utf-8") for line in open('./' + stop_word_file).readlines()]
    return set(stopkey)


def split_sentences(text):
    """
    Utility function to return a list of sentences.
    @param text The text that must be split in to sentences.
    """
    sentence_delimiters = re.compile(u'[.!?,;:，。；：？！\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
    sentences = sentence_delimiters.split(text)
    return [s.strip() for s in sentences]


def calculate_word_scores(phraseList):
    word_frequency = {}
    word_degree = {}
    for phrase in phraseList:
        word_list = phrase.split(" ")
        word_list_degree = len(word_list)

        word_set = set()
        for word in word_list:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            if word not in word_set:
                word_degree.setdefault(word, 0)
                word_degree[word] += word_list_degree
            word_set.add(word)

    # Calculate Word scores = deg(w)/frew(w)
    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
    #word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
    return word_score


def generate_candidate_keyword_scores(phrase_list, word_score):
    keyword_candidates = {}
    for phrase in phrase_list:
        keyword_candidates.setdefault(phrase, 0)
        word_list = phrase.split(" ")
        candidate_score = 0
        for word in word_list:
            candidate_score += word_score[word]
        keyword_candidates[phrase] = candidate_score
    return keyword_candidates


class Rake(object):

    def __init__(self, stop_words_path):
        self.stop_words = load_stop_words("./" + stop_words_path)
        self.key_phrase = {}
        self.key_words = {}

    def run(self, text):
        sentences = split_sentences(text)
        phrase_list = []
        for sent in sentences:
            if len(sent) < 1:
                continue
            seg_sent = segment(sent)
            phrase_list += generate_fix_lenth_candidate_keywords(seg_sent, self.stop_words, -1)

        word_scores = calculate_word_scores(phrase_list)

        self.key_words = word_scores

        keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores)

        sorted_keywords = sorted(keyword_candidates.iteritems(), key=operator.itemgetter(1), reverse=True)

        self.key_phrase = {sk[0]:sk[1] for sk in sorted_keywords}



def get_rank(keywords,  sentences):
    s_score = {}
    for s in sentences:
        score = 0.0
        for k in keywords:
            if k in s[0]:
                score += math.pow(2, keywords[k])
        s_score[s[0]] = score

    sort_weight = sorted(s_score.items(), key=lambda d:d[1], reverse=True)
    sort_sents = [i[0] for i in sort_weight]
    return sort_sents


def get_rank1(keyphrase, sentences):
    s_score = {}
    for s in sentences:
        score = 0.0
        for kph in keyphrase:
            flag = True
            for p in kph.split(" "):
                if p not in s[0]:
                    flag = False
                    break
            if flag:
                score += math.pow(2, keyphrase[kph])
        s_score[s[0]] = score

    sort_weight = sorted(s_score.items(), key=lambda d:d[1], reverse=True)
    sort_sents = [i[0] for i in sort_weight]
    return sort_sents


# text = "海军海军海军, 新闻, 发言人梁阳, 海军新闻, 发言人梁阳"
R = Rake("stopword.txt")

def rake_rank(text, sentobj):
    if text == None or sentobj == None:
        return []
    R.run(text)
    sents = [(s.sent, s.id) for s in sentobj]
    rank_sent = get_rank(R.key_words, sents)
    # print rank_sent
    return rank_sent

#
# text = "盐城南洋机场的相关负责人告诉交汇点记者，广大干部职工连夜奋战，斗风雪除冰雪，为的就是让机场跑到正常开放，航班准点起降，旅客便捷出行，市民度过一个欢乐祥和的春节。放眼银装素裹的城市，高架路面已不见积雪，车辆平稳畅行。"
# docObj = dataType.Document(text, "", "")
# rake_rank(text, docObj.sentences)
