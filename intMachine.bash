run_foreignEar1="cd emptyear && python3 subEar.py international1"
run_foreignEar2="cd emptyear && python3 subEar.py international2"
run_foreignEar3="cd emptyear && python3 subEar.py international3"

osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar1\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar2\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar3\""
