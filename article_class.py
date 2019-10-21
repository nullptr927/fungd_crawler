# -*- coding: utf-8 -*-

import requests
import bs4
from bs4 import BeautifulSoup


import json
from datetime import datetime
import anytree
from anytree import Node


class Article:
    def __init__(self, item_tag: bs4.element.Tag):
        self.raw = item_tag
        self.id = item_tag.select_one('div.list-title > a').attrs['href']
        self.id = int(self.id[1:])
        self.url = 'https://tgd.kr/' + str(self.id)

        self.title = item_tag.select_one('div.list-title > a').attrs['title']

        self.reply_count = item_tag.select_one('div.list-title > small.comment-count')
        if self.reply_count is None:
            self.reply_count = 0
        else:
            self.reply_count = int(self.reply_count.text.replace('[', '').replace(']', ''))

        if item_tag.select_one('div.list-title > div.list-writer.logged > span'):
            self.is_writer_logged = True
            self.writer = item_tag.select_one('div.list-title > div.list-writer.logged > span').text.strip()
        else:
            self.is_writer_logged = False
            self.writer = item_tag.select_one('div.list-title > div.list-writer > span').text.strip()

        self.vote = item_tag.select_one('div.list-header > span')
        if self.vote is None:
            self.vote = -1
        else:
            self.vote = int(self.vote.text)

        self.date = item_tag.select_one('div.list-time').text.strip()
        if self.date[2] == ':':
            self.datetime = datetime.strptime(self.date, '%H:%M')
            td = datetime.today()
            self.datetime = self.datetime.replace(year=td.year, month=td.month, day=td.day)
        else:
            self.datetime = datetime(year=2019, month=int(self.date[0:2]), day=int(self.date[3:5]))

        self.is_visited = False
        self.is_reachable = None

        self.content = None
        self.reply_tree = Node('0')
        self.reply_deleted = Node('deleted', parent=self.reply_tree)
        self.reply_list = []

    class Reply:
        def __init__(self, reply_ele):
            # print(type(reply_ele))
            self.id = reply_ele["id"]
            self.parent_id = reply_ele["parent"]

            content_soup = BeautifulSoup(reply_ele["content"], 'html.parser')
            self.content = content_soup.get_text(' ', strip=True)\
                .replace('Video 태그를 지원하지 않는 브라우저입니다.', '[Video Tag]')
            article_time = reply_ele["updated_at"]
            self.datetime = datetime.strptime(article_time, '%Y-%m-%d  %H:%M:%S')
            self.is_writer_logged = bool(reply_ele["logged"])
            self.writer = reply_ele["nickname"]
            self.vote = reply_ele["up"]
            self.is_secret = reply_ele["secret"]

            # print(self)
        def __repr__(self):
            return \
                f'{self.id=}, {self.writer}, {self.is_writer_logged=}, {self.is_secret=}, {self.content=}'

        def __str__(self):
            return \
                f'\t{self.id}, parent: {self.parent_id}, vote: {self.vote},\t{self.datetime}\n'\
                f'\t{self.is_writer_logged}, writer: {self.writer}, secret: {self.is_secret}\n' \
                f'\tcontent: {self.content}'

    # comment-30466326 > div.reply-header > div.reply-menu > span.time

    def read_reply(self):
        decoder = json.JSONDecoder()
        for i in range((self.reply_count // 50) + 1):
            reply_raw = requests.get(f'https://tgd.kr/board/comment_load/{self.id}/{i + 1}').text
            # print(reply_raw)
            reply_list = decoder.decode(reply_raw)["data"]
            for reply_ele in reply_list:
                ele = Article.Reply(reply_ele=reply_ele)
                self.reply_list.append(ele)
                ele_parent = anytree.search.find_by_attr(self.reply_tree, ele.parent_id)
                Node(ele.id, data=ele, parent=(ele_parent if ele_parent else self.reply_deleted))
            # print(RenderTree(self.reply_tree))
        return self

    def visit_link(self):
        self.is_visited = True
        html_text = requests.get(url=self.url, allow_redirects=False).text
        if html_text == '':
            self.is_reachable = False
        else:
            self.is_reachable = True
            soup = BeautifulSoup(html_text, 'html.parser')
            self.vote = int(soup.select_one('#up').text)
            content_soup = soup.select_one('#article-content')
            article_time = soup.select_one('#article-time > span').attrs['title']
            self.datetime = datetime.strptime(article_time, '%Y-%m-%d  %H:%M:%S')
            self.content = content_soup.get_text('\n', strip=True)\
                .replace('Video 태그를 지원하지 않는 브라우저입니다.', '\n[Video]\n')
        return self

    def __str__(self):
        return \
            f'{self.url=}, {self.vote=},\t{self.reply_count=},\t{self.datetime}\n'\
            f'{self.is_writer_logged=}, {self.writer=}, {self.title=}\n'\
            f'{self.content}'

    @staticmethod
    def is_item_valid(item: bs4.element.Tag):
        href = item.select_one('div.list-title > a').attrs['href']
        header = item.select_one('div > strong')
        if href:
            if header is None:
                return True
            elif header.text == 'AD':
                return False
            else:
                return True
        else:
            return False

    @staticmethod
    def items_to_articles(items: list):
        articles = [Article(item_tag=item) for item in items if Article.is_item_valid(item)]
        return articles
