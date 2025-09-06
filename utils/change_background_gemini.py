from PIL import Image
import os
def change_background_to_black(image_path, output_path, white_threshold=220):
    """
    Changes the grey background of an image to black, preserving white rice grains and their shadows.

    This function iterates through each pixel of the input image. If a pixel's
    Red, Green, and Blue values are all above the 'white_threshold', it's
    considered part of the white rice grain and is preserved. All other pixels
    (which would be the grey background or the darker shadow) are changed to black (0,0,0).

    Args:
        image_path (str): The file path to the input image (e.g., 'my_image.png').
        output_path (str): The file path where the modified image will be saved
                           (e.g., 'output_image_black_bg.png').
        white_threshold (int): An integer between 0 and 255. Pixels with all
                               R, G, B values greater than this threshold are
                               considered "white" (part of the rice grain).
                               You might need to adjust this value based on the
                               exact shade of white of your rice and the grey
                               of your background. A higher value means only
                               very bright pixels are preserved; a lower value
                               preserves more, potentially including very light
                               grey areas.
    """
    try:
        print(f"Processing {image_path}")
        # Open the image file
        img = Image.open(image_path)

        # Convert the image to RGB mode if it's not already.
        # This ensures we are working with Red, Green, Blue channels.
        img = img.convert("RGB")

        # Load the pixel data. This allows direct pixel manipulation.
        pixels = img.load()

        # Get the dimensions of the image
        width, height = img.size
        counter = 0
        # Iterate over every pixel in the image
        for x in range(width):
            for y in range(height):
                # Get the RGB values of the current pixel
                r, g, b = pixels[x, y]
                # if r > white_threshold:
                #     print(r, g, b)

                # Check if the pixel's RGB values are all above the white_threshold.
                # This condition identifies pixels that are part of the white rice grain.
                if r > white_threshold and g > white_threshold and b > white_threshold:
                    # If it's part of the rice grain, leave it unchanged.
                    pass
                else:
                    # If it's not part of the white rice grain (i.e., it's the grey background
                    # or the darker shadow), change it to black.
                    pixels[x, y] = (0, 0, 0) # Set pixel to black (R=0, G=0, B=0)

        # Save the modified image to the specified output path
        img.save(output_path)
        print(f"Image successfully processed and saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: The input image file was not found at '{image_path}'.")
        print("Please ensure the image path is correct and the file exists.")
    except Exception as e:
        print(f"An unexpected error occurred during image processing: {e}")

# --- How to Use This Script ---
# 1.  **Save the script:** Save the code above into a Python file (e.g., `image_processor.py`).
# 2.  **Install Pillow:** If you don't have it, install the Pillow library:
#     `pip install Pillow`
# 3.  **Place your image:** Put the image you want to process in the same directory
#     as the script, or provide its full path.
# 4.  **Modify the example usage:**
#     -   Replace `'input_image.png'` with the actual name/path of your image.
#     -   Replace `'output_image_black_background.png'` with your desired output file name.
# 5.  **Run the script:** Open a terminal or command prompt, navigate to the directory
#     where you saved the script, and run:
#     `python image_processor.py`

# Example usage:
# Uncomment the line below and replace the placeholders with your actual file names.
# For instance, if your image is named 'rice_with_grey_bg.jpg' and you want
# the output as 'rice_with_black_bg.png':
# change_background_to_black('rice_with_grey_bg.jpg', 'rice_with_black_bg.png', white_threshold=220)

# Example with your actual image:
# change_background_to_black('data/train/rice_chintu/image.jpg', 'output_image.png', white_threshold=220)