# api_yamdb
#### Разработчики: Андрей Пономарев, Владимир Рудаков, Андрей Скуридин
## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/morhond/api_yamdb.git
```

```
cd yatube_api
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
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Endpoints и функционал проекта: