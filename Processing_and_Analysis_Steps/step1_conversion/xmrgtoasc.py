"""
ABE 651 Final Project

Program: xmrgtoasc.py (Python ver.)

Created by Younghyun Cho <cho215@purdue.edu>
        on March 31, 2014

Contributed by NOAA website:
http://www.nws.noaa.gov/oh/hrl/distmodel/hrap.htm#extension

Description:
Read an XMRG file and write to an ASCII file that
can be read directly read by ArcGIS as a gird.
Output coordinates are either HRAP or polar stereographic
depending on input (hrap or ster) by the user.  
"""
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


import os
import struct # interpret strings as packed binary data


def prompt_user():
    prompt = "Select coordinate system: type 'hrap' or 'ster'\n"
    input_coord = raw_input(prompt) # read input, returen as string
    return input_coord

coord = prompt_user() # coordinate system
# print coord (check!)

# !Cautions: check current working directory (input files location)!
os.chdir("D:\\radar_project\cho215_project\program_conversion\XMRGFiles")
cwd = os.getcwd()
XMRGFiles = os.listdir(cwd) # return a list of the files in cwd
# print XMRGFiles (check!)


for files in XMRGFiles:
    fin = open(files, "rb") # rb: read binary
    fname = files.split("g")[1] # split file name, return last part
    fout = open("ascii%s.asc" % fname, "w")

    # [Header part]
    readheader = fin.read(86)
    Header = struct.unpack("i4i2i2s8s20s8s20s", readheader)
    # <first record>
    XOR = Header[1] # xllcorner
    xstereo = XOR*4762.5-401.0*4762.5
    YOR = Header[2] # yllcorner
    ystereo = YOR*4762.5-1601.0*4762.5
    MAXX = Header[3] # ncols
    MAXY = Header[4] # nrows
    # <second record>
    # oper_sys = Header[7]
    # user_id = Header[8] 
    # datetime = Header[9] # saved date/time
    # process_flag = Header[10]
    datetime2 = Header[11] # valid date/time

    if coord == "hrap":
        fout.write("ncols %d\n" % MAXX)
        fout.write("nrows %d\n" % MAXY)
        fout.write("xllcorner %d\n" % XOR)
        fout.write("yllcorner %d\n" % YOR)
        fout.write("cellsize 1\n")
        #log
        print "file name: %s" % files
        print "ncols %d" % MAXX
        print "nrows %d" % MAXY
        print "xllcorner %d" % XOR
        print "yllcorner %d" % YOR
        print "cellsize 1"
        print "valid date/time %s\n" % datetime2
    else:
        fout.write("ncols %d\n" % MAXX)
        fout.write("nrows %d\n" % MAXY)
        fout.write("xllcorner %f\n" % xstereo)
        fout.write("yllcorner %f\n" % ystereo)
        fout.write("cellsize 4762.5\n")
        fout.write("nodata_value -9999.0\n")
        print "file name: %s" % files
        print "ncols %d" % MAXX
        print "nrows %d" % MAXY
        print "xllcorner %f" % xstereo
        print "yllcorner %f" % ystereo
        print "cellsize 4762.5"
        print "valid date/time %s\n" % datetime2

    # [Data part]
    offset1 = -MAXX*2 - 4
    fin.seek(offset1, 2)
    # 2nd argument: 2 uses the end of the file as the reference point
    readdata1 = fin.read(MAXX*2)
    Data1 = struct.unpack("250h", readdata1)

    i = 0
    while i < 250: # n-1 count
        val = int(Data1[i])
        if val < 0:
            outval = -9999.0 # NoData check
        else:
            outval = int(Data1[i])/100.0
            # convert from hundredths of mm to mm
        fout.write('%f' % outval + ' ')
        i = i + 1
    fout.write("\n")

    offset2 = offset1 * 2
    for n in range(MAXY-1):
        fin.seek(offset2, 1)
        # 2nd argument: 1 uses the current file position
        readdata2 = fin.read(MAXX*2)
        Data2 = struct.unpack("250h", readdata2)
        i = 0
        while i < 250:
            val = int(Data2[i])
            if val < 0:
                outval = -9999.0
            else:
                outval = int(Data2[i])/100.0
            fout.write('%f' % outval + ' ')
            i = i + 1
        fout.write("\n")

    fin.close()
    fout.close()

print "Done, take your ASCII grid radar data from 'XMRGFiles'!"
