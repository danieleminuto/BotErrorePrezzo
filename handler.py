from telethon import TelegramClient, events, sync
import os

api_id = ###############
api_hash = '############################'
bot_token = '########################################################'


bot = TelegramClient('bot', api_id, api_hash,auto_reconnect=True,connection_retries=-1).start(bot_token=bot_token)


@bot.on(events.NewMessage)
async def my_event_handler(event):
    testo=event.raw_text
    if event.sender.id==##########:
        if 'START' == testo :
            os.system("bash -c 'bash ./run1.sh &'")
            await event.reply("Comando avviato, controlla")
        elif 'STOP' == testo:
            os.system("bash -c 'bash ./stop.sh &'")
            await event.reply("Comando avviato, controlla")
        else:
            await event.reply("Ti voglio bene papà")
    else:
        await event.reply("Scusami, papà mi ha detto di non parlare con gli sconosciuti!")
		



bot.loop.run_forever()

