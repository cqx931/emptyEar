run_foreignEar1="cd emptyear && python3 subEar.py internationalA1"
run_foreignEar2="cd emptyear && python3 subEar.py internationalA2"
run_foreignEar3="cd emptyear && python3 subEar.py internationalA3"
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar1\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar2\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar3\""
