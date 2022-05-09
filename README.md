## python version == 3.8

## 프로젝트 목표
- 클론 대상
  - velog
- 구현에 사용되는 프레임워크/라이브러리
  - Django
  - django restframework
- service target
  - 독자
  - 작가
- 구현해야 하는 API
  - 독자
    - 글 목록
      - 인기순
        - 시간 범위에 따른 인기순
        - `인기` = 조회수 + ’좋아요' * 5 = 인기지수
          - 모듈을 만들어서 따로 관리
          - 정규화 vs 반정규화
      - 최신순
        - `최신` = 첫 publish
    - 검색
      - 글 제목 검색 - 일부도 포함
      - 태그 검색
    - 좋아요
      - 취소 가능
      - url: `article/<id>/user/<id>/like`
      - url: `article/<id>/user/<id>/unlike`
    - 댓글 가능
      - 대댓글 or 스레드
      - url: `article/<id>/user/<id>/comment/<id>`
      - 대댓글 가능
  - 작성자
    - 글 CRUD
      - 내용은 마크다운
      - 태그 - 자유작성
      - url - 알아서 판단
    - 시리즈 기능

추가 기능

- 긴 글 나눠서 업로드
- 이미지 업로드
- 시간 범위에 따른 인기

유의 사항

- test 넣으면 좋고
- 함수형 뷰든 클래스 뷰든 DRF든 아니든 노상관
- 로컬에서만
- 인증/권한 관련 기능 x
- Delete는 진짜 DB에서 삭제하는 것이 로직 구현에 유리
