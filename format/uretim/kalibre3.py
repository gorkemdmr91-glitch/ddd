import subprocess, numpy as np
from PIL import Image

BAS = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
Collisions: Normal

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,Inter ExtraBold,69,&H00FFFFFF,&H00FFFFFF,&H40151215,&H00000000,0,0,0,0,100,100,0,0,3,13,0,8,90,90,0,1
Style: C,Inter ExtraBold,30,&H00000000,&H00000000,&H000EAFF5,&H00000000,0,0,0,0,100,100,0,0,3,5,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,C,,0,0,0,,{{\\pos({cx},{cy})}}{chip}
Dialogue: 1,0:00:00.00,0:00:05.00,T,,0,0,0,,{{\\pos(540,{y1})}}Her gün üç kişiye ücretsiz tadım
Dialogue: 1,0:00:00.00,0:00:05.00,T,,0,0,0,,{{\\pos(540,{y2})}}kampanyamızla alakalı,
"""
def render(y1, pitch, cx, cy, pad=9):
    chip='\\h'*pad+'Volkan Usta'+'\\h'*pad
    open('k3.ass','w',encoding='utf-8').write(
        BAS.format(y1=y1, y2=y1+pitch, cx=cx, cy=cy, chip=chip))
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=0x505050:s=1080x1920:d=1',
                    '-vf','ass=k3.ass,scale=720:1280','-frames:v','1','-y','k3.png'],check=True)
    im=np.array(Image.open('k3.png').convert('RGB')).astype(int)
    w=(im[:,:,0]>215)&(im[:,:,1]>215)&(im[:,:,2]>215)
    am=(abs(im[:,:,0]-245)<25)&(abs(im[:,:,1]-175)<30)&(im[:,:,2]<70)
    def bant(m,t=4):
        b=[];cur=None
        for y in range(700,1000):
            if m[y].sum()>t:
                if cur is None: cur=y
            else:
                if cur is not None and y-cur>3: b.append((cur,y-1))
                cur=None
        return b
    t=bant(w); c=bant(am,10)
    r={}
    if len(t)>=2:
        xs=np.where(w[t[0][0]:t[0][1]+1].any(0))[0]
        r['s1']=(t[0][0],t[0][1],xs.min(),xs.max()); r['s2t']=t[1][0]; r['pitch']=t[1][0]-t[0][0]
    if c:
        cx_=np.where(am[c[0][0]:c[0][1]+1].any(0))[0]
        r['chip']=(c[0][0],c[0][1],cx_.min(),cx_.max())
    return r

print("HEDEF: satir1 y822 x63-656 | satir2 y877 (pitch 55) | chip y775-802 x45-215\n")
for y1,pitch,cx,cy in [(1223,78,72,1168),(1222,77,72,1167)]:
    r=render(y1,pitch,cx,cy)
    print(f"y1={y1} pitch={pitch} chip=({cx},{cy}):")
    print("  ",r)
