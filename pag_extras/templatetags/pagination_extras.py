from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from pag_extras.paragraph_parser import html_block_tag_list, line_list, dbl_line_list

P_PER_PAGE = getattr(settings, 'PAGINATION_P_PER_PAGE', 20)
ORPHANS = getattr(settings, 'PAGINATION_P_ORPHANS', 4)

register = template.Library()

parsers = {
    'html': html_block_tag_list,
    'line': line_list,
    'dline': dbl_line_list,
}

def do_get_paragraphs(parser, token):
    """
    Splits the arguments to the paragraph_paginate tag and formats them correctly
    The second part of the name of the tag, indicates the paragraph parsing type:
    
    * html
    * line
    * dline (double line)
    
    The results of this can be passed to the ``autopaginate`` tag for pagination
    
    {% get_[html|line|dline]_paragraphs story as paragraphs %}
    
    Convert the paragraphs of ``story`` for the into ``paragraphs``
    """
    bits = token.split_contents()
    parser_type = bits[0].split("_")[1]
    if len(bits) != 4:
        raise template.TemplateSyntaxError("The %(tag)s tag should be in the " + \
            "format {%% %(tag)s <content_var> as <context_var> " +\
            "%%}" % {'tag':bits[0]})
    
    content_var = bits[1]
    context_var = bits[3]
    
    return GetParagraphsNode(parser_type, content_var, context_var)
    

class GetParagraphsNode(template.Node):
    """
    Converts text into a list of block tags for use in pagination
    """
    def __init__(self, parser_type, content_var, context_var):
        self.parser_type = parser_type
        self.content_var = template.Variable(content_var)
        self.context_var = template.Variable(context_var)
    
    def render(self, context):
        paragraphs = parsers[self.parser_type](self.content_var.resolve(context))
        try:
            context_var = self.context_var.resolve(context)
        except template.VariableDoesNotExist:
            context_var = self.context_var.var
        context[context_var] = [mark_safe(item) for item in paragraphs]
        return u''


register.tag('get_html_paragraphs', do_get_paragraphs)
register.tag('get_line_paragraphs', do_get_paragraphs)
register.tag('get_dline_paragraphs', do_get_paragraphs)