import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton,WebAppInfo
import random
import itertools
import os


TOKEN = '7247331457:AAFnPvqVxVcsJVI8hQ3NxBeVzQkdIRZpdmE' 


userStep={}


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        cid = m.chat.id
        if m.content_type == 'text':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)
        elif m.content_type == 'photo':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + "New photo recieved")
        elif m.content_type == 'document':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + 'New Document recieved')


bot = telebot.TeleBot(TOKEN,num_threads=3)
bot.set_update_listener(listener)

def send_long_message(chat_id, text, chunk_size=4000):
    # تقسیم متن به قسمت‌های کوچکتر
    for i in range(0, len(text), chunk_size):
        bot.send_message(chat_id, text[i:i + chunk_size])

def generate_words(word):
    word = word.lower()  
    word = word.replace(' ','')
    unique_combinations = set()  
    
    for i in range(3, len(word) + 1):
        combinations = itertools.permutations(word, i)
        unique_combinations.update([''.join(comb) for comb in combinations])
    
    return unique_combinations

#------------------------------------------------------commands-------------------------------------------------
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, f'سلام {m.from_user.first_name} عزیز \nلطفا کلمه مد نظر خود را ارسال کنید:')


@bot.message_handler(func=lambda m: True)
def all_msg(m):
    cid=m.chat.id
    text = m.text
    if len(text) < 20:
        if len(text) >= 3: 
            result = generate_words(text)
            text_res = ''
            with open(f'{cid}.txt', 'w', encoding='utf-8') as f:
                for r in result:
                    f.write(r + '\n')
                    text_res += r + '\n'

            send_long_message(cid, text_res)
            with open(f'{cid}.txt', 'rb') as file:
                bot.send_document(cid, file)
            os.remove(f'{cid}.txt')
            bot.send_message(cid, 'عملیات انجام شد \nلطفا کلمه مد نظر خود را ارسال کنید:')
        else:
            bot.send_message(cid, 'تعداد حروف کلمه ارسالی حداقل باید 3 حرف باشد.')
    else:
        bot.send_message(cid, 'تعداد کارکتر ها خیلی زیاده لطفا با تعداد کارکتر کمتر ارسال کنید')







bot.infinity_polling()
# with open('combinations.txt', 'w', encoding='utf-8') as f:
#     for r in result:
#         f.write(r + '\n')

# print("ترکیب‌ها داخل فایل 'combinations.txt' ذخیره شدند.")