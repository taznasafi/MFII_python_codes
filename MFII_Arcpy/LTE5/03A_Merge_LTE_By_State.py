import os
import time
import sys
import arcpy
import pandas as pd




data = pd.read_csv(r"E:\MFII_Dec2016\CSV Files\stateFIPS\state FiPS.txt",
                   sep='|')

data["STATE"] = data["STATE"].astype(str)

data['STATE'] = data["STATE"].apply(lambda x: x.zfill(2))

state = data.STATE.tolist()
#print(state)


s1 = state[0:9]
s2 = state[9:19]
s3 = state[19:29]
s4 = state[29:39]
s5 = state[39:49]
s6 = state[49:59]


s ={1: s1, 2: s2, 3: s3, 4:s4, 5:s5, 6: s6}

env_response = input("What is the Enviroment for LTE shapefiles:   ")
arcpy.env.workspace = env_response

outfeature_basefile = input("please provide a filepath for the geodatabase you want to save:    ")

while True:

    continue_response = input("\n\n\n\ndo you want to continue? y/n     ")


    if continue_response == "y":


        i = int(input("Choose 1, 2, 3, 4, 5, or 6 to run the process:   "))



        for states in s[i]:
            # Set up the Enviroment for unsubsizidized
            fc_response = "*_" + states + "_*"
            fc_list = arcpy.ListFeatureClasses(fc_response)
            print(fc_list, sep=",")

            if len(fc_list) == 0:
                print("Did not find this {} state".format(states))

            else:


                outfeature_name = "_merged_"+states


                outfeature_full_path = os.path.join(outfeature_basefile, outfeature_name)

                if arcpy.Exists(outfeature_full_path):
                    print("\n=========================================================")
                    print("Verified {} exists".format(outfeature_full_path))
                    print("=========================================================\n")

                else:
                    fm = arcpy.FieldMap() # DBA
                    fm1 = arcpy.FieldMap()  # Technology
                    fm2 = arcpy.FieldMap()  # Spectrum
                    fm3 = arcpy.FieldMap()  # MinDown
                    fm4 = arcpy.FieldMap()  # MinUp
                    fm5 = arcpy.FieldMap()  # PID
                    fms = arcpy.FieldMappings()


                    #DBA
                    for in_file in fc_list:
                        for field in arcpy.ListFields(in_file, "DBA"):
                            fm.addInputField(in_file, field.name)

                        for field in arcpy.ListFields(in_file, "Technology"):
                            fm1.addInputField(in_file, field.name)

                        for field in arcpy.ListFields(in_file, "Spectrum"):
                            fm2.addInputField(in_file, field.name)

                        for field in arcpy.ListFields(in_file, "MinDown"):
                            fm3.addInputField(in_file, field.name)

                        for field in arcpy.ListFields(in_file, "MinUp"):
                            fm4.addInputField(in_file, field.name)

                        for field in arcpy.ListFields(in_file, "pid"):
                            fm5.addInputField(in_file, field.name)



                    # DBA
                    fm.mergeRule = "First"

                    f_name = fm.outputField
                    f_name.name = 'DBA'
                    f_name.length = 255
                    f_name.type = "Text"

                    fm.outputField = f_name

                    fms.addFieldMap(fm)

                    # Technology
                    fm1.mergeRule = "First"

                    f_name = fm1.outputField
                    f_name.name = 'Technology'
                    f_name.type = "Short Integer"

                    fm1.outputField = f_name

                    fms.addFieldMap(fm1)

                    # Spectrum
                    fm2.mergeRule = "First"

                    f_name = fm2.outputField
                    f_name.name = 'Spectrum'
                    f_name.type = "Short Integer"

                    fm2.outputField = f_name

                    fms.addFieldMap(fm2)

                    # MinDown
                    fm3.mergeRule = "First"

                    f_name = fm3.outputField
                    f_name.name = 'MinDown'
                    f_name.type = "Short Integer"

                    fm3.outputField = f_name

                    fms.addFieldMap(fm3)

                    # MinUp
                    fm4.mergeRule = "First"

                    f_name = fm4.outputField
                    f_name.name = 'MinUp'
                    f_name.type = "Short Integer"

                    fm4.outputField = f_name

                    fms.addFieldMap(fm4)


                    #Pid

                    fm5.mergeRule = "First"

                    f_name = fm4.outputField
                    f_name.name = 'pid'
                    f_name.type = "Short Integer"

                    fm5.outputField = f_name

                    fms.addFieldMap(fm5)

                    print("\n=========================================================")
                    print("Merging {}, plz wait".format(outfeature_full_path))
                    arcpy.Merge_management(fc_list, outfeature_full_path, fms)
                    print(arcpy.GetMessages())
                    print("=========================================================\n")

    elif continue_response == "n":

        print("Ok, see you next time")
        time.sleep(1)
        sys.exit()

    elif continue_response != "y" or continue_response != "n":
        print("I didn't get that, try agian!!!")
        continue