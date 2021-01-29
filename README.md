# DigDiscord

[![Django CI](https://github.com/jean-charles-gibier/DigDiscord/workflows/Django%20CI/badge.svg)](https://github.com/jean-charles-gibier/DigDiscord/actions)

Discord Forum Analysis (Final Project of DA Python V1)

Purpose: Kind of a P.O.C. : "To crawl" and analyze the content of forums channels (and  all textual resources) from a discord server

Collect: Comments / Keywords / Urls / Code / Snippets / users / dates / images

Making it a "data cube" and present the results through an API DRF that can be used on a frontend based on Vue JS.
Frontend will consume our data and presents it thru axios and some Vue charts component.

keys concept :

Simple model entities

technical basis : Api / Django / DRF + Vue JS / Bootstrap

Suggested name: DigDiscord

Inspiration project

https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs

install :

```
pip install -r requirements.txt
```

modify settings
modify charset
Our DB Model must be updated in this way
(since Django ORM dos not seem to handle this features) :
````
ALTER TABLE `digdiscord`.`api_channel`
CHARACTER SET = utf8mb4 ;
````
modify messages index search
```
ALTER TABLE api_message ADD FULLTEXT (content);
```
