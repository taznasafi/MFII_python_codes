import arcpy
import os
import pandas as pd



evn_response =  input("what is the enviroment for the shapefile:    ")

arcpy.env.workspace = evn_response

fc_response = input("What is the wild card for the shapefile: ")

fc = arcpy.ListFeatureClasses(fc_response)

print(list(x for x in fc))

field_response = input("what is the field name: ")

field = field_response

state_dic = {}

for x in fc:

    # Use SearchCursor with list comprehension to return a
    # unique set of values in the specified field
    input_table = os.path.join(evn_response, x)
    values = [row[0] for row in arcpy.da.SearchCursor(input_table, field)]
    uniqueValues = set(values)

    state_dic[str(x[14:16])] = uniqueValues






print("\n\n\n\n\n")
print(state_dic, sep=",")


df = pd.DataFrame.from_dict(state_dic, orient="index")

df.sort_index

df.columns = ["pidnum_1", "pidnum_2", "pidnum_3", "pidnum_4",
              'pidnum_5', 'pidnum_6', 'pidnum_7', 'pidnum_8']


print(df)

df.to_csv(r"E:\MFII_Dec2016\GIS\Dec2016_LTE_Coverage\LTE5_number_of_providers_per_state.csv", index_label="stateFIPS")

