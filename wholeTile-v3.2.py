#Program: Square Counter
#Version: 3.2
#Created by B.Wu
#Date: 2019-02-04
#
#For identifying whole tiles in Takeoffs: 
#1. Save a PNG of your DWG model over a white background (including the boundaries and tiles hatch)
#2. Running from Commend Line Prompt: Navigate to the correct file address, copy the file address after "cd "
#    (e.g. cd C:\Users\Interns PC\Desktop\workspace\Python) and press Enter
#3. Type in "SquareCounter-v3.2.exe -f <filename.filetype>" (e.g. SquareCounter-v3.2.exe -f test.png), and press Enter
#4. A PNG called "<filename>-##.png" will be saved under the file address, with ## being the number of whole tiles detected.
#5. Click into the output picture to verify/edit tile numbers.
#
#Note: Verify the number of tiles from output file every time. Some perimeter tiles that are very close to a square 
#      may pass the threshold (Line 54) and get counted towards whole tiles. 
#
#List of Commends:
#	-h --help: help
#	-f --file <filename.filetype>: enter input file name


import sys, argparse, os
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

import numpy as np
import cv2 as cv

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    squares = []
    
    bin = cv.Canny(img, 0, 50, apertureSize=5)
    cv.imwrite('canny.png',bin)
    bin = cv.dilate(bin, None)
    cv.imwrite('dilate.png',bin)
    bin, contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        cnt_len = cv.arcLength(cnt, True)
        cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
        if len(cnt) == 4 and cv.contourArea(cnt) > 100 and cv.isContourConvex(cnt):  # 4 corners, area > 100
            cnt = cnt.reshape(-1, 2)
            max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
            if max_cos < 0.1 and is_square(cnt):
                squares.append(cnt)
    return squares

def is_square(cnt):
    p1 = cnt[0]
    p2 = cnt[1]
    p3 = cnt[2]
    p4 = cnt[3]
    x = np.max([np.abs(p1[0] - p2[0]), np.abs(p2[0] - p3[0]), np.abs(p3[0] - p4[0]), np.abs(p4[0] - p1[0])])
    y = np.max([np.abs(p1[1] - p2[1]), np.abs(p2[1] - p3[1]), np.abs(p3[1] - p4[1]), np.abs(p4[1] - p1[1])])
    if np.abs(x-y)<4:   # Square detection threshold
        return True
    else:
        return False

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename", help="sourse file name", metavar="FILE", action='store')
    args = parser.parse_args(argv)
    if args.filename:
        file = os.path.splitext(args.filename)[0]
        img = cv.imread(str(args.filename), 0)  # Change to correct picture name to count tiles
        print("INFO: " + args.filename + " has been successfully found")
        squares = find_squares(img)
        if len(squares) > 0:
            cv.drawContours( img, squares, -1, 100, 1 )
            cv.imwrite(str(file) + '-' + str(len(squares)) + '.png',img)   # Save to file name
            print("Output file: " + str(file) + '-' + str(len(squares)) + '.png' + " has been successfully created")
        else: 
            cv.drawContours( img, squares, -1, 100, 1 )
            cv.imwrite(str(file) + '-' + str(len(squares)) + '.png',img)   # Save to file name
            print("Warning: No whole tiles found, please try zoom in and clip a bigger picture")
    else:
        print("ERROR: Invalid argument")

if __name__ == '__main__':
    main(sys.argv[1:])


# credit to: https://github.com/opencv/opencv/blob/master/samples/python/squares.py
    
