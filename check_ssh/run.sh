#!/bin/bash

gamefile=gameserver.txt
gamenames=$(cat $gamefile | shyaml keys)

for gamename in $gamenames
do
	# echo $gamename
	count=$(cat $gamefile | shyaml get-value $gamename.server | wc -w)
	for server in $(cat $gamefile | shyaml get-value $gamename.server)
	do
		let count=$count-1

		echo "do some things"
		if [[ $server == "192.168.0.1" ]] || [[ $server == "192.168.0.3" ]]; then
			break
		fi

		if [[ $? -eq 0 ]]; then
			server_array="$server_array $server"
		fi

		if [[ $count == 0 ]] && [[ $server_array != "" ]]; then
			mailto=$(cat $gamefile | shyaml get-value $gamename.mail)
			echo "sendemail -t $mailto $server_array: discovery ssh port 22"
		fi
	done
		unset server_array
done
