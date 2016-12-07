# -*- coding: utf-8 -*-  
import requests
from hashlib import md5
import json

name = ''
pwdPlain = ''
answers = {"prob11":"A","prob12":"A","prob13":"D","prob14":"A","prob15":"A","prob21":"A","prob22":"A","prob23":"A","prob31":"A","prob32":"A","prob41":"A","prob42":"A","prob43":"A","prob51":"A","prob52":"A","sat6":"A","mulsel71":"EGHK","advice8":"good"}
ItemId = []

def makeTransferPwd(name, pwdPlain):
    inp = md5('UIMS' + name + pwdPlain).hexdigest()
    return inp

def login(name, inp):
    s = requests.session()
    #headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
    r = s.get('http://uims.jlu.edu.cn/ntms/userLogin.jsp')
    param = {'j_username':name, 'j_password':inp}
    p = s.post('http://uims.jlu.edu.cn/ntms/j_spring_security_check', param)
    userInfo = s.post('http://uims.jlu.edu.cn/ntms/action/getCurrentUserInfo.do')
    userId = json.loads(userInfo.text)['userId']
    search = json.dumps({"type":"search","tag":"blankEvalItem","branch":"default","params":{"personId":userId}})
    headers_foo = {'Content-Type':'application/json;charset=UTF-8'}
    result = s.post('http://uims.jlu.edu.cn/ntms/service/res.do', search, headers=headers_foo)
    dic_foo = json.loads(result.text)

    for i in dic_foo['value']:
        ItemId.append(i['evalItemId'])

    for item in ItemId:
        fuck = s.get('http://uims.jlu.edu.cn/ntms/page/eval/eval_detail_100.html?eitem=' + item)
        headers = {'Content-Type':'application/json'}
        dic = {"evalItemId":item, "answers":answers}
        data = json.dumps(dic)
        print data
        
        fuck_p = s.post('http://uims.jlu.edu.cn/ntms/eduEvaluate/eval-with-answer.do', data, headers = headers)
        print fuck_p.text

if __name__ == '__main__':
login(name, makeTransferPwd(name, pwdPlain))
