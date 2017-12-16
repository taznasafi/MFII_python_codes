import arcpy
import os


#arcpy.env.parallelProcessingFactor = "80%"  # Use all CPU capacity.


# Set up the Enviroment

evn_response = str(input("What is the path for the Enviroment:  "))
arcpy.env.workspace = evn_response


# list the fc


fc_response = str(input("what is the wildCard:  "))
LTElist = arcpy.ListFeatureClasses(fc_response)

output_geodatabase_path = input("what is the geodatabase output path:   ")

print(LTElist)

for x in LTElist:

    if arcpy.Exists(os.path.join(output_geodatabase_path, x + "__LTE5")):
        print("\n=========================================================")
        print("Verified {} exists".format(x))
        print("\n=========================================================")

    else:
        # create a new temp layer
        print("\n=========================================================")
        arcpy.MakeFeatureLayer_management(x, x + "_tempLayer")
        print("\nmade a temp layer for {}".format(x))

        print("\n\n\n\nCurrently I am working on this feature class file: " + str(x))

        print('\n"Selecting This criteria: "MINDOWN >=' + "5")
        arcpy.SelectLayerByAttribute_management(x + '_tempLayer', "New_SELECTION",
                                                'MINDOWN >=' + "5")

        print("\ncreating a new feature class to output:\n {}\n please wait!!!".format(
            os.path.join(output_geodatabase_path, x + "__LTE5")))
        arcpy.CopyFeatures_management(x + '_tempLayer',
                                      os.path.join(output_geodatabase_path, x + "__LTE5"))
        print(arcpy.GetMessages())
        print("\n=========================================================")


