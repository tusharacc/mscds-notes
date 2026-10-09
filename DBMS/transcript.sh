cd videos/dbms/week-1
printf "file '%s'\n" "$PWD"/*.mp4 > /tmp/dbms-w1.txt
ffmpeg -y -f concat -safe 0 -i /tmp/dbms-w1.txt -c copy /tmp/dbms-week1.mp4
whisper /tmp/dbms-week1.mp4 --model medium --language en \
    --task transcribe --output_format txt --output_dir "${PWD}/transcripts/dbms/week-1"
