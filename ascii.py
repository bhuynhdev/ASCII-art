from PIL import Image, ImageEnhance
import os
import lightness

# 65 characters correspond to 65 level of brightness
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def resize_keep_ratio(image, new_width=300):
    """ Resize image to fit terminal screen, but keep aspect ratio """
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height
    new_height = round(new_width / aspect_ratio)
    print(f"Resized image to {new_width} x {new_height}")
    return image.resize((new_width, new_height))

def change_contrast(image, ratio):
    ImContrast = ImageEnhance.Contrast(image)
    print(f"Changed contrast to {ratio} of the original.")
    return ImContrast.enhance(ratio)


def pixel_to_grayscale(R, G, B):
    return (0.2989 * R + 0.587 * G + 0.114 * B)


def make_ascii(Image, ASCII_CHARS, outfile):
    # Iterate pixel matrix
    x, y = Image.size
    for row in range(y):
        for col in range(x):
            R, G, B = Image.getpixel((col,row))

            # Change RGB to single brightness scale
            brightness = pixel_to_grayscale(R, G, B)

            # Covert to range of (0, 69) to correspond with 70 ASCII chars
            bright_ascii = round(69 * brightness / 255)

            # Print each character two times to prevent image squashing
            outfile.write(ASCII_CHARS[bright_ascii] * 2)
        # Print new line for next row
        outfile.write("\n")
    
    # Outout success message
    print(f"Successfully wrote to {outfile.name}")


if __name__ == "__main__":
    image_path = input("Enter image path: ")
    
    # Outpath = filename(without extension) + "TXT"
    out_path = os.path.basename(image_path).split('.')[0] + ".txt"

    # Open image file
    try:
        Im = Image.open(image_path)
    except FileNotFoundError:
        print("File not found. Check path again.")
    else:
        print("Successfully loaded image")
        print(Im.size)

    # Open output file for writing 
    with open(out_path, 'w') as ascii_text:
        # Resize image to fit screen
        Im_smaller = resize_keep_ratio(Im, 300)

        # Increase contrast for better ASCII art
        Im_contrast = change_contrast(Im_smaller, 2.1)

        # Create ASCII Art and write out to file
        make_ascii(Im_contrast, ASCII_CHARS, ascii_text)
