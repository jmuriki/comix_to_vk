# comix_to_vk

Данный проект помогает автоматизировать процесс скачивания и размещения комиксов [xkcd](https://xkcd.com) на стене вашей [vk](https://vk.com)-группы.


## Установка

Должен быть установлен python версии 3.9 или новее.
Затем используйте pip (или pip3, если есть конфликт с python2) для установки зависимостей:

```
pip install -r requirements.txt
```

или

```
pip3 install -r requirements.txt
```

Рекомендуется использовать venv для изоляции проекта.


## Ключи


Сохраните ключи/токены/параметры в `.env` файл в директорию проекта в следующем формате:

```
VK_GROUP_ID=вместо этого текста вставьте идентификационный номер вашей группы
```

```
VK_ACCESS_TOKEN=вместо этого текста вставьте токен
```

## Запуск


### main.py

Находясь в директории проекта, откройте с помощью python3 файл `main.py`

```
python3 main.py
```


## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков https://dvmn.org/.