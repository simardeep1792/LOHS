import itertools
import os,os.path
import time
import requests
import shutil
from PIL import Image
import greenViewCalculator as gv_calculate


def get_tiles(panoid):
    """
    Creates panaroma tiles corresponding to their positions.
    """
    url_for_image = "http://cbk0.google.com/cbk?output=tile&panoid={0:}&zoom=5&x={1:}&y={2:}"
    coordinates = list(itertools.product(range(26),range(13)))
    google_tiles = [(x, y, "%s_%dx%d.jpg" % (panoid, x, y), url_for_image.format(panoid, x, y)) for x,y in coordinates]
    return google_tiles

def download_tiles(google_tiles, directory):
    """
    Download all the tiles and put them in a directory.
    """
    for i, (x, y, fname, url) in enumerate(google_tiles):
        while True:
            try:
                response = requests.get(url, stream=True)
                break
            except requests.ConnectionError:
                print("Connection error. Trying again in 2 seconds.")
                time.sleep(2)
        with open(directory + '/' + fname, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response


def stitch_images(panoid, google_tiles, pano_directory, gsv_directory,file_name):
    """
    Stiches all the tiles to form a panaroma.
    """
    t_width = 512
    t_height = 512
    g_panaroma = Image.new('RGB', (26*t_width, 13*t_height))
    for x, y, fname, url in google_tiles:
        fname = pano_directory + "/" + fname
        tile = Image.open(fname)
        g_panaroma.paste(im=tile, box=(x*t_width, y*t_height))
        del tile
    
    g_panaroma = g_panaroma.resize((1024,512),Image.ANTIALIAS)    
    g_panaroma.save(gsv_directory + ("/%s.jpg" % file_name),optimize=True,quality=100)
   
    del g_panaroma
    filelist = [ f for f in os.listdir(pano_directory)]
    for f in filelist:
        os.remove(os.path.join(pano_directory, f))

