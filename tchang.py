# # -*- coding: utf-8 -*-

import sys
import os.name
import requests
from bs4 import BeautifulSoup

from article_class import Article

sys.setrecursionlimit(10000)


global_title_list = []
global_article_list = []


def get_item_list(page=1):
    page_url1 = f'https://tgd.kr/funzinnu/page/{page}'
    soup1 = BeautifulSoup(requests.get(url=page_url1).text, 'html.parser')
    return soup1.select('div.item')


dir1 = ''  # 경로를 설정해 주세요

if os.name == "posix":
    dir1 = "/output/output.txt"

# 조건 : 댓글이 늘어났거나 새 글임

line_length = 80
line = '〓' * line_length  # 구분선이 너무 길다 싶으면 줄이세요
line1 = '▼' * line_length
line2 = '▲' * line_length

print(f'{line}\n목록 점검 중\n')
with open(dir1, 'r') as file1:
    num = int(file1.readline())

    article_list = \
        (lambda l: [Article(e) for e in l if Article.is_item_valid(e)])(get_item_list(1))
    article_new = \
        (lambda l: [e.visit_link() for e in l if e.id > num])(article_list)
    article_new.sort(key=(lambda e: e.id))

    print(line1)
    if article_new:
        num = article_new[-1].id
        for ele in article_new:
            expr = f'{ele.vote=},\t{ele.reply_count=}\n' \
                f'{ele.writer=}, {ele.title=}\n\n' \
                f'{ele.content}'
            print(expr)
            print(line)
    else:
        print("새로운 글이 없습니다.")

print(f"가장 최근 글 id: {num}")
print(line2)

with open(dir1, 'w') as file1:
    file1.write(str(num))
