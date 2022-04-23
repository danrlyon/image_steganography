'''JPEG Steganography

'''
from os.path import exists
from PIL import Image
from hashlib import md5


END_OF_MESSAGE = "THAT'S ALL FOLKS!"
PIXEL_SPACING = 1
PREPEND_ENCODED = "secret_"


def decode_string(input_file):
    '''Extract the string from the image file'''
    print("Start decoding.")
    result = bytearray(b'')
    with Image.open(input_file, 'r') as image:
        pixels = list(image.getdata())
        byte_list = list()
        for pixel in pixels:
            byte_list.append(list(pixel))
    print("Incoming pixels:")
    print(pixels[:10])
    byte_index = 0
    # rgb_index = 0
    while byte_index < len(byte_list):
        temp_char = int(0)
        for i in range(8):
            # print(f"Starting with {bin(byte_list[byte_index][byte_index % 3])}")
            # print(f"Buffer is {bin(temp_char)}")
            bit_result = 1 if byte_list[byte_index][byte_index % 3] > 120 else 0
            # print(f"Bit found: {bin(bit_result)}")
            temp_char += (bit_result << i)
            byte_index += PIXEL_SPACING
            # print(bin(byte_list[byte_index][byte_index % 3]))
            # print(f"New buffer value: {bin(temp_char)}")

        result.append(temp_char)
        # print(result.decode('utf-8'))
        if  result.decode('utf-8')[-len(END_OF_MESSAGE):] == END_OF_MESSAGE:
            break
        # print(result)
    print("\nSuper secret message found!\n")
    print("*---------------------------------------------------*")
    print(result.decode('utf-8')[:-len(END_OF_MESSAGE)])
    print("*---------------------------------------------------*")

def hide_bits(pixels, message):
    '''Update the LSB of each byte in the pixel'''
    print("Starting to hide bits. Incoming pixels:")
    print(pixels[:10])
    temp = list()
    # Flatten bytes
    for pixel in pixels:
        temp.append(list(pixel))
    # Encode message so each character is a byte
    message = [ord(c) for c in f"{message}{END_OF_MESSAGE}"]
    pixel_index = 0
    for byte_letter in message:
        # print(bin(byte_letter))
        for _ in range(8):
            bit = byte_letter % 2
            # Alternate R->G->B values for each bit
            rgb_index = pixel_index % 3
            # img_bit = (temp[pixel_index][rgb_index] & (2 ** HIDER_BIT_POS)) >> HIDER_BIT_POS
            # print(f"Bit: {bit}, Image Bit: {img_bit}")
            # print(f"Current value to update: {bin(temp[pixel_index][rgb_index])}")
            if bit:
                temp[pixel_index][rgb_index] = 140
            else:
                temp[pixel_index][rgb_index] = 100
            # print(temp[pixel_index])
            pixel_index += PIXEL_SPACING
            byte_letter = byte_letter >> 1

    result = list()
    pixel_count = len(pixels)
    current_pixel = 0
    while current_pixel < pixel_count:
        result.append((
                temp[current_pixel][0],
                temp[current_pixel][1],
                temp[current_pixel][2]))
        current_pixel += 1
    print("Outgoing pixels after bit hiding:")
    print(result[:10])
    return result


def encode_string(input_file):
    '''Get input string to hide in JPEG file'''
    image = Image.open(input_file, 'r')
    new_image = image.copy()
    print(f"Image Size: {new_image.size}")
    pixels = list(new_image.getdata())
    pixel_count = len(pixels)
    print(f"Total number of pixels: {pixel_count}")
    writeable_bytes = pixel_count * 3
    print(f"Maximum message size: {writeable_bytes}")
    input_string = ""
    while len(input_string) < 1:
        input_string = input("Enter message to hide in image: ")
    encoded_pixels = hide_bits(pixels, input_string)
    i, j = 0, 0
    for pixel in encoded_pixels:
        new_image.putpixel((i, j), pixel)
        if i == new_image.size[0] - 1:
            i = 0
            j += 1
        else:
            i += 1
    new_filename = f"{PREPEND_ENCODED}{input_file}"
    new_image.save(
            new_filename,
            format="JPEG",
            quality=95,
            subsampling=0)
    print(f"\nOriginal File: {input_file}, MD5 Hash: {hash_file(input_file)}")
    print(f"Modified File: {new_filename}, MD5 Hash: {hash_file(new_filename)}")


def hash_file(input_file):
    '''Take input file and return hashed hex string'''
    with open(input_file, 'rb') as in_f:
        hash_hex = md5(in_f.read()).hexdigest()
        return hash_hex


def main():
    '''Main Function'''
    option_1 = input("Select option (embed or extract): ").lower()
    while option_1 != "embed" and option_1 != "extract":
        print(f"Invalid Selection: {option_1}")
        option_1 = input("Select option (embed or extract): ").lower()

    input_file = input(f"Select file to {option_1}: ")
    while not exists(input_file) or "jpg" not in input_file.lower():
        print(f"The file, {input_file} does not exist, or is not a JPEG.")
        input_file = input(f"Select file to {option_1}: ")

    if option_1 == "embed":
        encode_string(input_file)
    elif option_1 == "extract":
        decode_string(input_file)

    print("\nAll done! Good job!")


if __name__ == '__main__':
    main()
