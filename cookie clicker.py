import ctypes
import time
import cv2
import win32api
import mss
import numpy as np
from math import cos,sin

COOKIE_COORDS = (291,431)
UPGRADE_COORDS = (1745,247)
LOWEST_BUILDING = (1888,1000)
#HIGHEST_BUILDING = (LOWEST_BUILDING[0],362)
HIGHEST_BUILDING = (LOWEST_BUILDING[0],284)
DRAGON_COORDS = (20,962)
DRAGON_UPGRADE = (195,962)
RESEARCH_COORDS = (1628,189)
UPGRADE_SCROLL_UP = (1910,34)
UPGRADE_SCROLL_DOWN = (UPGRADE_SCROLL_UP[0],1026)
RIGHT_SIDE_WRINKLER_COORDS = (452,COOKIE_COORDS[1])
NEWS_COORDS = (1084,47)

sct = mss.mss()
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

template = np.array([np.array([218, 207, 197, 171, 158, 138, 151, 151, 209, 169, 171, 171, 184,       190, 169, 138, 138,  99,  87,  68,  50,  68,  87,  68,  99, 116,       131, 138, 190, 178, 124,  99, 131, 184, 218, 209, 158, 144, 254,       144, 171, 238, 218, 218, 200, 190, 200, 200, 218, 227, 227, 209,       209, 200, 169, 160, 116, 138, 207], dtype=np.uint8), np.array([197, 171, 178, 169, 190, 190, 151, 151, 190, 158, 171, 171, 200,       169, 178, 151, 178, 138,  87,  68,  68,  50,  50,  68,  50,  68,        87,  99,  99,  87,  87,  99, 111, 158, 218, 209, 158, 144, 190,       158, 254, 254, 218, 209, 200, 200, 200, 209, 218, 238, 218, 209,       200, 209, 190, 139, 145, 131, 151], dtype=np.uint8), np.array([158, 145, 138, 151, 160, 138, 138, 178, 200, 184, 184, 254, 209,       190, 160, 145, 178, 138, 131, 116,  87,  87,  68,  50,  68,  50,        50,  68,  68,  87,  87,  99, 116, 200, 254, 254, 218, 145, 131,       131, 145, 227, 227, 218, 218, 200, 200, 218, 227, 238, 209, 200,       209, 200, 209, 190, 160, 138, 138], dtype=np.uint8), np.array([138, 124, 124, 169, 124, 124, 145, 171, 184, 227, 254, 197, 178,       158, 160, 145, 145, 178, 145, 218, 254,  99,  87,  87,  50,  68,        50,  68,  87,  87,  99, 111, 165, 254, 227, 209, 171, 145, 131,       111, 124, 131, 145, 200, 200, 190, 200, 209, 218, 209, 200, 200,       209, 200, 190, 160, 151, 160, 145], dtype=np.uint8), np.array([124, 111,  99, 111, 111, 138, 238, 200, 197, 197, 209, 184, 178,       169, 178, 169, 160, 158, 171, 200, 227, 138, 111, 111,  99,  87,        99,  87,  99, 131, 144, 254, 238, 227, 209, 184, 178, 139, 190,       111, 111, 111, 138, 138, 178, 169, 169, 209, 200, 190, 190, 200,       200, 178, 178, 145, 145, 178, 200], dtype=np.uint8), np.array([111, 111, 116, 111, 131, 138, 171, 209, 254, 218, 197, 209, 178,       169, 178, 145, 145, 169, 171, 200, 227, 171, 178, 190, 218, 209,       131, 131, 254, 227, 254, 227, 227, 207, 209, 184, 171, 190, 190,       145, 124, 178, 124, 124, 124, 138, 145, 139, 190, 169, 209, 178,       190, 178, 169, 160, 145, 138, 190], dtype=np.uint8), np.array([124, 160, 158, 151, 169, 169, 184, 218, 238, 227, 218, 197, 209,       178, 145, 145, 169, 184, 209, 238, 227, 158, 145, 200, 200, 209,       227, 238, 209, 218, 218, 218, 207, 209, 209, 200, 171, 209, 209,       138, 124, 124, 200, 151,  99, 116, 145, 200, 200, 169, 178, 169,       169, 200, 158, 158, 138, 124, 124], dtype=np.uint8), np.array([158, 181, 254, 209, 184, 171, 197, 227, 254, 254, 216, 200, 169,       145, 145, 145, 254, 218, 227, 227, 200, 139, 124, 111, 138, 200,       218, 218, 227, 207, 218, 209, 209, 218, 209, 209, 184, 178, 178,       160, 138, 124, 111,  99,  99,  99, 124, 131, 200, 171, 178, 171,       190, 139, 184, 178, 124, 111, 124], dtype=np.uint8), np.array([254, 227, 254, 216, 197, 216, 207, 216, 254, 254, 216, 184, 169,       145, 131, 178, 209, 200, 200, 200, 158, 116,  87,  87,  99, 145,       218, 238, 197, 209, 218, 218, 238, 218, 218, 227, 200, 178, 169,       145, 178, 178, 111,  87,  87,  87, 160, 124, 169, 218, 190, 209,       178, 178, 145, 158, 124, 169, 124], dtype=np.uint8), np.array([228, 228, 239, 239, 255, 254, 254, 255, 255, 228, 219, 219, 170,       146, 158, 255, 185, 172, 219, 178, 124,  99,  50,  68,  70, 112,       200, 201, 185, 207, 219, 219, 228, 255, 219, 201, 190, 178, 169,       161, 191, 124, 112,  99, 101, 180, 101, 112, 124, 210, 210, 200,       147, 116, 116, 101, 112, 190, 210], dtype=np.uint8), np.array([216, 254, 255, 255, 238, 217, 255, 255, 227, 219, 209, 184, 169,       158, 209, 190, 158, 169, 190, 138, 111,  99,  68,  50,  68,  87,       111, 145, 200, 254, 238, 238, 254, 238, 210, 184, 190, 190, 160,       160, 178, 131, 111, 116, 139, 116,  99,  87, 112, 124, 158, 131,       116,  99,  87,  87,  99, 138, 227], dtype=np.uint8), np.array([207, 255, 228, 227, 227, 227, 254, 217, 218, 210, 200, 178, 169,       160, 178, 190, 145, 132, 138, 124, 116,  68,  68,  87,  68,  68,        87, 112, 184, 207, 209, 228, 218, 207, 197, 200, 200, 169, 190,       178, 151, 138, 139,  99, 116,  87,  87, 124, 111, 111, 111, 131,        87,  87,  87,  68,  87,  87, 169], dtype=np.uint8), np.array([238, 255, 255, 227, 217, 219, 207, 209, 209, 184, 190, 178, 160,       178, 178, 190, 131, 140, 116,  87,  87,  68,  87,  87,  87, 111,        87,  99,  99, 131, 169, 210, 200, 200, 190, 209, 190, 169, 160,       190, 138, 138, 140,  99,  87,  87, 111, 197, 151, 111,  99,  99,        99,  87, 124,  68,  87,  87,  99], dtype=np.uint8), np.array([239, 255, 228, 217, 218, 207, 218, 197, 200, 200, 178, 178, 178,       145, 139,  99,  99,  87,  87,  87,  87,  99,  99, 124, 124, 217,       191, 112,  87,  87, 124, 178, 160, 191, 198, 201, 161, 160, 152,       147, 152, 139, 124, 112,  87,  87, 152, 219, 239, 112, 112, 112,       124, 151, 178,  99,  68,  87,  87], dtype=np.uint8), np.array([255, 228, 216, 210, 210, 227, 197, 200, 190, 210, 178, 190, 160,       132, 116,  99,  68,  87,  87, 111, 124, 131, 144, 158, 238, 216,       160,  87,  87,  68,  87, 111, 151, 184, 178, 160, 151, 151, 138,       160, 151, 178, 151, 111,  99,  87,  99, 124, 124, 131, 138, 138,       200, 169, 138, 111, 112,  99,  87], dtype=np.uint8), np.array([239, 239, 219, 198, 201, 209, 201, 201, 219, 200, 180, 170, 139,       112,  87,  68,  87, 112, 132, 144, 239, 209, 216, 254, 184, 151,       124, 111,  68,  68,  68,  87, 101, 124, 138, 151, 152, 152, 152,       152, 180, 191, 151, 138, 112, 112,  87, 111, 144, 169, 178, 201,       228, 180, 139, 124, 124,  87,  87], dtype=np.uint8), np.array([239, 219, 197, 201, 200, 198, 201, 210, 201, 210, 191, 146, 132,        99,  87,  87, 101, 158, 186, 228, 255, 239, 197, 186, 152, 139,       124, 139, 112,  70,  68,  50,  87, 112, 139, 170, 152, 161, 180,       170, 180, 170, 139, 161, 117, 117,  87, 117, 217, 228, 200, 210,       210, 160, 117, 124,  87,  68,  87], dtype=np.uint8), np.array([239, 207, 201, 200, 190, 210, 200, 200, 200, 200, 178, 146, 116,        99,  87,  87, 138, 239, 218, 228, 255, 207, 172, 158, 152, 124,       124, 152, 152, 124,  68,  50,  50,  87, 112, 139, 161, 161, 170,       180, 170, 152, 152, 139, 117,  87,  99, 124, 239, 255, 172, 219,       210, 178, 124,  99, 117,  70,  87], dtype=np.uint8), np.array([228, 219, 200, 200, 200, 200, 200, 190, 190, 190, 190, 146, 139,        87,  87, 112, 172, 210, 219, 255, 238, 197, 158, 151, 112, 112,       139, 161, 112, 112,  70,  50,  70,  70,  87, 160, 190, 190, 170,       160, 169, 151, 170, 180, 116,  87,  68,  99, 112, 132, 145, 144,       132, 132, 116,  87,  87,  68,  68], dtype=np.uint8), np.array([228, 210, 201, 201, 219, 210, 200, 200, 200, 200, 169, 172, 116,       101,  99, 124, 209, 200, 238, 239, 182, 190, 131, 112, 111,  99,        87,  99, 151, 111,  87,  68,  50,  68, 111, 169, 178, 184, 160,       160, 160, 151, 178, 190, 112,  87,  68,  87, 124, 151, 124, 170,       151,  99,  87,  87,  87,  68,  68], dtype=np.uint8), np.array([216, 219, 209, 200, 227, 209, 200, 209, 190, 209, 158, 158, 139,        87,  99, 124, 209, 200, 210, 184, 165, 131, 124,  99,  99,  87,        99,  99,  87,  99, 112,  68,  50,  70,  87, 151, 178, 178, 160,       151, 160, 160, 160, 146, 112,  87,  68,  50,  87,  87, 111, 160,        99,  87,  68,  68,  87, 111,  87], dtype=np.uint8), np.array([239, 218, 209, 209, 210, 200, 200, 190, 200, 178, 145, 116, 139,        99, 111, 151, 200, 200, 200, 158, 146, 116,  99,  99,  87,  99,        87,  87,  87,  87,  68,  68,  50,  68,  87, 111, 178, 151, 138,       112, 124, 124, 124, 124, 116,  87,  68,  68,  50,  68,  68,  68,        68,  50,  68,  68,  87, 124, 112], dtype=np.uint8), np.array([217, 210, 210, 228, 228, 219, 191, 178, 178, 160, 132, 140,  87,        87, 112, 191, 190, 190, 239, 190, 132, 116,  99,  99,  87, 101,       101,  87,  87,  87,  87,  50,  50,  50,  87, 161, 112, 124, 112,       124, 101, 124, 124, 124, 112, 116,  70,  50,  68,  70,  70,  68,        70,  70,  70,  70,  87,  87, 147], dtype=np.uint8), np.array([209, 209, 227, 209, 209, 200, 190, 169, 169, 145, 138, 116, 116,        87, 111, 178, 178, 200, 218, 178, 139, 111,  99, 124, 111, 111,        99,  99,  87,  99,  68,  68,  50,  50,  68, 160, 111,  99,  99,        87,  99, 111, 124, 124, 160, 190,  87,  68,  68,  87,  87,  99,        99,  99,  87,  99,  87,  99,  99], dtype=np.uint8), np.array([209, 200, 209, 190, 178, 178, 190, 178, 169, 145, 139,  87,  68,        99,  87,  99, 124, 124, 111, 116,  99,  99,  99,  99, 138, 169,       111,  87, 111,  68,  68,  50,  68,  68,  68, 111, 111, 111,  87,        99,  87, 111, 131, 190, 190, 111,  99,  99, 111, 111, 131, 254,       227, 197, 138, 131, 178, 169, 124], dtype=np.uint8), np.array([200, 200, 190, 158, 169, 178, 178, 169, 190, 139, 139,  87,  68,        50,  87,  87,  87,  87,  87,  87,  87,  87,  99,  99, 111, 151,       111, 111,  99,  68,  50,  87,  68,  87,  87, 124, 169, 124,  87,        87,  99, 160, 200, 184, 124, 131, 171, 254, 254, 184, 184, 200,       238, 200, 190, 178, 200, 254, 197], dtype=np.uint8), np.array([169, 178, 145, 145, 145, 178, 190, 178, 169, 160, 139,  99,  68,        68,  50,  68,  50,  68,  68,  68,  68,  87,  99,  99,  99,  87,        99,  87,  68,  50, 111,  87,  99, 111, 116, 238, 254, 111,  87,        99, 111, 178, 254, 144, 111, 111, 144, 254, 209, 200, 184, 218,       209, 200, 200, 200, 209, 209, 200], dtype=np.uint8), np.array([218, 171, 145, 131, 145, 171, 190, 200, 200, 190, 138, 111,  87,        68,  50,  50,  68,  68,  87,  68,  87,  68,  68, 138, 111,  68,        68,  68,  50,  87,  87, 111, 254, 171, 178, 200, 178, 131,  99,       131, 131, 254, 184, 131, 111, 131, 144, 254, 209, 184, 190, 190,       190, 178, 190, 169, 169, 178, 169], dtype=np.uint8), np.array([218, 190, 169, 131, 158, 200, 218, 218, 209, 200, 190, 138, 111,        87,  68,  68,  50,  68,  68,  87, 151,  87,  87,  68,  99,  68,        50,  68,  87,  99, 124, 200, 178, 178, 178, 169, 158, 138, 144,       254, 254, 209, 184, 124, 131, 144, 254, 218, 197, 184, 169, 160,       160, 190, 160, 145, 145, 138, 151], dtype=np.uint8), np.array([184, 158, 160, 145, 207, 238, 209, 218, 209, 209, 190, 190, 151,       111, 111,  68,  68,  50,  68, 111, 151,  68,  68,  50,  50,  50,        68,  87,  99, 254, 218, 178, 169, 160, 200, 178, 169, 190, 171,       254, 218, 184, 178, 138, 144, 165, 254, 218, 200, 169, 160, 151,       138, 138, 138, 124, 124, 124, 178], dtype=np.uint8), np.array([171, 145, 138, 145, 218, 209, 209, 209, 200, 209, 200, 200, 178,       190, 151, 169,  87,  87,  87,  68,  68,  50,  50,  50,  50,  87,        87, 131, 209, 200, 158, 160, 160, 169, 160, 178, 178, 197, 184,       184, 200, 190, 158, 160, 178, 254, 209, 200, 178, 160, 151, 124,       124, 111, 111, 111, 111, 111,  99], dtype=np.uint8), np.array([169, 145, 124, 145, 209, 190, 200, 209, 190, 200, 200, 190, 200,       190, 190, 190, 178, 111,  87,  87,  68,  68,  50,  68,  87,  99,       144, 238, 200, 158, 171, 190, 160, 160, 190, 169, 171, 254, 178,       169, 151, 158, 151, 160, 200, 200, 209, 200, 190, 160, 124, 124,       111, 111, 111,  87,  87, 111, 111], dtype=np.uint8), np.array([178, 124, 116, 151, 158, 190, 200, 190, 200, 190, 190, 190, 200,       190, 200, 200, 190, 190, 200, 124, 111,  87, 111,  99, 124, 254,       200, 171, 178, 171, 190, 169, 178, 160, 190, 178, 200, 178, 158,       145, 145, 138, 138, 151, 190, 190, 209, 209, 169, 138, 138, 111,        87,  99,  87,  87,  99,  99,  87], dtype=np.uint8), np.array([160, 131, 131, 138, 184, 184, 197, 209, 190, 190, 178, 200, 200,       190, 190, 209, 169, 158, 190, 209, 190, 160, 207, 218, 200, 200,       190, 190, 171, 190, 200, 169, 169, 160, 160, 160, 169, 151, 151,       138, 124, 124, 151, 190, 151, 160, 178, 190, 190, 169, 111,  99,        99,  87,  87,  68,  68,  68,  68], dtype=np.uint8), np.array([158, 145, 145, 158, 218, 207, 254, 216, 209, 190, 178, 178, 190,       178, 190, 158, 169, 178, 190, 200, 200, 169, 209, 209, 190, 190,       178, 178, 190, 178, 178, 160, 190, 151, 151, 160, 190, 160, 138,       124, 124, 124, 138, 138, 138, 138, 138, 160, 169, 124, 111,  87,        99, 116,  50,  68,  68,  50,  68], dtype=np.uint8), np.array([171, 171, 171, 216, 254, 254, 254, 254, 197, 178, 160, 160, 145,       145, 158, 169, 178, 160, 178, 160, 169, 145, 190, 178, 160, 169,       169, 178, 190, 190, 178, 151, 138, 160, 151, 169, 151, 151, 138,       124, 124, 151, 138, 151, 138, 111, 124, 111, 116, 111,  99,  99,        87,  68,  68,  50,  50,  68,  68], dtype=np.uint8), np.array([209, 254, 218, 227, 218, 216, 218, 207, 200, 184, 145, 138, 116,       124, 131, 138, 138, 145, 138, 138, 124, 111, 111, 131, 145, 160,       178, 190, 190, 178, 169, 138, 151, 138, 138, 151, 169, 178, 151,       124, 124, 138, 151, 116,  99, 111, 151, 138, 124,  99,  87,  68,        68,  50,  68,  50,  50,  68,  99], dtype=np.uint8), np.array([218, 209, 200, 209, 207, 209, 207, 209, 200, 160, 138, 124, 116,        87, 111, 111, 138, 131, 138, 138, 178,  87,  87,  99, 254, 169,       160, 151, 151, 138, 138, 138, 124, 124, 138, 138, 151, 160, 178,       138, 111, 124, 111, 139,  87,  68,  68,  87,  87,  87,  68,  68,        68,  50,  68,  68,  68,  87, 151], dtype=np.uint8), np.array([218, 200, 209, 200, 200, 197, 254, 200, 200, 145, 138, 131,  87,        68,  68,  87, 131, 200, 209, 169, 111,  87,  68,  99, 184, 169,       178, 184, 178, 151, 138, 124, 124, 124, 124, 160, 151, 178, 138,       124, 124, 124,  99, 116,  68,  68,  68,  87,  68,  68,  50,  68,        68,  87,  68, 116,  68,  87, 144], dtype=np.uint8), np.array([200, 200, 190, 190, 190, 200, 200, 171, 145, 138, 131,  87,  50,        50,  50,  68,  87, 184, 138, 138, 111,  87,  68,  99, 124, 151,       160, 151, 138, 138, 160, 138, 124, 151, 138, 151, 124, 138, 124,       138, 111, 111,  99, 116,  68,  68,  68,  68,  68,  87, 111,  68,       116,  68,  87,  68,  87,  99, 144], dtype=np.uint8), np.array([190, 178, 190, 178, 178, 209, 178, 145, 138,  99,  68,  68,  50,        50,  68,  50,  50,  87,  99, 138, 145,  87,  87, 207, 207, 124,       124, 138, 160, 184, 160, 124, 124, 178, 138, 124, 138, 111, 124,       138, 124, 111, 116,  99, 116,  68,  99,  50,  50, 124,  68,  99,       116,  68,  68,  68,  87, 111, 144], dtype=np.uint8), np.array([190, 170, 170, 180, 190, 169, 160, 138, 124,  99,  68,  50,  50,        50,  50,  50,  50,  70,  87, 151, 124, 116,  87,  87, 152, 124,       138, 147, 178, 170, 139, 139, 139, 180, 124, 112, 112, 112, 112,       101, 101, 101, 101, 116, 117,  70,  50,  70,  68,  50,  68,  68,        70,  68,  68, 112, 172, 138, 132], dtype=np.uint8), np.array([145, 151, 151, 151, 145, 146, 146, 138, 116,  99,  68,  50,  68,        87,  50,  50,  50,  68,  87, 160, 184, 116,  68,  68,  87, 111,       131, 216, 171, 151, 151, 124, 111, 111,  99, 124,  99, 124,  99,        99,  99, 124,  99, 139,  87,  68,  68,  68,  87,  68,  68,  87,        87,  87,  87,  99,  99, 158, 124], dtype=np.uint8), np.array([160, 138, 146, 138, 151, 160, 160, 191, 160, 116,  68,  50, 151,        50,  68,  50,  68,  87,  99, 200, 169,  87,  68,  68,  68, 111,       238, 255, 160, 151, 169, 112,  99,  99,  87,  87,  87,  87,  87,        87,  99,  87,  99, 116,  68,  68,  68,  68,  68,  87,  87,  87,       111, 116, 111, 218, 111, 124, 131], dtype=np.uint8), np.array([178, 160, 151, 160, 190, 178, 178, 178, 200, 139,  68,  50,  68,        68,  68,  87,  87, 255, 184, 124,  99, 116,  50,  68,  68,  99,       255, 218, 169, 131, 124, 112, 112,  87,  68,  87,  68,  87,  87,        87,  87,  68, 116, 116,  99,  87,  87,  87,  87,  87, 112, 131,       132, 165, 254, 169, 144, 138, 207], dtype=np.uint8), np.array([200, 178, 178, 178, 200, 190, 178, 190, 190, 124,  87,  68,  50,        68,  87, 254, 178, 112,  99,  68,  68,  68,  68,  68, 124, 101,       180, 180, 124, 112, 112,  99,  68,  70,  87, 101, 112, 112,  87,        87,  87, 117, 101, 140, 140, 144, 145, 132, 124, 124, 210, 255,       239, 255, 219, 165, 172, 172, 182], dtype=np.uint8), np.array([200, 178, 209, 190, 200, 178, 178, 178, 160, 112,  87,  87,  87,        87, 238, 181,  99,  87,  68,  68,  68,  68,  87, 138,  87,  87,        87,  87,  99,  87,  99, 139,  68,  68,  87,  87,  68,  87,  87,        99,  87,  87,  99, 116, 165, 254, 254, 227, 184, 151, 207, 200,       255, 254, 207, 207, 197, 255, 255], dtype=np.uint8), np.array([190, 180, 191, 180, 191, 169, 170, 161, 124, 112, 152, 161, 239,       186,  87,  99,  68,  70,  50,  68,  70,  68, 124, 111, 111,  68,        68,  68,  68,  87,  99,  87,  70,  87, 124, 124, 101,  87,  70,        70,  87,  87, 116, 140, 239, 255, 255, 254, 210, 158, 144, 180,       219, 228, 207, 207, 255, 228, 198], dtype=np.uint8), np.array([152, 180, 178, 170, 151, 147, 152, 112, 112, 112, 112,  87,  87,        87,  87,  50,  70,  50,  50,  50,  50,  87,  68, 112,  87, 112,        70,  70,  70,  87, 112,  87,  70,  87, 255, 201, 139,  87,  70,        87,  70, 101, 132, 166, 255, 255, 255, 217, 186, 158, 138, 124,       132, 185, 198, 255, 201, 172, 158], dtype=np.uint8), np.array([124, 132, 139, 124, 124, 124, 111, 116,  87,  87,  68,  68,  68,        68,  50,  68,  50,  50,  50,  70,  68, 112, 112,  87,  87,  70,        87,  87, 101,  87,  87,  70,  70,  87, 101, 124, 117, 101,  87,       101, 112, 112, 132, 198, 255, 255, 228, 207, 185, 161, 124, 124,       112, 138, 201, 185, 158, 147, 138], dtype=np.uint8), np.array([ 99, 116,  99, 112, 112, 124,  99,  87,  68,  68,  68,  68,  68,        87,  87,  68,  68,  87,  68,  68,  68,  68, 101,  99,  68,  87,        87, 101, 217, 217,  87,  87,  70, 124,  99, 112,  99,  99, 124,       112, 151, 169, 152, 210, 255, 255, 217, 219, 201, 151, 139, 112,       124, 124, 146, 158, 145, 138, 124], dtype=np.uint8), np.array([ 87,  87, 101, 101, 112, 116,  99,  87,  68,  68,  68, 112, 138,       112,  87, 116,  87,  99, 111,  99,  87,  87,  87,  87,  87,  68,        87, 131, 254, 158, 111,  87,  87, 124,  99, 111,  99, 111, 124,       160, 200, 190, 178, 158, 185, 228, 219, 200, 200, 160, 170, 139,       138, 217, 200, 160, 145, 138, 138], dtype=np.uint8), np.array([111,  99, 111, 111, 124, 124, 131,  87,  87,  68, 124, 160, 111,        87,  87,  68,  87,  68,  87,  87,  87,  99, 124, 111,  87,  87,       111, 255, 197, 169, 112,  87,  87, 180, 200, 112, 112, 112, 124,       178, 160, 124, 124, 138, 158, 219, 219, 210, 190, 169, 190, 190,       160, 169, 178, 178, 178, 151, 138], dtype=np.uint8), np.array([124, 111, 124, 138, 138, 178, 169, 112,  87,  68, 111, 124,  99,       116,  99,  87,  87, 112,  87, 112, 124, 160, 217, 169, 138, 112,       132, 172, 169, 146, 144,  87,  99, 160, 160, 111,  99,  99, 111,       112, 124, 111,  87, 111, 132, 200, 209, 190, 178, 178, 178, 200,       160, 160, 178, 178, 200, 190, 169], dtype=np.uint8)])
h,w = template.shape

def is_q_pressed():
    return ctypes.windll.user32.GetKeyState(0x51) > 1

def click(coords):
    win32api.SetCursorPos(coords)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
    time.sleep(0.001)

def clickFaster(coords):
    win32api.SetCursorPos(coords)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

def clickSlowly(coords):
    win32api.SetCursorPos(coords)
    time.sleep(0.2)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
    time.sleep(0.1)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
    time.sleep(0.2)

def clickCookie(stopped):
    stop = stopped
    for idx in range(10):
        for i in range(100):
            if is_q_pressed():
                stop = True
                return stop
            click(COOKIE_COORDS)
        clickGoldenCookies()
        clickNews()
    for i in range(2):
        if not stop:
            stop = popWrinklers(stop)
    return stop

def buyUpgrades(stopped):
    stop = upgradeDragon(stopped)
    if not stop:
        stop = doResearch(stop)
        if not stop:
            for i in range(10):
                if is_q_pressed():
                    stop = True
                    return stop
                click(UPGRADE_COORDS)
    return stop

def buyBuildings(stopped):
    stop = stopped
    x = LOWEST_BUILDING[0]
    y = LOWEST_BUILDING[1]
    useBuildingScroll(False)
    while y != HIGHEST_BUILDING[1]:
        if is_q_pressed():
            stop = True
            useBuildingScroll(True)
            return stop
        clickFaster((x,y))
        y -= 1
    useBuildingScroll(True)
    y = LOWEST_BUILDING[1]
    while y != HIGHEST_BUILDING[1]:
        if is_q_pressed():
            stop = True
            useBuildingScroll(True)
            return stop
        clickFaster((x,y))
        y -= 1
    useBuildingScroll(True)
    return stop

def clickGoldenCookies():
    img = np.array(sct.grab(monitor))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF)
    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
    topleft = max_loc
    click((int(topleft[0]+w/2),int(topleft[1]+h/2)))
    click((int(topleft[0]+w/2),int(topleft[1]+h/2)))

def upgradeDragon(stopped):
    stop = stopped
    if not stop:
        if is_q_pressed():
            stop = True
            return stop
        clickSlowly(DRAGON_COORDS)
        if is_q_pressed():
            stop = True
            return stop
        clickSlowly(DRAGON_UPGRADE)
    return stop

def doResearch(stopped):
    stop = stopped
    for i in range(10):
        if is_q_pressed():
            stop = True
            return stop
        click(RESEARCH_COORDS)
    return stop

def useBuildingScroll(up):
    if up:
        click(UPGRADE_SCROLL_UP)
    else:
        click(UPGRADE_SCROLL_DOWN)

def popWrinklers(stopped):
    stop = stopped
    distance = RIGHT_SIDE_WRINKLER_COORDS[0]-COOKIE_COORDS[0]
    degree = 0
    while degree < 360:
        if is_q_pressed():
            stop = True
            return stop
        clickFaster((int(COOKIE_COORDS[0] + (cos(degree)*distance)),int(COOKIE_COORDS[1] + (sin(degree)*distance))))
        degree += 1
    clickFaster((int(COOKIE_COORDS[0] + (cos(degree)*distance)),int(COOKIE_COORDS[1] + (sin(degree)*distance))))
    return stop

def clickNews():
    for i in range(10):
        clickFaster(NEWS_COORDS)

stopped = False
while True:
    if is_q_pressed():
        while is_q_pressed():
            pass
        while not is_q_pressed() and not stopped:
            stopped = clickCookie(stopped)
            if not stopped:
                stopped = buyUpgrades(stopped)
            if not stopped:
                stopped = buyBuildings(stopped)
            if not stopped:
                clickGoldenCookies()
        stopped = False
        while is_q_pressed():
            pass