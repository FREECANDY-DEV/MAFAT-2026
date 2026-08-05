from PIL import Image

def crop_laptop(input_path, output_path):
    img = Image.open(input_path)
    # the laptop is roughly in the right-middle area
    width, height = img.size
    # let's crop the right half
    box = (width//2, height//4, width, height)
    cropped = img.crop(box)
    cropped.save(output_path)

if __name__ == "__main__":
    crop_laptop("junior_developer.png", "laptop.png")
