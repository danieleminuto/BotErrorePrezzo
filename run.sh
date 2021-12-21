

python3 handler.py &
exc=$!
echo $exc>nonChiudere.txt

a="Avviati programmi " 
b=$(date)
echo $a$b>log.txt
python3 echo.py &
p1=$!
echo "Avviato echo, pid:"$p1>>log.txt
python3 NoRipetizioni.py &
p2=$!
echo "Avviato programma, pid:"$p2>>log.txt

echo ' '$p1' '$p2' '>pids.txt


sleep 24h

bash ./stop.sh #termina i processi bash e sleep e i pids salvati
a="Uccisi programmi " 
b=$(date)
echo $a$b>>log.txt

bash ./run1.sh &

