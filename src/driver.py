from src.utility import FreeImageHoster
import os
class Driver:
    def uploadAllImages(paths):
        print("INFO: Upload Started")
        storage = []
        for image in paths:
            image = os.path.abspath(image)
            try:
                link = FreeImageHoster.UploadImage(image_path = image)
                storage.append(link+"\n")
                print("SUCCESS: File Uploaded Successfully to",link)
            except Exception as e:
                print(e)
                print("ERROR: File Upload Unsuccessfull for",image)
        with open("storage.txt","+a") as file:
            file.writelines(storage)
        for i in storage:
            print(i,end=",")
    def downloadAllImages(links,save_path = "output/"):
        print("INFO: Download Started")
        for link in links:
            try:
                FreeImageHoster.ScrapeImageFromLink(link,save_path=save_path)
                print("SUCCESS: Image Downloaded Successfully from link",link)
            except Exception as e:
                print(e)
                print("ERROR: Image Download Unsuccessfull from link",link)
    def convertAllLinks(links):
        print("INFO: Conversion Started")
        direct_links = []
        for link in links:
            try:
                direct_link = FreeImageHoster.GetDirectLink(link)
                print("SUCCESS: Converted",link,"to",direct_link)
                direct_links.append(direct_link)
            except Exception as e:
                print(e)
                print("ERROR: Unable to convert",link)
        for i in direct_links:
            print(i,end=",")
    def downloadImage(link,save_path = "output/"):
        print("INFO: Download Started", save_path)
        try:
            FreeImageHoster.ScrapeImageFromLink(link,save_path=save_path)
            print("SUCCESS: Image Downloaded Successfully from link",link)
        except Exception as e:
            print(e)
            print("ERROR: Image Download Unsuccessfull from link",link)
    def uploadImage(image_path):
        print("INFO: Upload Started")
        try:
            link = FreeImageHoster.UploadImage(image_path)
            print("SUCCESS: File Uploaded Successfully to",link)
        except Exception as e:
            print(e)
            print("ERROR: File Upload Unsuccessfull for",image_path)
    def convertLink(link):
        print("INFO: Conversion Started")
        try:
            direct_link = FreeImageHoster.GetDirectLink(link)
            print("SUCCESS: Converted",link,"to",direct_link)
        except Exception as e:
            print(e)
            print("ERROR: Unable to convert",link)