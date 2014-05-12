#coding: utf-8
from django.template.loader import *
from django.template import *
from django.http import *

from tinylog.models import *
from tinylog.util import *
from django.views.decorators.csrf import csrf_exempt

import json
import tinytrue
  
def get_mngcomment_count_block():
    d = {}
    d['data_role'] = 'manage/comment'
    d['data_page'] = 1
    
    count = Comment.objects.count()
    
    pages = count / tinytrue.settings.MORE_DISPLAY_COUNT
    
    if count % tinytrue.settings.MORE_DISPLAY_COUNT != 0:
        pages = pages + 1

    d['page_total'] = pages
    
    t = get_template('pagecount.html')
    c = Context(d)
    h = t.render(c)

    return h
  
def get_mngcomment_block():
    
    comments = Comment.objects.all()[:tinytrue.settings.MORE_DISPLAY_COUNT]
 
    d = {}        
    d['comments'] = comments
    d['page_count_block'] = get_mngcomment_count_block()
    t = get_template('mngcomment.html')
    c = Context(d)
    h = t.render(c)

    return h
 
@csrf_exempt
def fetch_page_mngcomment(req, ctx):
    if req.method != 'POST':
        return HttpResponseRedirect('/')
    
    data = ''
    page = ''
    try:
        
        page = int(ctx)
        
        start = tinytrue.settings.MORE_DISPLAY_COUNT * (page - 1)
        end = start + tinytrue.settings.MORE_DISPLAY_COUNT
        comments = Comment.objects.all().order_by('-create_time')[start:end]
        if len(comments) == '':
            return HttpResponse('FAIL')
        d = {}        
        ll = []
        for c in comments:
            di = {}
            di['id'] = c.id
            di['pre_id'] = start + 1
            start = start + 1
            di['title'] = c.passage.title
            di['content'] = c.content
            di['author'] = c.author
            di['create_time'] = c.create_time
            di['passage_id'] = c.passage.id
            ll.append(di)
        d['items'] = ll
        
        t = get_template('mngcommentmore.html')
        c = Context(d)        
        h = t.render(c)        
        
        page = ctx
        data = h
    except Exception, e:
        print e
        return HttpResponse('FAIL')
    
    return HttpResponse(page + '|' + data)
 
@csrf_exempt
def fetch_page_comment(req, ctx):
    if req.method != 'POST':
        return HttpResponseRedirect('/')
    
    data = ''
    page = ''
    try:
        
        page = int(ctx)
        
        start = tinytrue.settings.MORE_DISPLAY_COUNT * (page - 1)
        end = start + tinytrue.settings.MORE_DISPLAY_COUNT
        
        comments = Comment.objects.all().order_by('-create_time')[start:end]
        
        h = ''
        t = get_template('tablemore.html')
        d = {}
        dl = []
        for c in comments:           
            di = {}
            di['id'] = c.passage.id
            di['pre_id'] = start + 1
            start = start + 1
            di['name'] = c.passage.title
            di['desc'] = c.author
            di['passage_count'] = c.content
            di['link'] = '/passage/' + str(c.passage.id)
            dl.append(di)
        if len(dl) == 0:
            return HttpResponse('FAIL')
            
        d['items'] = dl
        c = Context(d)        
        h = t.render(c)        
        
        page = ctx
        data = h
    except Exception, e:
        print e
        return HttpResponse('FAIL')
    
    return HttpResponse(page + '|' + data)
    

@csrf_exempt
def fetch_page_commenthot(req, ctx):
    if req.method != 'POST':
        return HttpResponseRedirect('/')
    
    data = ''
    page = ''
    try:
        
        page = int(ctx)
        
        start = tinytrue.settings.MORE_DISPLAY_COUNT * (page - 1)
        end = start + tinytrue.settings.MORE_DISPLAY_COUNT
        
        passages = Passage.objects.filter(visiable=True, draft_flag=False).annotate(num_comments=Count('comment')).order_by('-num_comments')[start:end]
        
        h = ''
        t = get_template('tablemore.html')
        d = {}
        dl = []
        for p in passages:           
            di = {}
            di['id'] = p.id            
            di['pre_id'] = start + 1
            start = start + 1
            di['name'] = p.title
            di['desc'] = p.hot
            di['passage_count'] = p.comment_set.count()
            di['link'] = '/passage/' + str(p.id)
            dl.append(di)
        if len(dl) == 0:
            return HttpResponse('FAIL')
            
        d['items'] = dl
        c = Context(d)        
        h = t.render(c)        
        
        page = ctx
        data = h
    except Exception, e:
        print e
        return HttpResponse('FAIL')
    
    return HttpResponse(page + '|' + data)