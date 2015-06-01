from zlib import compress, crc32


def wrap_chunk(chunk):
    length = (len(chunk) - 4).to_bytes(4, 'big')
    crc = crc32(chunk).to_bytes(4, 'big')
    return length + chunk + crc


def gen_ihdr(pixels):
    chunk_type = b'\x49\x48\x44\x52'
    width = len(pixels[0]).to_bytes(4, 'big')
    height = len(pixels).to_bytes(4, 'big')
    bit_depth = (8).to_bytes(1, 'big')
    color_type = (2).to_bytes(1, 'big')
    comp_method = (0).to_bytes(1, 'big')
    filt_method = (0).to_bytes(1, 'big')
    lace_method = (0).to_bytes(1, 'big')
    chunk = chunk_type + width + height + bit_depth \
        + color_type + comp_method + filt_method \
        + lace_method
    return wrap_chunk(chunk)


def pixel_to_bytes(pixel):
    red = pixel[0]
    green = pixel[1]
    blue = pixel[2]
    data = red.to_bytes(1, 'big')
    data += green.to_bytes(1, 'big')
    data += blue.to_bytes(1, 'big')
    return data


def gen_idat(pixels):
    chunk_type = b'\x49\x44\x41\x54'
    data = b''
    filter_type = b'\x00'
    for row in pixels:
        data += filter_type
        for pixel in row:
            data += pixel_to_bytes(pixel)
    chunk = chunk_type + compress(data, 0)
    return wrap_chunk(chunk)


def gen_iend():
    chunk_type = b'\x49\x45\x4E\x44'
    return wrap_chunk(chunk_type)


def gen_png_data(pixels):
    png_sig = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    ihdr = gen_ihdr(pixels)
    idat = gen_idat(pixels)
    iend = gen_iend()
    data = png_sig + ihdr + idat + iend
    return data


def main():
    pixels = []
    for i in range(255):
        row = []
        for j in range(255):
            row.append((i, j, (i+j)//2))
        pixels.append(row)
    data = gen_png_data(pixels)
    with open('tmp.png', 'wb') as f:
        f.write(data)

if __name__ == '__main__':
    main()
