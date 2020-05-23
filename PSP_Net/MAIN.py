import os
import sys
if len(sys.argv) == 2:
    imgfilepath = sys.argv[1]
    processedImgPath = imgfilepath + '_SEGNET'
    isExists = os.path.exists(processedImgPath)

    if not isExists:
        os.mkdir(processedImgPath)
    imgfiles = os.listdir(imgfilepath)

    #for imageFile in imgfiles:
        #os.system('python inference.py --img-path='+str(imgfilepath)+'/'+str(imageFile)+' --dataset cityscapes --save-dir='+processedImgPath+'/')

    os.system('python fisheyeconversion.py '+processedImgPath)
    os.system('python calculateResults.py '+processedImgPath+ '_FISHEYE')



    

    
