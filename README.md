# autoreplybot_vk
This bot can reply to added user in text messages or photos

## Команды

- **+sms/+смс  (prefix)** - adds the user from the forwarded message to the list

- **-sms/-смс  (prefix)** - remove the user from the list
- **!cd/!кд  (prefix)  (seconds)** - delay message sending
## Prefixes:
- **Photo/фото** - sends photos

- **текст/text** - sends text messages
## How to install/Как установить

```
git clone https://github.com/agent502/autoreplybot_vk.git
```
```
open autoreplybot_vk folder(открыть папку autoreplybot_vk)
```
In **config.py** enter the requirements (в файле config.py введите следующие требования)
  
```
u_admins = [] your id in number (ваш идентификатор в номере)
bot_id = your id in number (ваш идентификатор в номере)
u_token = ''  your token (ваш токен)

```

**token/Токен** получаем [здесь](https://oauth.vk.com/authorize?client_id=2685278&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1)

## bot for a group (для группы)
In **config.py**:
```
g_admins = [] - ID of pages that can give commands to the bot
group_id = - Group ID(айди группы бота)
g_token = '' - Group Token/токен группы бота
```
```
запустить bot_user.py (для пользователя)
запустить bot_group.py (для группы)
```
[вы можете посмотреть это видео](https://disk.yandex.com/i/wwoQ00RPGBydpw)
  
[Мой вк](https://vk.com/a_502)
