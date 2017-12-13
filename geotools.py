import arcpy
import traceback
import sys
import os



class Tools:
    def __int__(self, inputPath=None, inputGDB = None, outputName=None, outputPathFolder=None, outputGDB = None):
        self.inputPath = inputPath
        self.inputGDB = inputGDB
        self.outputName = outputName
        self.outputPathFolder = outputPathFolder
        self.outputGDB = outputGDB


    def create_gdb(self):
        try:
            arcpy.CreateFileGDB_management(out_folder_path=self.outputPathFolder, out_name=self.outputName)
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
        from MFII_tools import get_path
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
        from MFII_tools import get_path
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


