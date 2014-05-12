#coding: utf-8
from django.template.loader import *
from django.template import *
from django.http import *

from django.views.decorators.csrf import csrf_exempt

import json
from datetime import *


from tinylog.models import *
from tinylog.util import *
    
def get_mngsetting_block():
    settings = get_settings()
    
    setting = settings['setting']
    
    d = {}        
    d['setting'] = setting
    modules = Module.objects.all().order_by('id')
        
    l = len(modules)
    
    lst = []
    if l > 0:
        lst_tmp = []
        for i in range(l):
            module = modules[i]
            lst_tmp.append(module)
            if (i + 1) % 3 == 0:
                lst.append(lst_tmp)
                lst_tmp = []
        if len(lst_tmp) > 0:
            lst.append(lst_tmp)
    d['modules'] = lst
    
    t = get_template('mngsetting.html')
    c = Context(d)
    h = t.render(c)

    return h
    
def get_mngsetting_extral_block():    
    h = get_confirm_dialog()
    
    return h
    
#management admin required
@csrf_exempt 
def update_setting(req):
    r = try_redirect(req)
    if r != None:
        return r
    try:
        jobj = json.loads(req.body)
        setting = Settings.objects.get(id=jobj['id'])
        setting.title = jobj['title']
        setting.brand = jobj['brand']
        setting.copy_info = jobj['copy']
        setting.blog_display_count = jobj['display_count']
        setting.blog_notify = jobj['notify']
        setting.blog_overview = jobj['overview']
        setting.game_menu_count = jobj['game_count']
        setting.update_time = datetime.datetime.today()
        setting.save()
        
        for m in jobj['module']:
            module = Module.objects.get(id=m['id'])
            module.visiable = m['visiable']
            module.save()
        get_settings(True)
    except Exception, e:
        print e
        return HttpResponse('FAIL')

    return HttpResponse('SUCCESS')