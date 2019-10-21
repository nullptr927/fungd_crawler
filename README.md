# fungd_crawler
crawler of https://tgd.com/funzinnu

may not work at the other community of tgd.

# 펀게더 크롤러

~핫산발상

![hsbs](http://puu.sh/z0zZo/037402fb12.png)
---
트게더 funzinnu 게시판을 크롤링 하기 위한 목적으로 만든 파이썬 코드입니다.
다른 트게더 게시판에서 되는지는 검증되지 않았습니다.
(펀즈님이 디폴트에 비해 게시판 개조를 많이 해서 안될 것으로 추정됩니다.)
개인적으로 갖고 놀려고 만든 코드이기 때문에 코드가 조잡할 수 있습니다.
GPL 라이선스로 배포됩니다.

## 파일 설명

### article_class.py
코어 클래스 입니다. bs4.tag 형태의 <div.item> 태그를 init arg로 집어넣으면 하나의 클래스로 만들어냅니다.
자세한 내용은 직접 코드를 뜯어보시길 바랍니다.

### tchang.py
크롤링해서 아직 읽지 못한 글의 제목과 내용을 표시해줍니다. 한번 읽은 글은 다시 표시되지 않습니다.

## tchang.py 실행하기
### 필요한 패키지
* anytree
* bs4
* requests

### 본격적인 실행

아쉽지만 파이썬에 대한 기반 지식이 없다면 실행하기 힘들 것 같습니다 ㅠㅠ
제 능력이 부족한 탓이니 다른 분들이 어찌할지 방법을 찾아주십쇼

--------
### python 3.8을 바탕으로 짜여진 코드입니다. 기존에 3.7을 쓰시던 분은 3.8을 새로 설치하셔야 합니다.

### 1. 두 파일을 적당한 경로에 같이 둡니다.
![asdf1](https://i.imgur.com/ivAzbtX.png)

### 2. tchang.py의 20번 줄에 있는 dir의 경로를 작성합니다. 
![dir1](https://i.imgur.com/S8SQ5Yh.png)

### 3. bat 파일을 생성해 다음과 같이 작성합니다.
![batbat](https://i.imgur.com/LZLrvCj.png)

### 4. 실행시켜놓고 계속 띄워두시면 됩니다.
![asdf3](https://i.imgur.com/zJY90LV.png)

------
## TODO (여러분이 도와주면 좋겠지만 딱히 바라진 않는 것)

* 일반인도 쓸 수 있도록 executable file로 배포하기
* 역게더 등 다른 게시판에서도 general하게 사용할 수 있도록 만들기
* 댓글 추가된 게시글도 업데이트 목록에 뜨게 할 것 (코드를 아예 뜯어고쳐야 )
