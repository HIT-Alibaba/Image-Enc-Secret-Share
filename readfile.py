# filename = "DECENC_img.bmp"
filename = "img.bmp"
f = open(filename, 'rb')
buf = f.read()
f.close()
print(buf)