#coding: utf-8
from django.template.loader import *
from django.template import *
from django.http import *

from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth

import json

from tinylog.models import *
from tinylog.util import *

def get_mnglogin_block():
    d = {}
    t = get_template('login.html')
    c = Context(d)
    h = t.render(c)

    return h
    
    
@csrf_exempt    
def login(req):
    try:
        jobj = json.loads(req.body)
        
        usr = jobj['name']
        psw = jobj['password']
        user = auth.authenticate(username=usr, password=psw)
        if user is not None and user.is_active:
            auth.login(req, user)
            return HttpResponse('SUCCESS')
        else:
            return HttpResponse('FAIL|用户名或密码错误')
    except Exception, e:
        print e
        return HttpResponse('FAIL|用户名或密码错误')

    
    