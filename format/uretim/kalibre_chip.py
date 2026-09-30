import subprocess, numpy as np
from PIL import Image
BAS = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Inter ExtraBold,{size},&H00000000,&H00000000,&H000EAFF5,&H00000000,0,0,0,0,100,100,0,0,3,{ol},0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,C,,0,0,0,,{{\\pos({x},{y})}}{chip}
"""
def olc(size, ol, pad, x=72, y=1168):
    chip='\\h'*pad+'Volkan Usta'+'\\h'*pad
    open('kc.ass','w',encoding='utf-8').write(BAS.format(size=size,ol=ol,x=x,y=y,chip=chip))
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=0x505050:s=1080x1920:d=1',
                    '-vf','ass=kc.ass,scale=720:1280','-frames:v','1','-y','kc.png'],check=True)
    im=np.array(Image.open('kc.png').convert('RGB')).astype(int)
    am=(abs(im[:,:,0]-245)<30)&(abs(im[:,:,1]-175)<35)&(im[:,:,2]<80)
    ys=np.where(am.any(1))[0]
    if not len(ys): return None
    y0,y1=ys.min(),ys.max()
    xs=np.where(am.any(0))[0]; x0,x1=xs.min(),xs.max()
    ic=im[y0+2:y1-1, x0+2:x1-1]
    kd=(ic.sum(2)/3 < 110)
    ty=np.where(kd.any(1))[0]; tx=np.where(kd.any(0))[0]
    return dict(kutu=(y0,y1,x0,x1), kh=y1-y0+1, kw=x1-x0+1,
                th=(ty.max()-ty.min()+1) if len(ty) else 0,
                tw=(tx.max()-tx.min()+1) if len(tx) else 0)
print("HEDEF: kutu ~y768-805 (h38) x44-220 (w177) | ic yazi yuk19 gen144\n")
for size in (40,44,46,48,50):
    r=olc(size, 5, 4)
    print(f"  size={size:3d} ol=5 pad=4 -> kutu h={r['kh']:3d} w={r['kw']:3d} (y{r['kutu'][0]}-{r['kutu'][1]} x{r['kutu'][2]}-{r['kutu'][3]})  yazi h={r['th']} w={r['tw']}")
