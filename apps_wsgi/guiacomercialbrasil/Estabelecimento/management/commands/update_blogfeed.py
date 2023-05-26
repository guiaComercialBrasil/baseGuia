from bs4 import BeautifulSoup as bs
import requests
from django.template.loader import render_to_string
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime

class Command(BaseCommand):
    help = 'Atualiza a lista de "Posts Recentes" do Blog'

    def add_arguments(self, parser):
        parser.add_argument('num_posts', type=int)
    
        parser.add_argument(
            '--URL',
            action='store',
            help='Optional URL for the Blog RSS Feed. Defaults to: https://blog.guiacomercialbrasil.com.br/feed/',
            default = "https://blog.guiacomercialbrasil.com.br/feed/"
        )

    def handle(self, num_posts, *args, **options):

        rss = requests.get(options["URL"])
        soup = bs(rss.text, "xml")
        feed = []
        limit = num_posts

        def get_description(description_node):

            rnode = bs(description_node.text, "lxml")
            try:
                inode = rnode.find("img")
                inode.extract()
            except:
                pass

            return rnode.text.strip()

        for node in soup.find_all("item"):
            if len(feed) >= limit:
                break

            feed.append({
                "title" : node.find("title").text,
                "thumbnail": node.find("media").decode_contents(),
                "thumbnail_sm" : node.find("thumbnail").decode_contents(), 
                "categorias": [category.text for category in node.find_all("category")],
                "description" : get_description(node.find("content:encoded")),
                "link" : node.find("link").text,
                "date" : datetime.strptime(node.find("pubDate").text, "%a, %d %b %Y %H:%M:%S +0000"),
                "creator" : node.find("dc:creator").text,
                "creator_url" : node.find("creator_url").text
            })

        html = render_to_string(template_name = "prerender_blogfeed.html", context = {"feed" : feed})

        with open("/home/agendadecartoes/apps_wsgi/guiacomercialbrasil/Estabelecimento/templates/blogfeed.html", "w") as file:
            file.write(html)

        self.stdout.write(self.style.SUCCESS('Number of Posts: %s' % num_posts))
        self.stdout.write(self.style.SUCCESS('URL: %s' % options['URL']))
        self.stdout.write(self.style.SUCCESS('feed: %s' % feed))
