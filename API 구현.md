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
    - JSON Data: `profile_id`, `title`, `slug`, `content`, `tags`, `series_id`
- `api/article/{int: article_id}/`
  - `GET`
    - JSON Data: `profile_nickname`, `article_title`, `article_content`, `comments`(in nested json)
      - `comments`: `comment_id`, `profile_id`, `content`, `depth`
  - `PUT`
    - JSON Data: `profile_id`, `title`, `slug`, `content`, `tags`, `series_id`
  - `Delete`
    - JSON Data: `profile_id`



### Series

- `api/series/`
  - `POST`
    - JSON Data: `profile_id`, `title`
- `api/series/{int: series_id}`
  - `PUT`
    - JSON Data: `profile_id`, `title`
  - `DELETE`
    - JSON Data: `profile_id`
    - series아래의 article들은 profile 밑에 붙이고 나서 series만 삭제한다.



### Likes

- `api/article/{int: article_id}/like`
  - `POST`
    - JSON Data: `profile_id`
- `api/article/{int: article_id}/unlike`
  - `POST`
    - JSON Data: `profile_id`



### Comments

- depth 제한?
- GET은 article detail view에서 보자

- `api/comment/`
  - `POST`
    - JSON Data: `post_id` or `comment_id`, `profile_id`, `content`
  - `GET`
    - JSON Data: `article_id` or `comment_id`
- `api/comment/{int: comment_id}`
  - `PUT`
    - JSON Data: `profile_id`, `content`
  - `DELETE`
    - JSON Data: `profile_id`

