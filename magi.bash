IP='192.168.0.20'
cmdBrowser="/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://\"$IP\":8080?role=master"

osascript -e "tell application \"Terminal\" to do script \"$cmdBrowser\""
osascript -e "tell application \"Terminal\" to do script \"$cmdBrowser\""
osascript -e "tell application \"Terminal\" to do script \"$cmdBrowser\""

#########

cmd1="cd emptyear && python server/app.py"
cmd2="cd emptyear && python mainEar.py"
cmd3="cd emptyear && python3 subEar.py danish1"
cmd4="cd emptyear && python3 subEar.py english1"
cmd5="cd emptyear && python3 subEar.py english2"

osascript -e "tell application \"Terminal\" to do script \"$cmd1\""
sleep 5s
osascript -e "tell application \"Terminal\" to do script \"$cmd2\""
sleep 10s
osascript -e "tell application \"Terminal\" to do script \"$cmd3\""
osascript -e "tell application \"Terminal\" to do script \"$cmd4\""
osascript -e "tell application \"Terminal\" to do script \"$cmd5\""

#########
sleep 2s
run_foreignEar1="cd emptyear && python3 subEar.py internationalA1"
run_foreignEar2="cd emptyear && python3 subEar.py internationalA2"
run_foreignEar3="cd emptyear && python3 subEar.py internationalA3"

osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar1\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar2\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar3\""

#########
sleep 2s
run_foreignEar1="cd emptyear && python3 subEar.py internationalB1"
run_foreignEar2="cd emptyear && python3 subEar.py internationalB2"
run_foreignEar3="cd emptyear && python3 subEar.py internationalB3"

osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar1\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar2\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar3\""
