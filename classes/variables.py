import requests
import re
import xml.etree.cElementTree as ET
import PIL
from PIL import Image
import requests
from io import BytesIO
from PIL import ImageFilter
from PIL import ImageEnhance
from IPython.display import display
import numpy as np
import os
import string
import sys
import random
from termcolor import colored
import asyncio
import time
from bs4 import BeautifulSoup


def get_random_string(length):
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(string.ascii_uppercase) for i in range(length))
    return result_str

def get_random_cookie():
    open_file = open("cookies.txt", "r")
    lines = open_file.read().splitlines()
    cookie = ""
    while len(cookie) < 10:
        cookie = random.choice(lines)
    open_file.close()
    return cookie

async def run(cmd: str):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()
    
    if stdout:
        #print(f'{stdout.decode()}')
        return(f'{stdout.decode()}')
    if stderr:
        #print(f'{stderr.decode()}')
        return(f'{stderr.decode()}')



BASE_POSITION = (random.randint(1,255), random.randint(1,255), random.randint(1,255))
# 164, 100, 47
# cam:
# +63, -63, +86

RANDOM_PIXEL = """<Item class="Part" referent="{REF}"><Properties><BinaryString name="AttributesSerialize" /><CoordinateFrame name="CFrame"><X>{xx}</X><Y>{yy}</Y><Z>{zz}</Z><R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12><R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame><string name="CollisionGroup">Default</string><int name="CollisionGroupId">0</int><Color3uint8 name="Color3uint8">{colorr}</Color3uint8><token name="shape">1</token><Vector3 name="size"><X>0.5</X><Y>0.5</Y><Z>0.5</Z></Vector3></Properties></Item>""".format(REF=get_random_string(15), xx=str(random.randint(200,1000)), yy=str(random.randint(200,1000)), zz=str(random.randint(200,1000)), colorr = str(random.randint(1111111,9999999)))


PIXEL_ELEMENT = """<Item class="Part" referent="{reff}"><Properties><BinaryString name="AttributesSerialize" /><CoordinateFrame name="CFrame"><X>{xx}</X><Y>{yy}</Y><Z>{zz}</Z><R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12><R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame><string name="CollisionGroup">Default</string><int name="CollisionGroupId">0</int><Color3uint8 name="Color3uint8">{colorr}</Color3uint8><token name="shape">1</token><Vector3 name="size"><X>0.5</X><Y>0.5</Y><Z>0.5</Z></Vector3></Properties></Item>"""

CAMERA_ELEMENT = """<Item class="Camera" referent="{reff}"><Properties><BinaryString name="AttributesSerialize"></BinaryString><CoordinateFrame name="CFrame"><X>{xx}</X><Y>{yy}</Y><Z>{zz}</Z><R00>0.999988317</R00><R01>1.4234256e-05</R01><R02>0.00485229073</R02><R10>-0</R10><R11>0.999995768</R11><R12>-0.00293349964</R12><R20>-0.00485231215</R20><R21>0.00293346541</R21><R22>0.999983907</R22></CoordinateFrame><Ref name="CameraSubject">null</Ref><token name="CameraType">0</token><float name="FieldOfView">70</float><token name="FieldOfViewMode">0</token><CoordinateFrame name="Focus"><X>{xx}</X><Y>{yy}</Y><Z>{zz}</Z><R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12><R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame><bool name="HeadLocked">true</bool><float name="HeadScale">1</float><string name="Name">ThumbnailCamera</string><int64 name="SourceAssetId">-1</int64><BinaryString name="Tags"></BinaryString></Properties></Item>""".format(reff = get_random_string(32), xx=BASE_POSITION[0]+163, yy=BASE_POSITION[1]-163, zz=BASE_POSITION[2]+186)

XML_HEADER = """<roblox xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4"><Meta name="ExplicitAutoJoints">true</Meta><External>null</External><External>nil</External><Item class="Folder" referent="{reff}"><Properties><BinaryString name="AttributesSerialize" /><string name="Name">Folder</string><int64 name="SourceAssetId">-1</int64><BinaryString name="Tags" /></Properties>""".format(reff = get_random_string(32))


# pointlight1:
# -92, +15, +1  

#pointlight2:
# -92, 90, -1 

#pointlight3:
# -19, +87, +1 

#pointlight4:
# 19, -87, -1

XML_FOOTER ="""<Item class="Part" referent="{reff}"><Properties><bool name="Anchored">false</bool><BinaryString name="AttributesSerialize"></BinaryString><float name="BackParamA">-0.5</float><float name="BackParamB">0.5</float><token name="BackSurface">0</token><token name="BackSurfaceInput">0</token><float name="BottomParamA">-0.5</float><float name="BottomParamB">0.5</float><token name="BottomSurface">0</token><token name="BottomSurfaceInput">0</token><CoordinateFrame name="CFrame"><X>{x1}</X><Y>{y1}</Y><Z>{z1}</Z><R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12><R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame><bool name="CanCollide">true</bool><bool name="CanQuery">true</bool><bool name="CanTouch">true</bool><bool name="CastShadow">true</bool><string name="CollisionGroup">Default</string><int name="CollisionGroupId">0</int><Color3uint8 name="Color3uint8">4288914085</Color3uint8><PhysicalProperties name="CustomPhysicalProperties"><CustomPhysics>false</CustomPhysics></PhysicalProperties><float name="FrontParamA">-0.5</float><float name="FrontParamB">0.5</float><token name="FrontSurface">0</token><token name="FrontSurfaceInput">0</token><float name="LeftParamA">-0.5</float><float name="LeftParamB">0.5</float><token name="LeftSurface">0</token><token name="LeftSurfaceInput">0</token><bool name="Locked">false</bool><bool name="Massless">false</bool><token name="Material">256</token><string name="MaterialVariantSerialized"></string><string name="Name">Lightpart</string><CoordinateFrame name="PivotOffset"><X>0</X><Y>0</Y><Z>0</Z><R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12><R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame><float name="Reflectance">0</float><float name="RightParamA">-0.5</float><float name="RightParamB">0.5</float><token name="RightSurface">0</token><token name="RightSurfaceInput">0</token><int name="RootPriority">0</int><Vector3 name="RotVelocity"><X>0</X><Y>0</Y><Z>0</Z></Vector3><int64 name="SourceAssetId">-1</int64><BinaryString name="Tags"></BinaryString><float name="TopParamA">-0.5</float><float name="TopParamB">0.5</float><token name="TopSurface">0</token><token name="TopSurfaceInput">0</token><float name="Transparency">1</float><Vector3 name="Velocity"><X>0</X><Y>0</Y><Z>0</Z></Vector3><token name="formFactorRaw">1</token><token name="shape">1</token><Vector3 name="size"><X>59</X><Y>52</Y><Z>55</Z></Vector3></Properties><Item class="PointLight" referent="{reff1}"><Properties><BinaryString name="AttributesSerialize"></BinaryString><float name="Brightness">1</float><Color3 name="Color"><R>1</R><G>1</G><B>1</B></Color3><bool name="Enabled">true</bool><string name="Name">PointLight</string><float name="Range">60</float><bool name="Shadows">false</bool><int64 name="SourceAssetId">-1</int64><BinaryString name="Tags"></BinaryString></Properties></Item></Item><Item class="Part" referent="{reff2}"><Properties><bool name="Anchored">false</bool><BinaryString name="AttributesSerialize"></BinaryString><float name="BackParamA">-0.5</float><float name="BackParamB">0.5</float><token name="BackSurface">0</token><token name="BackSurfaceInput">0</token><float name="BottomParamA">-0.5</float><float name="BottomParamB">0.5</float><token name="BottomSurface">0</token><token name="BottomSurfaceInput">0</token><CoordinateFrame name="CFrame"><X>{x2}</X><Y>{y2}</Y><Z>{z2}</Z><R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12><R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame><bool name="CanCollide">true</bool><bool name="CanQuery">true</bool><bool name="CanTouch">true</bool><bool name="CastShadow">true</bool><string name="CollisionGroup">Default</string><int name="CollisionGroupId">0</int><Color3uint8 name="Color3uint8">4288914085</Color3uint8><PhysicalProperties name="CustomPhysicalProperties"><CustomPhysics>false</CustomPhysics></PhysicalProperties><float name="FrontParamA">-0.5</float><float name="FrontParamB">0.5</float><token name="FrontSurface">0</token><token name="FrontSurfaceInput">0</token><float name="LeftParamA">-0.5</float><float name="LeftParamB">0.5</float><token name="LeftSurface">0</token><token name="LeftSurfaceInput">0</token><bool name="Locked">false</bool><bool name="Massless">false</bool><token name="Material">256</token><string name="MaterialVariantSerialized"></string><string name="Name">Lightpart</string><CoordinateFrame name="PivotOffset"><X>0</X><Y>0</Y><Z>0</Z><R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12><R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame><float name="Reflectance">0</float><float name="RightParamA">-0.5</float><float name="RightParamB">0.5</float><token name="RightSurface">0</token><token name="RightSurfaceInput">0</token><int name="RootPriority">0</int><Vector3 name="RotVelocity"><X>0</X><Y>0</Y><Z>0</Z></Vector3><int64 name="SourceAssetId">-1</int64><BinaryString name="Tags"></BinaryString><float name="TopParamA">-0.5</float><float name="TopParamB">0.5</float><token name="TopSurface">0</token><token name="TopSurfaceInput">0</token><float name="Transparency">1</float><Vector3 name="Velocity"><X>0</X><Y>0</Y><Z>0</Z></Vector3><token name="formFactorRaw">1</token><token name="shape">1</token><Vector3 name="size"><X>59</X><Y>52</Y><Z>55</Z></Vector3></Properties><Item class="PointLight" referent="{reff3}"><Properties><BinaryString name="AttributesSerialize"></BinaryString><float name="Brightness">1</float><Color3 name="Color"><R>1</R><G>1</G><B>1</B></Color3><bool name="Enabled">true</bool><string name="Name">PointLight</string><float name="Range">60</float><bool name="Shadows">false</bool><int64 name="SourceAssetId">-1</int64><BinaryString name="Tags"></BinaryString></Properties></Item></Item><Item class="Part" referent="{reff4}"><Properties><bool name="Anchored">false</bool><BinaryString name="AttributesSerialize"></BinaryString><float name="BackParamA">-0.5</float><float name="BackParamB">0.5</float><token name="BackSurface">0</token><token name="BackSurfaceInput">0</token><float name="BottomParamA">-0.5</float><float name="BottomParamB">0.5</float><token name="BottomSurface">0</token><token name="BottomSurfaceInput">0</token><CoordinateFrame name="CFrame"><X>{x3}</X><Y>{y3}</Y><Z>{z3}</Z><R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12><R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame><bool name="CanCollide">true</bool><bool name="CanQuery">true</bool><bool name="CanTouch">true</bool><bool name="CastShadow">true</bool><string name="CollisionGroup">Default</string><int name="CollisionGroupId">0</int><Color3uint8 name="Color3uint8">4288914085</Color3uint8><PhysicalProperties name="CustomPhysicalProperties"><CustomPhysics>false</CustomPhysics></PhysicalProperties><float name="FrontParamA">-0.5</float><float name="FrontParamB">0.5</float><token name="FrontSurface">0</token><token name="FrontSurfaceInput">0</token><float name="LeftParamA">-0.5</float><float name="LeftParamB">0.5</float><token name="LeftSurface">0</token><token name="LeftSurfaceInput">0</token><bool name="Locked">false</bool><bool name="Massless">false</bool><token name="Material">256</token><string name="MaterialVariantSerialized"></string><string name="Name">Lightpart</string><CoordinateFrame name="PivotOffset"><X>0</X><Y>0</Y><Z>0</Z><R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12><R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame><float name="Reflectance">0</float><float name="RightParamA">-0.5</float><float name="RightParamB">0.5</float><token name="RightSurface">0</token><token name="RightSurfaceInput">0</token><int name="RootPriority">0</int><Vector3 name="RotVelocity"><X>0</X><Y>0</Y><Z>0</Z></Vector3><int64 name="SourceAssetId">-1</int64><BinaryString name="Tags"></BinaryString><float name="TopParamA">-0.5</float><float name="TopParamB">0.5</float><token name="TopSurface">0</token><token name="TopSurfaceInput">0</token><float name="Transparency">1</float><Vector3 name="Velocity"><X>0</X><Y>0</Y><Z>0</Z></Vector3><token name="formFactorRaw">1</token><token name="shape">1</token><Vector3 name="size"><X>59</X><Y>52</Y><Z>55</Z></Vector3></Properties><Item class="PointLight" referent="{reff5}"><Properties><BinaryString name="AttributesSerialize"></BinaryString><float name="Brightness">1</float><Color3 name="Color"><R>1</R><G>1</G><B>1</B></Color3><bool name="Enabled">true</bool><string name="Name">PointLight</string><float name="Range">60</float><bool name="Shadows">false</bool><int64 name="SourceAssetId">-1</int64><BinaryString name="Tags"></BinaryString></Properties></Item></Item><Item class="Part" referent="{reff6}"><Properties><bool name="Anchored">false</bool><BinaryString name="AttributesSerialize"></BinaryString><float name="BackParamA">-0.5</float><float name="BackParamB">0.5</float><token name="BackSurface">0</token><token name="BackSurfaceInput">0</token><float name="BottomParamA">-0.5</float><float name="BottomParamB">0.5</float><token name="BottomSurface">0</token><token name="BottomSurfaceInput">0</token><CoordinateFrame name="CFrame"><X>{x4}</X><Y>{y4}</Y><Z>{z4}</Z><R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12><R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame><bool name="CanCollide">true</bool><bool name="CanQuery">true</bool><bool name="CanTouch">true</bool><bool name="CastShadow">true</bool><string name="CollisionGroup">Default</string><int name="CollisionGroupId">0</int><Color3uint8 name="Color3uint8">4288914085</Color3uint8><PhysicalProperties name="CustomPhysicalProperties"><CustomPhysics>false</CustomPhysics></PhysicalProperties><float name="FrontParamA">-0.5</float><float name="FrontParamB">0.5</float><token name="FrontSurface">0</token><token name="FrontSurfaceInput">0</token><float name="LeftParamA">-0.5</float><float name="LeftParamB">0.5</float><token name="LeftSurface">0</token><token name="LeftSurfaceInput">0</token><bool name="Locked">false</bool><bool name="Massless">false</bool><token name="Material">256</token><string name="MaterialVariantSerialized"></string><string name="Name">Lightpart</string><CoordinateFrame name="PivotOffset"><X>0</X><Y>0</Y><Z>0</Z><R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12><R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame><float name="Reflectance">0</float><float name="RightParamA">-0.5</float><float name="RightParamB">0.5</float><token name="RightSurface">0</token><token name="RightSurfaceInput">0</token><int name="RootPriority">0</int><Vector3 name="RotVelocity"><X>0</X><Y>0</Y><Z>0</Z></Vector3><int64 name="SourceAssetId">-1</int64><BinaryString name="Tags"></BinaryString><float name="TopParamA">-0.5</float><float name="TopParamB">0.5</float><token name="TopSurface">0</token><token name="TopSurfaceInput">0</token><float name="Transparency">1</float><Vector3 name="Velocity"><X>0</X><Y>0</Y><Z>0</Z></Vector3><token name="formFactorRaw">1</token><token name="shape">1</token><Vector3 name="size"><X>59</X><Y>52</Y><Z>55</Z></Vector3></Properties><Item class="PointLight" referent="{reff7}"><Properties><BinaryString name="AttributesSerialize"></BinaryString><float name="Brightness">1</float><Color3 name="Color"><R>1</R><G>1</G><B>1</B></Color3><bool name="Enabled">true</bool><string name="Name">PointLight</string><float name="Range">60</float><bool name="Shadows">false</bool><int64 name="SourceAssetId">-1</int64><BinaryString name="Tags"></BinaryString></Properties></Item></Item></Item></roblox>""".format(reff = get_random_string(32), reff1 = get_random_string(32), reff2 = get_random_string(32), reff3 = get_random_string(32), reff4 = get_random_string(32), reff5 = get_random_string(32), reff6 = get_random_string(32), reff7 = get_random_string(32), x1=BASE_POSITION[0], y1=BASE_POSITION[1]-15, z1=BASE_POSITION[2]+1, 
x2=BASE_POSITION[0]+91, y2=BASE_POSITION[1]-78, z2=BASE_POSITION[2]-1, 
x3=BASE_POSITION[0]+91, y3=BASE_POSITION[1]-15, z3=BASE_POSITION[2]+1, 
x4=BASE_POSITION[0], y4=BASE_POSITION[1]-78, z4=BASE_POSITION[2]-1)



USER_AGENT = "Roblox/WinInet"


