from src.utility import FreeImageHoster
from src.addons import Addons
import os
storage = []
images = [i for i in os.listdir("input") if i.split(".")[-1] in Addons.supported_formats]
if not os.path.exists("./storage.txt"):
    with open("storage.txt","w") as file:
        file.close()
for image in images:
    try:
        link = FreeImageHoster.UploadImage(image_path = "input/"+image)
        storage.append(link+"\n")
        print("File Uploaded Successfully as ",image,end="")
        print(" to link ",link)
    except Exception as e:
        print(e)
        print("File Upload Unsuccessfull for ",image)
with open("storage.txt","+a") as file:
    file.writelines(storage)