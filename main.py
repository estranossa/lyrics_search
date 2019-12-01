# -*- coding: utf8 -*-

import vk_api, random, time, requests, json, os
from config import VK_API_TOKEN, URL_SERVICE, API_KEY_SERVICE

vk = vk_api.VkApi(token = VK_API_TOKEN)
vk._auth_token()

status_search = 0
musician_text = title_text = ""

def GET_BUTTON(label, color, payload = ""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

keyboard = {
    "one_time": True,
    "buttons": [
        [GET_BUTTON(label = "Найти текст песни", color = "positive"), GET_BUTTON(label = "Информация", color = "primary")],
        [GET_BUTTON(label = "Закрыть", color = "negative")]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii = False).encode("utf-8")
keyboard = str(keyboard.decode("utf-8"))

keyboard_stop = {
    "one_time": True,
    "buttons": [
        [GET_BUTTON(label = "Прекратить поиск", color = "negative")]
    ]
}

keyboard_stop = json.dumps(keyboard_stop, ensure_ascii = False).encode("utf-8")
keyboard_stop = str(keyboard_stop.decode("utf-8"))

def SEND_USER_MESSAGE(id, string_message):
    vk.method("messages.send", {"peer_id": id, 
                                "message": string_message, 
                                "random_id": random.randint(1, 2147483647)})

def SHOW_USER_BUTTON(id, keyboard_name, string_message):
    vk.method("messages.send", {"peer_id": id, 
                                "keyboard": keyboard_name,
                                "message": string_message, 
                                "random_id": random.randint(1, 2147483647)})

def GET_LYRICS(id, musician, title):
    r = requests.get(fr'{URL_SERVICE}{musician}/{title}?apikey={API_KEY_SERVICE}') 
    data_dict = json.loads(r.text) 

    check_get = str(data_dict)

    if check_get.find("error") != -1:
        SHOW_USER_BUTTON(id, keyboard, "&#128165; [БОТ]: К сожалению, по Вашему запросу ничего не найдено... Попробуйте перепроверить введенные даннные... &#128165;\n&#128313; Имя исполнителя: " + musician + "\n&#128313; Название песни: " + title)
    else: 
        SHOW_USER_BUTTON(id, keyboard, "&#128165; Наши невероятно сверхмощные сервера, находящиеся на орбитальной космической станции, получили необходимую информацию... &#128165;\n&#128313; Имя исполнителя: " + musician + "\n&#128313; Название песни: " + title + "\n\n" + data_dict['result']['track']['text'])

while True:

    try:

        messages = vk.method("messages.getConversations", {"offset": 0, 
                                                           "count": 20, 
                                                           "filter": "unanswered"})

        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            text_message = body.lower()
            
            if text_message == "!меню" or text_message == "начать":
                SHOW_USER_BUTTON(id, keyboard, "&#128313; [БОТ]: Начинаю запускать меню управления специально для Вас, дайте мне всего лишь несколько миллисекунд, а то и меньше... &#128313;")
                status_search = 0
                
            elif text_message == "найти текст песни" or text_message == "!поиск":
                SHOW_USER_BUTTON(id, keyboard_stop, "&#128313; [БОТ]: Итак, сейчас мы начнем процесс поиска текста искомой песни. Первым делом, что Вам необходимо будет сделать — это ввести и отправить мне ответным сообщением имя исполнителя... &#128313;")
                status_search = 1

            elif text_message == "информация" or text_message == "!инфо":
                status_search = 0
                SHOW_USER_BUTTON(id, keyboard, "&#128165; Привет-привет! Появились вопросы или просто стало интересно? &#128165;\n\n&#128313; Lyric Search — проект, созданный специально для удобного поиска текста песен, зная при этом имя исполнителя и название самой песни. Все это не выходя из нашей любимой социальной сети: очень просто, комфортно и удобно.\n&#128312; Проект разработали: @id156062976(Егор Шаров), @id165427609(Римма Яковлева), @id344233179(Никита Чебан)")

            elif text_message.find("закрыть") != -1:
                status_search = 0
                SEND_USER_MESSAGE(id, "&#128313; [БОТ]: Вы хотите закрыть меню управления? Хорошо, задача весьма проста, ясна и легка, поэтому слушаюсь и выполняю... &#128313;")
                SEND_USER_MESSAGE(id, "&#128313; [БОТ]: Используйте команду: \"!меню\", если захотите его снова открыть... &#128313;")

            elif text_message == "прекратить поиск" or text_message == "!стоп":
                status_search = 0
                SHOW_USER_BUTTON(id, keyboard, "&#128165; Поиск текста песни прекращен... &#128165;")

            else:
                if status_search == 1:
                    SHOW_USER_BUTTON(id, keyboard_stop, "&#128313; [БОТ]: Итак, великолепно! Без каких-либо проблем мы записали исполнителя песни, текст которой Вы хотите найти. Следующее, что Вам необходимо будет сделать — это ввести и отправить мне ответным сообщением название самой песни... &#128313;")
                    musician_text = text_message
                    status_search = 2

                elif status_search == 2:
                    SEND_USER_MESSAGE(id, "&#128313; [БОТ]: Замечательно, мы записали имя исполнителя и название песни, текст которой Вы хотите получить. Перенаправляю все свободные ресурсы на невероятно сверхмощные сервера, находящиеся на орбитальной космической станции, и начинаю поиск... &#128313;")
                    title_text = text_message
                    GET_LYRICS(id, musician_text, title_text)
                    status_search = 0

                else:
                    SEND_USER_MESSAGE(id, "&#128532; [БОТ]: К сожалению, я не совсем понимаю, что Вы от меня хотите...")
                    SEND_USER_MESSAGE(id, "&#128165; Команды, которые возможно смогут Вам помочь... &#128165;\n\n&#128313; !меню — команда, предназначенная для вызова меню управления.\n&#128313; !информация — команда, предназначенная для получения информации о данном боте.\n&#128313; !поиск — команда, предназначенная для запуска процесса поиска текста песни.")


    except Exception as E:
        time.sleep(1)