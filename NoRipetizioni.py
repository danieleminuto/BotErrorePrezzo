import http.client
import urllib
import http.client
import threading
from threading import Thread
import requests
import time

from telethon import TelegramClient, events, sync

api_id = ###########
api_hash = '#################################'
client = TelegramClient('###########', api_id, api_hash,auto_reconnect=True,connection_retries=-1)
links=[]
lock=threading.RLock()
idBot = '###########'
idGruppo = '######################'

def ins_rem(link):
    global links
    lock.acquire()
    links.append(link)
    lock.release()

    time.sleep(60*30)

    lock.acquire()
    links.remove(link)
    lock.release()


#################### SCREENSHOT KEEPA #######################
def screen(url):
    BASE = 'https://mini.s-shot.ru/1024x0/JPEG/1024/Z90/?'  # you can modify size, format, zoom
    url = urllib.parse.quote_plus(url)  # service needs link to be joined in encoded format

    path = 'target1.jpg'
    response = requests.get(BASE + url, stream=True)

    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response:
                file.write(chunk)
#################### FINE SCREENSHOT KEEPA #######################


#################### UTILITY SECTION #######################

def unshorten_url(url):
    parsed = urllib.parse.urlparse(url)
    h = http.client.HTTPConnection(parsed.netloc)
    resource = parsed.path
    if parsed.query != "":
        resource += "?" + parsed.query
    h.request('HEAD', resource )
    response = h.getresponse()
    return response.getheader('Location')

def get_asin(url):
    pippo=url.split("https://www.amazon.it/dp/")
    pippo=pippo[1]
    return pippo[:10]


def get_url(testo):
    ret=""
    if "https://amzn.to/" in testo:
        pippo=testo.split("https://amzn.to/")
        pippo=pippo[1]
        stringa="https://amzn.to/"+pippo[:7]
        ret=unshorten_url(stringa)
        tmp=ret.split("/dp/")
        stringa=tmp[1]
        ret="https://www.amazon.it/dp/"+stringa[:10]

    elif "https://www.amazon.it/dp/" in testo:
        pippo=testo.split("https://www.amazon.it/dp/")
        pippo=pippo[1]
        ret="https://www.amazon.it/dp/"+pippo[:10]

    elif "https://www.amazon.it/" in testo:
        pippo=testo.split("/dp/")
        pippo=pippo[1]
        ret="https://www.amazon.it/dp/"+pippo[:10]

    elif "https://www.ebay.it/itm/" in testo:
        pippo=testo.split("https://www.ebay.it/itm/")
        pippo=pippo[1]
        ret="https://www.ebay.it/itm/"+pippo[:12]

    elif "https://bit.ly/" in testo:
        pippo=testo.split("https://bit.ly/")
        pippo=pippo[1]
        stringa="https://bit.ly/"+pippo[:7]
        ret=unshorten_url(stringa)

    return ret

#true lo manda a tutti, false solo a me
async def invia_messaggio(bool,url, testo):
    if url == "":
        if bool:
            await client.send_message(idBot, testo)
            await client.send_message(idGruppo, testo)
        else:
            await client.send_message(idBot, testo)

    elif url not in links:
        t = Thread(target=ins_rem, args=(url,))
        t.start()

        if bool:
            await client.send_message(idBot, testo)
            await client.send_message(idGruppo, testo)
        else:
            await client.send_message(idBot, testo)

        if "https://www.amazon.it/dp/" in url:
                if(bool):
                    try:
                        screen("https://keepa.com/#!product/8-" + get_asin(url))
                        await client.send_file(idBot, './target1.jpg')
                        await client.send_file(idGruppo, './target1.jpg')
                    except:
                        await client.send_message(idBot, 'Grafico non disponibile, mi fido di te!')
                        await client.send_message(idGruppo, 'Grafico non disponibile, mi fido di te!')
                else:
                    try:
                        screen("https://keepa.com/#!product/8-" + get_asin(url))
                        await client.send_file(idBot, './target1.jpg')
                    except:
                        await client.send_message(idBot, 'Grafico non disponibile, mi fido di te!')


#################### END UTILITY SECTION #######################

################### INIZIO SEZIONE MESSAGGIO ###################
@client.on(events.NewMessage(from_users=[###########]))
async def handler(event):
    try:
        usr = await event.get_sender()
        usr = usr.id
        testo = event.text
        url = get_url(testo)

        if usr != ########### and ('ERRORE PREZZO').casefold() in event.raw_text.casefold() \
                or ('ERRORE di PREZZO').casefold() in event.raw_text.casefold() \
                or ('possibile ERRORE').casefold() in event.raw_text.casefold():

                await invia_messaggio(False,url,testo)

        elif "https://www.amazon.it/dp/" in url:
            try:
                screen("https://keepa.com/#!product/8-" + get_asin(url))
                await client.send_file('###########', './target1.jpg')
            except:
                await client.send_message('###########', 'Grafico non disponibile, mi fido di te!')
    except:
        pass


@client.on(events.NewMessage())
async def handler(event):
    try:
        usr = await event.get_sender()
        usr = usr.id
        if usr!=########### and usr!=########### and (('ERRORE PREZZO').casefold() in event.raw_text.casefold() \
                or ('ERRORE di PREZZO').casefold() in event.raw_text.casefold() \
                or ('possibile ERRORE').casefold() in event.raw_text.casefold()):
            testo = event.text
            url = get_url(testo)
            await invia_messaggio(True, url, testo)
    except:
        pass


client.start()
client.loop.run_forever()




