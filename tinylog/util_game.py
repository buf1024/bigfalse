#coding: utf-8
from django.template.loader import *
from django.template import *
from django.http import *

from django.views.decorators.csrf import csrf_exempt

import json
from datetime import *

from tinylog.models import *
from tinylog.util import *

import tinytrue

def get_mnggame_block():
    
    games = Game.objects.all()
       
    d = {}
    d['games'] = games
    t = get_template('mnggame.html')
    c = Context(d)
    h = t.render(c)

    return h
    
def get_game_form(): 
    settings = get_settings()
    gcat = settings['gcatalogs']
    
    d = {}
    d['catologs'] = gcat
    
    t = get_template('gameform.html')
    c = Context(d)
    h = t.render(c)
    
    return h
   
def get_mnggame_extral_block():
    
    cnt = get_game_form()
    
    d = {}
    d['dialog_body'] = cnt
    d['dialog_id'] = 'dialog_game'
    d['dialog_title_id'] = 'dialog_game_title'
    d['dialog_body_id'] = 'dialog_game_body'
    
    btn = {}
    btn['id'] = 'dialog_game_save'
    btn['title'] = u'保存'
    
    d['btns'] = [btn]
       
    t = get_template('dialog.html')
    c = Context(d)
    h = t.render(c)
    
    confirm = get_confirm_dialog()
    
    h = h + confirm
    
    return h 
def get_play_game_block(ctx):
    h = ''
    d = {}
    try:
        game = Game.objects.get(id = ctx)
        d['game_src'] = '/game/' + game.name + '/index.html'
        d['game_width'] = game.width
        d['game_height'] = game.height
        
        t = get_template('game.html')
        c = Context(d)        
        h = t.render(c)
        
        game.hot = game.hot + 1
        game.save()
        
    except Exception, e:
        print e
        t = get_template('404.html')
        c = Context(d)
        h = t.render(c)       
        
    return h

def get_play_game_more_count_block():
    d = {}
    d['data_role'] = 'playgame'
    d['data_page'] = 1
    
    count = Game.objects.filter(visiable=True).count()
    
    pages = count / tinytrue.settings.MORE_DISPLAY_COUNT
    
    if count % tinytrue.settings.MORE_DISPLAY_COUNT != 0:
        pages = pages + 1

    d['page_total'] = pages
    
    t = get_template('pagecount.html')
    c = Context(d)
    h = t.render(c)

    return h    
 
def get_play_game_more_block():
    h = ''
    try:
        games = Game.objects.filter(visiable=True)[:tinytrue.settings.MORE_DISPLAY_COUNT]
        
        t = get_template('gameitem.html')
        idx = 0
        for game in games:
            d = {}
            d['game_image'] = game.image
            d['game_src'] = '/playgame/' + str(game.id)
            d['game_name'] = game.name
            d['game_hot'] = game.hot
            d['game_desc'] = game.desc
            
            c = Context(d)        
            g = t.render(c)
            
            if idx != 0:
                g = '<hr>' + g
            idx = idx + 1
            
            h = h + g
    except Exception, e:
        print e
        t = get_template('404.html')
        c = Context(d)
        h = t.render(c)       
        
    return h
    
@csrf_exempt
def fetch_page_game(req, ctx):
    if req.method != 'POST':
        return HttpResponseRedirect('/')
    
    data = ''
    page = ''
    try:        
        page = int(ctx)
        
        start = tinytrue.settings.MORE_DISPLAY_COUNT * (page - 1)
        end = start + tinytrue.settings.MORE_DISPLAY_COUNT
        
        games = Game.objects.filter(visiable=True)[start:end]
        
        h = ''
        t = get_template('gameitem.html')
        for game in games:
            d = {}
            d['game_image'] = game.image
            d['game_src'] = '/playgame/' + str(game.id)
            d['game_name'] = game.name
            d['game_hot'] = game.hot
            
            c = Context(d)        
            g = t.render(c)
            
            g = '<hr>' + g
            
            h = h + g
        if h == '':
            return HttpResponse('FAIL')
        
        page = ctx
        data = h
    except Exception, e:
        print e
        return HttpResponse('FAIL')
    return HttpResponse(page + '|' + data)

#management admin required   
def req_game(req, ctx):
    r = try_redirect(req)        
    if r != None:
        return r
    obj = Game.objects.get(id=ctx)
    d = {}
    if obj != None:
        d['id'] = obj.id
        d['name'] = obj.name
        d['desc'] = obj.desc
        d['image'] = obj.image
        d['width'] = obj.width
        d['height'] = obj.height
        d['visiable'] = obj.visiable
        
        dcat = {}
        dcat['id'] = obj.catalog.id
        dcat['name'] = obj.catalog.name
        dcat['desc'] = obj.catalog.desc
        
        d['catalog'] = dcat
        
    h = json.dumps(d)
    return HttpResponse(h)
 
@csrf_exempt    
def new_game(req):
    r = try_redirect(req)
    if r != None:
        return r
    try:
        jobj = json.loads(req.body)  
        cat = Catalog.objects.get(id=jobj['catalog']['id'])        
        t = datetime.datetime.today()    
        game = Game(name=jobj['title'], desc=jobj['desc'],
                image=jobj['image'], width=jobj['width'], height=jobj['height'],
                visiable=jobj['visiable'], hot=0,
                create_time=t, update_time=t,
                catalog = cat)
        game.save()
        get_settings(True)
    except Exception, e:
        print e
        return HttpResponse('FAIL')

    return HttpResponse('SUCCESS')
  
@csrf_exempt    
def update_game(req):
    r = try_redirect(req)
    if r != None:
        return r
    try:
        jobj = json.loads(req.body)
        
        t = datetime.datetime.today()        
        game = Game.objects.get(id=jobj['id'])
        game.name = jobj['title']
        game.desc = jobj['desc']
        game.image = jobj['image']
        game.width = int(jobj['width'])
        game.height = int(jobj['height'])
        game.visiable = jobj['visiable']
        cat = Catalog.objects.get(id=jobj['catalog']['id'])
        game.catalog = cat
        game.update_time = t
        game.save()
        get_settings(True)
    except Exception, e:
        print e
        return HttpResponse('FAIL')

    return HttpResponse('SUCCESS')
    
@csrf_exempt 
def del_game(req):
    r = try_redirect(req)
    if r != None:
        return r
    try:
        jobj = json.loads(req.body)
        game = Game.objects.get(id=jobj['id'])
        game.delete()
        get_settings(True)
    except:
        return HttpResponse('FAIL')

    return HttpResponse('SUCCESS')
