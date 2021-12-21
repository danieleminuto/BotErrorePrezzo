pids=$(cat ./pids.txt)
for pid in $pids; do
	kill $pid
done
bash ./pulisci.sh
