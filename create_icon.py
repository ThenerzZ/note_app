from PIL import Image, ImageDraw

# Create a new image with a transparent background
size = (256, 256)
image = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Draw a rounded rectangle for the notepad
padding = 40
rect_bounds = [padding, padding, size[0]-padding, size[1]-padding]
draw.rounded_rectangle(rect_bounds, fill='#141414', radius=20)

# Draw some "text lines"
line_color = '#ff69b4'  # Pink color
line_padding = 80
line_height = 20
line_gap = 40

for y in range(line_padding, size[1]-line_padding, line_gap):
    line_width = size[0] - (line_padding * 2)
    if y == line_padding:  # First line is longer
        width = line_width
    else:
        width = line_width * 0.7  # Other lines are shorter
    
    draw.rounded_rectangle(
        [line_padding, y, line_padding + width, y + line_height],
        fill=line_color,
        radius=5
    )

# Save as ICO file
image.save('app_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]) 