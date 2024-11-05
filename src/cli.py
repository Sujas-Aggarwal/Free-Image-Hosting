import os
from src.driver import Driver
class CLIInterface:
    def ValidatedInput(self,prompt,filter,error_message="Invalid Input"):
        print(prompt)
        a = input()
        if a=="exit":
            exit()
        elif a=="help":
            self.displayHelp()
            return self.ValidatedInput(prompt,filter)
        elif a=="restart":
            self.start()
            return
        if filter(a):
            return a
        else:
            print(error_message,f"'{a}'")
            return self.ValidatedInput(prompt,filter)

    def start(self):
        print("CLI Interface Started")
        print("Enter 'help' for help")
        self.chooseTask()

    def displayHelp(self):
        print("Help:")
        print("1. To download image from URL, use 'download'")
        print("2. To upload image from path, use 'upload'")
        print("3. To convert links from indirect to direct, use 'convert'")
        print("4. To exit, use 'exit'")
        print("5. To restart, use 'restart'")
        print("6. To display this help, use 'help'")

    def downloadImage(self):
        link = self.ValidatedInput("Enter the link of the image",lambda x:x.find(".")!=-1,"Please Enter a Valid Link")
        download_path = self.ValidatedInput("Enter the path to download the image",lambda x:os.path.exists(x),"Path does not Exist")
        download_path = os.path.abspath(download_path)
        if link.find(","):
            links = link.split(",")
            Driver.downloadAllImages(links,save_path=download_path)
        else:
            Driver.downloadImage(link,save_path=download_path)
    
    def uploadImage(self):
        path = self.ValidatedInput("Enter the path of the image",lambda x:x.find(",") or os.path.exists(x),"Path does not Exist")
        if path.find(",")!=-1:
            paths = path.split(",")
            Driver.uploadAllImages(paths)
        else:
            Driver.uploadImage(path)
    
    def convertLink(self):
        link = self.ValidatedInput("Enter the link to be converted",lambda x:x.find(".")!=-1,"Please Enter a Valid Link")
        if link.find(","):
            links = link.split(",")
            Driver.convertAllLinks(links)
        else:
            Driver.convertLink(link)


    def chooseTask(self):
        task = self.ValidatedInput("Enter the task to be performed",lambda x:x in ["download","upload","convert","c","d","u"],"Invalid Task")
        if task=="download" or task=="d":
            self.downloadImage()
        elif task=="upload" or task=="u":
            self.uploadImage()
        elif task=="convert" or task=="c":
            self.convertLink()
        return self.chooseTask()
