import time
import vk_api
import random
import config as c
from threading import Thread
from modules import sqlite_methods as m
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk = vk_api.VkApi(token=c.g_token)
vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, c.group_id)


def get_variants(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def send_msg(peer_id: int, message: str, attachment: str = ""):
    return vk.method("messages.send", {**locals(), "random_id": 0})


message_user_ids = []
message_users = m.get_all_message_users()
for user in message_users:
    message_user_ids.append(user[0])

photo_user_ids = []
photo_users = m.get_all_photo_users()
for user in photo_users:
    photo_user_ids.append(user[0])

settings_result = []
settings = m.get_settings(2)
for value in settings:
    settings_result.append(value)

MESSAGE_VARIANTS = get_variants("variants/message_variants.txt")
random.shuffle(MESSAGE_VARIANTS)
PHOTO_VARIANTS = get_variants("variants/photo_variants.txt")
random.shuffle(PHOTO_VARIANTS)


def hate():
    message_index = 0
    photo_index = 0
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:

                    if event.obj.from_id in message_user_ids:
                        if message_index < len(MESSAGE_VARIANTS):
                            time.sleep(settings_result[1])
                            send_msg(event.obj.peer_id, f'{MESSAGE_VARIANTS[message_index]}')
                            message_index += 1
                        else:
                            message_index = 0
                            random.shuffle(MESSAGE_VARIANTS)
                            time.sleep(settings_result[1])
                            send_msg(event.obj.peer_id, f'{MESSAGE_VARIANTS[message_index]}')
                            message_index += 1

                    if event.obj.from_id in photo_user_ids:
                        if photo_index < len(PHOTO_VARIANTS):
                            time.sleep(settings_result[2])
                            send_msg(event.obj.peer_id, '', f'{PHOTO_VARIANTS[photo_index]}')
                            photo_index += 1
                        else:
                            photo_index = 0
                            random.shuffle(PHOTO_VARIANTS)
                            time.sleep(settings_result[2])
                            send_msg(event.obj.peer_id, '', f'{PHOTO_VARIANTS[photo_index]}')
                            photo_index += 1
        except Exception as e:
            print(repr(e))


def commands():
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:

                    split_text = event.object.text.split(' ')

                    if split_text[0] in c.hate:
                        if len(split_text) == 2 and split_text[1] in c.hate_message_prefix:
                            if event.obj.from_id in c.g_admins:
                                if 'reply_message' in event.object:
                                    user = event.obj.reply_message['from_id']
                                    if user != -c.group_id:
                                        if not m.is_message_user_hatelisted(user):
                                            message_user_ids.append(user)
                                            m.insert_message_hatelist(user)
                                            send_msg(event.obj.peer_id, '✅ User added to the text list')
                                        else:
                                            send_msg(event.obj.peer_id, '❎ The user is already in the text list')
                                    else:
                                        send_msg(event.obj.peer_id, '❎ Unable to add bot to the list')
                                else:
                                    send_msg(event.obj.peer_id, '❎ User not specified')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.obj.peer_id, f'{choice}')

                        elif len(split_text) == 2 and split_text[1] in c.hate_photo_prefix:
                            if event.obj.from_id in c.g_admins:
                                if 'reply_message' in event.object:
                                    user = event.obj.reply_message['from_id']
                                    if user != -c.group_id:
                                        if not m.is_photo_user_hatelisted(user):
                                            photo_user_ids.append(user)
                                            m.insert_photo_hatelist(user)
                                            send_msg(event.obj.peer_id, '✅ User added to the photo list')
                                        else:
                                            send_msg(event.obj.peer_id, '❎ The user is already in the photo list')
                                    else:
                                        send_msg(event.obj.peer_id, '❎ Unable to add bot to the list')
                                else:
                                    send_msg(event.obj.peer_id, '❎ User not specified')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.obj.peer_id, f'{choice}')
                        else:
                            send_msg(event.obj.peer_id, '❎ Invalid command format')

                    if split_text[0] in c.unhate:
                        if len(split_text) == 2 and split_text[1] in c.hate_message_prefix:
                            if event.obj.from_id in c.g_admins:
                                if 'reply_message' in event.object:
                                    user = event.obj.reply_message['from_id']
                                    if m.is_message_user_hatelisted(user):
                                        message_user_ids.remove(user)
                                        m.delete_message_hatelist(user)
                                        send_msg(event.obj.peer_id, '✅ User removed from the text list')
                                    else:
                                        send_msg(event.obj.peer_id, '❎ User is missing from the text sheet')
                                else:
                                    send_msg(event.obj.peer_id, '❎ User not specified')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.obj.peer_id, f'{choice}')

                        elif len(split_text) == 2 and split_text[1] in c.hate_photo_prefix:
                            if event.obj.from_id in c.g_admins:
                                if 'reply_message' in event.object:
                                    user = event.obj.reply_message['from_id']
                                    if m.is_photo_user_hatelisted(user):
                                        photo_user_ids.remove(user)
                                        m.delete_photo_hatelist(user)
                                        send_msg(event.obj.peer_id, '✅ User removed from photo list')
                                    else:
                                        send_msg(event.obj.peer_id, '❎ The user is not in the photo list')
                                else:
                                    send_msg(event.obj.peer_id, '❎ User not specified')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.obj.peer_id, f'{choice}')
                        else:
                            send_msg(event.obj.peer_id, '❎ Invalid command format')

                    if split_text[0] in c.cooldown:
                        if len(split_text) == 3 and split_text[1] in c.hate_message_prefix and split_text[2].isnumeric():
                            if event.obj.from_id in c.g_admins:
                                settings_result.pop(1)
                                settings_result.insert(1, int(split_text[2]))
                                m.set_message_cooldown(int(split_text[2]), 2)
                                send_msg(event.obj.peer_id, f'✅ Delay text changed to {split_text[2]} second')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.obj.peer_id, f'{choice}')

                        elif len(split_text) == 3 and split_text[1] in c.hate_photo_prefix and split_text[2].isnumeric():
                            if event.obj.from_id in c.g_admins:
                                settings_result.pop(2)
                                settings_result.insert(2, int(split_text[2]))
                                m.set_photo_cooldown(int(split_text[2]), 2)
                                send_msg(event.obj.peer_id, f'✅ Photo delay changed to {split_text[2]} second')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.obj.peer_id, f'{choice}')
                        else:
                            send_msg(event.obj.peer_id, '❎ Invalid command format')
        except Exception as e:
            print(repr(e))


if __name__ == '__main__':
    Thread(target=hate, args=[]).start()
    Thread(target=commands, args=[]).start()
