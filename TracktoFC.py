'''TRACK TO FC:
Converts Ozi Explorer Track file (.plt) to Geodatabase Point Feature Class, complete with time data

'''
import os, arcpy, time


def convert(plt):
    #Input File - One or many PLT Files
    # Set Input Parameters:
    endProgram = False
    endMessage = ["","I am unable to deal with that coordinate system", "this file doesn't look right"]
    # Input track file (single at first)

    outPath = "C:\Dropbox\\2. Active Jobs\\Brion 15-16\\shp\\CustomAnalytics.gdb\\testing\\"
    inTrack = "C:\\scripting\\sample.txt"
    outFile = "test1"
    sr_UTM = arcpy.SpatialReference(26912)

    # Get data
    record = []
    with open(plt) as inFile:
        for line in inFile:
            record.append(line)

    # Carry out file verification

    if record[0] != 'OziExplorer Track Point File Version 2.1\n':
        end_program = True
        error_message = 2
    if record[1] != 'WGS 84\n':
        end_program = True
        error_message = 1
    else:
        sr = arcpy.SpatialReference(4326)
    if record[2] != 'Altitude is in Feet\n':
        end_program = True
    # If not file verification: Kill the program
    if not end_program:
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

                # verify the integrity of each of the coordinates. Lat needs to have only two characters before the dec
                cursor = arcpy.da.InsertCursor(fc,
                                               ("SHAPE@XY", "Lat", "Long", "Altitude", "GPSTime", "Date", "Time"))

                cursor.insertRow((xy,lat,long,altitude,gpsTime,date,ptTime))

                del cursor
            count = count + 1

        arcpy.RepairGeometry_management(fc)
        arcpy.Project_management(fc, outPath + "track1", sr_UTM)
        arcpy.Delete_management(fc)


1



