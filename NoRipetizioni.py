import http.client
import urllib
import threading
from threading import Thread
import requests
import time

from telethon import TelegramClient, events, sync

api_id = ##########
api_hash = '########################'
client = TelegramClient('#####', api_id, api_hash,auto_reconnect=True,connection_retries=-1)




links=[]
lock=threading.RLock()

############################ SEZIONE THREAD ###############################
##### IL THREAD MANTIENE UN QUARTO D'ORA IL LINK NEI LINK SALVATI #########
class ControllerThread(Thread):
    def __init__(self,link,lock):
        Thread.__init__(self)
        self.link=link
        self.lock=lock

    def run(self):
        self.lock.acquire()
        links.append(self.link)
        self.lock.release()

        time.sleep(60*30) #dorme 30 minuti

        self.lock.acquire()
        links.remove(self.link)
        self.lock.release()


############################ FINE SEZIONE THREAD ###############################


#################### SCREENSHOT KEEPA #######################

def screen(url):
    BASE = 'https://mini.s-shot.ru/1024x0/JPEG/1024/Z90/?' # you can modify size, format, zoom
    print(url)
    url = urllib.parse.quote_plus(url) #service needs link to be joined in encoded format
    
    path = 'target1.jpg'
    response = requests.get(BASE + url, stream=True)

    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response:
                file.write(chunk)

#################### FINE SCREENSHOT KEEPA #######################


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


############## INIZIO SEZIONE MESSAGGIO ##############
@client.on(events.NewMessage)
async def my_event_handler(event):
    global lock


    if ('ERRORE PREZZO').casefold() in event.raw_text.casefold() \
            or ('ERRORE di PREZZO').casefold() in event.raw_text.casefold() \
            or ('ERRORE o bomba').casefold() in event.raw_text.casefold() \
            or ('possibile ERRORE').casefold() in event.raw_text.casefold()\
            or ('bomba ERRORE').casefold() in event.raw_text.casefold():
        sender = await event.get_sender();
        idBot='#######'
        idGruppo='#########'

        ############################ EVITO RIPETIZIONI DI LINK ###############################
        testo=event.text
        url=get_url(testo)
        
        if event.sender.id==########: #se il messaggio lo mando io, arriva solo al bot
            lock.acquire()
            if url=="":
                await client.send_message(idBot,event.text)
            elif url not in links:
                await client.send_message(idBot,event.text)
                ControllerThread(url).start()
                if "https://www.amazon.it/dp/" in url:
                    try:
                        screen("https://keepa.com/#!product/8-"+get_asin(url))
                        await client.send_file(idBot,'./target1.jpg')
                    except:
                        await client.send_message(idBot,'Grafico non disponibile, mi fido di te!' )
                else:
                    print(url+" ripetuto: inoltro annullato")
            lock.release()


        elif event.sender.id!=################ : #serve ad evitare che il bot mandi il messaggio in loop

            ############################ SE URL È VUOTO SIGNIFICA CHE NON È STATO RICONOSCIUTO, NEL DUBBIO LO MANDO ###############################
            if url=="":
                await client.send_message(idBot,event.text)
                await client.send_message(idGruppo,event.text)

            lock.acquire()
            if url not in links and url!="":
            ##################### SE URL NON È PRESENTE IN LINKS DEVO INVIARLO ###############################
                await client.send_message(idBot,event.text)
                await client.send_message(idGruppo,event.text)
                ControllerThread(url,lock).start()
                if "https://www.amazon.it/dp/" in url:
                    try:
                        screen("https://keepa.com/#!product/8-"+get_asin(url))
                        await client.send_file(idBot,'./target1.jpg')
                        await client.send_file(idGruppo,'./target1.jpg')
                    except:
                        await client.send_message(idBot,'Grafico non disponibile, mi fido di te!' )
                        await client.send_message(idGruppo,'Grafico non disponibile, mi fido di te!' )
            elif url!="":
                print(url+" ripetuto: inoltro annullato")
                
            lock.release()

    else:
        testo=event.text
        sender=await event.get_sender()
        url=get_url(testo)
        if event.sender.id== #### and "https://www.amazon.it/" in url:
            screen("https://keepa.com/#!product/8-"+get_asin(url))
            await client.send_file(##########,'./target1.jpg')
                




############## FINE SEZIONE MESSAGGIO ##############

client.start()
client.loop.run_forever()



