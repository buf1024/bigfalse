#coding: utf-8
from django.template.loader import *
from django.template import *
from django.http import *
from django.views.decorators.csrf import csrf_exempt

import json
from datetime import *

from tinylog.models import *
from tinylog.util import *

def get_mngcatalog_block():
    
    settings = get_settings()
    pcatalogs = settings['pcatalogs']
    gcatalogs = settings['gcatalogs']
        
    l = []
    for catalog in pcatalogs:
        d = {}
        d['catalog'] = catalog
        d['passage_count'] = catalog.passage_set.count()
        l = l + [d]
    
    for catalog in gcatalogs:
        d = {}
        d['catalog'] = catalog
        d['passage_count'] = catalog.game_set.count()
        l = l + [d]
    d = {}
    d['catalogs'] = l
    
    t = get_template('mngcatalog.html')
    c = Context(d)
    h = t.render(c)

    return h
    
def get_catalog_form(id = None):
    cat = None
    if id != None:
        cat = Catalog.objects.get(id=id)
    
    d = {}
    d['catalog'] = cat
    
    t = get_template('catalogform.html')
    c = Context(d)
    h = t.render(c)
    
    return h
    
def get_mngcatalog_extral_block():
    
    cnt = get_catalog_form()
    
    d = {}
    d['dialog_body'] = cnt
    d['dialog_id'] = 'dialog_catalog'
    d['dialog_title_id'] = 'dialog_catalog_title'
    d['dialog_body_id'] = 'dialog_catalog_body'
    
    btn = {}
    btn['id'] = 'dialog_catalog_save'
    btn['title'] = u'保存'
    
    d['btns'] = [btn]
       
    t = get_template('dialog.html')
    c = Context(d)
    h = t.render(c)
    
    confirm = get_confirm_dialog()
    
    h = h + confirm
    
    return h
    
#management admin required
def req_catalog(req, ctx):
    r = try_redirect(req)
    if r != None:
        return r
        
    obj = Catalog.objects.get(id=ctx)
    d = {}
    if obj != None:
        d['id'] = obj.id
        d['name'] = obj.name
        d['desc'] = obj.desc
        d['type'] = obj.type
        
    h = json.dumps(d)
    
    return HttpResponse(h)

@csrf_exempt    
def new_catalog(req):
    r = try_redirect(req)
    if r != None:
        return r
    id = -1
    try:
        jobj = json.loads(req.body)
        
        t = datetime.datetime.today()    
        cat = Catalog(name=jobj['title'], desc=jobj['desc'],
                type=jobj['sel'], create_time=t, update_time=t)
        cat.save()
        id = cat.id
        get_settings(True)
    except Exception, e:
        print e
        return HttpResponse('FAIL')

    return HttpResponse('SUCCESS|' + str(id))

@csrf_exempt    
def update_catalog(req):
    r = try_redirect(req)
    if r != None:
        return r
    try:
        jobj = json.loads(req.body)
        t = datetime.datetime.today()    
        cat = Catalog.objects.get(id=jobj['id'])
        cat.name = jobj['title']
        cat.desc = jobj['desc']
        cat.type = jobj['sel']
        cat.update_time = t
        cat.save()
        get_settings(True)
    except:
        return HttpResponse('FAIL')

    return HttpResponse('SUCCESS')
        
@csrf_exempt 
def del_catalog(req):
    r = try_redirect(req)
    if r != None:
        return r
    try:
        jobj = json.loads(req.body)
        cat = Comment.objects.get(id=jobj['id'])
        p_count = cat.passage_set.count()
        if p_count > 0:
            return HttpResponse('FAIL')
        cat.delete()
        get_settings(True)
    except:
        return HttpResponse('FAIL')

    return HttpResponse('SUCCESS')
