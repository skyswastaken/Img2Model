from classes.variables import *
from classes.handler import *



def checkDecals():
    new_decal_file = open("decals1.txt", "x")
    new_decal_file.close()
    new_decal_file = open("decals1.txt", "a")
    decal_file = open("decals.txt").read().splitlines()
    for l in decal_file:
        decal = l.split("-")[0].replace(" ","")
        description = l.split("-")[1]
        library_page = requests.get("https://roblox.com/library/"+str(decal))
        soup = BeautifulSoup(library_page.text, "lxml")
        decal_thumb = soup.find_all("img")
        decal_thumb = decal_thumb[0]["src"]
        if decal_thumb == "https://t1.rbxcdn.com/ce8aa442e702233adbf058be41cf4eca":
            print("Deleted decal removed.")
        else:
            new_decal_file.write(decal+" -"+description+"\n")

    new_decal_file.close()
    os.remove("decals.txt")
    os.rename("decals1.txt", "decals.txt")
    print("Decal list updated!")


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    print("Checking decals...")
    checkDecals()
   
    imgur = input(colored("[PixelBypass] - Please input direct image url.\n[User]: ", "yellow"))
    desc = input(colored("[PixelBypass] - Add a short image description.\n[User]: ", "yellow"))
    imgHandler = ImageHandler(imgur, desc)

    