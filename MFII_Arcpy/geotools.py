import os
import sys
import traceback

import arcpy


class Tools:
    def __int__(self, inputPath=None, inputGDB=None, outputGDBName=None, outputPathFolder=None, outputGDB=None):
        self.inputPath = inputPath
        self.inputGDB = inputGDB
        self.outputGDBName = outputGDBName
        self.outputPathFolder = outputPathFolder
        self.outputGDB = outputGDB

    def create_gdb(self):
        try:
            arcpy.CreateFileGDB_management(out_folder_path=self.outputPathFolder, out_name=self.outputGDBName)
            print(arcpy.GetMessages(0))

        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)

    def import_shapefiles_to_gdb(self, wildcard=None):
        from MFII_tools.Master.MFII_Arcpy import get_path
        shplist = get_path.pathFinder.get_shapefile_path_wildcard(self.inputPath, wildcard)

        print("\nI found {} files to import!!!".format(len(shplist)))

        try:
            for x in shplist:
                name = os.path.split(x)[1]
                output = os.path.join(self.outputGDB, name)
                if arcpy.Exists(output):
                    print("exists, passing over this fc")
                else:
                    arcpy.FeatureClassToGeodatabase_conversion(x, self.outputGDB)
                    print(arcpy.GetMessages(0))
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)

    def merge_feature_class(self, name):
        from MFII_tools.Master.MFII_Arcpy import get_path
        input_obj = get_path.pathFinder(env_0=self.inputGDB)
        fcList = input_obj.get_path_for_all_feature_from_gdb()

        try:
            arcpy.Merge_management(fcList, os.path.join(self.outputGDB, name))
            print(arcpy.GetMessages(0))
        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)

    @classmethod
    def addJoin_and_copy_feature(cls, left_table, righttable, create_id_field, joinField, outpath, joinType=None):
        arcpy.env.qualifiedFieldNames = False
        try:
            templayer = arcpy.MakeFeatureLayer_management(left_table, "temp")

            if create_id_field == 0:
                print("adding join")
                arcpy.AddJoin_management("temp", joinField, righttable, joinField, joinType)
                print(arcpy.GetMessages(0))

                arcpy.CopyFeatures_management("temp", outpath)
                print(arcpy.GetMessages(0))
                arcpy.Delete_management("temp")

            if create_id_field == 1:
                arcpy.AddField_management("temp", "id", "TEXT")
                id_input = "{}+{}".format("!WC_CLLI!", 'str(!TT_ID!)')
                arcpy.CalculateField_management("temp", "id", expression=id_input, expression_type="python 10.5")

                print("adding join")
                arcpy.AddJoin_management("temp", joinField, righttable, joinField, joinType)
                print(arcpy.GetMessages(0))

                arcpy.CopyFeatures_management("temp", outpath)
                print(arcpy.GetMessages(0))
                arcpy.Delete_management("temp")

        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)
            arcpy.Delete_management("temp")
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)
            arcpy.Delete_management("temp")

    @classmethod
    def intersect_files(cls, inlist, outpath):

        try:
            print("intersect......plz wait!!")
            arcpy.Intersect_analysis(inlist, outpath)
            print(arcpy.GetMessages(0))
        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)

    def CopyFeatureclassToFeatureclass_with_expression(self):
        from MFII_tools.Master.MFII_Arcpy import get_path

        fcTOfc = get_path.pathFinder(env_0=self.inputGDB)

        stateList = fcTOfc.make_fips_list()

        for state in stateList:
            wildcard = "*_" + state
            fcList = fcTOfc.get_file_path_with_wildcard_from_gdb(wildcard)
            print(fcList)

            if len(fcList) == 0:
                print("there is no feature class by that query")
            else:
                where_clause = " STATE_FIPS =  %s " % int(state)
                print(where_clause)
                split_name = os.path.split(fcList[0])
                outname = "_cleaned_" + split_name[1]
                print(outname)

                if arcpy.Exists(os.path.join(self.outputGDB, outname)):
                    print("\nVARIFIED:\n{} exists, skipping!!!!!!!!!!!".format(outname))
                else:
                    try:

                        print("\n----------------------------------- Copying -----------------------------------")
                        arcpy.FeatureClassToFeatureClass_conversion(fcList[0], self.outputGDB, outname,
                                                                    where_clause)
                        print(arcpy.GetMessages())
                        print("\n-------------------------------------------------------------------------------")


                    except arcpy.ExecuteError:
                        msgs = arcpy.GetMessages(2)
                        arcpy.AddError(msgs)
                        print(msgs)
                    except:
                        tb = sys.exc_info()[2]
                        tbinfo = traceback.format_tb(tb)[0]
                        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(
                            sys.exc_info()[1])
                        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
                        arcpy.AddError(pymsg)
                        arcpy.AddError(msgs)
                        print(pymsg)
                        print(msgs)

    @classmethod
    def deleteEmptyfeaturesFiles(cls, path, type):
        from MFII_tools.Master.MFII_Arcpy import get_path
        try:
            if type == "Shapefile":
                shapefile_path = get_path.pathFinder()
                shapefileList = shapefile_path.get_shapefile_path_walk(path)

                for x in shapefileList:
                    if arcpy.GetCount_management(x)[0] == "0":
                        arcpy.Delete_management(x)
                        (arcpy.GetMessages(0))
            if type == "gdb":
                gdb = get_path.pathFinder(env_0=path)
                fcList = gdb.get_path_for_all_feature_from_gdb()

                for x in fcList:
                    if arcpy.GetCount_management(x)[0] == "0":
                        arcpy.Delete_management(x)
                        print(arcpy.GetMessages(0))


        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(
                sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)

    @classmethod
    def findField(cls,fc,fi):
        fieldnames = [field.name for field in arcpy.ListFields(fc)]
        if fi in fieldnames:
            return fi
        else:
            print("field not found")


    def export_subsidized_Coverage(self):
        try:

            from MFII_tools.Master.MFII_Arcpy import get_path, path_links


            sub_Coverage = get_path.pathFinder()
            sub_Coverage.env_0 = self.inputGDB

            StatesList = sub_Coverage.make_fips_list()

            for fips in StatesList:

                pidList = sub_Coverage.query_provider_by_FIPS(path_links.LTE5_table_path,str(int(fips)))
                print("\n{} : {}".format(fips, pidList))

                fc_response = "*_" + fips
                fcList = sub_Coverage.get_file_path_with_wildcard_from_gdb(fc_response)
                print("\t", fcList)


                if len(fcList) == 0:
                    print("skipping state: {}!!!".format(fips))

                else:

                    # make a layer from the feature class
                    arcpy.MakeFeatureLayer_management(fcList[0], "temp_layer")

                    # list fields
                    field_names = [f.name for f in arcpy.ListFields("temp_layer")]
                    field_type = [f.type for f in arcpy.ListFields("temp_layer")]
                    field_dic = dict(zip(field_names, field_type))
                    #print(field_names)
                    print()
                    #print(field_type)

                    for y in pidList:
                        field = "provider_id{}".format(y)
                        print(field)

                        def findField(fc, fi):
                            fieldnames = [field.name for field in arcpy.ListFields(fc)]
                            if fi in fieldnames:
                                return fi
                            else:
                                return "pass"

                        field_found = findField('temp_layer', field)

                        if field_found == "pass":
                            print("could not find the field passing it!!")
                        else:

                            try:

                                if field_dic[field_found] == "String":

                                    # where_clause = """ "p%s" = %d AND "pid" = %s""" % (y, y, y)
                                    where_clause = " provider_id%s = '%d' AND pid = %s" % (y, y, y)
                                    arcpy.SelectLayerByAttribute_management("temp_layer", "ADD_TO_SELECTION",where_clause)
                                    print(arcpy.GetMessages())


                                else:
                                    where_clause = """ provider_id%s = %s AND pid = %s""" % (y, y, y)
                                    print(where_clause)

                                    arcpy.SelectLayerByAttribute_management("temp_layer", "ADD_TO_SELECTION",
                                                                                where_clause)
                                    print(arcpy.GetMessages())

                            except arcpy.ExecuteError:
                                msgs = arcpy.GetMessages(2)
                                arcpy.AddError(msgs)
                                print(msgs)
                                pass

                    name = os.path.split(fcList[0])
                    out_feature_class = os.path.join(self.outputGDB, "_subsidized_" + name[1])

                    if arcpy.Exists(out_feature_class):
                        print("the file exists, skipping!!!!!!")
                        arcpy.Delete_management("temp_layer")
                    else:

                        # export the feature layer
                        arcpy.CopyFeatures_management("temp_layer", out_feature_class)
                        print(arcpy.GetMessages())
                        # Delete Temp feature layer
                        arcpy.Delete_management("temp_layer")


        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)

        except:

            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(
                sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)


    def splitCoverages(self, split_fields):
        from MFII_tools.Master.MFII_Arcpy import get_path, path_links

        try:

            split = get_path.pathFinder()
            split.env_0 = self.inputGDB

            fcList = split.get_path_for_all_feature_from_gdb()

            for x in fcList:
                name = os.path.split(x)
                print("\n\n\nlooking at '{}' feature class, please wait!!!".format(name[1]))
                print("Splitting the files, might take a while. Go for a walk :) \n\n")
                arcpy.SplitByAttributes_analysis(x, self.outputGDB, split_fields)
                print(arcpy.GetMessages(0))

        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)

        except:

            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(
                sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)


    def clipshapefiles(self, clippath, infeaturepath, type):
        from MFII_tools.Master.MFII_Arcpy import get_path

        try:
            fipsList = get_path.pathFinder.make_fips_list()
            if type == "gdb":
                clipFC = get_path.pathFinder()
                clipFC.env_0 = clippath

                inFeatureFC = get_path.pathFinder()
                inFeatureFC.env_0 = infeaturepath


                for state in fipsList:

                    clipwildcard = "*_"+state+"_"

                    clipFCList = clipFC.get_file_path_with_wildcard_from_gdb(clipwildcard)

                    inFeatureFCList = inFeatureFC.get_path_for_all_feature_from_gdb()
                    inFeatureFCName = os.path.split(inFeatureFCList[0])
                    outfeature = os.path.join(self.outputGDB, inFeatureFCName[1]+"_"+state)

                    if arcpy.Exists(outfeature):
                        print("Verified {} exists".format(outfeature))
                    else:
                        arcpy.Clip_analysis(inFeatureFCList[0], clipFCList[0], outfeature)
                        print("\n", arcpy.GetMessages(0))


        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)

        except:

            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(
                sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)



    def importLTE5Coverages(self, wilcard, outputpath):
        from MFII_tools.Master.MFII_Arcpy import get_path

        try:

            lte5 = get_path.pathFinder()
            lte5.env_0 = self.inputGDB
            lte5List = lte5.get_file_path_with_wildcard_from_gdb(wilcard)
            print(lte5List)


            print(outputpath)

            for x in lte5List:
                name = os.path.split(x)
                outputName = name[1]
                print(outputName)

                if arcpy.Exists(os.path.join(outputpath, outputName + "__LTE5")):
                    print("\n=========================================================")
                    print("Verified {} exists".format(outputName))
                    print("\n=========================================================")

                else:
                    # create a new temp layer
                    print("\n=========================================================")
                    arcpy.MakeFeatureLayer_management(x, outputName + "_tempLayer")
                    print("\nmade a temp layer for {}".format(outputName))

                    print("\n\n\n\nCurrently I am working on this feature class file: " + str(outputName))

                    print('\n"Selecting This criteria: "MINDOWN >=' + "5")
                    arcpy.SelectLayerByAttribute_management(outputName + '_tempLayer', "New_SELECTION",
                                                            'MINDOWN >=' + "5")

                    print("\ncreating a new feature class to output:\n {}\n please wait!!!".format(
                        os.path.join(outputpath, outputName + "__LTE5")))
                    arcpy.CopyFeatures_management(outputName + '_tempLayer',
                                                  os.path.join(outputpath, outputName + "__LTE5"))
                    print(arcpy.GetMessages())
                    print("\n=========================================================")

        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)

        except:

            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(
                sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)





    def importShapefilesToGDB(self):
        from MFII_tools.Master.MFII_Arcpy import get_path

        try:
            importShp = get_path.pathFinder()

            ShpList = importShp.get_shapefile_path_walk(self.outputPathFolder)

            for shapefile in ShpList:
                print("\mImporting Shapefiles")
                arcpy.FeatureClassToGeodatabase_conversion(shapefile, self.outputGDB)
                print(arcpy.GetMessages(0))


        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)

        except:

            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(
                sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)




