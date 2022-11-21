# BotErrorePrezzo
Bot Telegram per errori di prezzo

Esistono su Telegram diversi gruppi che monitorano i principali siti di e-commerce (concentrandosi per lo più su amazon) 
e segnalano in tempo reale offerte ed eventuali errori di prezzo.

Data la grande mole di offerte che ogni minuto sono notificate sui vari gruppi, mantenere attive le notifiche su ognuno di essi è 
praticamente infattibile. Si è così costretti a silenziare le varie chat e perdere la possibilità di fare grossi affari.

Il mio bot monitora tutti i messaggi in entrata su telegram tramite la libreria
telethon. Per ogni messaggio che contiene alcune parole chiave che il programma sa essere associate agli errori di prezzo, 
inoltra il messaggio ad un echo bot (in modo da produrre una notifica sul mio cellulare) e ad un gruppo (per condividere con più persone 
la notizia) permettendo agli utenti di silenziare tutti i canali che segnalano offerte.

Inoltre, se il messaggio contiene un link appartenente al dominio di amazon, il bot invia anche un grafico contenente lo storico dei prezzi del prodotto
(generato tramite un sito terzo).

