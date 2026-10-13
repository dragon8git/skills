from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
import argparse
import json

parser = argparse.ArgumentParser(description='Render the fixed example (3, 1) + (1, 2) = (4, 3). Requires Pillow.')
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--preview-dir', type=Path, required=True)
parser.add_argument('--font', help='Path to a Chinese-capable TrueType/OpenType font')
parser.add_argument('--latin-font', help='Optional Latin font path; defaults to the Chinese font')
args = parser.parse_args()
if args.output.suffix.lower() != '.gif':
    parser.error('--output must end in .gif')
candidates = [args.font] if args.font else [
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    'C:/Windows/Fonts/msyh.ttc',
]
font_path = next((p for p in candidates if p and Path(p).is_file()), None)
if font_path is None:
    parser.error('No Chinese font found; provide --font /path/to/font.ttc')
args.output.parent.mkdir(parents=True, exist_ok=True)
args.preview_dir.mkdir(parents=True, exist_ok=True)
W,H,S = 960,640,2
BG=(13,18,29); GRID=(30,42,59); AXIS=(90,110,136); WHITE=(231,238,247)
MUTED=(148,164,188); BLUE=(85,177,255); YELLOW=(255,211,93); GREEN=(99,230,165)
FONT=font_path
LATIN=args.latin_font or FONT
fonts={}
def font(n,latin=False):
    k=(n,latin)
    if k not in fonts: fonts[k]=ImageFont.truetype(LATIN if latin else FONT,n*S)
    return fonts[k]
def blend(c,k): return tuple(round(BG[i]+(c[i]-BG[i])*k) for i in range(3))
def ease(t):
    t=max(0,min(1,t)); return t*t*(3-2*t)
def xy(p): return (130+70*p[0],420-70*p[1])
def draw_frame(t):
    im=Image.new('RGB',(W*S,H*S),BG); d=ImageDraw.Draw(im)
    def line(a,b,c,width=1): d.line(tuple(v*S for p in (a,b) for v in p),fill=c,width=round(width*S))
    def text(p,s,n=22,c=WHITE,latin=False): d.text((p[0]*S,p[1]*S),s,font=font(n,latin),fill=c)
    def arrow(a,b,c,k=1,width=4):
        a=xy(a); b=xy(b); dx=b[0]-a[0];dy=b[1]-a[1]; length=math.hypot(dx,dy)
        if length<1:return
        c=blend(c,k); ux=dx/length;uy=dy/length; head=min(16,length*.5)
        q=(b[0]-head*ux,b[1]-head*uy)
        line(a,q,c,width)
        d.polygon([(b[0]*S,b[1]*S),((q[0]-7*uy)*S,(q[1]+7*ux)*S),((q[0]+7*uy)*S,(q[1]-7*ux)*S)],fill=c)
    def dashed(a,b,c):
        a=xy(a);b=xy(b);L=math.dist(a,b)
        for off in range(0,int(L),13):
            u=off/L;v=min(1,(off+6)/L)
            line((a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u),(a[0]+(b[0]-a[0])*v,a[1]+(b[1]-a[1])*v),c,1.5)
    text((46,30),'向量相加',32)
    text((48,77),'把第二个向量的起点，接到第一个向量的终点。',18,MUTED)
    for x in range(-1,7): line(xy((x,-1)),xy((x,4)),GRID)
    for y in range(-1,5): line(xy((-1,y)),xy((6,y)),GRID)
    line(xy((-1,0)),xy((6.2,0)),AXIS,1.5)
    line(xy((0,-1.1)),xy((0,4.15)),AXIS,1.5)
    text((568,420),'x',18,MUTED,True);text((112,120),'y',18,MUTED,True)
    text((111,429),'0',15,MUTED,True)
    for x in range(1,6): text((xy((x,0))[0]-4,431),str(x),14,MUTED,True)
    for y in range(1,5): text((109,xy((0,y))[1]-8),str(y),14,MUTED,True)
    line((628,146),(628,492),GRID)
    text((670,160),'两个向量',18,MUTED)
    text((670,203),'a = (3, 1)',27,BLUE,True)
    text((670,247),'b = (1, 2)',27,YELLOW,True)
    a=ease((t-.3)/1.1); b=ease((t-1.45)/1.1)
    shift=ease((t-3.1)/2)
    result=ease((t-5.7)/1.5)
    arrow((0,0),(3*a,a),BLUE)
    if a>.9:text((340,354),'a',27,BLUE,True)
    if shift>0:arrow((0,0),(1,2),YELLOW,.18,2)
    start=(3*shift,shift);end=(3*shift+b,shift+2*b)
    arrow(start,end,YELLOW)
    if b>.9:
        p=xy(end);text((p[0]+12,p[1]-6),'b',27,YELLOW,True)
    if result>0:
        dashed((4,0),(4,3),blend(GREEN,.4*result));dashed((0,3),(4,3),blend(GREEN,.4*result))
        arrow((0,0),(4*result,3*result),GREEN,1,5)
        if result>.95:
            text((236,286),'a + b',26,GREEN,True)
            text((390,180),'(4, 3)',21,GREEN,True)
        text((670,322),'对应分量相加',18,blend(MUTED,result))
        text((670,364),'(3 + 1, 1 + 2)',24,blend(WHITE,result),True)
        text((670,409),'= (4, 3)',32,blend(GREEN,result),True)
    if t<3.1: step='01   从同一个起点画出 a 和 b'
    elif t<5.7: step='02   平移 b：长度和方向保持不变'
    else: step='03   从原点指向最终终点，就是 a + b'
    text((48,554),step,23)
    text((48,601),'VECTOR ADDITION  /  TIP-TO-TAIL',12,MUTED,True)
    out=im.resize((W,H),Image.Resampling.LANCZOS)
    return out

frames=[draw_frame(i/20) for i in range(210)]
# A short fade leads back into the loop, with a moment of rest.
for i in range(10):
    frames.append(Image.blend(frames[-1],draw_frame(0),ease((i+1)/10)))
frames += [draw_frame(0)]*8
palette=draw_frame(8).quantize(colors=192,method=Image.Quantize.MEDIANCUT)
quantized=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
path=args.output
quantized[0].save(path,save_all=True,append_images=quantized[1:],duration=50,loop=0,optimize=True,disposal=1)
for name, moment in [('initial', 2.8), ('translation', 4.1), ('result', 8.0)]:
    draw_frame(moment).save(args.preview_dir / f'{name}.png')
with Image.open(path) as check:
    duration=sum(check.seek(i) or check.info.get('duration',0) for i in range(check.n_frames))
    assert check.size == (W,H) and check.n_frames > 1
    assert duration == 11400 and check.info.get('loop') == 0
    print(json.dumps({'file':str(path.resolve()),'dimensions':check.size,'frames':check.n_frames,'duration_ms':duration,'bytes':path.stat().st_size}))
assert (3+1,1+2)==(4,3)
