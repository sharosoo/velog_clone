## API 구현

### Articles: Article ListView

- `api/articles/recent/`
  - `GET`
- `api/articles/recommend/`
  - `GET`
  - +`daily/`, `weekly/`, `monthly/`, `annually/`
    - default is `weekly/`
- `api/articles/search/?{querystring}`
  - `GET`
  - `tag` or `keyword`
- `api/articles/{int: profile_id}/`
  - `GET`
- `api/articles/{int: series_id}/`
  - `GET`

- Data
  - JSONData : `article_id`, `profile_nickname`

### Article: Article DetailView

- `api/article/`
  - `POST`
    - JSON Data: `profile_id`, `title`, `slug`, `content`
- `api/article/{int: article_id}/`
  - `GET`
    - JSON Data: `profile_nickname`, `article_title`, `article_content`, `root_comment`, `comments`
      - `comments`: `comment_id`, `profile_id`, `content`, `depth`
  - `PUT`
    - JSON Data: `profile_id`, `title`, `slug`, `content`
  - `Delete`
    - JSON Data: `profile_id`, `article_id`



### Series

- `api/series/`
  - `POST`
    - JSON Data: `profile_id`, `title`
- `api/series/{int: series_id}`
  - `GET`
    - JSON Data: `profile_id`, `title`
  - `PUT`
    - JSON Data: `profile_id`, `title`
  - `DELETE`
    - JSON Data: `profile_id`
- `api/series/add`
  - `POST`
    - JSON Data: `profile_id`, `series_id`, `article_id`
  - `DELETE`
    - JSON Data: `profile_id`, `article_id`
    - article의 series를 null처리



### Likes

- `api/article/like`
  - `POST`
    - JSON Data: `profile_id`, `article_id`
- `api/article/unlike`
  - `POST`
    - JSON Data: `profile_id`, `article_id`



### Comments

- depth 제한 = 30
- 더 깊어지느 것은 새로운 테이블을 만들거나 foreign키로 관리해도된다.(확률적으로 그렇게 깊게 댓글이 파고들어가지 않음)
- GET은 article detail view에서 보자

- `api/comment/`
  - `POST`
    - JSON Data: `post_id` or `comment_id`, `profile_id`, `content`
  - `GET`
    - JSON Data: `article_id` or `comment_id`
  - `DELETE`
    - JSON Data: `comment_id`, `profile_id`

