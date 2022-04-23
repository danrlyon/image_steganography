'''PNG Steganography

    TODO:
    - Open Image
    - Access Pixels
    - Update pixel LSB with text
    - Read pixel LSB to build text

'''
from os.path import exists
from PIL import Image
from hashlib import md5


PREPEND_ENCODED = "secret_"
END_OF_MESSAGE = "THAT'S ALL FOLKS!"


def decode_string(input_file):
    '''Extract the string from the image file'''
    print("Starting to decode.")
    result = ''
    with Image.open(input_file, 'r') as image:
        pixels = list(image.getdata())
        byte_list = list()
        for pixel in pixels:
            byte_list.extend(list(pixel))
    # print(byte_list[:10])
    byte_index = 0
    while byte_index < len(byte_list):
        temp_char = int(0)
        for i in range(8):
            temp_char += (byte_list[byte_index] % 2) << i
            byte_index += 1
        result += str(chr(temp_char))
        if  result[-len(END_OF_MESSAGE):] == END_OF_MESSAGE:
            break
    print("\nSuper secret message found!\n")
    print("*---------------------------------------------------*")
    print(result[:-len(END_OF_MESSAGE)])
    print("*---------------------------------------------------*")


def hide_bits(pixels, message):
    '''Update the LSB of each byte in the pixel'''
    temp = list()
    # Flatten bytes
    for pixel in pixels:
        temp.extend(list(pixel))
    # Encode message so each character is a byte
    message = f"{message}{END_OF_MESSAGE}".encode("utf-8")
    pixel_index = 0
    for byte_letter in message:
        for _ in range(8):
            bit = byte_letter % 2
            if temp[pixel_index] % 2 != bit:
                if temp[pixel_index] < 200:
                    temp[pixel_index] += 1
                else:
                    temp[pixel_index] -= 1
            pixel_index += 1
            byte_letter = byte_letter >> 1
    
    result = list()
    pixel_count = len(pixels)
    current_pixel = 0
    while current_pixel < pixel_count:
        result.append((
                temp[current_pixel],
                temp[current_pixel + 1],
                temp[current_pixel + 2]))
        current_pixel += 3
    print(result[:10])
    return result


def encode_string(input_file):
    '''Get input string to hide in JPEG file'''
    # Since the transparent pixels are an issue, convert to a white
    # background. This has no effect if there are no transparent pixels.
    image = Image.open(input_file, 'r').convert('RGBA')
    background = Image.new('RGBA', image.size, (255, 255, 255))
    new_image = Image.alpha_composite(background, image).convert('RGB')

    print(f"Image Size: {new_image.size}")
    pixels = list(new_image.getdata())
    pixel_count = len(pixels)
    print(f"Total number of pixels: {pixel_count}")
    writeable_bytes = pixel_count * 3
    print(f"Maximum message size: {writeable_bytes}")
    input_string = ""
    while len(input_string) < 1:
        input_string = input("Enter message to hide in image: ")
    # print(pixels)
    encoded_pixels = hide_bits(pixels, input_string)
    i, j = 0, 0
    for pixel in encoded_pixels:
        new_image.putpixel((i, j), pixel)
        if i == new_image.size[0] - 1:
            i = 0
            j += 1
        else:
            i += 1
    # print(new_image.getpixel((0, 0)))
    # print(new_image.load()[0, 0], new_image.getdata()[1], new_image.getdata()[2])
    new_filename = f"{PREPEND_ENCODED}{input_file}"
    new_image.save(new_filename, format="PNG")
    print(f"\nOriginal File: {input_file}, MD5 Hash: {hash_file(input_file)}")
    print(f"Modified File: {new_filename}, MD5 Hash: {hash_file(new_filename)}")


def hash_file(input_file):
    '''Take input file and return hashed hex string'''
    with open(input_file, 'rb') as in_f:
        hash_hex = md5(in_f.read()).hexdigest()
        return hash_hex


def main():
    '''Main Function'''
    option_1 = input("Select option (encode or decode): ").lower()
    while option_1 != "encode" and option_1 != "decode":
        print(f"Invalid Selection: {option_1}")
        option_1 = input("Select option (encode or decode): ").lower()

    input_file = input(f"Select file to {option_1}:")
    while not exists(input_file) or "png" not in input_file:
        print(f"The file, {input_file} does not exist.")
        input_file = input(f"Select file to {option_1}: ")

    if option_1 == "encode":
        encode_string(input_file)
    elif option_1 == "decode":
        decode_string(input_file)

    print("\nAll done! Good job!")


if __name__ == '__main__':
    main()
