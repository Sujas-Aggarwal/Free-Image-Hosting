from requests import get,post
from addons import Addons
from pathlib import Path
class FreeImageHoster:
    def GetSourceCode(url):
        try:
            response = get(url)
        except Exception as e:
            print(e)
            return
        return response.text
    
    def GetDirectLink(indirect_link):
        direct_link = indirect_link
        try:
            if indirect_link.find("postimg.cc")!=-1:
                direct_link = Addons.GetDirectLinkFromPostImg(indirect_link)
            elif indirect_link.find("imgur.com")!=-1:
                direct_link = Addons.GetDirectLinkFromImgur(indirect_link)
            else:
                direct_link = Addons.GetGeneralDirectLink(indirect_link)
        except Exception as  e:
            print('Error in getting direct link!')
            print(e)
            return
        try:
            assert direct_link!=indirect_link and direct_link!=None
        except AssertionError:
            return
        print(f"Converted {indirect_link} to {direct_link}")
        return direct_link

    def DownloadImage(image_link, image_name = 'image.jpg'):
        image = get(image_link)
        file_name = ("image" if image_name==None else image_name) +"."+ image_link.split('.')[-1]
        try:
            assert image.status_code == 200
        except AssertionError:
            print('Image not found!')
            return
        try:
            with open(Path("output/"+file_name), 'wb') as file:
                file.write(image.content)
        except Exception as e:
            print(e)
            return

    def ScrapeImageFromLink(link="", image_name = 'output/image.jpg'):
        try:
            image_link = FreeImageHoster.GetDirectLink(link)
            FreeImageHoster.DownloadImage(image_link, image_name)
        except Exception as e:
            print("Unable to Download Image")
            return
        print('Image downloaded successfully!')
    def UploadImage(image_path:str):
        assert Path(image_path).exists()
        image = open(image_path, 'rb')
        image_name = image_path.split("/")[-1]
        assert image_name.split(".")[-1] in Addons.supported_formats
        try:
            response = Addons.UploadImageOnPostImg(image,image_name=image_name)
            print(response)
        except Exception as e:
            print("Error Uploading Image")
            print(e)