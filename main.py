import telebot, requests
import time
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

token = config["token"]
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def start(message):
	bot.reply_to(message, "<b>Привет!</b>\n\n<i>Я могу конвертировать голосовое сообщение в MP3 и наоборот.</i>\nПросто отправь мне голосовое сообщение или аудио файл!\n\nРазработчик: @kirillsaint_info, https://kirillsaint.xyz\nСвязь с разработчиком: @kirillsaint, @kirillsaint_bot\nБлог разработчика: @kirillsaint_blog", parse_mode="HTML")


@bot.message_handler(content_types=["audio"])
def mp3tovoice(message):
  msg = bot.reply_to(message, "Скачиваю файл...")
  file_info = bot.get_file(message.audio.file_id)
  file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
  with open('audio.ogg','wb') as f:
  	f.write(file.content)
  bot.delete_message(message.chat.id, msg.id)
  filec = bot.reply_to(message, "Конвертирую файл...")
  time.sleep(1)
  bot.delete_message(message.chat.id, filec.id)
  filem = bot.reply_to(message, "Отправляю файл...")
  bot.send_voice(message.chat.id, open('audio.ogg', 'rb'), caption="by @vconvertor_bot")
  bot.delete_message(message.chat.id, filem.id)
  
@bot.message_handler(content_types=["voice"])
def voicetomp3(message):
  msg = bot.reply_to(message, "Скачиваю файл...")
  file_info = bot.get_file(message.voice.file_id)
  file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
  with open('audio.mp3','wb') as f:
  	f.write(file.content)
  bot.delete_message(message.chat.id, msg.id)
  filec = bot.reply_to(message, "Конвертирую файл...")
  time.sleep(1)
  bot.delete_message(message.chat.id, filec.id)
  filem = bot.reply_to(message, "Отправляю файл...")
  bot.send_audio(message.chat.id, open('audio.mp3', 'rb'), caption="by @vconvertor_bot")
  bot.delete_message(message.chat.id, filem.id)
	
bot.polling(none_stop=True)
