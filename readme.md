**Запуск** бота осуществляется командой `python -B main.py` из **корня проекта**.

В корне проекта должен быть файл `.env`
```
TOKEN = '<ТОКЕН_БОТА>'

ADMIN_ID = [<ID_АДМИНИСТРАТОРОВ>, ]

DATABASE_NAME = '<НАЗВАНИЕ_БД>'

SUPERUSER = <ID_СУПЕРЮЗЕРА>
```

`<ID_СУПЕРЮЗЕРА>` - этому пользователю приходит уведомление о том, что бот запущен

В проекте используется БД `SQLite3` и по умолчанию должна находится в **корне проекта**. Если ее нет, то она автоматически создается вместе с необходимыми таблицами.

Объекты, кварталы и корпуса явно указаны в файле `request_kb.py`