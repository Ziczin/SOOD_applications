from PIL import Image, ImageDraw, ImageFont
import textwrap, os, sys

input_path="content.txt"
output_path="output.png"
font_size=14
padding=10
bg_color=(255,255,255)
text_color=(0,0,0)
max_width=800

if not os.path.exists(input_path):
    sys.exit("content.txt not found")

with open(input_path,"r",encoding="utf-8") as f:
    text=f.read()

try:
    font=ImageFont.truetype("DejaVuSans.ttf",font_size)
except:
    font=ImageFont.load_default()

# создаём временное изображение для измерений
tmp_img=Image.new("RGB",(10,10))
draw_tmp=ImageDraw.Draw(tmp_img)
char_width=draw_tmp.textlength("A", font=font) or 7
wrap_width=int((max_width - padding*2)/char_width)
lines=[]
for paragraph in text.splitlines():
    if paragraph.strip()=="":
        lines.append("")
    else:
        lines.extend(textwrap.wrap(paragraph, width=max(1,wrap_width)))

ascent, descent = font.getmetrics() if hasattr(font, "getmetrics") else (font.size, 0)
line_height = ascent + descent + 4
img_height = padding*2 + line_height*max(1, len(lines))
img_width = max_width
img = Image.new("RGB",(img_width,img_height),color=bg_color)
draw = ImageDraw.Draw(img)
y = padding
for line in lines:
    draw.text((padding, y), line, font=font, fill=text_color)
    y += line_height

img.save(output_path)
print(output_path)
