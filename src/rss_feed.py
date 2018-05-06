#!/usr/bin/python

import feedparser
import time
from bs4 import BeautifulSoup


class RSSFeed(object):
    def __init__(self, name, url):
        self.feed_name = name
        self.title = None
        self.url = url
        self.homepage_url = None
        self.description = None
        self._posts = self._get_feed_data()  # TODO: refresh once in awhile

    @staticmethod
    def _get_current_time():
        return time.strftime('%a, %b %d %I:%M %p')

    def _get_feed_data(self):
        f = feedparser.parse(self.url)
        self.title = f.feed.title
        self.homepage_url = f.feed.link
        self.description = f.feed.description

        posts = []

        for post in f.entries:
            soup = BeautifulSoup(post.description, 'html.parser')
            pretty_description = soup.get_text()
            posts.append(Post(post.id, post.title, post.author, post.tags, post.updated, pretty_description, post.link))

        return posts

    def print_feed(self):
        print(self.title + '\n')
        print(self.description + '\n')
        for post_count, post in enumerate(self._posts):
            print(post)
            time.sleep(1)


class Post(object):
    def __init__(self, post_id, title, author, tags, updated, description, link):
        self.id = post_id
        self.title = title
        self.author = author
        self.tags = tags
        self.last_updated = updated
        self.description = description
        self.link = link

    def __str__(self):
        return '\n%s - %s  %s \n -----------------------------------------\n %s \n %s \n %s \n' \
               % (self.title, self.author, self.last_updated, self.link, self.description, self.get_tags())

    def get_tags(self):
        tag_str = ''
        for tag in self.tags:
            tag_str += '#%s ' % tag.get('term')
        return tag_str


if __name__ == "__main__":
    _title = 'test'
    _url = 'https://www.reddit.com/r/python/.rss'
    rss = RSSFeed(_title, _url)

    start_time = time.time()
    timeout_sec = 60

    while time.time() < start_time + timeout_sec:
        rss.print_feed()


