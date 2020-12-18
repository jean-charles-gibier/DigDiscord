# DigDiscord

![Django CI(https://github.com/jean-charles-gibier/DigDiscord/actions)](https://github.com/jean-charles-gibier/DigDiscord/workflows/Django%20CI/badge.svg)

Discord Forum Analysis Project X

Purpose: "To crawl" and analyze the content of forums channels (and  all textual resources) from a discord server

Collect: Comments / Keywords / Urls / Code / Snippets / users / dates / images

Making it a "data cube" and present the results through an API that can be used on a web front => DRF

TO DO

Provide a model => what are the entities?

Test the nosql technique ? make a poc ?
technical basis : Api / Django / DRF

Suggested name: DigDiscord

Inspiration project

https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs

install :

```
python -m pip install djangorestframework
python -m pip install markdown
python -m pip install django-filter
python -m pip install Pillow
python -m pip install mysqlclient
```

modify settings
modify charset
````
ALTER TABLE `digdiscord`.`api_channel`
CHARACTER SET = utf8mb4 ;
````
test
