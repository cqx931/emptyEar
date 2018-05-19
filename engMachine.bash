run_engEar1="cd emptyear && python subEar.py english1"
run_engEar2="cd emptyear && python subEar.py english2"
run_engEar3="cd emptyear && python subEar.py english3"

osascript -e "tell application \"Terminal\" to do script \"$run_engEar1\""
osascript -e "tell application \"Terminal\" to do script \"$run_engEar2\""
osascript -e "tell application \"Terminal\" to do script \"$run_engEar3\""
