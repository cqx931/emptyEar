cmd1="cd emptyear && python server/app.py"
cmd2="cd emptyear && python mainEar.py"
d5="cd emptyear && python3 subEar.py english2"

run_foreignEar1="cd emptyear && python3 subEar.py internationalA1"
run_foreignEar2="cd emptyear && python3 subEar.py internationalA2"
run_foreignEar3="cd emptyear && python3 subEar.py internationalA3"


osascript -e "tell application \"Terminal\" to do script \"$cmd1\""
sleep 5s
osascript -e "tell application \"Terminal\" to do script \"$cmd2\""
sleep 10s
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar1\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar2\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar3\""
