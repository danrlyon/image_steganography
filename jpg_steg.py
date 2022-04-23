'''JPEG Steganography

    TODO:
    - Open Image
    - Access Pixels
    - Update pixel LSB with text
    - Read pixel LSB to build text

'''

from cgi import test
from os.path import exists
from tracemalloc import start
from xxlimited import new
from PIL import Image

start_image = 'jpeg_file_0.jpg'
# pixels = list(start_image.getdata())
END_OF_MESSAGE = "THAT'S ALL FOLKS!"
PREPEND_ENCODED = "secret_"
HIDER_BIT_POS = 3
SUPER_LONG_STRING = """
    Writing a super long string to test out this thing already yo.
    Hoping it works.
    Let's see how this all goes and if it works that would
    be sooooo cool and I would really like it.
"""


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
    while byte_index < 10000: #len(byte_list):
        temp_char = int(0)
        for i in range(8):
            print(f"Starting with {bin(byte_list[byte_index][byte_index % 3])}")
            print(f"Buffer is {bin(temp_char)}")
            bit_result = 1 if byte_list[byte_index][byte_index % 3] > 150 else 0
            print(f"Bit found: {bin(bit_result)}")
            temp_char += (bit_result << i)
            byte_index += 1
            # print(bin(byte_list[byte_index][byte_index % 3]))
            print(f"New buffer value: {bin(temp_char)}")

            # print(f"Starting with {bin(byte_list[byte_index][byte_index % 3])}")
            # print(f"Buffer is {bin(temp_char)}")
            # bit_result = (byte_list[byte_index][byte_index % 3] >> HIDER_BIT_POS) % 2
            # print(f"Bit found: {bin(bit_result)}")
            # temp_char = temp_char << 1
            # temp_char += bit_result
            # byte_index += 1
            # # print(bin(byte_list[byte_index][byte_index % 3]))
            # print(f"New buffer value: {bin(temp_char)}")
        result.append(temp_char)
        if  result.decode('utf-8')[-len(END_OF_MESSAGE):] == END_OF_MESSAGE:
            break
        # print(result)
    print(result.decode('utf-8'))


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
        print(bin(byte_letter))
        for _ in range(8):
            bit = byte_letter % 2
            # Alternate R->G->B values for each bit
            rgb_index = pixel_index % HIDER_BIT_POS
            img_bit = (temp[pixel_index][rgb_index] & (2 ** HIDER_BIT_POS)) >> HIDER_BIT_POS
            print(f"Bit: {bit}, Image Bit: {img_bit}")
            print(f"Current value to update: {bin(temp[pixel_index][rgb_index])}")
            if bit:
                temp[pixel_index][rgb_index] = 200
            else:
                temp[pixel_index][rgb_index] = 100
            print(temp[pixel_index])
            pixel_index += 1
            byte_letter = byte_letter >> 1
            # if bit == img_bit:
            #     print(f"Bits are equal, no change.")
            # if bit:
            #     temp[pixel_index][rgb_index] |= ((2 ** (HIDER_BIT_POS + 1)) - 1)
                
            # else:
            #     temp[pixel_index][rgb_index] &= ((2 ** 8) - 1) - (2 ** HIDER_BIT_POS)
            
            # temp[pixel_index][rgb_index] |= (2 ** (HIDER_BIT_POS -1))
            # temp[pixel_index][rgb_index] -= (2 ** (HIDER_BIT_POS-2) - 1)
            # print(f"Bit set to {bit}, new value: {bin(temp[pixel_index][rgb_index])}")
            # pixel_index += 1
            # byte_letter = byte_letter >> 1

            # bit = byte_letter % 2
            # if temp[pixel_index] % 2 != bit:
            #     if temp[pixel_index] < 200:
            #         temp[pixel_index] += 1
            #     else:
            #         temp[pixel_index] -= 1
            # pixel_index += 1
            # byte_letter = byte_letter >> 1
    
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
    # TODO: calculate maximum message length based on image
    # input_string = ""
    # while len(input_string) < 1:
    #     input_string = input("Enter message to hide in image: ")
    encoded_pixels = hide_bits(pixels, SUPER_LONG_STRING)
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
    new_image.save(
            new_filename,
            format="JPEG",
            quality=95,
            subsampling=0)#,
            # dpi=(new_image.size[0],
            # new_image.size[1]))
    test_image = Image.open(new_filename, 'r')
    


def main():
    '''Main Function'''
    # option_1 = input("Select option (encode or decode): ").lower()
    # while option_1 != "encode" and option_1 != "decode":
    #     print(f"Invalid Selection: {option_1}")
    #     option_1 = input("Select option (encode or decode): ").lower()

    # input_file = input(f"Select file to {option_1}:")
    # while not exists(input_file):
    #     print(f"The file, {input_file} does not exist.")
    #     input_file = input(f"Select file to {option_1}: ")
    # TODO: validate jpeg
    # if option_1 == "encode":
    #     encode_string(input_file)
    # elif option_1 == "decode":
    #     decode_string(input_file)
    encode_string(start_image)
    decode_string(f'{PREPEND_ENCODED}{start_image}')
    print("\nAll done! Good job!")  


if __name__ == '__main__':
    main()
