import requests
import time
from random import choice
from bots_token import BOT_TOKEN

timeout = 1
API_URL = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
DOGS_URL ='https://random.dog/woof.json'
FOX_URL = 'https://randomfox.ca/floof/'
CAPYBARA_API_URL = "https://api.capy.lol/v1/capybara?json=true"
# BOT_TOKEN = '6471784185:AAEWakBbPrU-bKGGanxahUq__ZbyZ1s8dBI'
ERROR_TEXT = 'Здесь должна была быть картинка :('

animal_dict={"cat":API_CATS_URL, "dog":DOGS_URL, "fox":FOX_URL, "bar":CAPYBARA_API_URL, 'da':'da', "net":"net"}
Key_ERROR_TEXT = "Не знаю такого животного)))) попробуй ещё раз ! Только cat/dog/fox и bar "
TEXT  = "Вас приветствует Чаппи!"
TEXT2 = "Если хочешь, я могу показать тебе фотогрфафии котиков, пёсикорв, лисичек и капибар !"
offset = -2
counter = 0
ID_CHAT = 6831521683 # Ольгин id = 818273096
# u = requests.get(f'{API_URL}{BOT_TOKEN}/getMe').json()
# print(u)
# updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
id_list = []
update_list=[]
while counter < 100:
    print('attempt =', counter)

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()

    if updates['result']:

        print(updates, "update_list = ", update_list)
        user_message  = updates["result"][0]["message"]["text"]
        communication = user_message
        print("Enter message    ", user_message)
        offset = updates['result'][0]['update_id']
        chat_id = updates['result'][0]['message']['from']['id']

        if chat_id not in id_list and len(update_list)==0:
            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')
            id_list.append(chat_id)
            print(id_list)
            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT2}')
            update_list.append(user_message)
        try:
            if user_message not in ('da', 'net'):
                animal_response = requests.get(animal_dict[user_message])
                if animal_response.status_code == 200 and user_message == 'cat':
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Отличный выбор ! - Держи Котика !')
                    an_link = animal_response.json()[0]["url"]
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={an_link}')
                    time.sleep(2)
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Нравится котик ?))) \nПродолжим ? da/net')

                elif animal_response.status_code == 200 and user_message == 'dog':
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Держи Пёсика !')
                    an_link = animal_response.json()["url"]
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={an_link}')
                    time.sleep(2)
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Нравится пёсик ?))) \n Еще надо ? da/net')

                elif animal_response.status_code == 200 and user_message== "fox":
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Держи Лисичку')
                    an_link = animal_response.json()["image"]
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={an_link}')
                    time.sleep(2)
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Нравится лисичка ?)))\n Еще надо ? da/net')

                elif animal_response.status_code == 200 and user_message=="bar":
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={user_message} -  Держи Капибару !')
                    an_link = animal_response.json()["data"]["url"]
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={an_link}')
                    time.sleep(2)
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Нравится это чудо ?))) \n Еще надо ? da/net')
                else:
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
            else:
                if communication=="da":
                    requests.get(
                        f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Отлично ! Выбери чьё фото тебе прислать !')
                elif communication=="net":
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Ну ладно ! Передохну пока !')
        except KeyError:
            update_list.append(1)
            if len(update_list)>2:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={user_message} {Key_ERROR_TEXT}')


    time.sleep(1)
    counter += 1