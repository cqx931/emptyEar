cmd1="cd emptyear && python server/app.py"
cmd2="cd emptyear && python mainEar.py"
cmd3="cd emptyear && python subEar.py danish"

osascript -e "tell application \"Terminal\" to do script \"$cmd1\""
sleep 5s
osascript -e "tell application \"Terminal\" to do script \"$cmd2\""
sleep 5s
osascript -e "tell application \"Terminal\" to do script \"$cmd3\""