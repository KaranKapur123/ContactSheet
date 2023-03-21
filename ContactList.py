import os
import sys
from PIL import Image, ImageDraw, ImageFont
import exifread

def correct_orientation(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
        orientation = tags.get('Image Orientation', 1)
        orientation = orientation.values[0]
        compressed_bits = tags.get('Compressed Bits Per Pixel', 1)
        if orientation == 3 or (orientation == 1 and compressed_bits == 2):
            image = Image.open(image_path).resize((250, 175), Image.ANTIALIAS)
            image = image.transpose(Image.ROTATE_180)
            print("180")
        elif compressed_bits == 2:
            image = Image.open(image_path)
            if image.width>image.height:
                image = image.transpose(Image.ROTATE_90)
            image = image.resize((175,250), Image.ANTIALIAS)
            print("01")
        elif orientation == 6:
            image = Image.open(image_path).resize((250, 175), Image.ANTIALIAS)
            image = image.transpose(Image.ROTATE_270)
            print("270")
        elif orientation == 8:
            image = Image.open(image_path).resize((250, 175), Image.ANTIALIAS)
            image = image.transpose(Image.ROTATE_90)
            print("90")
        else:
            image = Image.open(image_path)
            if image.width>image.height:
                image = image.transpose(Image.ROTATE_90)
            image = image.resize((175,250), Image.ANTIALIAS)
            print("0")
    return image

def create_contact_sheet(folder):
    parent_folder_name = os.path.basename(os.path.dirname(folder))
    print(parent_folder_name," in progress...")
    columns=4
    rows=5
    images = [f for f in os.listdir(folder) if f.endswith(".JPG")]
    num_images = len(images)
    cells_per_page = columns * rows
    num_pages = (num_images + cells_per_page - 1) // cells_per_page
    font = ImageFont.truetype("arial.ttf", 14)
    for page in range(num_pages):
        font = ImageFont.truetype("arial.ttf", 14)
        width = columns * 400
        height = rows * 300 + rows * 20 # add 20 pixels per row for the labels
        contact_sheet = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(contact_sheet)
        for i, image in enumerate(images[page * cells_per_page : (page + 1) * cells_per_page]):
            font = ImageFont.truetype("arial.ttf", 14)
            img = correct_orientation(os.path.join(folder, image))
            #img = img.resize((250, 175), Image.ANTIALIAS)
            x = (i % columns) * 400 
            y = (i // columns) * 300
            contact_sheet.paste(img, (x+100, y+75))
            label = image.split(".")[0]
            label_width, label_height = draw.textsize(label, font=font)
            draw.text((x + (375 - label_width) / 2, y + 330), label, fill=(0, 0, 0), font=font)
        font = ImageFont.truetype("arial.ttf", 50)
        draw.text((width/2 -150, 0)," UnIndentified", fill=(0, 0, 0), font=font)
        contact_sheet.save(os.path.join("D:/GIIS ClassWise 2.2.23//Contact List UnIdentified", f"{parent_folder_name} - Sheet %d.jpg" % (page + 1)))
        #contact_sheet.save(os.path.join("D:/GIIS ClassWise 2.2.23//ContactList", " - Sheet %d.jpg" % (page + 1)))
        print(parent_folder_name +" Done")

root_dir = 'D:/GIIS ClassWise 2.2.23//ClassWise'
#create_contact_sheet("D:/GIIS ClassWise 2.2.23//All")
for subdir, dirs, files in os.walk(root_dir):
    for dir in dirs:
        if dir == 'Unpaid':
            paid_dir = os.path.join(subdir, dir)
            create_contact_sheet(paid_dir)

