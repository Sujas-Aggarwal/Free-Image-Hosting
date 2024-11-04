from requests import get
from bs4 import BeautifulSoup
from addons import Addons
class ImageDownloaderFromURL:
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
            else:
                direct_link = Addons.GetGeneralDirectLink(indirect_link)
        except Exception as  e:
            print('Error in getting direct link!')
            print(e)
            return
        try:
            assert direct_link!=indirect_link
        except AssertionError:
            print('Direct link not found for given indirect url!')
            return
        print(f"Converted {indirect_link} to {direct_link}")
        return direct_link

    def DownloadImage(image_link, image_name = 'output/image.jpg'):
        image = get(image_link)
        try:
            assert image.status_code == 200
        except AssertionError:
            print('Image not found!')
            return
        try:
            with open(image_name, 'wb') as file:
                file.write(image.content)
        except Exception as e:
            print('Error in saving image!')
            print(e)
            return
        

    def ScrapeImageFromLink(indirect_link="",direct_link="", image_name = 'output/image.jpg'):
        try:
            assert indirect_link or direct_link
        except AssertionError:
            print('Please provide either indirect_link or direct_link')
            return
        try:
            if direct_link:
                ImageDownloaderFromURL.DownloadImage(image_link, image_name)
            else:
                image_link = ImageDownloaderFromURL.GetDirectLink(indirect_link)
                ImageDownloaderFromURL.DownloadImage(image_link, image_name)
        except:
            return
        print('Image downloaded successfully!')