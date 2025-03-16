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
            print('ERROR: Error in getting direct link!')
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
            all_images = source_code_soup.findAll("img")
            for image in all_images:
                if image['class']=="image-placeholder" and image['src'].find("i.imgur.com")!=-1:
                    return image['src']
        except Exception as e:
            print('ERROR: Error in getting direct link!')
            print(e)
            return

    def UploadImageOnFreeHost(image, image_name):
        """
        Upload an image to freeimage.host and return the direct URL.
        
        Args:
            image: Either file content (bytes) or a path to the image file (str)
            image_name: Name of the image file with extension
        
        Returns:
            str: Direct URL to the uploaded image or None if upload fails
        """
        url = "https://freeimage.host/api/1/upload"
        payload = {'key': Config.API_KEYS["FREEIMAGEHOST_API_KEY"]}
        
        # Determine if image is a path (string) or file content (bytes)
        if isinstance(image, str):
            # Convert relative path to absolute path
            image_path = os.path.abspath(image)
            if not os.path.exists(image_path):
                print(f"ERROR: File not found at {image_path}")
                return None
                
            try:
                with open(image_path, 'rb') as f:
                    image_content = f.read()
            except Exception as e:
                print(f"ERROR: Unable to read file - {e}")
                return None
        else:
            # Assume image is already file content (bytes)
            image_content = image
        
        # Get the file extension from image_name
        image_extension = image_name.split(".")[-1]
        mime_type = f'image/{image_extension}'
        
        files = [
            ('source', (image_name, image_content, mime_type))
        ]
        headers = {
            'Accept': 'application/json'
        }
        
        try:
            response = post(url, headers=headers, data=payload, files=files)
            response.raise_for_status()  # Raise an exception for bad status codes
            response_json = response.json()
            return response_json['image']['url']
        except Exception as e:
            print(f"ERROR: Upload failed - {e}")
            return None

    # Example usage:
    # With absolute path:
    # url = UploadImageOnFreeHost("/home/user/images/test.jpg", "test.jpg")

    # With relative path:
    # url = UploadImageOnFreeHost("../images/test.png", "test.png")

    # With file content:
    # with open("test.jpg", "rb") as f:
    #     url = UploadImageOnFreeHost(f.read(), "test.jpg")