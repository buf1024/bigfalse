#coding: utf-8
from django.template.loader import *
from django.template import *
from django.http import *
from django.db.models import *

from tinylog.models import *

from time import time
import tinytrue


# 10分钟
_g_read_interval = 10 * 60
_g_last_time = 0

_g_settings = {}

       
def get_settings(is_force = False):
    
    global _g_last_time
    global _g_read_interval
    
    now = int(time())
    diff = now - _g_last_time
    if len(_g_settings) <= 0 or diff >= _g_read_interval or is_force:
        _g_last_time = now
        
        settings = Settings.objects.all()
        if len(settings) > 0:
            setting = settings[0]
            modules = Module.objects.filter(visiable=True)
            games = Game.objects.filter(visiable=True)[:setting.game_menu_count]
            passages = Passage.objects.order_by('-front_flag', '-update_time')[:setting.blog_display_count]
            pcatalogs = Catalog.objects.filter(type=1).order_by('-update_time')
            gcatalogs = Catalog.objects.filter(type=2).order_by('-update_time')
            labels = Label.objects.all()

            _g_settings['setting'] = setting
            _g_settings['modules'] = modules
            _g_settings['games'] = games
            _g_settings['passages'] = passages
            _g_settings['pcatalogs'] = pcatalogs
            _g_settings['gcatalogs'] = gcatalogs
            _g_settings['labels'] = labels
            
            _g_settings['stdjss'] = ['/js/jquery-2.0.0.min.js', '/js/bootstrap.min.js', '/js/bigfalse.js']
            _g_settings['stdcss'] = ['/css/bootstrap.min.css', '/css/bootstrap-theme.min.css', '/css/bigfalse.css']

    return _g_settings

def get_header_block(webtitle, extjs = None, extcss = None):
    settings = get_settings()
            
    d = {}    
    d['webtitle'] = webtitle    
    d['mstdjss'] = settings['stdjss']
    d['mstdcss'] = settings['stdcss']    
    d['mextjs'] = extjs
    d['mextcss'] = extcss       
    
    t = get_template('header.html')
    c = Context(d)
    h = t.render(c)
    
    return h
    
def get_home_extral_block():
    settings = get_settings()
    setting = settings['setting']
    
    games = settings['games']   
    h = ''
    
    if len(games) <= 0:    
        d = {}
        d['dialog_id'] = 'nogame_dialog'
        d['dialog_title'] = r'游戏'
        d['dialog_body'] = r'<h2>SORRY，由于懒惰，游戏列表为空……</h2>'
        d['dialog_buttongs'] = False

        t = get_template('dialog.html')
        c = Context(d)
        h = t.render(c)

    return h
   
def get_nav_block(req):
    settings = get_settings()
    setting = settings['setting']
    
    games = settings['games']
    
    d = {}
    
    d['brand'] = setting.brand
    d['games'] = games
    d['admin'] = is_admin(req)

    t = get_template('nav.html')
    c = Context(d)
    h = t.render(c)

    return h

def get_passage_block():
    settings = get_settings()
    setting = settings['setting']
    
    passages = Passage.objects.filter(visiable=True, draft_flag=False).order_by('-front_flag', '-update_time')[:setting.blog_display_count]


    h = ''
    t = get_template('passage.html')
    if len(passages) > 0:
        for p in passages:
            d = {}
            d['has_passage'] = True
            d['passage_id'] = p.id
            d['passage_title'] = p.title
            d['passage_create_time'] = p.create_time
            d['passage_update_time'] = p.update_time
            content = p.content
            if setting.blog_overview:
                content = p.summary
            d['passage_content'] = content
            

            count = p.comment_set.count()
            
            d['passage_comment_count'] = count
            d['passage_catolog'] = p.catalog
                    
        
            labels = p.labels.all()
            d['passage_label_list'] = labels
            
            c = Context(d)        
            h = h + t.render(c) + '\n'
    else:
        d = {}
        d['has_passage'] = False
        c = Context(d)        
        h = h + t.render(c) + '\n'
        
    return h
    
def get_leave_comment(req, title, id, exstyle, rid):
    d = {}
    d['comment_title'] = title
    d['comment_id'] = id
    d['exstyle'] = exstyle
    d['relate_id'] = rid
    d['is_admin'] = is_admin(req)
    t = get_template('leavecomment.html')
    c = Context(d)        
    h = t.render(c)
    
    return h
  
def get_child_comments(c):
    cc = []
    comments = c.comment_set.all().order_by('create_time')
    for comment in comments:
        cc.append(comment)
        scc = get_child_comments(comment)
        if len(scc) > 0:
            cc = cc + scc
    return cc

def get_view_passage_block(req, ctx):
    h = ''
    d = {}
    try:
        p = Passage.objects.get(id = ctx)
        d['has_passage'] = True
        d['passage_id'] = p.id
        d['passage_title'] = p.title
        d['passage_content'] = p.content
        d['passage_create_time'] = p.create_time
        d['passage_update_time'] = p.update_time
        
        cc = []
        comments = p.comment_set.all().order_by('create_time')
        count = p.comment_set.count()
        for comment in comments:
            if comment.parent != None:
                continue
            di = {}
            di['id'] = comment.id
            di['image'] = comment.image
            site = comment.site
            if site == None:
                site = ''
            if len(site) > 0 and not site.startswith('http'):
                site = 'http://' + site
            di['site'] = site
            di['author'] = comment.author
            di['create_time'] = comment.create_time
            di['content'] = comment.content
            di['leavecomment'] = get_leave_comment(req, None, comment.id, 'display-none', comment.id)
            scomments = get_child_comments(comment)
            ccs = []
            for c in scomments:
                sd = {}
                sd['id'] = c.id
                sd['image'] = c.image
                site = c.site
                if site == None:
                    site = ''
                if len(site) > 0 and not site.startswith('http'):
                    site = 'http://' + site
                sd['site'] = site
                sd['author'] = c.author
                sd['create_time'] = c.create_time
                sd['content'] = c.content
                sd['replyto'] = c.parent.author
                sd['leavecomment'] = get_leave_comment(req, None, c.id, 'display-none', c.id)
                ccs.append(sd)
            di['comment_set'] = ccs
            
            cc.append(di)
        d['passage_comment_count'] = count
        d['passage_catolog'] = p.catalog
                
        labels = p.labels.all()
        d['passage_label_list'] = labels
        
        
        t = get_template('passage.html')
        c = Context(d)        
        h = t.render(c)
        
        
        d = {}
        d['comments'] = cc
        d['enable_comment'] = p.enable_comment
        d['leavecomment'] = get_leave_comment(req, u'THANKS FOR COMMENT', 'z', '', p.id)
        pre  = Passage.objects.filter(id = (int(ctx) - 1))
        nxt = Passage.objects.filter(id = (int(ctx) + 1))
        if pre != None and len(pre) > 0:
            d['pre_passage'] = pre[0]
            d['has_passage'] = True
        if nxt != None and len(nxt) > 0:
            d['nxt_passage'] = nxt[0]
            d['has_passage'] = True
        
            
        h = h + '\n'
        t = get_template('comment.html')
        c = Context(d)        
        h = h + t.render(c)
        
        p.hot = p.hot + 1
        p.save()
        
    except Exception, e:
        print e
        t = get_template('404.html')
        c = Context(d)
        h = t.render(c)       
        
    return h
    
def get_passage_count_block():
    d = {}
    d['data_role'] = 'passage'
    d['data_page'] = 1
    
    count = Passage.objects.filter(visiable=True, draft_flag=False).count();
    
    settings = get_settings()
    setting = settings['setting']
    setting.blog_display_count
    
    pages = count / setting.blog_display_count
    if count % setting.blog_display_count != 0:
        pages = pages + 1

    d['page_total'] = pages
    
    t = get_template('pagecount.html')
    c = Context(d)
    h = t.render(c)

    return h
  
def get_comment_count_block():
    
    d = {}
    d['data_role'] = 'comment'
    d['data_page'] = 1
    
    count = Comment.objects.count()
    
    pages = count / tinytrue.settings.MORE_DISPLAY_COUNT
    if count % tinytrue.settings.MORE_DISPLAY_COUNT != 0:
        pages = pages + 1
    print pages
    d['page_total'] = pages
    
    t = get_template('pagecount.html')
    c = Context(d)
    h = t.render(c)

    return h
    
def get_hot_count_block():
    d = {}
    d['data_role'] = 'hot'
    d['data_page'] = 1
    
    count = Passage.objects.filter(visiable=True, draft_flag=False).count()
    
    pages = count / tinytrue.settings.MORE_DISPLAY_COUNT
    if count % tinytrue.settings.MORE_DISPLAY_COUNT != 0:
        pages = pages + 1

    d['page_total'] = pages
    
    t = get_template('pagecount.html')
    c = Context(d)
    h = t.render(c)

    return h

def get_commenthot_count_block():
    d = {}
    d['data_role'] = 'commenthot'
    d['data_page'] = 1
    
    count = Passage.objects.filter(visiable=True, draft_flag=False).count()
    
    pages = count / tinytrue.settings.MORE_DISPLAY_COUNT
    if count % tinytrue.settings.MORE_DISPLAY_COUNT != 0:
        pages = pages + 1

    d['page_total'] = pages
    
    t = get_template('pagecount.html')
    c = Context(d)
    h = t.render(c)

    return h    
def get_comment(t, m):
    comments = Comment.objects.all().order_by('-create_time')[:m.display_count]

    d = {}
    d['module'] = m
    cl = []
    for c in comments:
        if c.passage.visiable == False:
            continue
        di = {}
        di['link']  = '/passage/' + str(c.passage.id)
        di['title']  = ''
        c = c.content
        if len(c) > 15:
            c = c[:15] + ' ...... '
        di['content'] = c
        cl.append(di)
    if len(comments) == m.display_count:        
        d['module_more_link'] = '/comment/more' 
        
    d['module_list'] = cl
    d['nocontent'] = u'暂无评论'

    c = Context(d)
    h = t.render(c)
    
    return h
    
def get_hot(t, m):
    passages = Passage.objects.filter(visiable=True).order_by('-hot')[:m.display_count]
     
    d = {}
    d['module'] = m
    pl = []
    for p in passages:
        di = {}
        di['link']  = '/passage/' + str(p.id)
        di['title']  = ''
        di['content'] = p.title + '(' + str(p.hot) + ')'        
        pl.append(di)
    
    if len(passages) == m.display_count:        
        d['module_more_link'] = '/hot/more' 
    
    d['module_list'] = pl
    d['nocontent'] = u'暂无文章'

    c = Context(d)
    h = t.render(c)
    
    return h
    
def get_comment_hot(t, m):
    passages = Passage.objects.filter(visiable=True).annotate(num_comments=Count('comment')).order_by('-num_comments')[:m.display_count]
    
    d = {}
    d['module'] = m
    pl = []
    for p in passages:
        di = {}
        di['link']  = '/passage/' + str(p.id)
        di['title']  = ''
        c = p.comment_set.count()
        di['content'] = p.title + '(' + str(c) + ')'        
        pl.append(di)
    if len(passages) == m.display_count:        
        d['module_more_link'] = '/commenthot/more' 
    d['module_list'] = pl
    d['nocontent'] = u'暂无热评文章'

    c = Context(d)
    h = t.render(c)
    
    return h
def get_catalog(t, m):
    catalogs = Catalog.objects.filter(type='1')[:m.display_count]
    
    d = {}
    d['module'] = m
    cl = []
    for c in catalogs:
        di = {}
        di['link']  = '/cat/' + str(c.id)        
        di['content'] = c.name+'(' + str(c.passage_set.count()) + ')'
        di['title']  = c.desc
        cl.append(di)
    if len(catalogs) == m.display_count:        
        d['module_more_link'] = '/cat/more' 
    d['module_list'] = cl
    d['nocontent'] = u'暂无分类'

    c = Context(d)
    h = t.render(c)
    
    return h 
def get_tag(t, m):
    lables = Label.objects.all()[:m.display_count]
    
    d = {}
    d['module'] = m
    ll = []
    for l in lables:
        di = {}
        di['link']  = '/label/' + str(l.id)
        di['content'] = l.name + '(' + str(l.passage_set.count()) + ')'
        di['title']  = l.desc   
        ll.append(di)
    if len(lables) == m.display_count:        
        d['module_more_link'] = '/label/more' 
    d['module_list'] = ll
    d['nocontent'] = u'暂无标签'

    c = Context(d)
    h = t.render(c)
    
    return h     
def get_archive(t, m):
    archives = Archive.objects.all().order_by('-year').order_by('-month')[:m.display_count]
    
    d = {}
    d['module'] = m 
    al = []
    for a in archives:
        count = a.passage_set.count()
        if count <= 0:
            continue
        di = {}
        di['link']  = '/ar/' + a.year + a.month        
        di['title']  = ''  
        di['content'] = a.year + a.month + '(' + str(count) + ')'  
        al.append(di)
    if len(archives) == m.display_count:        
        d['module_more_link'] = '/ar/more' 
    d['module_list'] = al
    d['nocontent'] = u'暂无归档'

    c = Context(d)
    h = t.render(c)
    
    return h  

def get_module_map():
    d = {}
    
    d[1] = get_comment
    d[2] = get_hot
    d[3] = get_comment_hot
    d[4] = get_catalog
    d[5] = get_tag
    d[6] = get_archive
    
    return d

def get_bulletins_block():
    settings = get_settings()
    setting = settings['setting']
    
    modules = settings['modules']
    
    m = get_module_map()
    h = ''    
    t = get_template('module.html')
    for module in modules:
        if m.has_key(module.id):
            h = h + m[module.id](t, module)

    return h

def get_footer_block():
    settings = get_settings()

    setting = settings['setting']
    
    d = {}
    d['copy_info'] = setting.copy_info

    t = get_template('footer.html')
    c = Context(d)
    h = t.render(c)

    return h

def get_confirm_dialog():
    
    d = {}
    d['dialog_id'] = 'dialog_confirm'
    d['dialog_title_id'] = 'dialog_confirm_title'
    d['dialog_body_id'] = 'dialog_confirm_body'
    
    d['dialog_title'] = u'确认'
    d['dialog_body'] = u'<h2>操作不可逆，是否确定？</h2>'
    
    btn_no = {}
    btn_no['id'] = 'dialog_confirm_no'
    btn_no['title'] = u'取消'
    
    btn_yes = {}
    btn_yes['id'] = 'dialog_confirm_yes'
    btn_yes['title'] = u'确定'
    
    d['btns'] = [btn_no, btn_yes]

    t = get_template('dialog.html')
    c = Context(d)
    h = t.render(c)

    return h
    
def is_admin(req):
    return req.user.is_authenticated()
    
def try_redirect(req = None):
    if is_admin(req) == False:
        return HttpResponseRedirect('/manage/admin')
            
    return None
    

    