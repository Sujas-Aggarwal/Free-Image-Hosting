from utility import ImageDownloaderFromURL
import argparse
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Download Image from URL')
    parser.add_argument('--indirect_link', '--il', type=str, help='Indirect link to the image')
    parser.add_argument('--direct_link', '--dl', type=str, help='Direct link to the image')
    parser.add_argument('--image_name', '--in', type=str, help='Name of the image to be saved')
    args = parser.parse_args()
    ImageDownloaderFromURL.ScrapeImageFromLink(direct_link=args.direct_link, indirect_link=args.indirect_link,image_name= args.image_name)