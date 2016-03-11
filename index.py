#coding=utf-8
import unicodedata
import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

_STOP_WORDS = frozenset([',','…','。','“','；','”','（','）',' ','\n'])


#词偏移
def word_split(text):
    word_list = []#列表
    wcount = 0
    words = jieba.cut(text,cut_all=False)
    for word in words:#提取字母和偏移量
        wcount =wcount + 1
        word_list.append((wcount,word))
    return word_list

#把小于3或者在stopword中的词删除
def words_cleanup(words):
    cleaned_words = []#初始化
    for index, word in words:#提取每个词的索引号和单词
        if word in _STOP_WORDS:#如果是stopword不做处理
            continue#跳过循环
        cleaned_words.append((index, word))#将符合条件的词添加到列表
    return cleaned_words


#生成索引
def word_index(text):
    words = word_split(text)#将一段分割成词
    words = words_cleanup(words)#删掉不符合的单词
    return words

#倒排索引
def inverted_index(text):
    inverted = {}#初始化

    for index, word in word_index(text):#提取索引号和词
        locations = inverted.setdefault(word, [])#以单词为索引添加值
        locations.append(index)#将索引号作为值添加
    return inverted

#添加文档号
def inverted_index_add(inverted, doc_id, doc_index):
    for word, locations in doc_index.iteritems():#提取词和位置
        indices = inverted.setdefault(word, {})#以词尾索引添加值
        indices[doc_id] = locations#将文档号和位置作为值


def search(inverted, query):
    words = [word for _, word in word_index(query) if word in inverted]#将要检索的词分割，把在范围内的词提取出来
    results = [set(inverted[word].keys()) for word in words]
    return reduce(lambda x, y: x & y, results) if results else []#返回符合条件的词

if __name__ == '__main__':
    doc1 = """
人的价值判断一般有两部分，一个是外在的社会规范，一个是内心最本真的想法。在很多时候，
我们常常只有遵循了社会规范（考好成绩，听老师的话），才能得到认可和尊重（得到老师的喜爱，同学的羡慕）。
在这样的情况下，我们常常会为了得到关注和奖励，努力达到他人的期望（成为社交大神，在各个场合如鱼得水），
以别人的期望建构自我概念（我是社交大神），忽略并压抑自己最真实的体验（我也是人，也会怯场，也会没有自信）。
因此，当你感受到和自我概念不一致的经验（在陌生的场合怯场）时，就产生了很强的焦虑感。在这样的情景下，
你需要更多地接纳和尊重自己的感受，以自己的体验为主”我在一些社交场合很有天分，但是也会在陌生的场合也会有些怯场“，
而不是以别人的评价来认识自己”我是社交大神，在任何场合都如鱼得水“。在你慢慢从自我概念中剔除掉别人不真实的赞美和期待，
尊重并喜爱真实的自己，那焦虑感也会不断降低，因为你在任何场合都是真实的自己，没有与自我概念不协调的经验。
   """ 
    doc2 = """
题主一直在说，每次面对陌生的社交场合，想到自己可能不大好的表现，就会很痛苦。这个痛苦，
其实很大程度也是来源于题主对”社交大神跌落神坛“后他人的表现反应过度吧。可能会担心别人看到平庸的自己，
然后失望，嘲笑。但实际上，结果可能并没有那么糟糕。题主一方面要正确面对社交的表现，比如好好考虑，”如果我……（表现），
那可能会出现……（结果）“；另一方面，可以在现实中找来一帮好友，然后在他们面前做出不大良好的社交表现，
然后看看结果是不是有想象的那么糟糕。多经历几次“失败“的社交经历，或许你就能明白社交大神犯错也没那么可怕，
说不定“男神”变“逗比”后还能拉近和别人的距离呢。
   """


    #词偏移位置倒排索引
    inverted = {}
    documents = {'doc1':doc1, 'doc2':doc2}
    for doc_id, text in documents.iteritems():
        doc_index = inverted_index(text)
        inverted_index_add(inverted, doc_id, doc_index)
    for word, doc_locations in inverted.iteritems():
        print word, doc_locations

    #多词查询
    queries = ['题主', '陌生', '陌生的社交场合']
    for query in queries:
        result_docs = search(inverted, query)
        print "Search for '%s': %r" % (query, result_docs)
        for _, word in word_index(query):
            def extract_text(doc, index): 
                return documents[doc][index:index+20].replace('\n', ' ')

            for doc in result_docs:
                for index in inverted[word][doc]:
                    print '   - %s...' % extract_text(doc, index)
