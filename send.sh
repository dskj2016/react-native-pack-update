#!/bin/sh
port=$1
user=$2
ip=$3
local_dir=$4
remote_dir=$5
sftp -o Port=${port} ${user}@${ip} <<EOF
put -r /Users/yanaihua/workspace/mobile_app/react-native-pack-update/public/package/DashengChefu/ios/* /opt/applications/react-native-pack-update/public/package/DashengChefu/ios/
exit
close
bye
EOF