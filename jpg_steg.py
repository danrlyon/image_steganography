'''JPEG Steganography

    TODO:
    - Open Image
    - Access Pixels
    - Update pixel LSB with text
    - Read pixel LSB to build text

'''

from os.path import exists
from PIL import Image

start_image = Image.open('jpeg_file_0.jpg', 'r')
pixels = list(start_image.getdata())


def decode_string(input_file):
    '''Extract the string from the image file'''
    pass


def encode_string(input_file):
    '''Get input string to hide in JPEG file'''
    pass


def main():
    '''Main Function'''
    option_1 = input("Select option (encode or decode):").lower()
    while option_1 != "encode" and option_1 != "decode":
        print(f"Invalid Selection: {option_1}")
        option_1 = input("Select option (encode or decode):").lower()

    input_file = input(f"Select file to {option_1}:")
    while not exists(input_file):
        print(f"The file, {input_file} does not exist.")
        input_file = input(f"Select file to {option_1}:")

    if option_1 == "encode":
        encode_string(input_file)
    elif option_1 == "decode":
        decode_string(input_file)

    print("\nAll done! Good job!")    


if __name__ == '__main__':
    main()
