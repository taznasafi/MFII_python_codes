import arcpy
import os
import sys



arcpy.env.overwriteOutput = False

# create a new working geodatabse folder
folder_path =  input("what is the current folder path:   ")
wk_folder = folder_path  # set the workfolder

# name of the geodatabse
working_gdb_Name = input("what do you want to call you geodatabase:   ")
working_gdb = os.path.join(wk_folder, working_gdb_Name+".gdb")
print("\n Created working Geodatabase folder path")

# check if old geodatabase exists. if True, then ask to delete it. else exit.

if arcpy.Exists(working_gdb):
    # ask for response
    response = input(
        "\n seems like we detected another USA faces geodatabase,"
        " \n in order to move ahead we need to delete the old one and create a new geodatabase."
        " Do you wanted to proceed? y/n \n")
    if response == "y":
        arcpy.Delete_management(working_gdb)
        print("\n Ok I deleted the the old Geodatabase, here are some ArcGIS messages:")
        print(arcpy.GetMessages())


    elif response == "n":
        print('bye')
        sys.exit()
    elif response == "":
        print('bye')
        sys.exit()
    elif response != "n" or response != "Y":
        print('Not valid Entry, try agian, but for now, bye!')
        sys.exit()

arcpy.CreateFileGDB_management(wk_folder, working_gdb_Name)

arcpy.env.workspace = input("what is the environment for shapefile that you want to dissolve:   ")

in_features = arcpy.ListFeatureClasses(input("what is name wild card:        "))

dissolve_field = ["pid"]

for x in in_features:

    print("\n\n\n ------------------------------------------------------------")

    out_features = os.path.join(working_gdb, "_diss_" + x)

    if arcpy.Exists(out_features):
        print("{} exists!! Skipping!!".format(out_features))
        print("\n\n\n ------------------------------------------------------------")

    else:
        print("dissolving {}".format(x))

        arcpy.Dissolve_management(x, out_features, dissolve_field )
        print(arcpy.GetMessages())
        print("\n\n\n ------------------------------------------------------------")







