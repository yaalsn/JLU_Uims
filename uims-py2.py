#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" test """
import json
#  from hashlib import md5
import hashlib
import requests

NAME = ''
PWDPLAIN = ''
ANSWERS = {"prob11":"A", "prob12":"A", "prob13":"D", "prob14":"A", "prob15":"A", \
           "prob21":"A", "prob22":"A", "prob23":"A", "prob31":"A", "prob32":"A", \
           "prob41":"A", "prob42":"A", "prob43":"A", "prob51":"A", "prob52":"A", \
           "sat6":"A", "mulsel71":"EGHK", "advice8":"good"}

def maketransferpwd(name, pwdplain):
    """ transfer the passwd"""
    #  name.encode('utf-8')
    #  pwdplain.encode('utf-8')
    inp = hashlib.md5('UIMS'.encode('utf-8') + name.encode('utf-8') +\
                      pwdplain.encode('utf-8')).hexdigest()
    return inp

def login(name, inp):
    """ for login """
    itemid = []
    s_session = requests.session()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
    r_s_get = s_session.get('http://uims.jlu.edu.cn/ntms/userLogin.jsp')
    param = {'j_username':name, 'j_password':inp}
    p_s_post = s_session.post('http://uims.jlu.edu.cn/ntms/j_spring_security_check', param)
    userinfo = s_session.post('http://uims.jlu.edu.cn/ntms/action/getCurrentUserInfo.do')
    userid = json.loads(userinfo.text)['userId']
    search = json.dumps({"type":"search", "tag":"blankEvalItem",
                         "branch":"default", "params":{"personId":userid}})
    headers_foo = {'Content-Type':'application/json;charset=UTF-8'}
    result = s_session.post('http://uims.jlu.edu.cn/ntms/service/res.do',\
                            search, headers=headers_foo)
    dic_foo = json.loads(result.text)

    for i in dic_foo['value']:
        itemid.append(i['evalitemid'])

    for item in itemid:
        fuck = s_session.get('http://uims.jlu.edu.cn/ntms/page/eval\
                                /eval_detail_100.html?eitem=' + item)
        headers = {'Content-Type':'application/json'}
        dic = {"evalitemid":item, "answers":ANSWERS}
        data = json.dumps(dic)
        print(data)
        fuck_p = s_session.post('http://uims.jlu.edu.cn/ntms/eduEvaluate\
                                /eval-with-answer.do', data, headers=headers)
        print(fuck_p.text)

if __name__ == '__main__':
    login(NAME, maketransferpwd(NAME, PWDPLAIN))
