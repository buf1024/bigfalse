#coding: utf-8
from django.template.loader import *
from django.template import *
from django.http import *
from django.views.decorators.csrf import csrf_exempt

import json
from datetime import *

from tinylog.models import *
from tinylog.util import *

def get_mngpassword_block():    
    d = {}    
    t = get_template('mngpassword.html')
    c = Context(d)
    h = t.render(c)

    return h
    
    
#admin required
@csrf_exempt
def update_password(req):
    r = try_redirect(req)
    if r != None:
        return r
    try:
        jobj = json.loads(req.body)
        old = jobj['source']
        new = jobj['newpass']
        user = req.user
        if user.check_password(old):
            user.set_password(new)
            user.save()
        else:
            return HttpResponse('FAIL|密码不正确')
    except Exception, e:
        print e
        return HttpResponse('FAIL|更新密码异常')
    return HttpResponse('SUCCESS')
    