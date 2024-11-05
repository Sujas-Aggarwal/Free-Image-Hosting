from utility import FreeImageHoster
import argparse
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Download Image from URL')
    parser.add_argument('--link', '--l', type=str, help='Indirect link to the image')
    parser.add_argument('--image', '--i', type=str, help='Name of the image to be saved')
    args = parser.parse_args()
    FreeImageHoster.ScrapeImageFromLink(link=args.link,image_name= args.image)
    # FreeImageHoster.UploadImage("input/IMG20240813225308.jpg")