"""
ABE 651 Final Project

Program: hraptoshg.py (Python ver.)

Created by Younghyun Cho <cho215@purdue.edu>
        on April 05, 2014

Description:
Convert hrap gird to shg grid
using the ArcGIS Geoprocessing tools with ArcPy
"""
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


import os
import arcpy
arcpy.env.workspace="D:\\radar_project\cho215_project\program_georeferencing\SHGGrid"
# !Cautions: check work space directory (output files location)!
arcpy.env.overwriteOutput = True

# !Cautions: check current working directory (input files location)!
os.chdir("D:\\radar_project\cho215_project\program_georeferencing\HRAPGrid")
cwd = os.getcwd()
HRAPGrid = os.listdir(cwd) # return a list of the files in cwd
# print HRAPGrid (check!)


for files in HRAPGrid:
    print "Processing" + " " + files
    inputfiles = "D:\\radar_project\cho215_project\program_georeferencing\HRAPGrid" + str("/") + files
    # set inputfiles path

    # [Geo-referencing in ArcGIS; true]
    # ASCII to Raster (HRAP gird)
    arcpy.ASCIIToRaster_conversion(inputfiles, "grid_harp", "FLOAT")

    # Define Projection (Polar_Stereographic)
    arcpy.DefineProjection_management("grid_harp",
    "PROJCS['Polar_Stereographic',\
     GEOGCS['Sphere',\
     DATUM['<custom>',\
     SPHEROID['<custom>',6371200.0,0.0]],\
     PRIMEM['Greenwich',0.0],\
     UNIT['Degree',0.0174532925199433]],\
     PROJECTION['Stereographic_North_Pole'],\
     PARAMETER['False_Easting',0.0],\
     PARAMETER['False_Northing',0.0],\
     PARAMETER['Central_Meridian',-105.0],\
     PARAMETER['Standard_Parallel_1',60.0],\
     UNIT['Meter',1.0]]")

    # Project Raster (Sphere)
    arcpy.ProjectRaster_management("grid_harp", "grid_harp_gcs",
    "GEOGCS['Sphere',\
     DATUM['<custom>',\
     SPHEROID['<custom>',6371200.0,0.0]],\
     PRIMEM['Greenwich',0.0],\
     UNIT['Degree',0.0174532925199433]]",
    "NEAREST", "", "", "",
    "PROJCS['Polar_Stereographic',\
     GEOGCS['Sphere',\
     DATUM['<custom>',\
     SPHEROID['<custom>',6371200.0,0.0]],\
     PRIMEM['Greenwich',0.0],\
     UNIT['Degree',0.0174532925199433]],\
     PROJECTION['Stereographic_North_Pole'],\
     PARAMETER['False_Easting',0.0],\
     PARAMETER['False_Northing',0.0],\
     PARAMETER['Central_Meridian',-105.0],\
     PARAMETER['Standard_Parallel_1',60.0],\
     UNIT['Meter',1.0]]")

    # Project Raster 2 (Allbers Equal Area Conic)
    arcpy.ProjectRaster_management("grid_harp_gcs", "grid_shg",
    "PROJCS['USA_Contiguous_Albers_Equal_Area_Conic_USGS_version',\
     GEOGCS['GCS_North_American_1983',\
     DATUM['D_North_American_1983',\
     SPHEROID['GRS_1980',6378137.0,298.257222101]],\
     PRIMEM['Greenwich',0.0],\
     UNIT['Degree',0.0174532925199433]],\
     PROJECTION['Albers'],\
     PARAMETER['False_Easting',0.0],\
     PARAMETER['False_Northing',0.0],\
     PARAMETER['Central_Meridian',-96.0],\
     PARAMETER['Standard_Parallel_1',29.5],\
     PARAMETER['Standard_Parallel_2',45.5],\
     PARAMETER['Latitude_Of_Origin',23.0],\
     UNIT['Meter',1.0]]",
    "NEAREST", "2000", "", "",
    "GEOGCS['Sphere',\
     DATUM['<custom>',\
     SPHEROID['<custom>',6371200.0,0.0]],\
     PRIMEM['Greenwich',0.0],\
     UNIT['Degree',0.0174532925199433]]")
    
    # Raster to ASCII (SHG grid)
    outputfiles = files.split("ii")[1] # split file name, return last part
    arcpy.RasterToASCII_conversion("grid_shg", "shg"+outputfiles)

print "Done, take your SHG gird radar data from 'SHGGrid'!" 
