from bs4 import BeautifulSoup
from requests import get,post
class Addons:
    def GetSourceCode(url):
        try:
            response = get(url)
        except Exception as e:
            print(e)
            return
        return response.text
    def GetGeneralDirectLink(indirect_link):
        source_code = Addons.GetSourceCode(indirect_link)
        try:
            assert source_code!=None
        except AssertionError:
            return
        source_code_soup = BeautifulSoup(source_code, 'html.parser')
        direct_link = source_code_soup.find("img")['src']
        return direct_link
    def GetDirectLinkFromPostImg(indirect_link:str="",source_code:str=""):
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
    def UploadImageOnPostImg(image,image_name):
        SESSION_ID = '0000000000000000000'
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
        source_code = get(response['url'])
        source_code=  source_code.text
        source_code_soup = BeautifulSoup(source_code,"html.parser")
        direct_link = source_code_soup.find("input",id="code_direct")['value']
        return direct_link
