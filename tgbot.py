# import asyncio
import requests
import telegram
import time


class TGbot:
    def __init__(self):
        self.Token = "7747242868:AAFXW-PBuby_yME28m2k1y-DOAR_pFuPQWI"
        self.chat_id = self.get_chat_id()
        self.bot = telegram.Bot(
            "7206924017:AAG7RYQriBlnWfiFFe9FuuT8ox_wYlKSKoc")

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.Token}/sendMessage?chat_id={self.chat_id}&text={message}"
        time1 = time.time()
        data = requests.get(url).json() # this sends the message
        time2 = time.time()

        print(time2 - time1)

        print(f"\n Success to send a message!{data['result']['text']} \n")
        
        # async with self.bot:
        #     await self.bot.sendMessage(chat_id=self.chat_id, text=message)

    def get_chat_id(self):
        url = f"https://api.telegram.org/bot{self.Token}/getUpdates"
        data = requests.get(url).json()
        
        print(data["result"][0]["message"]['chat']['id'])
        return data["result"][0]["message"]['chat']['id']


tgbot = TGbot()

while True:
    message = input("Input: ")
    tgbot.send_message(message)
    # asyncio.run(tgbot.send_message(message))

