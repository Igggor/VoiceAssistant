from funcs import *
#Инициализация переменных
sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5
speaker = pyttsx3.init()
r = speech_recognition.Recognizer()
m = speech_recognition.Microphone(device_index=1)
is_work = True


#Слушаем и убираем шум
with m as source:
    r.adjust_for_ambient_noise(source)


#Словарик с командами и основными словами бота, типо небольшая иишка
commands_dict = {
    "alias": ('помощник','помоги', "help", "бот", "помощь", "эй", "боня", "голосовой"),
    "tbr": ("помоги", 'скажи','расскажи','покажи','сколько','произнеси'),
    'commands': {
        "thanks":["спасибо", "благодарю"],
        'off':['пока', "отключись", "досвидания"],
        'greeting': ['привет', 'приветствую'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка'],
        'date_now': ['текущее время','сейчас времени','который час'],
        'play_music': ['включить музыку', 'дискотека'],
        "anek": ['анекдот','рассмеши меня','ты знаешь анекдоты'],
        "weather":["какая погода", "погода", "погоду"],
        "curs":["евро", "доллар", "курс валют"]
    }
}

def anek():
    n = get_anek()
    return n


#Отключение бота
def off():
    global is_work
    is_work = False
    return "Пока, до скорых встреч, был рад помогать тебе"


#Основнй цикл работы ассистента
speak("Приветствую, я голосовой помощник Боня, я готов помогать тебе")
while(is_work):
    query = listen_command()
    print(f"[Log] Распознано: {query}")
    if query.startswith(commands_dict["alias"]):
    # обращаются к боту
        cmd = query
        #Удаляем обраение к ассистенту
        for x in commands_dict['alias']:
            cmd = cmd.replace(x, "").strip()
        #Удаляем действие
        for x in commands_dict['tbr']:
            cmd = cmd.replace(x, "").strip()
        #Получаем команду
        for k, v in commands_dict['commands'].items():
            if cmd in v:
                speak(globals()[k]())
                break