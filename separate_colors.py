import aspose.words as aw
import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog


def separate_colors(image_path, output_prefix):
    # Read the image
    img = cv2.imread(image_path)

    # Convert the image from BGR to RGB (OpenCV uses BGR by default)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Define color thresholds
    lower_green = np.array([0, 100, 0], dtype=np.uint8)
    upper_green = np.array([100, 255, 100], dtype=np.uint8)

    lower_red = np.array([100, 0, 0], dtype=np.uint8)
    upper_red = np.array([255, 100, 100], dtype=np.uint8)

    lower_white = np.array([200, 200, 200], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)

    # Create masks for each color
    mask_green = cv2.inRange(img_rgb, lower_green, upper_green)
    mask_red = cv2.inRange(img_rgb, lower_red, upper_red)
    mask_white = cv2.inRange(img_rgb, lower_white, upper_white)

    # Apply masks to the original image
    green_result = cv2.bitwise_and(img, img, mask=mask_green)
    red_result = cv2.bitwise_and(img, img, mask=mask_red)
    white_result = cv2.bitwise_and(img, img, mask=mask_white)

    # Apply blur to each image
    #ksize = (10,2)
    #green_result = cv2.blur(green_result, ksize)              
    #red_result = cv2.blur(red_result, ksize)                  
    #white_result = cv2.blur(white_result, ksize)              

    # Save each result as a separate image
    cv2.imwrite('G.png', green_result)
    cv2.imwrite('R.png', red_result)
    cv2.imwrite('W.png', white_result)

def browse_file():
    # open the file browser and get the file path
    fileName = filedialog.askopenfilename(filetypes=[('SVG Files', '*.svg')])
    # display the file path in the text field
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, fileName)

def generate():
    # get the file path from the text field
    fileName = file_path_entry.get()
    # create a document
    doc = aw.Document()

    # create a document builder and initialize it with document object
    builder = aw.DocumentBuilder(doc)

    # insert SVG image to document
    shape = builder.insert_image(fileName)

    # OPTIONAL
    # Calculate the maximum width and height and update page settings 
    # to crop the document to fit the size of the pictures.
    pageSetup = builder.page_setup
    pageSetup.page_width = shape.width
    pageSetup.page_height = shape.height
    pageSetup.top_margin = 0
    pageSetup.left_margin = 0
    pageSetup.bottom_margin = 0
    pageSetup.right_margin = 0

    # save as PNG
    doc.save("svg-to-png.png")
    input_image_path = "svg-to-png.png"
    output_prefix = 'output_image'

    # Separate colors and save as separate images
    separate_colors(input_image_path, output_prefix)
    os.remove("svg-to-png.png")

if __name__ == "__main__":
        # Replace 'input.svg' and 'output_prefix' with your SVG file path and desired output prefix
    # SVG file's path
    # fileName = "input.svg"


    # create a GUI window
    root = tk.Tk()
    root.title("RoboSketch Pre-Processing")

    # create a logo
    label = tk.Label(root, text="R⚙️B⚙️SKETCH", font=("Helvetica", 16, "bold"))
    label.pack()

    # create a browse button
    browse_button = tk.Button(root, text="Browse your Vector", command=browse_file)
    browse_button.pack()

    # create a text field to display the file path
    file_path_entry = tk.Entry(root, width=50)
    file_path_entry.pack()

    # create a generate button
    generate_button = tk.Button(root, text="Split Colors", command=generate)
    generate_button.pack()

    root.mainloop()



    