import sys
import os.path
import time
import arcpy


workspace_response = input("what is the folder that you want to create the geodatabase: ")

print("current workspace is " + workspace_response)

arcpy.env.overwriteOutput = True

# create a new working geodatabse folder

wk_folder = workspace_response	#set the workfolder

# name of the geodatabse
geodatabase_response = input("what is the the name of geodatabase:      ")
USA_working_gdb_Name= geodatabase_response+".gdb"
USA_working_gdb = os.path.join(wk_folder,USA_working_gdb_Name)


#check if old geodatabase exists. if True, then ask to delete it. else exit.

if arcpy.Exists(USA_working_gdb_Name):
    confirm_response = input("\n seems like we detected another USA faces geodatabase,"
                            " \n in order to move ahead we need to delete the old one and create a new geodatabase."
                            " Do you wanted to proceed? y/n \n")
    if confirm_response == "y":
        arcpy.Delete_management(USA_working_gdb)
        print("\n Ok I deleted the the old Geodatabase, here are some ArcGIS messages:")
        print(arcpy.GetMessages())

        arcpy.CreateFileGDB_management(wk_folder, USA_working_gdb_Name)
        print("\n whoo hooo created a new geodatabase file, here are some ArcGIS messages: ")
        print(arcpy.GetMessages())

    elif confirm_response == "n":
        time.sleep(0.5)
        print('bye')

    elif confirm_response == "":
        time.sleep(0.5)
        print('bye')
        sys.exit()
else:
    arcpy.CreateFileGDB_management(wk_folder, USA_working_gdb_Name)
    print("\n Created working Geodatabase")

# Find all the shapefiles and put it in a list
shapefile_loc_response = input("what is the shapefile file path:        ")
filepath = shapefile_loc_response

file_loc=[]
for root, dirs, files in os.walk(filepath):
    for file in files:
        if file.endswith(".shp"):
            #print(os.path.join(root,file))
            file_loc.append(os.path.join(root,file))
            #print(file_loc)

i=0
while i<len(file_loc):
    print("\nImporting Shapefile \nPlease Wait!!!")
    arcpy.FeatureClassToGeodatabase_conversion(file_loc[i],USA_working_gdb)
    print(arcpy.GetMessages())
    i +=1