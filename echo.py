from telethon import TelegramClient, events, sync

api_id = ##########
api_hash = '############################'
bot_token = '############################'


bot = TelegramClient('bot', api_id, api_hash,auto_reconnect=True,connection_retries=-1).start(bot_token=bot_token)


@bot.on(events.NewMessage)
async def my_event_handler(event):
    if event.text!="":
        await event.reply(event.text)



bot.loop.run_forever()
