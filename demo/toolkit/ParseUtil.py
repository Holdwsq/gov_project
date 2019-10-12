import os
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SentenceSplitter

LTP_DATA_DIR = 'D:\ltp_data'
# 分词模型路径，模型名称为`cws.model`
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
# 词性标注模型路径，模型名称为`pos.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
# 命名实体识别模型路径，模型名称为`ner.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
# 依存句法分析模型路径，模型名称为`parser.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')


class Parse_Util(object):
    def __init__(self, lexicon_path='./data/lexicon'):
        # 分词
        self.segmentor = Segmentor()
        # self.segmentor.load_with_lexicon(cws_model_path, lexicon_path)
        self.segmentor.load(cws_model_path)
        # 词性标注
        self.postagger = Postagger()
        self.postagger.load(pos_model_path)
        # 依存句法分析
        self.parser = Parser()
        self.parser.load(par_model_path)
        # 命名实体识别
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(ner_model_path)
        # jieba 分词
        # jieba.load_userdict(lexicon_path)

    def __del__(self):
        self.segmentor.release()
        self.postagger.release()
        self.recognizer.release()
        self.parser.release()

    # 解析句子
    def parse_sentence(self, sentence):
        words = self.segmentor.segment(sentence)
        postags = self.postagger.postag(words)
        netags = self.recognizer.recognize(words, postags)
        arcs = self.parser.parse(words, postags)
        # child_dict_list = ParseUtil.build_parse_child_dict(words, arcs)

        return words, postags, netags, arcs

    # @staticmethod
    # def build_parse_child_dict(words, arcs):
    #     """
    #     为句子中的每个词语维护一个保存句法依存儿子节点的字典
    #     Args:
    #         words: 分词列表
    #         postags: 词性列表
    #         arcs: 句法依存列表, head表示父节点索引，relation表示依存弧的关系
    #     """
    #     child_dict_list = []
    #     for index in range(len(words)):
    #         child_dict = {}
    #         for arc_index in range(len(arcs)):
    #             if arcs[arc_index].head == index + 1:
    #                 relation = arcs[arc_index].relation
    #                 if relation not in child_dict:
    #                     child_dict[relation] = []
    #                 child_dict[relation].append(arc_index)
    #         child_dict_list.append(child_dict)
    #     return child_dict_list
