from PIL import Image

def extract_lsb(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    bits = []
    for pixel in pixels:
        if isinstance(pixel, tuple):
            for val in pixel:
                bits.append(str(val & 1))
        else:
            bits.append(str(pixel & 1))
            
    # Convert bits to bytes
    bytes_arr = []
    for i in range(0, len(bits), 8):
        byte = "".join(bits[i:i+8])
        if len(byte) == 8:
            bytes_arr.append(int(byte, 2))
            
    data = bytes(bytes_arr)
    print(data[:200])

if __name__ == "__main__":
    extract_lsb("junior_developer.png")
