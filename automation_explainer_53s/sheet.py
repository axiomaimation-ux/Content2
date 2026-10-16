import sys, time
sys.path.insert(0,'.')
from PIL import Image, ImageDraw
import render as R
times=[float(x) for x in sys.argv[2:]]
t0=time.time()
ims=[R.frame_img(int(round(t*30))).resize((270,480), Image.LANCZOS) for t in times]
print("sec/frame", (time.time()-t0)/len(ims))
cols=6; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(cols*280,rows*500),(20,20,20))
d=ImageDraw.Draw(sh)
for k,(im,t) in enumerate(zip(ims,times)):
    x=(k%cols)*280+5; y=(k//cols)*500+5
    sh.paste(im,(x,y)); d.text((x+4,y+484),f"{t:.2f}s",fill=(255,255,0))
sh.save(sys.argv[1])
