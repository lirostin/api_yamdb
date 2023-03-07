# API для YaMDB

### Описание
Проект YaMDb собирает **отзывы** пользователей на **произведения**. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на **категории**, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен **жанр** из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые **отзывы** и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять **комментарии** к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Реализованные ресурсы API YaMDb

- AUTH: аутентификация.
- CATEGORIES:разделение произведений на категории.
- COMMENTS: возможность комментариев к отзывам аутентифицированными пользователями.
- GENRES: жанры произведений.
- REVIEWS: отзывы на произведения аутентифицированными пользователями.
- TITLES: произведения, к которым пишут отзывы.
- USERS: пользователи.


### Используемые технологии:
* Python 3.9
* Django REST Framework (DRF 3.12)
* Django 3.2,
* База данных - SQLite3

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/lirostin/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Импорт  csv-файла в базу данных

Файл для импорта тестовой базы данных находится по адресу: 
```
api_yamdb\reviews\management\commands\importcsvfile.py
```

Импорт базы данных осуществляется командой:

```
python manage.py importcsvfile
```

* Импорт необходимо осуществлять на чистую БД.
* При ошибке в ходе импорта рекомендуется удалить все миграции и выполнить импорт повторно.

### Пути запуска 

- Запуск проекта:  http://127.0.0.1:8000/
- Полная документация:  http://127.0.0.1:8000/redoc/
- Доступ к админ панели:  http://127.0.0.1:8000/admin/

## Регистрация пользователя
- Пользователь отправляет запрос */auth/signup/* с параметрами *email* и *username*.
- На указаный *email* система отправляет код подтверждения.
- Пользователь отправляет запрос на */auth/token/*, указывает параметры *email* и *confirmation_code на */auth/token/*
- В ответ на запрос пользователю  приходит token (JWT-токен).


### Базовые эндопоинты API:
```
"genres": "http://127.0.0.1:8000/api/v1/genres/",
"comments": "http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/",
```

# Примеры запросов к API:
**Получение JWT-токена:**

POST http://127.0.0.1:8000/api/v1/auth/token/
```
{
  "username": "string",
  "confirmation_code": "string"
}
```
*Ответ 200 OK:*
```
{
  "token": "string"
}
```
**Получение списка всех произведений:**

GET http://127.0.0.1:8000/api/v1/titles/

*Ответ 200 OK:*
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
**Добавление произведения:**

POST http://127.0.0.1:8000/api/v1/titles/
```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
"category": "string"
}
```
*Ответ 201 CREATED:* 
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
**Частичное обновление отзыва по id:**

PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
{
  "text": "string",
  "score": 1
}
```
*Ответ 200 OK:*
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
**Получение комментария к отзыву:**

GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

*Ответ 200 OK:*
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Авторы: :+1:

**Кирилл** организовывал работу в качестве тимлида и работал над
https://github.com/lirostin
-       отзывами,
-       комментариями,
-       рейтингом произведений.


**Алексей** работал над частью, касающуюся управления пользователями:  
https://github.com/Aleks-go
-      систему регистрации и аутентификации,
-       права доступа,
-       работу с токеном,
-       систему подтверждения через e-mail.


**Сергей** написал модели, view и эндпойнты для  

 - произведений,
 - категорий,
 - жанров;
 - реализовал импорт данных из `csv` файлов.
 https://github.com/SergeyPegas




