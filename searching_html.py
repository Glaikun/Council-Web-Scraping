import requests
import re
from lxml import html


def from_sting_webpage_contain(html_page):
    page = requests.get(html_page)
    return html.fromstring(page.content)


def to_sting_webpage_contain(html_page):
    page = requests.get(html_page)
    return re.sub(r"[\n\t]*", "", html.tostring(html.fromstring(page.content), encoding='utf-8').decode('utf-8'))
