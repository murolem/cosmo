# trying to read the data using 2 bits per channel and without alpha

import gzip
from PIL import Image

def retrieve_low_order_bits_from_png(image_path, num_bits):
    # Open the PNG image
    image = Image.open(image_path)

    # Get the pixel data
    pixels = image.load()

    # Retrieve the low-order bits from each pixel channel
    data = bytearray()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]  # Adjust the order of color channels

            # Retrieve the low-order bits from red, green, blue, and alpha channels
            r_low = r & ((1 << num_bits) - 1) # line 103 get 2 bits per channel
            g_low = g & ((1 << num_bits) - 1)
            b_low = b & ((1 << num_bits) - 1)
            # a_low = a & ((1 << num_bits) - 1) line 103 0 bit used to store on the alpha channel

            # Combine the low-order bits into a byte and append it to the data bytearray
            byte = (r_low << (2 * num_bits)) | (g_low << num_bits) | b_low # | a_low
            data.append(byte)

    return data

# Usage example
image_path = "decode_ship_data/ship.png"
num_bits = 2
low_order_bits_data = retrieve_low_order_bits_from_png(image_path, num_bits)

print(low_order_bits_data)

decompressed_data = gzip.decompress(low_order_bits_data)
print(decompressed_data)

## trying bruteforce header ?
import gzip

def decompress_data_with_headers(compressed_data, headers):
    for header in headers:
        try:
            compressed_data_with_header = header + compressed_data
            decompressed_data = gzip.decompress(compressed_data_with_header)

            return decompressed_data

        except OSError:
            continue

    # If none of the headers succeed in decompression
    raise ValueError("Unable to decompress data with the given headers.")


# Usage example
compressed_data = low_order_bits_data

headers = [
    #b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03',
    #b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x02',
    b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x01'
]

try:
    decompressed_data = decompress_data_with_headers(compressed_data, headers)
    print(decompressed_data.decode('utf-8'))

except ValueError as e:
    print(str(e))