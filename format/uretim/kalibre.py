import subprocess, numpy as np
from PIL import Image

HEDEF_GEN = 594      # referans satir genisligi @720
METIN = "Her gün üç kişiye ücretsiz tadım"

BAS = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,{font},{size},&H00FFFFFF,&H00FFFFFF,&H40151215,&H00000000,0,0,0,0,100,100,0,0,3,{outline},0,8,90,90,1223,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 1,0:00:00.00,0:00:05.00,T,,0,0,1223,,{metin}
"""

def olc(font, size, outline=13, metin=METIN):
    open('k.ass','w',encoding='utf-8').write(
        BAS.format(font=font, size=size, outline=outline, metin=metin))
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=0x505050:s=1080x1920:d=1',
                    '-vf','ass=k.ass,scale=720:1280','-frames:v','1','-y','k.png'],check=True)
    im=np.array(Image.open('k.png').convert('RGB')).astype(int)
    w=(im[:,:,0]>215)&(im[:,:,1]>215)&(im[:,:,2]>215)
    ys=np.where(w.any(1))[0]; xs=np.where(w.any(0))[0]
    if not len(xs): return None
    return dict(gen=xs.max()-xs.min()+1, ust=ys.min(), alt=ys.max(),
                x0=xs.min(), x1=xs.max())

if __name__ == "__main__":
    import sys
    font = sys.argv[1] if len(sys.argv)>1 else "Inter ExtraBold"
    print(f"hedef genislik @720 = {HEDEF_GEN}\n")
    for s in range(56, 82, 2):
        r = olc(font, s)
        if r:
            d=(r['gen']-HEDEF_GEN)/HEDEF_GEN*100
            m="  <-- " if abs(d)<1.5 else ""
            print(f"  Fontsize {s:3d}: genislik={r['gen']:4d} ({d:+5.1f}%)  y{r['ust']}-{r['alt']}{m}")
