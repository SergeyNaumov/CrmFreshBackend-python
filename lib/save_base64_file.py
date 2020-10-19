def save_base64_file(save_to,data):
    fh = open("imageToSave.png", "wb")
    fh.write(img_data.decode('base64'))
    fh.close()