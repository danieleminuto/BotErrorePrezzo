pids=$(ps)
exc=$(cat ./nonChiudere.txt)
i=0
pid=23944
flag=false

for elem in $pids; do
	
	if [ $i -eq 0 ];  then
        if [ $elem -ne $exc ];then 
		    pid=$elem
        fi
        let i=$i+1
	elif [ $i -eq 3 ]; then
		if [ $elem = 'bash' ]; then
			flag=true
		fi
		
		if  $flag ; then
			kill $pid
			flag=false
		fi
		let i=0
	else
		let i=$i+1
	fi
	
	
done
