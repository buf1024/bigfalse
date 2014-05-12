# coding: utf-8
# Create your views here.

import tinytrue.settings

if tinytrue.settings.DEBUG:
	from django.template.loader import get_template
	from django.template import Context
	from django.http import HttpResponse

	def test_view_header(req):
		t = get_template('header.html')
		g = {'link':'abc', 'title':'2048'}
		d = {
		'brand' : 'BIGFALSE',
		'game_list' : [g],
		'admin' : True
		}
		html = t.render(Context(d))
		return HttpResponse(html)

	def test_view_footer(req):
		t = get_template('footer.html')
		d = {
		'copy_info' : 'Copyright &copy; buf1024@gmail.com, Power by',
		}
		html = t.render(Context(d))
		return HttpResponse(html)

	def test_view_passage(req):
		t = get_template('passage.html')
		p = {
		'link' : '123',
		'title' : '在',
		'content' : '''为了解决问题，我花时间去研究了一下 Python 的字符编码处理。网上也有不少文章讲 Python 的字符编码，但是我看过一遍，觉得自己可以讲得更明白些。
 
下面先复述一下 Python 字符串的基础，熟悉此内容的可以跳过。
 
对应 C/C++ 的 char 和 wchar_t, Python 也有两种字符串类型，str 与 unicode：''',
        'link_comment': 'abc',
        'comment_count': 200,
        'label_list' : [{'link': 'adf/adf', 'name':'c++'}, {'link': 'adf/adf', 'name':'单元测试'}]
		}
		d = {'passage' : p}
		html = t.render(Context(d))
		return HttpResponse(html)

	def test_view_pagecount(req):
		t = get_template('pagecount.html')
		pc = {
		'laquo' : True,
		'count_list': [{'class':'active', 'link':'tmp', 'num':1}, {'class':'', 'link':'tmp', 'num':2}],
		'raquo' : True
		}
		d = {
		'page_count' : pc,
		}
		html = t.render(Context(d))
		return HttpResponse(html)

	def test_view_gameitem(req):
		t = get_template('gameitem.html')
		g = {
		'src' : 'http://www.baidu.com',
		'width': '800',
		'height' : '600'
		}
		d = {
		'game' : g,
		}
		html = t.render(Context(d))
		return HttpResponse(html)