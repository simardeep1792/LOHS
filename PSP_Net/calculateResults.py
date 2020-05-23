import cv2
import os
import math
import sys


if len(sys.argv) == 2:
    filepath = sys.argv[1]
    files = os.listdir(filepath)
    x0 = 86
    y0 = 86
    outputpath = filepath + '_RESULTS'

    isExists = os.path.exists(outputpath)

    if not isExists:
        os.mkdir(outputpath)

    f = open(outputpath+'/SEGNET_Results.csv','w')

    for value,inputimg in enumerate(files):
        r = 82
        if inputimg=='.DS_Store':
            continue
        fisheye_img = cv2.imread(filepath+'/'+inputimg)
        pano_ID = inputimg.split('.')[0]
        svf = 0.00
        tvf = 0.00
        bvf = 0.00
        for index in range(1,28):
            circled_img = cv2.imread(filepath+'/'+inputimg)
            cv2.circle(circled_img,(86,86),r,[0,255,255])
            cv2.circle(circled_img,(86,86),r-1,[0,255,255])
            cv2.circle(circled_img,(86,86),r-2,[0,255,255])

            circle_points = []
            sky_points = []
            tree_points = []
            building_points =[]
            for i in range(0, 173):
                for j in range(0, 173):
                    if circled_img[i][j][0] == 0 and circled_img[i][j][1] == 255 and circled_img[i][j][2] == 255:
                        circle_points.append([i,j])

            for point in circle_points:
                x= point[0]
                y= point[1]
                if fisheye_img[x][y][0] in range(7,60)  and fisheye_img[x][y][1] in range(60,173) and fisheye_img[x][y][2] in range(52,144):
                    tree_points.append(point)
                elif fisheye_img[x][y][0] in range(176,182) and fisheye_img[x][y][1] in range(129,132) and fisheye_img[x][y][2] in range(69,71):
                    sky_points.append(point)
                elif fisheye_img[x][y][0] in range(67,71) and fisheye_img[x][y][1] in range(67,71) and fisheye_img[x][y][2] in range(67,71):
                    building_points.append(point)


     
            sky = len(sky_points)/len(circle_points)
            svf = svf + math.sin(math.pi*(2*index-1)/54)*sky
            tree = len(tree_points)/len(circle_points)
            tvf = tvf + math.sin(math.pi*(2*index-1)/54)*tree
            building = len(building_points)/len(circle_points)
            bvf = bvf + math.sin(math.pi*(2*index-1)/54)*building
            
            r=r-3
        if value==0:
            lineTxt = '%s,%s,%s,%s\n'%('pano_ID','svf','tvf','bvf')
            f.write(lineTxt)
        svf = (math.pi/54) * svf
        tvf = (math.pi/54) * tvf
        bvf = (math.pi/54) * bvf
        lineTxt = '%s,%s,%s,%s\n'%(pano_ID,svf,tvf,bvf)
        print(lineTxt)

        f.write(lineTxt)

    f.close()

print('*****Process Completed****')
