from django.test import TestCase
import os

class ParserTest(TestCase):
    """
    Tests that the parsers work as expected
    """
    def request_factory(self, **kwargs):
        from django.core.handlers.wsgi import WSGIRequest
        environ = {
            'HTTP_COOKIE': self.client.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        environ.update(self.client.defaults)
        environ.update(kwargs)
        return WSGIRequest(environ)
        
    def testHTML(self):
        html = open(os.path.abspath(os.path.join(os.path.dirname(__file__),'fixtures','test_html.html'))).read()
        from paragraph_paginator import html_block_tag_list
        tag_list = html_block_tag_list(html)
        expected = ['<p>para1</p>',
            '<p>para2</p>',
            '<ul><li>item1</li><li>item2</li></ul>',
            '<blockquote>blockquote</blockquote>',
            '<p><em>emphasized</em> and <strong>styled</strong> text should also not be counted</p>']
        for tag, exp in zip(tag_list, expected):
            self.assertEqual(str(tag), exp)
    
    def test_lines(self):
        text = open(os.path.abspath(os.path.join(os.path.dirname(__file__),'fixtures','test_lines.txt'))).read()
        from paragraph_paginator import line_list
        l_list = line_list(text)
        expected = ['para1','para2','para3','para4','para5',]
        self.assertEqual(l_list, expected)
    
    def test_dbl_lines(self):
        text = open(os.path.abspath(os.path.join(os.path.dirname(__file__),'fixtures','test_dbllines.txt'))).read()
        from paragraph_paginator import dbl_line_list
        l_list = dbl_line_list(text)
        expected = ['this is\nparagraph1','para2\n * item 1\n * item 2','para3','\npara4',]
        self.assertEqual(l_list, expected)
    
    def test_html_template_tag(self):
        from django.template import Template, Context
        html = open(os.path.abspath(os.path.join(os.path.dirname(__file__),'fixtures','test_html.html'))).read()
        
        t = Template("{% load pagination_extras %}" + \
            "{% get_html_paragraphs var as paragraphs %}" + \
            "{% for item in paragraphs %}{{item}}{% endfor %}")
        result = t.render(Context({'var': html, 'request': self.request_factory()}))
        expected = "<p>para1</p><p>para2</p><ul><li>item1</li><li>item2</li></ul><blockquote>blockquote</blockquote><p><em>emphasized</em> and <strong>styled</strong> text should also not be counted</p>"
        self.assertEqual(result, expected)
    
    def test_line_template_tag(self):
        from django.template import Template, Context
        html = open(os.path.abspath(os.path.join(os.path.dirname(__file__),'fixtures','test_lines.txt'))).read()
        
        t = Template("{% load pagination_extras %}" + \
            "{% get_line_paragraphs var as paragraphs %}" + \
            "{% for item in paragraphs %}{{item}}{% endfor %}")
        result = t.render(Context({'var': html, 'request': self.request_factory()}))
        expected = "para1para2para3para4para5"
        self.assertEqual(result, expected)
    
    def test_dblline_template_tag(self):
        from django.template import Template, Context
        html = open(os.path.abspath(os.path.join(os.path.dirname(__file__),'fixtures','test_dbllines.txt'))).read()
        
        t = Template("{% load pagination_extras %}" + \
            "{% get_line_paragraphs var as paragraphs %}" + \
            "{% for item in paragraphs %}{{item}}{% endfor %}")
        result = t.render(Context({'var': html, 'request': self.request_factory()}))
        expected = "this isparagraph1para2 * item 1 * item 2para3para4"
        self.assertEqual(result, expected)
    
    