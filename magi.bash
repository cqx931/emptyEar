run_englishEar="cd emptyear && python ear_demo.py 1"
run_danishEar="cd emptyear && python ear_demo.py 2"
run_foreignEar="cd emptyear && python ear_demo.py 3"

osascript -e "tell application \"Terminal\" to do script \"$run_danishEar\""
osascript -e "tell application \"Terminal\" to do script \"$run_englishEar\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar\""