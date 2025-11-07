from PIL import Image

def encode_image(image_path, message, output_path):
    img = Image.open(image_path).convert("RGB")
    message += "####END####"
    binary_message = ''.join(format(ord(i), "08b") for i in message)
    pixels = list(img.getdata())

    new_pixels = []
    msg_index = 0

    for pixel in pixels:
        r, g, b = pixel
        new_colors = []
        for color in (r, g, b):
            if msg_index < len(binary_message):
                new_color = (color & ~1) | int(binary_message[msg_index])
                msg_index += 1
            else:
                new_color = color
            new_colors.append(new_color)
        new_pixels.append(tuple(new_colors))

    img.putdata(new_pixels)
    img.save(output_path)
    print("✅ Message hidden inside", output_path)


def decode_image(image_path):
    img = Image.open(image_path).convert("RGB") 
    pixels = list(img.getdata())

    binary_message = ""
    for pixel in pixels:
        for color in pixel:
            binary_message += str(color & 1)

    bytes_ = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded = "".join(chr(int(b, 2)) for b in bytes_)
    message = decoded.split("####END####")[0]
    print("💬 Hidden message:", message)


image_path = " " # your image path 
message = "kia is awesome"
output_path = "awesome.png"

encode_image(image_path, message, output_path)
decode_image(output_path)