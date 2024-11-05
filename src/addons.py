from bs4 import BeautifulSoup
import secrets
from requests import get,post
from src.config import Config
class Addons:
    supported_formats = ["jpg","jpeg","webp","png","heic","gif"]
    def GetSourceCode(url):
        try:
            response = get(url,allow_redirects=True)
        except Exception as e:
            print(e)
            return
        return response.text
    def GetGeneralDirectLink(indirect_link):
        if Addons.IsLinkDirect(indirect_link):
            return indirect_link
        source_code = Addons.GetSourceCode(indirect_link)
        try:
            assert source_code!=None
        except AssertionError:
            return
        source_code_soup = BeautifulSoup(source_code, 'html.parser')
        direct_link = source_code_soup.find("img")['src']
        return direct_link
    def GetDirectLinkFromPostImg(indirect_link:str="",source_code:str=""):
        if indirect_link and Addons.IsLinkDirect(indirect_link):
            return indirect_link
        assert indirect_link or source_code
        if indirect_link:
            source_code = Addons.GetSourceCode(indirect_link)
            try:
                assert source_code!=None
            except AssertionError:
                return
        try:
            source_code_soup = BeautifulSoup(source_code, 'html.parser')
            direct_link = source_code_soup.find("img",id="main-image")['src']
        except Exception as e:
            print('Error in getting direct link!')
            print(e)
            return
        return direct_link
    def GetDirectLinkFromImgur(indirect_link:str="",source_code:str=""):
        if indirect_link and Addons.IsLinkDirect(indirect_link):
            return indirect_link
        assert indirect_link or source_code
        if indirect_link:
            source_code = Addons.GetSourceCode(indirect_link)
            try:
                assert source_code!=None
            except AssertionError:
                return
        try:
            source_code_soup = BeautifulSoup(source_code, 'html.parser')
            print(source_code_soup.prettify())
            all_images = source_code_soup.findAll("img")
            for image in all_images:
                if image['class']=="image-placeholder" and image['src'].find("i.imgur.com")!=-1:
                    return image['src']
        except Exception as e:
            print('Error in getting direct link!')
            print(e)
            return
    def UploadImageOnPostImg(image,image_name):
        SESSION_ID = secrets.randbits(64) 
        image_extension = image_name.split(".")[-1]
        url = "https://postimages.org/json/rr"
        payload = {'optsize': '0',
        'expire': '0',
        'numfiles': '1',
        'upload_session':SESSION_ID,
        'gallery': ''}
        files=[
        ('file',(image_name,image,f'image/{image_extension}'))
        ]
        headers = {
        'Cache-Control': 'no-cache',
        'Referer': 'https://postimages.org/',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json'
        }

        try:
            response = post(url, headers=headers, data=payload, files=files)
            response = response.json()
        except Exception as e:
            return            
        # Since PostImg does not directly provide the indirect link but provide the indirect indirect link, we need to use a different method of direct link finding
        source_code = Addons.GetSourceCode(response['url'])
        source_code_soup = BeautifulSoup(source_code,"html.parser")
        direct_link = source_code_soup.find("input",id="code_html")['value']
        direct_link = Addons.GetDirectLinkFromPostImg(direct_link)
        return direct_link
    def IsLinkDirect(link):
        try:
            response = get(link)
        except Exception as e:
            print(e,"Unable to Fetch Response")
        response_type = response.headers.get("Content-Type")
        if response_type==None:
            return False
        if response_type.split("/")[0]=="image":
            return True
        return False
    def UploadImageOnFreeHost(image,image_name):
        url = "https://freeimage.host/api/1/upload"
        payload = {'key': Config.API_KEYS["FREEIMAGEHOST_API_KEY"]}
        files=[
        ('source',(image_name,image,f'image/{image_name.split(".")[-1]}'))
        ]
        headers = {
        'Accept': 'application/json'
        }
        try:
            response = post(url, headers=headers, data=payload, files=files)
            response = response.json()
        except Exception as e:
            print(e)
            return
        return response['image']['url']