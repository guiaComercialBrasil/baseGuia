from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup as bs
import requests


register = template.Library()

@register.simple_tag(name = "make_blogfeed")
def blogfeed(*args, **kwargs):
    rss = requests.get("https://blog.guiacomercialbrasil.com.br/feed/")
    soup = bs(rss.text, "xml")
    feed = []
    limit = 3

    def get_description(description_node):
        
        rnode = bs(description_node.text, "lxml")
        inode = rnode.find("img")
        inode.extract()

        return rnode.text.strip()

    for node in soup.find_all("item"):
        if len(feed) >= limit:
            break

        feed.append({
            "title" : node.find("title").text,
            "thumbnail": bs(node.find("description").text, "lxml").find("img"),
            "categorias": [category.text for category in node.find_all("category")],
            "description" : get_description(node.find("description")),
            "link" : node.find("link").text,
            "date" : node.find("pubDate").text,
            "autor" : node.find("dc:creator").text
        })

        print(feed)
        #html = render_to_string(template_name = "blog_feed.html", context = {"feed" : feed})
        html = "TESTE"
    return html
