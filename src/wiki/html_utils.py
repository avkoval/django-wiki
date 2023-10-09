"""
Find unclosed HTML tags
"""

from collections import Counter
from html.parser import HTMLParser

IGNORE_TAGS = {
    'img',
    'input',
    'meta',
    'br',
    'link',
    'hr',
}


class TagsCounter(HTMLParser):
    """
    Count HTML tags
    """
    def __init__(self):
        super().__init__()
        self.tagsopen = Counter()
        self.tagsclosed = Counter()

    def handle_starttag(self, tag, attrs):  # pylint: disable=unused-argument
        """
        Count open tags
        """
        self.tagsopen[tag] += 1

    def handle_endtag(self, tag):
        """
        Count closed tags
        """
        self.tagsclosed[tag] += 1

    def reset(self):
        """
        Reset stats
        """
        super().reset()
        self.tagsopen = Counter()
        self.tagsclosed = Counter()


def find_unclosed_html_tags(html_text):
    """
    Return an array of unclosed html tags

    >>> find_unclosed_html_tags('<html>')
    ['html']
    >>> find_unclosed_html_tags('<html></html>')
    []
    >>> find_unclosed_html_tags('<html><a></html>')
    ['a']
    >>> 
    """
    unclosed_tags = []
    tags_counter = TagsCounter()
    tags_counter.feed(html_text)
    for tag in tags_counter.tagsopen:
        if tag in IGNORE_TAGS:
            continue
        if tags_counter.tagsclosed[tag] != tags_counter.tagsopen[tag]:
            unclosed_tags.append(tag)
    return unclosed_tags


if __name__ == "__main__":
    import doctest
    doctest.testmod()
