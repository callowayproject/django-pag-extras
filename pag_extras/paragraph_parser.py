from django.core.paginator import Paginator

from BeautifulSoup import BeautifulSoup, Tag

def html_block_tag_list(html_text):
    """
    Convert HTML-formatted text into a list of block tags.
    
    Does not handle a fully-formed HTML document
    """
    text = "<html><head></head><body>" + html_text + "</body></html>"
    soup = BeautifulSoup(text)
    return [i for i in soup.body.childGenerator() if isinstance(i, Tag)]


def line_list(text):
    """
    Split the text into a list of content.  Multiple carriage returns or linebreaks
    count as 1 separator
    """
    import re
    return re.split('[\n\r]+', text)

def dbl_line_list(text):
    """
    Split the text into a list of content. Two LFs or CRs or two LFCRs are 
    considered a paragraph break. All other line breaks are left as is.
    """
    import re
    return re.split('\n{2}|\r{2}|\n\r\n\r', text)
    

class HTMLTagPaginator(Paginator):
    """
    A paginator that takes HTML-formatted text, and returns a paginator of paragraphs
    and other block tags.
    """
    
    def __init__(self, text, per_page, orphans=0, allow_empty_first_page=True):
        """
        Instead of an ``object_list`` this object takes an HTML-formatted string
        """
        self.object_list = html_block_tag_list(text)
        self.per_page = per_page
        self.orphans = orphans
        self.allow_empty_first_page = allow_empty_first_page
        self._num_pages = self._count = None


class LinePaginator(Paginator):
    """
    A paginator that takes text, and returns a paginator of paragraphs.
    """
    
    def __init__(self, text, per_page, orphans=0, allow_empty_first_page=True):
        """
        Instead of an ``object_list`` this object takes an HTML-formatted string
        """
        self.object_list = line_list(text)
        self.per_page = per_page
        self.orphans = orphans
        self.allow_empty_first_page = allow_empty_first_page
        self._num_pages = self._count = None


class DoubleLinePaginator(Paginator):
    """
    A paginator that takes text with 2 line breaks signifying a paragraph break, 
    and returns a paginator of paragraphs.
    """
    
    def __init__(self, text, per_page, orphans=0, allow_empty_first_page=True):
        """
        Instead of an ``object_list`` this object takes an HTML-formatted string
        """
        self.object_list = html_block_tag_list(text)
        self.per_page = per_page
        self.orphans = orphans
        self.allow_empty_first_page = allow_empty_first_page
        self._num_pages = self._count = None

