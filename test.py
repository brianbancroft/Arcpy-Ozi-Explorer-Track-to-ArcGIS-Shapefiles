import os, arcpy, time
inFile = "C:\\scripting\\sample.txt"
'''Some notes about the file:
If you break the thing by line starting at 0, here are the lines:
0: header
1: Datum
2: Altitude setting (defaults in feet)
3: reserved
4: some details. I'm unsure'
5: some other details
6: TRACK FEATURES START HERE

For the actual track features, if you split them by comma, you get the following bits:
0: Latitude, degrees
1: Longitude, degrees
2
3: Altitude, feet
4: GPS Time
5: Date
6: Time. Remove the last two characters ie: testSample[n][:-1]


In order to avoid double algorithms, the conversion process to feature should take place within the for loop.

For the actual scripting, I may make a class or function that does the actual work, while making the main just the thing
 that interfaces with the class...

>>> a[0]
'OziExplorer Track Point File Version 2.1\n'
>>> a[1]
'WGS 84\n'
>>> a[2]
'Altitude is in Feet\n'
>>> a[3]
'Reserved 3\n'
>>> a[4]
'0,3,11858584,Traccia [148] 11/05/2015 10:18:29  ,0,0,2,8421376,-1,0\n'
>>> a[5]
'1589\n'
>>> a[6]
'  55.229164,-118.522850,1, 2284.0,42135.6794792, 11-May-15, 4:18:27 PM\n'
>>> a[7]
'  55.229160,-118.522850,0, 2283.5,42135.6795949, 11-May-15, 4:18:36 PM\n'
>>> a[8]
'  55.229160,-118.522850,0, 2282.2,42135.6797106, 11-May-15, 4:18:46 PM\n'
>>>

'''


# Set Input Parameters:
endProgram = False
endMessage = ["","I am unable to deal with that coordinate system", "this file doesn't look right"]
# Input track file (single at first)

outPath = "C:\Dropbox\\2. Active Jobs\\Brion 15-16\\shp\\CustomAnalytics.gdb\\testing\\"
inTrack = "C:\\scripting\\sample.txt"
outFile = "test1"
sr_UTM = arcpy.SpatialReference(26912)

'''Time zone info: This might not be required, but if the output time is in Zulu, I'm going to have to carry out
some major conversion here
# Input Time Zone
timeZone = ""
# Input Daylight Savings
isDaylightSavings = True'''


# Get data
record = []
with open(inTrack) as inFile:
    for line in inFile:
        record.append(line)

# Carry out file verification
'''
>>> a[0]
'OziExplorer Track Point File Version 2.1\n'
>>> a[1]
'WGS 84\n'
>>> a[2]
'Altitude is in Feet\n'
>>> a[3]
'Reserved 3\n'
>>> a[4]
'0,3,11858584,Traccia [148] 11/05/2015 10:18:29  ,0,0,2,8421376,-1,0\n'
>>> a[5]
'1589\n'
>>> a[6]
'  55.229164,-118.522850,1, 2284.0,42135.6794792, 11-May-15, 4:18:27 PM\n'
'''
if record[0] != 'OziExplorer Track Point File Version 2.1\n':
    endProgram = True
    errorMessage = 2
if record[1] != 'WGS 84\n':
    endProgram = True
    errorMessage = 1
else:
    sr = arcpy.SpatialReference(4326)
if record[2] != 'Altitude is in Feet\n':
    endProgram = True
# If not file verification: Kill the program
if not endProgram:


    # Create Feature Class
    arcpy.CreateFeatureclass_management(outPath, outFile,"POINT", spatial_reference=sr)
    fc = outPath + outFile
    # Add columns to feature class. Everything but time and date are float.

    arcpy.AddField_management(fc, "Lat", "FLOAT")
    arcpy.AddField_management(fc, "Long", "FLOAT")
    arcpy.AddField_management(fc, "Altitude", "FLOAT")
    arcpy.AddField_management(fc, "GPSTime", "FLOAT")
    arcpy.AddField_management(fc, "Date","DATE")
    arcpy.AddField_management(fc,"Time","DATE")



    count = 6

    while count < len(record):
        row = record[count].split(',')
        if len(row) == 7:
            lat =  float(row[0][2:])
            long = float(row[1])
            xy = (long,lat)
            altitude = float(row[3])
            gpsTime = float(row[4])
            date = row[5][1:]
            ptTime = row[6][1:-1]




            # verify the integrity of each of the coordinates. Lat needs to have only two characters before the decimal.
            cursor = arcpy.da.InsertCursor(fc,
                                           ("SHAPE@XY", "Lat", "Long", "Altitude", "GPSTime", "Date", "Time"))

            cursor.insertRow((xy,lat,long,altitude,gpsTime,date,ptTime))

            del cursor
        count = count + 1

            # END WHILE LOOP
            #end if statement

    arcpy.RepairGeometry_management(fc)
    arcpy.Project_management(fc, outPath + "track1", sr_UTM)
    arcpy.Delete_management(fc)






