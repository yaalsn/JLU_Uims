# -*- coding: utf-8 -*-  
import requests
from hashlib import md5
import json
from wa import get_zip_path

name = raw_input('username: ')
pwdPlain = raw_input('password: ')
answers = {"prob11":"A","prob12":"A","prob13":"D","prob14":"A","prob15":"A","prob21":"A","prob22":"A","prob23":"A","prob31":"A","prob32":"A","prob41":"A","prob42":"A","prob43":"A","prob51":"A","prob52":"A","sat6":"A","mulsel71":"EGHK","advice8":"good"}

ItemId = []

def makeTransferPwd(name, pwdPlain):
    inp = md5('UIMS' + name + pwdPlain).hexdigest()
    return inp

def login(name, inp):
    s = requests.session()
    #headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
    r = s.get('http://uims.jlu.edu.cn/ntms/userLogin.jsp')
    param = {'j_username':name, 'j_password':inp, 'mousePath':get_zip_path()}
    p = s.post('http://uims.jlu.edu.cn/ntms/j_spring_security_check', param)
    userInfo = s.post('http://uims.jlu.edu.cn/ntms/action/getCurrentUserInfo.do')
    userId = json.loads(userInfo.text)['userId']
    search = json.dumps({"tag":"teachClassStud@schedule","branch":"default","params":{"termId":126,"studId":231432}})
    headers_foo = {'Content-Type':'application/json;charset=UTF-8'}
    result = s.post('http://uims.jlu.edu.cn/ntms/service/res.do', search, headers=headers_foo)
    print result.text

if __name__ == '__main__':
    login(name, makeTransferPwd(name, pwdPlain))
