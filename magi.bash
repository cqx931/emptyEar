move_position="tell application \"Terminal\" to set bounds of window 1 to {0, 0, 505, 320}"
run_englishEar="cd emptyear && python ear_demo.py 1"
run_danishEar="cd emptyear && python ear_demo.py 2"
run_foreignEar="cd emptyear && python ear_demo.py 3"

osascript -e "tell application \"Terminal\" to do script \"$run_danishEar\""
osascript -e "tell application \"Terminal\" to do script \"$run_englishEar\""
osascript -e "tell application \"Terminal\" to do script \"$run_foreignEar\""