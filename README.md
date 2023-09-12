[첫 번째 미션](https://likelion.notion.site/a39c371947944c3596655245392dc905)

# 테스트 방법

## 서버실행
1. 깃클론 생성
   - `git clone https://github.com/likelion-backend-6th/TrackProject_1_Leegeunhan.git`
   - `cd TrackProject_1_Leegeunhan`
2. 가상환경 설치 및 접속 
    - `python -m venv venv`
    - `source ./venv/Scripts/activate`
3. 패키지 설치
    - `pip install -r requirements.txt`
4. 데이터베이스 생성
    - `python manage.py makemigrations`
    - `python manage.py migrate`
5. 슈퍼유저 생성
    - `python manage.py createsuperuser`
6. 더미데이터 추가
    - `python -Xutf8 manage.py loaddata books_data.json`
7. 서버 실행
    - `python manage.py runserver`

## 일반 유저 ( 비로그인 )
- Library - 메인화면으로 간다.
- Books List - 모든 책 목록을 볼 수 있다.
- Books List > - 카테고리별 책 목록을 볼 수 있다.
- Search - 검색어가 포함된 제목 또는 저자의 책 목록을 볼 수 있다.
- 책제목 클릭시 책의 세부항목을 볼 수 있다.
- 대여 클릭시 로그인 화면으로 간다.

## 일반 유저 ( 로그인 )
- 비로그인시 할 수 있는 기능 가능
- Rental - 대여 클릭시 대여기간 7일로 대여 가능
- My Rental - 내가 대여한 도서의 목록을 볼 수 있다.
- 자신의이름 
    - Update - 회원정보 수정 가능
    - changePW - 비밀번호 변경 가능
    - Logout - 로그아웃

## 관리자
- 메뉴에 Books Add 와 Not Return List 칸이 생긴다.
- Books Add - 도서를 추가 할 수 있다.
- Not Return List - 대여기간이 지나 연체된 도서 목록과 대여한 사람을 볼 수 있다.

## UI 링크
1. [회원가입](http://127.0.0.1:8000/accounts/register/)
2. [로그인](http://127.0.0.1:8000/accounts/login/)
3. [회원정보변경](http://127.0.0.1:8000/accounts/update/)
4. [비밀번호변경](http://127.0.0.1:8000/accounts/changePW/)
5. [로그아웃](http://127.0.0.1:8000/accounts/logout/)
6. [메인페이지](http://127.0.0.1:8000/)
7. [도서목록](http://127.0.0.1:8000/books/list/)
8. [카테고리도서목록](http://127.0.0.1:8000/books/list/1/)
9. [도서상세사항](http://127.0.0.1:8000/books/1/detail/)
10. [도서대여](http://127.0.0.1:8000/books/1/rent/)
11. [나의대여목록](http://127.0.0.1:8000/books/my_rentals/)
12. [검색(검색내용: the)](http://127.0.0.1:8000/books/search/?word=the)
13. [도서추가](http://127.0.0.1:8000/books/create/)
14. [연체도서목록](http://127.0.0.1:8000/books/return_books/)


### POSTGRESQL 사용시 생성법
- shell
1. psql -U postgres -d template1;
2. CREATE ROLE track WITH LOGIN PASSWORD '1234';
3. CREATE DATABASE track_db OWNER track;
- book_rental_system/settings.py
```
"ENGINE": "django.db.backends.postgresql",
        "NAME": 'track_db',
        "USER": 'track',
        "PASSWORD": "1234",
```

### fixture 데이터 
- 데이터 내보내기 <br>
`python -Xutf8 manage.py dumpdata books.category books.book --indent 2 >  books_data.json`
- 데이터 가져오기 <br>
`python -Xutf8 manage.py loaddata books_data.json`

