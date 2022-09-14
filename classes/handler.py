from classes.variables import *


class ImageHandler:
    def __init__(self, imageURL, desc):
        self.__imageURL = imageURL 
        self.__cookie = get_random_cookie()
        self.__description = desc
        self.__proxy = None
        self.newproxy()
        self.writexml()

    def getcsrf(self):
        print(self.__proxy["http"])
        csrf_request = requests.post("https://www.roblox.com", cookies={".ROBLOSECURITY":self.__cookie}, headers={"User-Agent":USER_AGENT}, proxies=self.__proxy)
        csrf_regex = re.findall(r'data-token=\"(.+)\"', csrf_request.text)
        csrf_token = csrf_regex[0]
        return csrf_token

    def newproxy(self):
        le = random.choice(open("proxies.txt").readlines()).split(":")
        self.__proxy = {
            "http":"http://"+le[2] + ":" + le[3] + "@" +le[0] +":"+le[1],
            "https":"http://"+le[2] + ":" + le[3] + "@" +le[0] +":"+le[1]
        }


    def writexml(self):
        print(colored("[PixelBypass] - Preparing .rbxmx file...", "blue"))
        print(colored("[PixelBypass] - Using proxy: "+self.__proxy["http"], "blue"))
        image_bytes = requests.get(self.__imageURL)
        image_object = Image.open(BytesIO(image_bytes.content))

        if image_object.height != 250 or image_object.width != 250:
            print(colored("[PixelBypass] - Image size mismatch, resizing...", "blue"))

            image_object_resized = image_object.resize((250,250))
            image_object_buff = BytesIO()
            image_object_resized.save(image_object_buff, format="PNG", optimiize=True)
            image_object = Image.open(image_object_buff)

            print(colored("[PixelBypass] - Image resize successful!", "green"))

        # brightness
        image_object_bright = ImageEnhance.Brightness(image_object)
        image_object = image_object_bright.enhance(1)
        im_buff = BytesIO()
        #image_object.save("./test.png", format="PNG", optimize=True)
        image_object.save(im_buff, format="PNG", optimize=True)
        image_object = Image.open(im_buff)


        # contrast
        image_object_contrast = ImageEnhance.Contrast(image_object)
        image_object = image_object_contrast.enhance(1)
        im_buff = BytesIO()
        #image_object.save("./test1.png", format="PNG", optimize=True)
        image_object.save(im_buff, format="PNG", optimize=True)

        image_object = Image.open(im_buff)

        rbxmx_file = open("output.rbxmx", "w")
        rbxmx_file.writelines(XML_HEADER+"\n"+CAMERA_ELEMENT)

        print(colored("[PixelBypass] - Converting Image to .rbxmx...", "blue"))

        current_vector = BASE_POSITION
        progress_counter = 0
        progress_percentage = 0
        
        #temporary variables 
        rh = 0 
        rw = 0
        # print(image_object.width, image_object.height)

        for x in range(image_object.width):
            progress_counter += 1
            
            for y in range(image_object.height):
                pixel_data = image_object.getpixel((x,y))
                if len(pixel_data) == 4:
                    pixel_data = pixel_data[:len(pixel_data)-1]
                hex_color = '%02x%02x%02x' % pixel_data
                uintcolor = int(hex_color, 16)
                rbxmx_file.writelines(PIXEL_ELEMENT.format(reff=get_random_string(32), xx=str(current_vector[0]+rh), yy=str(current_vector[1]+rw), zz=str(current_vector[2]), colorr=str(uintcolor)))
                rw-=.5
                progress_counter += 1
                if progress_counter >= 625:
                    progress_counter = 0
                    progress_percentage += 1
                    print(colored("[PixelBypass] - Progress: " + str(progress_percentage)+"% Done.", "magenta"), end="\r")
        
            rh+=.5
            rw=0 

        rbxmx_file.writelines(RANDOM_PIXEL)
        rbxmx_file.writelines(XML_FOOTER)
        rbxmx_file.close()

        print(colored("[PixelBypass] - Successfully constructed rbxmx file!", "green"))

    
        
        stdout_result = "NOT"
        ctr = 0
        #while not "DONE" in stdout_result:
        #    if ctr == 0:
        #        stdout_result = asyncio.run(run('RbxmConversion.exe output.rbxmx'))
        ##    print(colored("[PixelBypass] - Converting to binary format"+''.join(['.' for i in range(ctr % 4)]), "blue"))
         #   time.sleep(1)
         #   ctr += 1
        
        stdout_result = asyncio.run(run('RbxmConversion.exe output.rbxmx'))

        
        print(colored("[PixelBypass] - Finished conversion!", "green"))

        print(colored("[PixelBypass] - Checking provided cookie...", "blue"))

        mobileapi_response = False

        while not mobileapi_response:
            mobileapi_request = requests.get("http://www.roblox.com/mobileapi/userinfo", cookies={".ROBLOSECURITY":self.__cookie}, proxies=self.__proxy)
            if mobileapi_request.status_code == 200 and "UserName" in mobileapi_request.text:
                print(colored("[PixelBypass] - Uploading on user: " + mobileapi_request.json()["UserName"], "green"))
                mobileapi_response = True
            else:
                print(colored("[PixelBypass] - Provided cookie seems to be invalid, please supply a valid cookie.", "red"))
                self.__cookie = input("[.ROBLOSECURITY]\n> ")

        time.sleep(3)
        
        csrf_token = self.getcsrf()

        if len(csrf_token) > 1:
            print(colored("[PixelBypass] - Successfully grabbed csrf token!", "green"))
        else:
            print(colored("[PixelBypass] - Failed to grab csrf token", "red"))
            quit()
        
        #uploadname = get_random_string(8)

       
        print(colored("[PixelBypass] - Uploading bait file...", "blue"))
        bait_choice = random.choice(["AGod", "Bench", "katana"])
        bait_file = open("./baits/"+bait_choice+".rbxm", "rb")
        bait_req = requests.post("http://data.roblox.com/Data/Upload.ashx?assetid=0&type=10&name="+bait_choice+"&description=&genreTypeId=1&ispublic=true&allowcomments=true", data=bait_file, cookies={".ROBLOSECURITY":self.__cookie}, headers={"X-CSRF-TOKEN":csrf_token, "User-Agent":USER_AGENT, "content-type":"application/octet-stream", "accept":"*/*"}, proxies=self.__proxy)
        if bait_req.status_code == 200:
            print(colored("[PixelBypass] - Successfully uploaded bait file!", "green"))

        for i in range(10):
            print(colored("[PixelBypass] - Waiting {s} seconds to prevent ratelimit.".format(s=str(10-i)), "blue"), end="\r")
            time.sleep(1)

        print(colored("[PixelBypass] - Finished ratelimit cooldown!", "green"))
   
        file_object = open("output.rbxm", "rb")

        print(colored("[PixelBypass] - Uploading image...", "blue"))
        inapropriate_name = True
        while inapropriate_name:
            upload_description = random.choice(["Fu{{aieixzvzx:ck}}in damnit!!! ng", "I love a good sl{{aieixzvzx:ut}} ng", "fu{{aieixzvzx:ck}} a fa{{aieixzvzx:ggot}} ng", "Ride a bike, ki{{aieixzvzx:ll}} a dy{{aieixzvzx:ke}}! ng", "ni{{aieixzvzx:gga}} please.. ng", "a good sl{{aieixzvzx:ut}} loves a good as{{aieixzvzx:s}} fu{{aieixzvzx:ck}} ng"])
            upload_name = random.choice(["Image", "Texture", get_random_string(8), "File", "Image/Texture.png", "Random", "Hi mom", "Testing", "Files", "asldklnasdk", "lololollol", "coolio", "ships", "helloWorld", "New Decal", "My first model"])
            upl_req = requests.post("http://data.roblox.com/Data/Upload.ashx?assetid=0&type=10&name="+upload_name+"&description="+upload_description+"&genreTypeId=1&ispublic=false&allowcomments=false", data=file_object, cookies={".ROBLOSECURITY":self.__cookie}, headers={"X-CSRF-TOKEN":csrf_token, "User-Agent":USER_AGENT, "content-type":"application/octet-stream", "accept":"*/*"}, proxies=self.__proxy)
            #print(upl_text)
            print(upl_req.status_code)
            print(upl_req.text)
            if upl_req.status_code == 200 and not "Inapropriate" in upl_req.text:
                print(colored("[PixelBypass] - Successfully uploaded image!", "green"))
                print(colored("[PixelBypass] - https://www.roblox.com/library/"+upl_req.text+"/"+upload_name))
                ids_file = open("decals.txt", "a")
                ids_file.writelines(upl_req.text+" - "+self.__description+"\n")
                ids_file.close()
                inapropriate_name = False
            elif upl_req.status_code == 429 or upl_req.status_code == 407:
                self.newproxy()
                csrf_token = self.getcsrf()
                print(colored("[PixelBypass] - Ratelimited, switching proxy and csrf", "red"))
                time.sleep(3)
            else:
               
                if "Inapropriate" in upl_req.text:
                    upload_name = random.choice(["Image", "Texture", get_random_string(8), "File", "Image/Texture.png", "Random", "Hi mom", "Testing", "Files", "asldklnasdk", "lololollol", "coolio", "ships", "helloWorld", "New Decal", "My first model"])
        

    
        #r1 = requests.post("https://accountsettings.roblox.com/v1/inventory-privacy", cookies={".ROBLOSECURITY":self.__cookie},headers={"X-CSRF-TOKEN":csrf_token}, data={"inventoryPrivacy":"Everyone"})
        #print(r1.text)

        
        
        


