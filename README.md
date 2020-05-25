# Level Of Heat Stress Mapping 

From the past few decades, there has been an exponential increase in the global temperature. This unprecedented rise in temperature causes heat stress for the people, especially during the hot summers. Thus, reducing heat stress and UV exposure has become an important issue primarily for the people living in the thickly populated urban areas. This project aims at extracting and analyzing the google street view images to quantify the shade provision by the street trees and building during the hot summer. The SVF (Sky View factor) and GVI (Green View Index) are important indicators to quantify the level of enclosure of street canyons. These factors are widely used to analyze the amount of direct solar radiation reaching the surface of the earth, thus holds direct implications on the thermal comfort of citizens. However, these measurements have been fairly limited due to the high costs of field surveys. The project makes use of the Google Street View (GSV) tile images to design a cylindrical panorama which is further projected onto a sphere to finally derive a hemispherical fisheye image. These fisheye images are further analyzed by using OSTU image processing technique and are classified using Caffe Segnet Image recognition techniques. The final results are being displayed via Tableau to see the green, sky and building view cover over selected areas. In addition, this prject tracks sun's azimuth position across each latitude and longitude.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

## Installing

A step by step series of examples that tell you how to get a development env running

1) Install Anaconda Naviagtor from the URL :- https://docs.anaconda.com/anaconda/install/mac-os/

2) Either Install dependencies: pip install -r Requirements_1.txt --upgrade or install each one of the manually through LOHS Project.ipynb file

3) Install Pymeanshift Library. You can easily find the instructions at : https://github.com/fjean/pymeanshift/wiki/Install

Creating an Environment for PSPNet-Tensorflow

3) Create a Python 3.5 Conda Environment . The instructions are at :- https://docs.anaconda.com/anaconda/navigator/tutorials/create-python35-environment/

4) Install the mandatory libraries using the link at pip install -r Requirements_2.txt --upgrade



## Running the tests

1) Locate the File LOHSProject.ipynb under the LOHS Project folder. Place an .xlxs file containing the latitude and longitude of the locations in the Project Folder.

2) Replace 'Your_File_Name.xlsx' with your file consisting of the Latitude and Longitude.

```
Route = pd.read_excel('Your_File_Name.xlsx')
```

3) 'downloadPanaromaForGoogleImages()' --> This method will create a text file consisting of the Panaroma Id's for the particular location as per the latitude and longitude. 

```
'downloadPanaromaForGoogleImages()'

Result:
panoID      I3_kUy4QR3neGplESvPOAA        
panoDate    2019-05,
longitude  -75.706272,
latitude    45.415549
```

3) 'downloadPanaromaImages()' --> This method will download the panaroma images for the specified locations and stitch them up to create a cylindrical panaroma which can be further used to create a hemispherical fisheye image. Only specific months are being selected from May to September.

```
downloadPanaromaImages()
```
![q05QYLJdN8I6MSNa8l9dow](https://user-images.githubusercontent.com/42692738/82768503-74cb7900-9dfd-11ea-99ff-b583670246dd.jpg)

4) 'greenViewCalculator' --> Using Otsu's method and the pymeanshift package, the Green View Index for each cylndrical panaroma image is calculated for each sampling point and then the GVI values are averaged to provide a single GVI value for every point along the street network. A text file is generated at the end specifying the green view points for the particular panaromas.

```
Result:
panoID-            3JM3shM8DmY6_Srq3WnirQ
greenViewValue-    27.0536
```
![q05QYLJdN8I6MSNa8l9dow](https://user-images.githubusercontent.com/42692738/82768519-87de4900-9dfd-11ea-80e1-76449844a713.jpg)

5) Solar Azimuth Calculation and Position --> This method generates the hemispherical fisheye images of the clyindrical panaromas along with solar position being calculated for every latitude and longitude for the specified time of the year.

![q05QYLJdN8I6MSNa8l9dow](https://user-images.githubusercontent.com/42692738/82768522-9593ce80-9dfd-11ea-981c-0d9add291b87.jpg)

6) Launch Python 3.5 environment in the terminal change directory to PSP_Net and run:

```
python PSP_Net/Segnet_Calculate_Results.py Project/GSV_Stiched_Images
```

This method takes google street view images from the folder segments them into sky, tree and buildings. The Segmented images are used to generate fisheye images by projecting GSV panoramas from the cylindrical projection to azimuthal projection. Furtermore on the basis of the segmentation results, Sky View, Tree View and Building View Factor are being calculated.

```
Segmented Image
```
![q05QYLJdN8I6MSNa8l9dow](https://user-images.githubusercontent.com/42692738/82768534-ac3a2580-9dfd-11ea-9265-3f7aec5a0353.jpg)

```
Fisheye Image
```
![q05QYLJdN8I6MSNa8l9dow](https://user-images.githubusercontent.com/42692738/82768564-cb38b780-9dfd-11ea-86ee-408947838aed.jpg)


```


```


