import os
import sys
import traceback
import arcpy


class Tools:
    def __int__(self, inputPath=None, inputGDB = None, outputGDBName=None, outputPathFolder=None, outputGDB = None):
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

            if create_id_field==0:

                print("adding join")
                arcpy.AddJoin_management("temp", joinField, righttable, joinField, joinType)
                print(arcpy.GetMessages(0))

                arcpy.CopyFeatures_management("temp", outpath)
                print(arcpy.GetMessages(0))
                arcpy.Delete_management("temp")

            if create_id_field ==1:
                arcpy.AddField_management("temp", "id", "TEXT")
                id_input= "{}+{}".format("!WC_CLLI!", 'str(!TT_ID!)')
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
                where_clause =  " STATE_FIPS =  %s " % int(state)
                print(where_clause)
                split_name = os.path.split(fcList[0])
                outname = "_cleaned_" +split_name[1]
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
                    if arcpy.GetCount_management(x)[0]=="0":
                        arcpy.Delete_management(x)
                        (arcpy.GetMessages(0))
            if type == "gdb":
                gdb= get_path.pathFinder(env_0=path)
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











