import sys
import os.path
import arcpy




# set the enviorment
arcpy.env.workspace = input("what is the env path:      ")

##
arcpy.env.overwriteOutput = True

while True:
        response = str(input("\n Do you want to continue:   y/n     "))

        if response == "y":
                
                in_features = []

                while True:
                        search_reponse = str(input("\n you want to add more names: y/n? "))
                        
                        if search_reponse == "y":
                                name = str(input('Enter Wildcard name:\t'))
                                list_feature = arcpy.ListFeatureClasses(name, "Polygon")
                                for x in list_feature:
                                    in_features.append(x)
                                print("These are the files in the list for merging: \n{}".format(in_features))

                        
                        
                        elif response == "n":
                        
                                break
                
                        elif response == "":
                        
                                break
                
                        elif response !="n" or response != "y":
                                break




                fc_rename = str(input("What do you want to name your file:    "))
                
                target_path = input("what is the output path:   ")

                print(in_features)
                
                arcpy.Merge_management(in_features, os.path.join(target_path, fc_rename))
                
                print(arcpy.GetMessages())
                print("\ndone!")
                
                

        elif response == "n":
                print("bye")

                sys.exit()
                
        elif response == "":
                print("bye")

                sys.exit()
                
        elif response !="n" or response != "Y":
                print("Not Valid Entry, try agian, but for now, bye!")

                sys.exit()

        
