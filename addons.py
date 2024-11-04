from bs4 import BeautifulSoup
from requests import get
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