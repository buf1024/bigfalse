# coding: utf-8
# Create your views here.
from django.template.loader import *
from django.template import *
from django.http import *
from django.views.decorators.csrf import csrf_exempt

from tinylog.models import *
from tinylog.util import *

from tinylog.util_login import *
from tinylog.util_game import *
from tinylog.util_catalog import *
from tinylog.util_label import *
from tinylog.util_comment import *
from tinylog.util_setting import *
from tinylog.util_passage import *
from tinylog.util_password import *

def home(req):
    settings = get_settings()
    setting = settings['setting']
    
    d = {}    
    d['header_block'] = get_header_block(setting.title,
                                            extjs=['/js/pagecount.js'])    
    d['extral_block'] = get_home_extral_block()    
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = get_passage_block()    
    d['passage_count_block'] = get_passage_count_block()    
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)
    
    return HttpResponse(h)
    
def admin(req):
    
    if is_admin(req) == False:
        settings = get_settings()
        setting = settings['setting']

        d = {}    
        d['header_block'] = get_header_block(setting.title + u' : 登录',
                                                extjs=['/js/login.js'])    
        d['extral_block'] = ''  
        d['nav_block'] = get_nav_block(req)
        d['content_block'] = get_mnglogin_block()    
        d['footer_block'] = get_footer_block()        

        t = get_template('general.html')
        c = Context(d)
        h = t.render(c)

        return HttpResponse(h)
    
    return HttpResponseRedirect('/manage/passage')


def cat_passage(req, ctx):
    settings = get_settings()
    setting = settings['setting']
    
    d = {}    
    d['header_block'] = get_header_block(setting.title + u' : 分类汇总',
                                             extjs = ['/js/collect.js'])    
    d['extral_block'] = get_home_extral_block()    
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = get_cat_passage_block(ctx)    
    d['passage_count_block'] = ''
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def label_passage(req, ctx):
    
    settings = get_settings()
    setting = settings['setting']
    
    d = {}    
    d['header_block'] = get_header_block(setting.title + u' : 标签汇总',
                                             extjs = ['/js/collect.js'])    
    d['extral_block'] = get_home_extral_block()    
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = get_label_passage_block(ctx)    
    d['passage_count_block'] = ''   
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
def ar_passage(req, ctx):
        
    settings = get_settings()
    setting = settings['setting']
    
    d = {}    
    d['header_block'] = get_header_block(setting.title + u' : 归档汇总',
                                             extjs = ['/js/collect.js'])    
    d['extral_block'] = get_home_extral_block()    
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = get_ar_passage_block(ctx)    
    d['passage_count_block'] = ''   
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def cat_more(req):
    settings = get_settings()
    setting = settings['setting']
    
    d = {}    
    d['header_block'] = get_header_block(setting.title + u' : 分类汇总',
                                             extjs = ['/js/collectmore.js'])    
    d['extral_block'] = get_home_extral_block()    
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = get_cat_more_block()    
    d['passage_count_block'] = ''   
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def label_more(req):
    settings = get_settings()
    setting = settings['setting']
    
    d = {}    
    d['header_block'] = get_header_block(setting.title + u' : 标签汇总',
                                             extjs = ['/js/collectmore.js'])    
    d['extral_block'] = get_home_extral_block()    
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = get_label_more_block()    
    d['passage_count_block'] = ''   
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def ar_more(req):
    settings = get_settings()
    setting = settings['setting']
    
    d = {}    
    d['header_block'] = get_header_block(setting.title + u' : 归档汇总',
                                             extjs = ['/js/collectmore.js'])    
    d['extral_block'] = get_home_extral_block()    
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = get_ar_more_block()    
    d['passage_count_block'] = ''   
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def comment_more(req):
    settings = get_settings()
    setting = settings['setting']
    
    d = {}    
    d['header_block'] = get_header_block(setting.title + u' : 评论汇总',
                                             extjs = ['/js/collectmore.js', '/js/tablemore.js'])    
    d['extral_block'] = get_home_extral_block()    
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = get_comment_more_block()    
    d['passage_count_block'] = get_comment_count_block()
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def commenthot_more(req):
    settings = get_settings()
    setting = settings['setting']
    
    d = {}    
    d['header_block'] = get_header_block(setting.title + u' : 评论汇总',
                                             extjs = ['/js/collectmore.js', '/js/tablemore.js'])    
    d['extral_block'] = get_home_extral_block()    
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = get_commenthot_more_block()    
    d['passage_count_block'] = get_commenthot_count_block()
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def hot_more(req):
    settings = get_settings()
    setting = settings['setting']
    
    d = {}    
    d['header_block'] = get_header_block(setting.title + u' : 热门汇总',
                                             extjs = ['/js/collectmore.js', '/js/tablemore.js'])    
    d['extral_block'] = get_home_extral_block()    
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = get_hot_more_block()    
    d['passage_count_block'] = get_hot_count_block()
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def view_passage(req, ctx):
    settings = get_settings()
    setting = settings['setting']
    d = {}    
    d['header_block'] = get_header_block(setting.title,
                                            extjs = ['/js/viewpassage.js'])    
    d['extral_block'] = get_home_extral_block()    
    d['nav_block'] = get_nav_block(req)   
    d['passages_block'] = get_view_passage_block(req, ctx)    
    d['passage_count_block'] = ''   
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)

def play_game(req, ctx):
    settings = get_settings()
    setting = settings['setting']

    d = {}
    d['extral_block'] = ''
    d['header_block'] = get_header_block(setting.title + u' : 游戏')    
    d['nav_block'] = get_nav_block(req)
    d['content_block'] = get_play_game_block(ctx)
    d['footer_block'] = get_footer_block()
    
    t = get_template('general.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def play_game_more(req):
    settings = get_settings()
    setting = settings['setting']

    d = {}
    d['extral_block'] = ''
    d['header_block'] = get_header_block(setting.title + u' : 更多游戏',
                                            extjs=['/js/pagecount.js'])    
    d['nav_block'] = get_nav_block(req)
    d['passages_block'] = get_play_game_more_block()
    d['passage_count_block'] = get_play_game_more_count_block()
    d['bulletins_block'] = ''
    d['footer_block'] = get_footer_block()
    
    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def search(req):
    k = req.GET.get('navq')
    
    d = {}    
    d['header_block'] = get_header_block(u'搜索')    
    d['extral_block'] = ''  
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = u'<p><h2>搜索"' + k + u'", 该功能目前还没有实现</h2></p>'   
    d['passage_count_block'] = ''   
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def error404(req):    
    d = {}    
    d['header_block'] = get_header_block(u'你访问的页面不存在')    
    d['extral_block'] = ''  
    d['nav_block'] = get_nav_block(req)    
    d['passages_block'] = u'<p><h2>你访问的页面不存在</h2></p>'   
    d['passage_count_block'] = ''   
    d['bulletins_block'] = get_bulletins_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('home.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
#management admin required  
def mngpassage(req):
    r = try_redirect(req)
    if r != None:
        return r
    
    settings = get_settings()
    setting = settings['setting']

    d = {}
    d['extral_block'] = get_mngpassage_extral_block()
    d['header_block'] = get_header_block(setting.title + u' : 文章管理',
                                              extjs = ['/js/mngpassage.js', '/js/tablemore.js'])    
    d['nav_block'] = get_nav_block(req)
    d['content_block'] = get_mngpassage_block()
    d['footer_block'] = get_footer_block()
    
    t = get_template('general.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def mngpassage_newpassage(req):
    r = try_redirect(req)
    if r != None:
        return r
        
    settings = get_settings()
    setting = settings['setting']

    d = {}
    d['extral_block'] = get_editpassage_extral_block()
    d['header_block'] = get_header_block(setting.title + u' : 新增文章',
                                              extjs = ['/tinymce/tinymce.min.js',
                                                '/js/editpassage.js'])    
    d['nav_block'] = get_nav_block(req)
    d['content_block'] = get_mngpassage_newpassage_block()
    d['footer_block'] = get_footer_block()
    
    t = get_template('general.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
def mngpassage_modifypassage(req, ctx):
    r = try_redirect(req)
    if r != None:
        return r
    
    settings = get_settings()
    setting = settings['setting']
    
    p = Passage.objects.get(id=ctx)
    
    d = {}
    d['extral_block'] = get_editpassage_extral_block()
    d['header_block'] = get_header_block(setting.title + u' : 修改文章',
                                              extjs = ['/tinymce/tinymce.min.js',
                                                '/js/editpassage.js'])    
    d['nav_block'] = get_nav_block(req)
    d['content_block'] = get_mngpassage_modifypassage_block(p)
    d['footer_block'] = get_footer_block()
    
    t = get_template('general.html')
    c = Context(d)
    h = t.render(c)        
    
    return HttpResponse(h)

def mngcomment(req):
    r = try_redirect(req)
    if r != None:
        return r
    
    settings = get_settings()
    setting = settings['setting']

    d = {}   
    d['extral_block'] = get_mngcomment_extral_block()
    d['header_block'] = get_header_block(setting.title + u' : 评论管理',
                                              extjs = ['/js/mngcomment.js', '/js/tablemore.js'])    
    d['nav_block'] = get_nav_block(req)
    d['content_block'] = get_mngcomment_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('general.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
    
def mngcatalog(req):
    r = try_redirect(req)
    if r != None:
        return r
    
    settings = get_settings()
    setting = settings['setting']

    d = {}
    d['extral_block'] = get_mngcatalog_extral_block()
    d['header_block'] = get_header_block(setting.title + u' : 分类管理',
                                              extjs = ['/js/mngcatalog.js'])
    d['nav_block'] = get_nav_block(req)
    d['content_block'] = get_mngcatalog_block()
    d['footer_block'] = get_footer_block()
        

    t = get_template('general.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def mnglabel(req):
    r = try_redirect(req)
    if r != None:
        return r
    
    settings = get_settings()
    setting = settings['setting']

    d = {}    
    d['extral_block'] = get_mnglabel_extral_block()
    d['header_block'] = get_header_block(setting.title + u' : 标签管理',
                                              extjs = ['/js/mnglabel.js'])    
    d['nav_block'] = get_nav_block(req)    
    d['content_block'] = get_mnglabel_block()    
    d['footer_block'] = get_footer_block()
        

    t = get_template('general.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def mngsetting(req):
    r = try_redirect(req)
    if r != None:
        return r
    
    settings = get_settings()
    setting = settings['setting']

    d = {}        
    d['extral_block'] = get_mngsetting_extral_block()
    d['header_block'] = get_header_block(setting.title + u' : 博客设置',
                                             extjs = ['/js/mngsetting.js'])    
    d['nav_block'] = get_nav_block(req)    
    d['content_block'] = get_mngsetting_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('general.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)

    
def mngpassword(req):
    r = try_redirect(req)
    if r != None:
        return r
    
    settings = get_settings()
    setting = settings['setting']

    d = {}        
    d['extral_block'] = get_mngsetting_extral_block()
    d['header_block'] = get_header_block(setting.title + u' : 密码设置',
                                             extjs = ['/js/mngpassword.js'])    
    d['nav_block'] = get_nav_block(req)    
    d['content_block'] = get_mngpassword_block()    
    d['footer_block'] = get_footer_block()        

    t = get_template('general.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
    
def mnggame(req):
    r = try_redirect(req)
    if r != None:
        return r
    
    settings = get_settings()
    setting = settings['setting']

    d = {}    
    d['extral_block'] = get_mnggame_extral_block()
    d['header_block'] = get_header_block(setting.title + u' : 游戏管理',
                                             extjs = ['/js/mnggame.js'])    
    d['nav_block'] = get_nav_block(req)
    d['content_block'] = get_mnggame_block()    
    d['footer_block'] = get_footer_block()
        

    t = get_template('general.html')
    c = Context(d)
    h = t.render(c)

    return HttpResponse(h)
       
def mnglogout(req):
    r = try_redirect(req)
    if r != None:
        return r
    auth.logout(req)
    return HttpResponseRedirect("/")