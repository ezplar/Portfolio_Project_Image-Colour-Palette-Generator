import random
import numpy as np
from flask import Flask, render_template, redirect, url_for, request
from PIL import Image
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['UPLOAD_FOLDER'] = "path_to_upload_folder_static"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        #Get number of colors from form
        n_colors = int(request.form.get("num-colors"))

        #Get uploaded file into variable
        upload_image = request.files.get("file-new")

        # Save image to static/images folder
        path = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
        upload_image.save(path)

        img_open = Image.open(f'static/images/{upload_image.filename}')
        img_array = np.array(img_open)

        #Test sample of RBG to HEX color code
        # hex_triplet = f"#%02x%02x%02x" % image_pix.getpixel((0,0))
        # print(hex_triplet.upper())

        #Convert to sRGB to get percentage
        # conv_sRGB = img_array / 255
        # print(conv_sRGB)
        # uq = np.unique(conv_sRGB)
        # print(uq)

        # Get Dominant Color - 1
        # cp_img = img_open.copy()
        # cp_img = cp_img.convert("RGBA")
        # cp_img = cp_img.resize((1,1),resample=0)
        # dominant_color = cp_img.getpixel((0,0))
        # print(dominant_color)

        # Get Dominant Color - 2
        pallette_size = 16
        cp_img = img_open.copy()
        cp_img.thumbnail((100,100))

        palletted = cp_img.convert('P',palette=Image.ADAPTIVE, colors=pallette_size)

        pallette = palletted.getpalette()
        color_counts = sorted(palletted.getcolors(),reverse=True)
        pallette_index = color_counts[0][1]
        dominant_color = pallette[pallette_index*3:pallette_index*3+3]
        dominant_color_tuple = tuple(dominant_color)
        hex_triplet_dominant_color = f"#%02x%02x%02x" % dominant_color_tuple

        print(f"Dominant: {dominant_color} {hex_triplet_dominant_color.upper()}")


        # Get Random Unique Colors
        uniq_colors = np.unique(img_array.reshape(-1,img_array.shape[2]), axis=0)

        #Map/convert numpy array unique to tuple
        tuple_unique = tuple(map(tuple,uniq_colors))

        hex_random_tuple = []
        for ten in range(0, n_colors):
            print(random.choice(tuple_unique))
            hex_triplet = f"#%02x%02x%02x" % random.choice(tuple_unique)
            print(hex_triplet.upper())
            hex_random_tuple.append(hex_triplet.upper())
        # print(hex_random_tuple[0])

        #TODO: Get the most common color in an image - Done
        #Get Common color
        cp_img2 = img_open.copy()
        cp_img2 = cp_img2.convert("RGB")

        w , h = cp_img2.size

        r_total = 0
        g_total = 0
        b_total = 0

        count = 0

        common_colors = []

        for x in range(0, w):
            for y in range(0, h):
                r, g, b = cp_img2.getpixel((x,y))

                r_total += r
                g_total += g
                b_total += b
                count += 1

                common_colors.append((int(r_total/count), int(g_total/count), int(b_total/count)))
        # print(common_colors)

        hex_common_colors = []
        for ten in range(0, n_colors):
            print(random.choice(common_colors))
            hex_triplet = f"#%02x%02x%02x" % random.choice(common_colors)
            print(hex_triplet.upper())
            hex_common_colors.append(hex_triplet.upper())

        img_open.close()

        return render_template("index.html", img=upload_image.filename,hex=hex_random_tuple, hex2 = hex_common_colors, hex_dom = hex_triplet_dominant_color.upper())

    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True, port=5010)
