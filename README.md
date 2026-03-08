# Image Metadata Extractor & Remover
This is a python script for extracting and removing metadata from images.       
It supports both individual files and folders, and works with JPEG and PNG images.

## What is Metadata?
Metadata is data about another data. It is data embedded into a file (another data) that describes its attributes and properties.         
The purpose of this script is to read and remove metadata attached to JPEGs and PNGs.               

## Metadata in Common File Formats
JPEG uses EXIF (Exchangeable Image File Format).         
PNG stores text chunks with key-value pairs.          
PDF embeds an info dictionary.              
Office formats use core properties in XML structures.             

## What is EXIF?
EXIF stands for Exchangeable Image File Format.       
It is hidden information stored inside image files (mostly JPEG and sometimes PNG) that describes how and where the photo was taken.              

### What Kind of Information Does EXIF Store?           
1) Location data        
If GPS is enabled on the camera or phone, the latitude, longitude and sometimes altitude will be stored.        
This can reveal exactly where a photo was taken.       
2) Date and time the photo was taken    
3) Camera brand and model  
4) Camera settings         
5) Other information           

All this information may seem useless but with enough and in combination, it can be used to create a profile on an anonymous individual and deanonymize them.                   

## EXIF Data Structure    
EXIF data is organized into sections called IFDs:     
0th IFD → basic image info     
Exif IFD → camera settings     
GPS IFD → location data      
1st IFD → thumbnail info        

## How it works          
The script retrieves metadata from images and converts it into a Python data structure (a dictionary).           

```
for ifd in exif_dict:
    if isinstance(exif_dict[ifd], dict):
```
EXIF metadata is structured into IFDs (Image File Directories).         
The binary data i.e thumbnail does not contain IFDs, so we skip those.         

```
exif_dict = piexif.load(img.info.get("exif", b""))
```
This loads the EXIF metadata from the image.
```
for tag in list(exif_dict[ifd].keys()):
```
Loops through all metadata tags in the current IFD.      
```
tag_name = piexif.TAGS[ifd].get(tag, {"name": str(tag)})["name"]
```
Converts the tag number to a readable name.          

When removing metadata, the script deletes most EXIF tags while preserving essential ones.
```
if tag_name not in ("Orientation", "ColorSpace"):     
    del exif_dict[ifd][tag]
```
Deletes all tags except two (Orientation, ColorSpace).        
Without them the photo might appear sideways or upside down or have color issues.         
```
exif_bytes = piexif.dump(exif_dict)
``` 
Converts the cleaned exif_dict back into binary EXIF format, ready to save in the image.       

## Features   
Extract metadata from JPEG and PNG    
Remove metadata from images   
Support for single files       
Support for folders     

### Example Usage    
Read Metadata        
```
python ex_cli.py -r image.jpg       
```
Remove Metadata From File       
```
python ex_cli.py -c image.jpg       
```
Remove Metadata From Folder   
```
python ex_cli.py -c images/ 
```

## What I learnt from this project:        
How metadata works in image files       
How EXIF data is structured                  
How metadata can be extracted and modified using Python      
How bad OPSEC can lead to privacy risks e.g the case of John McAfee in 2013.        

## Possible Future Updates:     
Add support for other image formats (webp) and videos     
Add support for PDFs and Office files    
Add GUI version for easier use          
