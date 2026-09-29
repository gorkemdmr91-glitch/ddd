set -e
cd /tmp/claude-0/-home-user-ddd/a72183c6-78df-5cb8-a69c-e72729f84191/scratchpad
echo "[1/2] ses olcumu (loudnorm analiz)"
M=$(ffmpeg -hide_banner -ss 3.10 -i dl/ham.mp4 -t 94.40 -map 0:a:0 \
    -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 \
    | sed -n '/^{/,/^}/p')
echo "$M"
gi=$(echo "$M" | python3 -c "import sys,json;print(json.load(sys.stdin)['input_i'])")
tp=$(echo "$M" | python3 -c "import sys,json;print(json.load(sys.stdin)['input_tp'])")
lra=$(echo "$M" | python3 -c "import sys,json;print(json.load(sys.stdin)['input_lra'])")
th=$(echo "$M" | python3 -c "import sys,json;print(json.load(sys.stdin)['input_thresh'])")
echo "[2/2] render"
ffmpeg -hide_banner -v warning -stats \
  -ss 3.10 -i dl/ham.mp4 -t 94.40 \
  -map 0:v:0 -map 0:a:0 \
  -vf "fps=30,ass=altyazi.ass" \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$gi:measured_TP=$tp:measured_LRA=$lra:measured_thresh=$th:linear=true,aresample=48000" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -profile:v high -level 4.1 \
  -x264-params "keyint=60:min-keyint=30" \
  -c:a aac -b:a 192k -ar 48000 -ac 2 \
  -movflags +faststart \
  -y mistanbul_gizem_gorkem.mp4
echo "RENDER_TAMAM"
ls -lh mistanbul_gizem_gorkem.mp4
