# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf

import sys

sys.path.append("..")
from toolkit.pre_load import pre_load_thu, neo_con, predict_labels
from toolkit.NER import get_NE, temporaryok, get_explain, get_detail_explain, nowok
from toolkit import ParseUtil

parse_util = None


def ER_post2(request):
    """
    sdf
    :param request:
    :return:
    """
    global parse_util
    ctx = {}
    if request.POST:
        org_text = request.POST['user_text']
        text = ""
        if parse_util is None:
            parse_util = ParseUtil.Parse_Util()
        words, postags, netags, arcs = parse_util.parse_sentence(org_text)
        NE_List = get_NE_List(words, netags)
        for pair in NE_List:  # 根据实体列表，显示各个实体
            if pair[1] == 'O':
                text += pair[0]
                continue
            if temporaryok(pair[1]):
                text += "<a href='#'  data-original-title='" + get_explain(
                    pair[1]) + "(暂无资料)'  data-placement='top' data-trigger='hover' data-content='" + get_detail_explain(
                    pair[1]) + "' class='popovers'>" + pair[0] + "</a>"
                continue

            text += "<a href='detail.html?title=" + pair[0] + "'  data-original-title='" + get_explain(
                pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='" + get_detail_explain(
                pair[1]) + "' class='popovers'>" + pair[0] + "</a>"
        ctx['rlt'] = text
    seg_word = ""
    for index in range(len(words)):  # 测试打印词性序列
        seg_word += words[index] + " <strong><small>[" + postags[index] + "]</small></strong> "
    seg_word += ""
    ctx['seg_word'] = seg_word
    return render(request, "index.html", ctx)


def get_NE_List(words, nets):
    db = neo_con
    label = predict_labels
    NE_list = []
    word = ''
    net_pos = ''
    flag = False
    for i in range(len(nets)):
        if nets[i] == 'O':
            flag = True
            word = words[i]
            net_pos = nets[i]
        elif str(nets[i]).startswith('S'):
            flag = True
            word = words[i]
            # 取最后两位
            net_pos = nets[i][-2:]
        else:
            word += words[i]
            if str(nets[i]).startswith('E'):
                flag = True
                net_pos = nets[i][-2:]
        if flag:
            exit_flag = db.matchHudongItembyTitle(word)
            # neo4j中存在该实体
            if word in label and exit_flag is not None and nowok(net_pos):
                # answerList.append([p1, label[p1]])
                net_pos = label[word]
            NE_list.append((word, net_pos))
            word = ''
            net_pos = ''
            flag = False
    return NE_list


# 读取实体解析的文本
def ER_post(request):
    ctx = {}
    if request.POST:
        key = request.POST['user_text']
        thu1 = pre_load_thu  # 提前加载好了
        # 使用thulac进行分词 TagList[i][0]代表第i个词
        # TagList[i][1]代表第i个词的词性
        key = key.strip()
        TagList = thu1.cut(key, text=False)
        text = ""
        NE_List = get_NE(key)  # 获取实体列表

        for pair in NE_List:  # 根据实体列表，显示各个实体
            if pair[1] == 0:
                text += pair[0]
                continue
            if temporaryok(pair[1]):
                text += "<a href='#'  data-original-title='" + get_explain(
                    pair[1]) + "(暂无资料)'  data-placement='top' data-trigger='hover' data-content='" + get_detail_explain(
                    pair[1]) + "' class='popovers'>" + pair[0] + "</a>"
                continue

            text += "<a href='detail.html?title=" + pair[0] + "'  data-original-title='" + get_explain(
                pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='" + get_detail_explain(
                pair[1]) + "' class='popovers'>" + pair[0] + "</a>"

        ctx['rlt'] = text

        #		while i < length:
        #			# 尝试将2个词组合，若不是NE则组合一个，还不是就直接打印文本
        #			p1 = TagList[i][0]
        #			p2 = "*-"  # 保证p2没被赋值时，p1+p2必不存在
        #			if i+1 < length:
        #				p2 = TagList[i+1][0]
        #
        #			t1 = TagList[i][1]
        #			t2 = "*-"
        #			if i+1 < length:
        #				t2 = TagList[i+1][1]
        #
        #			p = p1 + p2
        #			if i+1 < length and preok(t1) and nowok(t2):
        #				answer = db.matchHudongItembyTitle(p)
        #				if answer != None:
        #					text += "<a href='detail.html?title=" + str(p) + "' data-toggle='tooltip' title='" + get_explain(t2) + "'>" + p + "</a>"
        #					i += 2
        #					continue
        #
        #			p = p1
        #			if nowok(t1):
        #				answer = db.matchHudongItembyTitle(p)
        #				if answer != None:
        #					text += "<a href='detail.html?title=" + str(p) + "' data-toggle='tooltip' title='" + get_explain(t1) + "'>" + p + "</a>"
        #					i += 1
        #					continue
        #				elif temporaryok(t1):
        #					text += "<a href='#' data-toggle='tooltip' title='" + get_explain(t1) + "(暂无资料)'>" + p + "</a>"
        #					i += 1
        #					continue
        #
        #
        #			i += 1
        #			text += str(p)

        seg_word = ""
        length = len(TagList)
        for t in TagList:  # 测试打印词性序列
            seg_word += t[0] + " <strong><small>[" + t[1] + "]</small></strong> "
        seg_word += ""
        ctx['seg_word'] = seg_word

    return render(request, "index.html", ctx)
