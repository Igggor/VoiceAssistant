import random
import pyttsx3, os, time, datetime, requests
import speech_recognition
from fuzzywuzzy import fuzz


sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5
speaker = pyttsx3.init()
r = speech_recognition.Recognizer()
m = speech_recognition.Microphone(device_index=1)

#Слушаем, что сказал пользователь
def listen_command():
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()

        return query
    except speech_recognition.UnknownValueError:
        return 'Damn... Не понял что ты сказал :/'

def play_music():# Проигрование функции, но еще надо дописать
    #os.system('cd H:\Программирование\Python files\VoiceAssestant')
    return "Не танцуем, я еще не умею включать музыку, извини, но я активно учусь" #f'Танцуем под {random_file.split("/")[-1]} 🔊🔊🔊'

def create_task():#Создание заметки в todo листе
    speak('Что добавим в список дел?')
    query = listen_command()
    with open('todo-list.txt', 'a') as file:
        file.write(f'{query}\n')
    return f'Задача {query} добавлена в todo-list!'


#Функция анекдотов (хотел сделать API но мне не понравились анекдоты на том сайте, поэтому пока что массив)
anekdots = ["А вот к нам в студию пришло письмо от Шамиля Прохоровича Кацнельсона из Нигерии...Да уж, как же судьба распорядилась человеком!",
            "С годами становишься всё более мудрым, и мудрость помогает понять, что мудрость не помогает.",
            "Старый еврей говорит жене:- Сара, как только кто-нибудь из нас умрет, я уезжаю в Израиль",
            "«В Прикамье отметят праздник гуся. Гости праздника смогут купить гусиные тушки, одеяла, перины и подушки». Так себе у гуся праздник.",
            "Сегодня Хэллоуин. Приду ненакрашенная",
            "Объявление на пограничном столбе: Товарищи Нарушители! В связи с нехваткой патронов предупредительныевыстрелы в воздух больше не производим!"
            ]
def get_anek():
    return anekdots[random.randint(0, len(anekdots)-1)]

def date_now():
    now = datetime.datetime.now()
    return ("Сейчас " + str(now.hour) + ":" + str(now.minute))

#Функция tts
def speak(sth):
    print(f"[log] said: {sth}")
    speaker.say(sth)
    speaker.runAndWait()
    speaker.stop()



def thanks():
    return "Был рад помочь."


def curs():
    return None


def greeting():
    return 'Приветcтвую тебя!'





def weather():
    speak("В каком городе ты хочешь узнать погоду?")
    city = listen_command()
    print(f"[Log] распознан город {city}")
    return get_weather(city)


#open_weather_token = "e37d54207830a94eee9d3babc8b0d27f"

def get_weather(city, open_weather_token = "e37d54207830a94eee9d3babc8b0d27f"):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        #pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        feel = data['main']['feels_like']

        return (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}° \nОщущается как {feel}°\n"
              f"Влажность: {humidity}% {wd}\nДавление: {pressure} милиметров ртутного столба\nВетер: {wind} метров в секунду\n"
              )

    except Exception as ex:
        print(ex)
        return("Проверьте название города")
