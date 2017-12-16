import os.path
import time
import arcpy

start = time.time()
# set the enviorment to get the county file locations

env_response_0 = str(input("what is the path for the block or state borders enviroment:     "))
arcpy.env.workspace = env_response_0


clip_feature_response = str(input("Enter the wild Card: "))
state_fc = arcpy.ListFeatureClasses(clip_feature_response)

clip_feature = []
for fc in state_fc:
    clip_feature.append(
        os.path.join(env_response_0,
                     os.path.splitext(fc)[0]))


for x in clip_feature:
    print(x)
    time.sleep(0.01)

arcpy.ClearEnvironment("workspace")

env_response_1 = input("what is the environment for the in features (provider coverage Shapefiles), Give the full path: ")
arcpy.env.workspace = env_response_1


in_features_response = input("Enter your wild card: ")
provider_shapefiles = arcpy.ListFeatureClasses(in_features_response)

in_features = []

for fc in provider_shapefiles:
    in_features.append(os.path.join(env_response_1, os.path.splitext(fc)[0]))

for x in in_features:
    print(x)
    time.sleep(0.01)

geodatabasepath = input("what is the the geodatabse path that you want to save: ")

for x in clip_feature:

    for y in in_features:
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("The clip feature is: {}".format(x[len(env_response_0)+1:].strip(' ')))
        time.sleep(0.01)
        print("The in_feature is: {}".format(y[len(env_response_1)+1:].strip(' ')))
        time.sleep(0.01)
        #infeature_list = [x, y]
        out_features = os.path.join(geodatabasepath,
                                    x[len(env_response_0) + 1:].strip(' ') + "_" + y[len(env_response_1)+1:].strip(' '))


        print("The output location is: {}".format(out_features))
        print()

        xy_tolerance = ""

        if arcpy.Exists(out_features):
            print("Verified {} exists".format(out_features))
        else:
            arcpy.Clip_analysis(y, x, out_features, xy_tolerance)
            print("\n", arcpy.GetMessages())

        #result = arcpy.GetCount_management(out_features)
        #result_count = int(result.getOutput(0))
        #if result_count == 0:
            #arcpy.Delete_management(out_features)
            #print("\n", arcpy.GetMessages())

        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


finish = time.time() - start
print("it took {} minutes to finish the job".format(finish/60))










