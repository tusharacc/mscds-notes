mkdir -p transcripts

find videos -type f -iname '*.mp4' -print0 |
while IFS= read -r -d '' video; do
    out_dir="transcripts/$(dirname "${video#videos/}")"
    mkdir -p "$out_dir"
    echo "Transcribing: $video"
    whisper "$video" \
        --model medium \
        --language en \
        --task transcribe \
        --output_format txt \
        --output_dir "$out_dir"
done