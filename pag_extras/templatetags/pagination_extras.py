from django import template
from django.conf import settings

from pag_extras.paragraph_parser import HTMLTagPaginator, LinePaginator, DoubleLinePaginator

P_PER_PAGE = getattr(settings, 'PAGINATION_P_PER_PAGE', 20)
ORPHANS = getattr(settings, 'PAGINATION_P_ORPHANS', 4)

register = template.Library()

parsers = {
    'html': HTMLTagPaginator,
    'line': LinePaginator,
    'dline': DoubleLinePaginator,
}

def do_paragraph_paginate(parser, token):
    """
    Splits the arguments to the paragraph_paginate tag and formats them correctly
    The first part of the name of the tag, indicates the paragraph parsing type:
    
    * html
    * line
    * dline (double line)
    
    {% html_tag_paginate story %}
    
    Put the ``PAGINATION_P_PER_PAGE`` paragraphs of ``story`` for the 
    current page into ``object_list``
    
    {% html_tag_paginate story 10 %}
    
    Put the 10 paragraphs of the ``story`` variable for the current page into 
    ``object_list``
    
    {% html_tag_paginate story as paragraphs %}
    
    Put the ``PAGINATION_P_PER_PAGE`` paragraphs of ``story`` for the 
    current page into ``paragraphs``
    
    {% html_tag_paginate story 10 as paragraphs %}
    
    Put the 10 paragraphs of ``story`` for the current page into ``paragraphs``
    """
    bits = token.split_contents()
    parser_type = bits[0].split("_")[0]
    as_index = None
    context_var = None
    for i, bit in enumerate(bits):
        if bit == 'as':
            as_index = i
            break
    if as_index is not None:
        try:
            context_var = bits[as_index + 1]
        except IndexError:
            raise template.TemplateSyntaxError("Context variable assignment " +\
                "must take the form of {%% %r content_variable ... as " + \
                "context_var_name %%}" % bits[0])
        del bits[as_index:as_index + 2]
    else:
        context_var = 'object_list'
    
    if len(bits) == 2:
        parser[parser_type](bits[1], context_var=context_var)
    elif len(bits) == 3:
        parser[parser_type](bits[1], paginate_by=int(bits[2]), context_var=context_var)
    else:
        raise template.TemplateSyntaxError("The %(tag)s tag should be in the " + \
            "format {%% %(tag)s <content_var> [<p per pg>] [as <context_var>] " +\
            "%%}" % {'tag':bits[0]})

class HTMLTagPaginateNode(Auto):
    """
    Converts HTML-formatted text into a list of block tags
    """
register.tag('html_para_paginate', do_paragraph_paginate)
register.tag('line_para_paginate', do_paragraph_paginate)
register.tag('dline_para_paginate', do_paragraph_paginate)