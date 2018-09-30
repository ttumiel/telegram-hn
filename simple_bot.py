import os
import telepot

token = os.environ['BOT_TOKEN']

TelegramBot = telepot.Bot(token)
# print (TelegramBot.getMe())
print(TelegramBot.getUpdates())