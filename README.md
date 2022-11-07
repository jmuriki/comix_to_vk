# comix_to_vk

Данный проект помогает автоматизировать процесс скачивания и размещения комиксов [xkcd](https://xkcd.com) на стене вашей vk-группы.


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

### Регистрация

Для получения необходимых ключей потребуются:
- [регистрация в vk](https://vk.com) ;
- [vk группа](https://vk.com/groups?tab=admin) ;
- [vk приложение](https://vk.com/apps?act=manage) .

Создать приложение можно в разделе `Мои приложения` [cтраницы для разработчиков](https://vk.com/dev) (используйте тип `standalone`).

### Получение

Пройдите процедуру [Implicit Flow](https://vk.com/dev/implicit_flow_user), используя браузерную строку:
- не используйте параметр `redirect_uri` ;
- вставьте `client_id` [своего приложения](https://vk.com/apps?act=manage) (можно найти в адресной строке) ;
- встатьте `scope=photos,groups,wall,offline` ;
- вставьте `response_type=token` .

```
https://oauth.vk.com/authorize?client_id=XХХХХХХХ&scope=photos,groups,wall,offline&response_type=token
```

Перейдите по составленному адресу, а затем извлеките из адресной строки access token. Не забудьте отсечь параметры в конце строки, начиная с символа `&`.

### Хранение

Сохраните id группы и токен приложения в `.env` файл в директорию проекта в следующем формате:

```
VK_GROUP_ID=вместо этого текста вставьте id группы
```

```
VK_ACCESS_TOKEN=вместо этого текста вставьте токен приложения
```

## Запуск


### main.py

Находясь в директории проекта, откройте с помощью python3 файл `main.py`

```
python3 main.py
```


## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков https://dvmn.org/.