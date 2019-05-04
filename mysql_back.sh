#!/bin/bash
<< Mark
Description: Backup gameserver MySQL Database
Version: 1.1
Last Modify: 2015/09/23
Author: Hai
QQ: xxxxx
Email: Hai@xxxxx.com
Mark

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:$HOME/bin:/usr/local/mysql/bin
#set -x
umask 0077
prog=`basename $0`
Date=`date +%F`
Time=`date "+%Y%m%d_%H%M%S"`
MYSQL="mysql"
MYSQLDUMP="mysqldump"
DBuser='backuser'
DBpass='mysqlbackpass'
BAKDIR="/home/baksql"
IgnoreDB='information_schema|#mysql50|lost\+found|performance_schema|test'
DB=`$MYSQL -u$DBuser -p$DBpass -ss -e "SHOW DATABASES;"| egrep -v ${IgnoreDB}`
dump_opts="--skip-opt --extended-insert=false --add-drop-table --create-options --disable-keys --quick --triggers=false --hex-blob --single-transaction --routines "
# dump_opts="--skip-opt --extended-insert=true --add-drop-table --create-options --disable-keys --quick --triggers=false --hex-blob --single-transaction --routines --master-data=2 --set-gtid-purged=OFF"

# 只備份表結構（-B會自動加上USE database_name語句）
# --compact --skip-opt --create-options --no-create-db --add-drop-database=false --add-drop-table=false --triggers=true --routines -d database_name | sed 's/AUTO_INCREMENT=[0-9]*\s*//g'
# --compact --skip-opt --create-options --no-create-db --add-drop-database=false --add-drop-table=false --triggers=true --routines -d -B database_name | sed 's/AUTO_INCREMENT=[0-9]*\s*//g'

# 只備份表數據
# --skip-opt --extended-insert --quick --triggers=false --hex-blob --single-transaction --compact -t database_name table_name


# 記錄備份時間日誌
writeLog ()
{
        LogFile="$BAKDIR/$prog.log"
        BakInfo=$1
        echo "`date "+%F %T"` : ${prog} : ${BakInfo}" >> ${LogFile}
}

# 開始備份
backUp ()
{
	for bakdb in ${DB}
	do
		file="${bakdb}_${Time}.sql"
		writeLog "${file} mysqldump begin"
		logger -t $prog "${file} mysqldump begin"
		$MYSQLDUMP -u${DBuser} -p${DBpass} ${dump_opts} "$bakdb" > $BAKDIR/${Date}/${file}
		bzip2 -9 -f $BAKDIR/${Date}/${file}
		if [ $? -eq 0 ]; then
		  writeLog "${file} mysqldump is ok"
		  logger -t $prog "${file} mysqldump is ok"
		else
		  writeLog "${file} mysqldump is error"
		  logger -t $prog "${file} mysqldump is error"
		fi
	done
}

# 備份輪轉
Rotate ()
{
if [ "$BAKDIR" == "" ] || [ "$BAKDIR" == "/" ];then
    echo "BAKDIR cat not be / or null, now is $BAKDIR"
    exit 1
else
    for bakdir in `find $BAKDIR -type d -mtime +45`
    do
        rm -rf $bakdir
        writeLog "$bakdir delete success"
        logger -t $prog "${bakdir} delete success"
    done
fi
}

# rsync異地備份
function offsite_Back(){
[[ -f /game/conf/userctl.cfg ]] || (echo "/game/conf/userctl.cfg is not exist" && exit 1)
[[ -f /etc/.rsync.pass ]] || (echo 'myrsyncpassword' > /etc/.rsync.pass && chmod 600 /etc/.rsync.pass)
server=$(awk '/^world_id/{print $NF}' /game/conf/userctl.cfg)
day=$(date '+%Y%m%d')
date=$(date +%F)
backdb=$(ls /home/baksql/$date/| grep -E 'login|nexus'| grep -Ev 'merge')
for db in $backdb
do
        rsync -avzP --password-file=/etc/.offsite.pass /home/baksql/$date/$db username@rsync_server_IP::mysqldata/"$server"-"$db"
done
}

[ ! -d $BAKDIR/$Date ] && mkdir -p $BAKDIR/$Date
backUp
Rotate
offsite_Back
