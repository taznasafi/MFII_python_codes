import os
import sys
import traceback
import arcpy
import logging
import time
from MFII_python_codes.MFII_Arcpy import get_path, path_links

formatter = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename=r"{}_Log_{}.csv".format(__name__.replace(".", "_"), time.strftime("%Y_%m_%d_%H_%M")),
                                 level=logging.DEBUG, format=formatter)

class Tools:
    def __int__(self, inputPath=None, inputGDB=None, outputGDBName=None, outputPathFolder=None, outputGDB=None, name = None):
        self.inputPath = inputPath
        self.inputGDB = inputGDB
        self.outputGDBName = outputGDBName
        self.outputPathFolder = outputPathFolder
        self.outputGDB = outputGDB
        self.name = name


    def create_gdb(self):
        try:
            arcpy.CreateFileGDB_management(out_folder_path=self.outputPathFolder, out_name=self.outputGDBName)
            print(arcpy.GetMessages(0))
            logging.info("created GDB, messages: {}".format(arcpy.GetMessages(0)))


        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)
            logging.info(msgs)
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)
            logging.info(pymsg)
            logging.info(msgs)

    def import_shapefiles_to_gdb(self, wildcard=None):

        shplist = get_path.pathFinder.get_shapefile_path_wildcard(self.inputPath, wildcard)

        print("\nI found {} files to import!!!".format(len(shplist)))

        try:
            for x in shplist:
                name = os.path.split(x)[1]
                output = os.path.join(self.outputGDB, name.strip(".shp"))
                print(output)
                logging.info("Importing: {}".format(name.strip(".shp")))
                if arcpy.Exists(output):
                    print("exists, passing over this fc")
                    logging.warning("{} exists, passing over this fc".format(name.strip(".shp")))
                else:
                    arcpy.FeatureClassToGeodatabase_conversion(x, self.outputGDB)
                    print(arcpy.GetMessages(0))
                    logging.info(arcpy.GetMessages(0))
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)
            logging.error(pymsg)

    def merge_feature_class(self, name):

        input_obj = get_path.pathFinder(env_0=self.inputGDB)
        fcList = input_obj.get_path_for_all_feature_from_gdb()

        try:
            if arcpy.Exists(os.path.join(self.outputGDB, name)):
                logging.warning("the file exist, skipping over it")
            else:

                arcpy.Merge_management(fcList, os.path.join(self.outputGDB, name))
                print(arcpy.GetMessages(0))
                logging.info(arcpy.GetMessages(0))
        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)
            logging.error(msgs)
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)
            logging.error(msgs)

    @classmethod
    def addJoin_and_copy_feature(cls, left_table, righttable, create_id_field, joinField, outpath, joinType=None):
        arcpy.env.qualifiedFieldNames = False
        try:
            templayer = arcpy.MakeFeatureLayer_management(left_table, "temp")

            if arcpy.Exists(outpath):
                logging.warning("This file exists, skipping!!!")
            else:


                if create_id_field == 0:
                    print("adding join")
                    arcpy.AddJoin_management("temp", joinField, righttable, joinField, joinType)
                    print(arcpy.GetMessages(0))
                    logging.info("added join to {}".format(left_table))

                    arcpy.CopyFeatures_management("temp", outpath)
                    print(arcpy.GetMessages(0))
                    logging.info("copied feature to: {}".format(outpath))
                    arcpy.Delete_management("temp")

                if create_id_field == 1:
                    logging.info("create id field selected")
                    arcpy.AddField_management("temp", "id", "TEXT")
                    id_input = "{}+{}".format("!WC_CLLI!", 'str(!TT_ID!)')
                    logging.info("id field is statement is: {}".format(id_input))
                    arcpy.CalculateField_management("temp", "id", expression=id_input, expression_type="python 10.5")

                    print("adding join")
                    arcpy.AddJoin_management("temp", joinField, righttable, joinField, joinType)
                    print(arcpy.GetMessages(0))
                    logging.info("added join")

                    arcpy.CopyFeatures_management("temp", outpath)
                    print(arcpy.GetMessages(0))
                    logging.info("outpath: {}\nmessage: {}".format(outpath, arcpy.GetMessages(0)))
                    arcpy.Delete_management("temp")

        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)
            logging.error(msgs)
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
            logging.error(msgs)
            logging.error(pymsg)
            arcpy.Delete_management("temp")

    @classmethod
    def intersect_files(cls, inlist, outpath):

        try:
            print("intersect......plz wait!!")
            logging.info("intersecting files")
            arcpy.Intersect_analysis(inlist, outpath)
            print(arcpy.GetMessages(0))
            logging.info(arcpy.GetMessages(0))
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


        fcTOfc = get_path.pathFinder(env_0=self.inputGDB)

        stateList = fcTOfc.make_fips_list()
        logging.info("Copying Feature class to Featureclass with wildcard")
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
                        print("deleting file: {}".format(x))
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

    @classmethod
    def add_field(cls, fc, field_name, field_type, field_length):
        try:
            print("\nadding field")
            arcpy.AddField_management(fc, field_name, field_type, field_length)
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


    def export_subsidized_Coverage(self, lte5_table_basepath):
        try:




            sub_Coverage = get_path.pathFinder()
            sub_Coverage.env_0 = self.inputGDB

            StatesList = sub_Coverage.make_fips_list()

            for fips in StatesList:

                pidList = sub_Coverage.query_provider_by_FIPS(os.path.join(lte5_table_basepath,
                                                                           path_links.LTE5_table_path),str(int(fips)))
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


        try:
            fipsList = get_path.pathFinder.make_fips_list()
            if type == "gdb":
                clipFC = get_path.pathFinder()
                clipFC.env_0 = clippath

                inFeatureFC = get_path.pathFinder()
                inFeatureFC.env_0 = infeaturepath


                for state in fipsList:

                    clipwildcard = "*_"+state+"_*"
                    print(clipwildcard)

                    clipFCList = clipFC.get_file_path_with_wildcard_from_gdb(clipwildcard)


                    inFeatureFCList = inFeatureFC.get_path_for_all_feature_from_gdb()

                    for x in inFeatureFCList:
                        inFeatureFCName = os.path.split(x)
                        outfeature = os.path.join(self.outputGDB, inFeatureFCName[1]+"_"+state)
                        print("\n\n\nout Feature:\n{}".format(outfeature))

                        if len(x) ==0 or len(clipFCList) == 0:
                            print("print one of the feature class list are empty skipping")
                        else:
                            print("clip Feature List: {}\nin Feature List: {}".format(clipFCList[0], x))
                            if arcpy.Exists(outfeature):
                                print("Verified {} exists".format(outfeature))
                            else:
                                arcpy.Clip_analysis(x, clipFCList[0], outfeature)
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


        try:
            importShp = get_path.pathFinder()

            ShpList = importShp.get_shapefile_path_walk(self.inputPath)

            for x in ShpList:

                Shppathsplit = os.path.split(x)
                ShpName = Shppathsplit[1]

                if arcpy.Exists(os.path.join(self.outputGDB, ShpName.strip(".shp"))):
                    print("exits, skipping!!!")

                else:
                    arcpy.FeatureClassToGeodatabase_conversion(x, self.outputGDB)
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

    def attach_pid_StateFips_toCoverages(self):
        import re


        fipsList = get_path.pathFinder.make_fips_list()
        stateFips = get_path.pathFinder()
        stateFips.env_0 = self.inputGDB

        for state in fipsList:
            wildcard = "*_" + state
            fcList = stateFips.get_file_path_with_wildcard_from_gdb(wildcard)

            for fc in fcList:

                print("\n",fc)
                fc_path_split = os.path.split(fc)
                fc_name = fc_path_split[1]


                try:

                    print("\nadding field PID Field")
                    arcpy.AddField_management(fc, "PID", "LONG")
                    print(arcpy.GetMessages(0))

                    print("\nadding field pname Field")
                    arcpy.AddField_management(fc, "PNAME", "TEXT", field_length="255")
                    print(arcpy.GetMessages(0))

                    print("\nadding field STATEFIPS Field")
                    arcpy.AddField_management(fc, "STATE_FIPS", "LONG")
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

                finally:


                    fields = ["PID", "PNAME", "STATE_FIPS"]


                    #regex = r'(?i)^(?P<filename>(?P<dba>.+)_(?P<technology>\d{2})_(?P<spectrum>\d{2,3})_(?P<frn>\d{10})(?:_F477_\d+)?__LTE5_(?P<PID>\d{2}))$'
                    #regex = r'(?i)^(?P<filename>(?P<dba>.+)_(?P<technology>\d{2})_(?P<spectrum>\d{2,3})(?P<extra>.+)?)__LTE5_(?P<state>\d{2})'
                    #regex = r'(?i)^(?P<filename>propagation_(?P<provider_id>\d+)_(?P<sname>\w+)_(?P<spectrum>\d+|agg)'\
                    #            '(?:_(?P<bandwidth>\d+)mhz)?_(?P<state_fips>\d{2}))'
                    #regex   =   r'^.*_(?P<state_fips>\d+)$'
                    #final regex
                    regex = r'(?i)^propagation_(?:(?P<state>\d{2})|(?P<area>us))_(?P<pid>\d{1,2})_.*$'

                    namedic = re.match(regex, os.path.basename(fc)).groupdict()

                    pid = int(namedic['pid'])
                    print(pid)

                    #a = get_path.pathFinder.query_provider_pid_by_provider_FRN(path_links.filer_pid_mapping_table_path, FRN)
                    #a = get_path.pathFinder.query_pid_by_dba(path_links.filer_pid_mapping_table_path,dba)
                    a = get_path.pathFinder.query_provider_name_by_pid(path_links.filer_pid_mapping_table_path, pid)
                    print(a)


                    #fc_FRN = a["f477_provider_frn"]
                    #print(a)
                    fc_pid = a["provider_id"]
                    print(fc_pid)


                    print("Populating fields!!!")
                    with arcpy.da.UpdateCursor(fc, fields) as cursor:

                        for row in cursor:
                            if pid == fc_pid:

                                row[0] = a["provider_id"]
                                row[1] = a["provider_name"]
                                row[2] = int(state)
                                cursor.updateRow(row)

                    #with arcpy.da.UpdateCursor(fc, ["STATE_FIPS"]) as cursor:
                    #    for row in cursor:
                    #        row[0] = int(state)
                    #        cursor.updateRow(row)






    def erase_wireCenter_subsidy(self, lte5_table_folder_path, wirecenterEnv, LTE5CoverageEnv):



        stateList = get_path.pathFinder.make_fips_list()

        for state in stateList:

            print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

            print("\n\n\t\t\t\t\tState fips: {}".format(state))

            LTE5CoverageList = get_path.pathFinder.query_provider_by_FIPS(os.path.join(lte5_table_folder_path,
                                                                           path_links.LTE5_table_path), str(int(state)))

            for y in LTE5CoverageList:

                wirecenter_wildcard = "T{}_{}".format(str(int(state)),str(y))
                print("The Wild Card for Subsidy is: {}".format(wirecenter_wildcard))

                wireCenter = get_path.pathFinder()
                wireCenter.env_0 = wirecenterEnv
                wireCenterList = wireCenter.get_file_path_with_wildcard_from_gdb(wirecenter_wildcard)
                #print(wireCenterList)

                coverage_wildcard = "T{}_{}".format(str(int(state)),str(y))
                print("The Wild Card for coverage is: {}".format(wirecenter_wildcard))
                coverage = get_path.pathFinder()
                coverage.env_0 = LTE5CoverageEnv
                coverageList = coverage.get_file_path_with_wildcard_from_gdb(coverage_wildcard)
                #print(coverageList[0])

                # This part looks at Subsidy list that was created using the wildcard.
                # So if the Subsidy list is empty then using the same wildcard that results in coverage list, that coverage
                # would be exported or filtered to '_07_LTE5_Export.gdb' geodatabase.

                if len(wireCenterList)==0 and len(coverageList)==0:
                    print("The wirecenter is missing or CoverageList is empty")

                elif len(wireCenterList) == 0:
                    file_name = os.path.split(coverageList[0])
                    print("\nexporting this {} to out GDB".format(file_name[1]))

                    if arcpy.Exists(os.path.join(
                            self.outputGDB, file_name[1])):
                        print("the file exists, skipping this file:")

                    else:


                        try:
                            print("\nCopying to geodatabase")
                            arcpy.CopyFeatures_management(coverageList[0], os.path.join(
                                self.outputGDB, file_name[1]))


                        except arcpy.ExecuteError:
                            msg = arcpy.GetMessages(2)
                            arcpy.AddError(msg)
                            print(msg)



                # If the wireCenter list is not empty and coverage list is not empty using the same wildcard,
                # then, erase the from Subsidy coverage from _02_Subsidy coverage
                elif len(wireCenterList) != 0 and len(coverageList) != 0:

                    input_file = coverageList[0]

                    erase_feature = wireCenterList[0]

                    file_name = os.path.split(wireCenterList[0])
                    # save response value should be "_07_Erase_wirecenter_subsidy.gdb"
                    output_path = os.path.join(self.outputGDB, "{}".format(file_name[1]))

                    if arcpy.Exists(os.path.join(self.outputGDB, "{}".format(file_name[1]))):
                        print("the file exists, skipping this file:")

                    else:

                        try:
                            print("\nErasing the file please wait!!")
                            arcpy.Erase_analysis(input_file, erase_feature, output_path)

                        except arcpy.ExecuteError:
                            msg = arcpy.GetMessages(2)
                            arcpy.AddError(msg)
                            print(msg)

    def erase_MFI_Blocks(self, lte_tableList_folder):





        mfblocks = get_path.pathFinder()
        mfblocks.env_0 = os.path.join(path_links.inputbasepath, path_links.mfi_subsidized_splits_gdb_name+".gdb")

        coverage = get_path.pathFinder()
        coverage.env_0 = self.inputGDB

        stateList = coverage.make_fips_list()



        for state in stateList:
            print(state)
            pidList = get_path.pathFinder.query_provider_by_FIPS(os.path.join(lte_tableList_folder,
                                                                           path_links.LTE5_table_path), str(int(state)))

            for pid in pidList:

                mfiWildcard = "T" + state + "_" + str(pid)
                print("MF1 Block Wildcard: {}".format(mfiWildcard))
                mfiList = mfblocks.get_file_path_with_wildcard_from_gdb(mfiWildcard)

                coverageWildcard = "T{}_{}".format(str(int(state)),str(pid))
                print("coverage Wildcard: {}".format(coverageWildcard))
                coverageList = coverage.get_file_path_with_wildcard_from_gdb(coverageWildcard)

                if coverageList is None and mfiList is None:
                    print("none type discovered, skipping")

                elif len(mfiList) == 0 and len(coverageList) != 0:
                    file_name = os.path.split(coverageList[0])
                    if arcpy.Exists(os.path.join(self.outputGDB, file_name[1])):
                        print("the file exits")
                    else:

                        print("\nexporting this {} to {}".format(file_name[1], str(self.outputGDB)))

                        print(file_name)
                        try:
                            print("\nCopying to geodatabase")
                            arcpy.CopyFeatures_management(coverageList[0], os.path.join(self.outputGDB, file_name[1]))


                        except arcpy.ExecuteError:
                            msg = arcpy.GetMessages(2)
                            arcpy.AddError(msg)
                            print(msg)



                elif len(coverageList) == 0 and len(mfiList) == 0:
                    print("returned no coverage and no mfi block for this wildcard phrase: {}, {}. Skipping!!!!".format(coverageWildcard, mfiWildcard))


                else:
                    input_file = coverageList[0]

                    erase_feature = mfiList[0]

                    file_name = os.path.split(coverageList[0])
                    output_path = os.path.join(self.outputGDB, "_erased_MF_sub_{}".format(file_name[1]))


                    try:
                        print("\nErasing the file please wait!!")
                        arcpy.Erase_analysis(input_file, erase_feature, output_path)

                    except arcpy.ExecuteError:
                        msg = arcpy.GetMessages(2)
                        arcpy.AddError(msg)
                        print(msg)


    def create_MFII_subsidy_blocks_by_state(self, righttable):


        try:

            blocks = get_path.pathFinder()
            blocks.env_0 = self.inputGDB

            stateList = blocks.make_fips_list()
            arcpy.env.qualifiedFieldNames = False
            for x in stateList:

                wildcard = "*_{}_*".format(x)
                blockList = blocks.get_file_path_with_wildcard_from_gdb(wildcard)

                if len(blockList)==0:
                    print("empty list")
                else:

                    arcpy.MakeFeatureLayer_management(blockList[0], "temp")
                    print("adding join")

                    arcpy.AddJoin_management("temp", in_field="GEOID10", join_table=righttable, join_field='GEOID10',join_type="KEEP_COMMON")
                    print(arcpy.GetMessages(0))
                    blocksname = os.path.split(blockList[0])[1]
                    out_path = os.path.join(self.outputGDB, blocksname)
                    if arcpy.Exists(out_path):
                        print("file exists, skipping")
                        arcpy.Delete_management("temp")

                    else:

                        arcpy.CopyFeatures_management("temp", out_path)
                        print(arcpy.GetMessages(0))
                        arcpy.Delete_management("temp")



        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            arcpy.Delete_management("temp")
            print(msgs)
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(
                sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            arcpy.Delete_management("temp")
            print(pymsg)
            print(msgs)



    def mergeCoverages(self):


        input_obj = get_path.pathFinder(env_0=self.inputGDB)
        stateList = input_obj.make_fips_list()

        for state in stateList:
            wildcard = "*_{}".format(state)


            fcList = input_obj.get_file_path_with_wildcard_from_gdb(wildcard)

            name = "_merged_LTE5_{}".format(state)

            if arcpy.Exists(os.path.join(self.outputGDB, name)):
                print("file exists, skipping!!")

            else:

                try:
                    #fm = arcpy.FieldMap()  # DBA
                    #fm1 = arcpy.FieldMap()  # Technology
                    #fm2 = arcpy.FieldMap()  # Spectrum
                    #fm3 = arcpy.FieldMap()  # MinDown
                   #fm4 = arcpy.FieldMap()  # MinUp
                    fm5 = arcpy.FieldMap()  # PID
                    fm6 = arcpy.FieldMap()  # PNAME
                    fm7 = arcpy.FieldMap()  # STATE_FIPS

                    fms = arcpy.FieldMappings()

                    # DBA
                    for in_file in fcList:
                        #for field in arcpy.ListFields(in_file, "DBA"):
                            #fm.addInputField(in_file, field.name)

                        #for field in arcpy.ListFields(in_file, "Technology"):
                            #fm1.addInputField(in_file, field.name)

                        #for field in arcpy.ListFields(in_file, "Spectrum"):
                            #fm2.addInputField(in_file, field.name)

                        #for field in arcpy.ListFields(in_file, "MinDown"):
                            #fm3.addInputField(in_file, field.name)

                        #for field in arcpy.ListFields(in_file, "MinUp"):
                            #fm4.addInputField(in_file, field.name)

                        for field in arcpy.ListFields(in_file, "PID"):
                            fm5.addInputField(in_file, field.name)

                        for field in arcpy.ListFields(in_file, "PNAME"):
                            fm6.addInputField(in_file, field.name)

                        for field in arcpy.ListFields(in_file, "STATE_FIPS"):
                            fm7.addInputField(in_file, field.name)

                    # DBA
                    #fm.mergeRule = "First"

                    #f_name = fm.outputField
                    #f_name.name = 'DBA'
                    #f_name.length = 255
                    #f_name.type = "Text"

                    #fm.outputField = f_name

                    #fms.addFieldMap(fm)

                    # Technology
                    #fm1.mergeRule = "First"

                    #f_name = fm1.outputField
                    #f_name.name = 'Technology'
                    #f_name.type = "Short Integer"

                    #fm1.outputField = f_name

                    #fms.addFieldMap(fm1)

                    # Spectrum
                    #fm2.mergeRule = "First"

                    #f_name = fm2.outputField
                    #f_name.name = 'Spectrum'
                    #f_name.type = "Short Integer"

                    #fm2.outputField = f_name

                    #fms.addFieldMap(fm2)

                    # MinDown
                    #fm3.mergeRule = "First"

                    #f_name = fm3.outputField
                    #f_name.name = 'MinDown'
                    #f_name.type = "Short Integer"

                    #fm3.outputField = f_name

                    #fms.addFieldMap(fm3)

                    # MinUp
                    #fm4.mergeRule = "First"

                    #f_name = fm4.outputField
                    #f_name.name = 'MinUp'
                    #f_name.type = "Short Integer"

                    #fm4.outputField = f_name

                    #fms.addFieldMap(fm4)

                    # Pid

                    fm5.mergeRule = "First"

                    f_name = fm5.outputField
                    f_name.name = 'PID'
                    f_name.type = "Long Integer"

                    fm5.outputField = f_name

                    fms.addFieldMap(fm5)

                    # PNAME

                    fm6.mergeRule = "First"

                    f_name = fm6.outputField
                    f_name.name = 'PNAME'
                    f_name.type = "TEXT"

                    fm6.outputField = f_name

                    fms.addFieldMap(fm6)

                    # STATE_FIPS

                    fm7.mergeRule = "First"

                    f_name = fm7.outputField
                    f_name.name = 'STATE_FIPS'
                    f_name.type = "Long Integer"

                    fm7.outputField = f_name

                    fms.addFieldMap(fm7)

                    print("\n=========================================================")
                    print("Merging {}, plz wait".format(os.path.join(self.outputGDB, name)))
                    arcpy.Merge_management(fcList, os.path.join(self.outputGDB, name) , fms)
                    print(arcpy.GetMessages(0))
                    print("=========================================================\n")

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



    def dissolveCoverages(self):


        try:

            diss = get_path.pathFinder()
            diss.env_0 = self.inputGDB

            stateList = diss.make_fips_list()

            for state in stateList:

                wildcard = "*_{}".format(state)
                print(wildcard)

                mergeLTEList = diss.get_file_path_with_wildcard_from_gdb(wildcard)

                dissField = ["STATE_FIPS", "PID", "PNAME"]

                if len(mergeLTEList) ==0:
                    print("the merge list is empty")
                else:


                    out_features = os.path.join(self.outputGDB, "_diss_" + os.path.basename(mergeLTEList[0]))

                    if arcpy.Exists(out_features):
                        print("{} exists!! Skipping!!".format(out_features))
                        print("\n\n\n ------------------------------------------------------------")

                    else:
                        print("dissolving {}".format(os.path.basename(mergeLTEList[0])))
                        arcpy.Dissolve_management(mergeLTEList[0], out_features, dissField )
                        print(arcpy.GetMessages(0))
                        print("\n\n\n ------------------------------------------------------------")


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


    def create_number_LTE5_perState_table(self, name):

        import pandas as pd

        featureclass = get_path.pathFinder()
        featureclass.env_0 = self.inputGDB

        fcList = featureclass.get_path_for_all_feature_from_gdb()

        field = "pid"

        state_dic = {}

        for x in fcList:
            # Use SearchCursor with list comprehension to return a
            # unique set of values in the specified field
            input_table = os.path.join(x)
            values = [row[0] for row in arcpy.da.SearchCursor(input_table, field)]
            uniqueValues = set(values)

            state_dic[x[-2:]] = uniqueValues

        print("\n\n\n\n\n")
        print(state_dic, sep=",")

        df = pd.DataFrame.from_dict(state_dic, orient="index")

        df.sort_index

        #df.columns = ["pidnum_1", "pidnum_2", "pidnum_3", "pidnum_4",
                      #'pidnum_5', 'pidnum_6', 'pidnum_7', 'pidnum_8']

        print(df)

        df.to_csv(os.path.join(self.outputPathFolder, name),
                  index_label="stateFIPS")



    def intersect_coverages_by_stateGrid(self, lte_output_table_folder_path):


        stateList = get_path.pathFinder.make_fips_list()


        coverages = get_path.pathFinder()
        coverages.env_0 = self.inputGDB

        for state in stateList:
            print("\t\t\t\t\tFIPS: {}".format(state))

            providerList = get_path.pathFinder.query_provider_by_FIPS(os.path.join(lte_output_table_folder_path,
                                                                           path_links.LTE5_table_path), str(int(state)))
            print(providerList)

            grid_wildcard = "*_" + state
            print("\tthe wildcard for grid is: {}".format(grid_wildcard))

            gridList = get_path.pathFinder.get_shapefile_path_wildcard(path_links.raw_state_grid, grid_wildcard)

            for pid in providerList:

                ineligible_wildcard = '*' + str(int(state)) + '_' + str(pid)
                print("\t\tIneligible fc wildcard: {}".format(ineligible_wildcard))

                ineligibleList = coverages.get_file_path_with_wildcard_from_gdb(ineligible_wildcard)

                if len(ineligibleList) == 0 or len(gridList) == 0:

                    print("Unable to intersect, one or more parameter is missing!!!")


                else:
                    inputList = [gridList[0], ineligibleList[0]]
                    print("the input list:\n {}".format(inputList))

                    output = os.path.join(self.outputGDB, "Coverage_map_" + state + "_" + str(pid))
                    print("The out path is: {}".format(output))

                    if arcpy.Exists(output):
                        print("file exits, skipping")

                    else:


                        try:

                            arcpy.Intersect_analysis(inputList, output)
                            print(arcpy.GetMessages(0))


                        except arcpy.ExecuteError:
                            msg = arcpy.GetMessages(2)
                            arcpy.AddError(msg)
                            print(msg)
                            print("FIPS: {}\nInput List: {}\nMessage: {}".format(state, inputList, msg))


    def dissolve_ineligible_coverages(self):

        try:

            in_features = get_path.pathFinder()
            in_features.env_0 = self.inputGDB

            in_featuresList = in_features.get_path_for_all_feature_from_gdb()

            dissolve_field = ["STATE_FIPS", "GRID_COL", "GRID_ROW", "pid", "PNAME"]
            print("dissovle parameters: {}".format(dissolve_field))

            for x in in_featuresList:

                print("\n\n\n ------------------------------------------------------------")

                out_features = os.path.join(self.outputGDB, os.path.basename(x))

                if arcpy.Exists(out_features):
                    print("{} exists!! Skipping!!".format(out_features))

                    print("\n\n\n ------------------------------------------------------------")

                else:
                    print("dissolving {}".format(x))


                    try:
                        arcpy.Dissolve_management(x, out_features, dissolve_field)
                        print(arcpy.GetMessages(0))

                        print("\n\n\n ------------------------------------------------------------")
                    except arcpy.ExecuteError:
                        msg = arcpy.GetMessages(2)
                        arcpy.AddError(msg)
                        print(msg)
                        print("the state file name is: {}\n".format(x))
                        print("{}\n".format(msg))



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


    def create_water_area_blocks(self, expression):

        try:

            fcTOfc = get_path.pathFinder(env_0=self.inputGDB)

            stateList = fcTOfc.make_fips_list()

            for state in stateList:
                wildcard = "*_" + state + "_*"
                fcList = fcTOfc.get_file_path_with_wildcard_from_gdb(wildcard)
                print(fcList)

                if len(fcList) == 0:
                    print("there is no feature class by that query")
                else:
                    where_clause = expression
                    print(where_clause)
                    split_name = os.path.split(fcList[0])
                    outname = "water_only_blocks_" + split_name[1][:-11]
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

    def dissolveWaterArea(self):


        try:

            diss = get_path.pathFinder()
            diss.env_0 = self.inputGDB

            stateList = diss.make_fips_list()

            for state in stateList:

                wildcard = "*_{}".format(state)
                print(wildcard)

                mergeLTEList = diss.get_file_path_with_wildcard_from_gdb(wildcard)

                dissField = []

                if len(mergeLTEList) ==0:
                    print("the merge list is empty")
                else:


                    out_features = os.path.join(self.outputGDB, "_diss_" + os.path.basename(mergeLTEList[0]))

                    if arcpy.Exists(out_features):
                        print("{} exists!! Skipping!!".format(out_features))
                        print("\n\n\n ------------------------------------------------------------")

                    else:
                        print("dissolving {}".format(os.path.basename(mergeLTEList[0])))
                        arcpy.Dissolve_management(mergeLTEList[0], out_features, dissField )
                        print(arcpy.GetMessages(0))
                        print("\n\n\n ------------------------------------------------------------")


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


    def intersect_water_by_stateGrid(self):


        try:


            stateList = get_path.pathFinder.make_fips_list()


            water_area = get_path.pathFinder()
            water_area.env_0 = self.inputGDB

            for state in stateList:
                print("\t\t\t\t\tFIPS: {}".format(state))

                wildcard = "*_" + state
                print("\tthe wildcard for grid is: {}".format(wildcard))

                gridList = get_path.pathFinder.get_shapefile_path_wildcard(path_links.raw_state_grid, wildcard)


                waterAreaList = water_area.get_file_path_with_wildcard_from_gdb(wildcard)

                if len(waterAreaList) == 0 or len(gridList) == 0:

                    print("Unable to intersect, one or more parameter is missing!!!")


                else:
                    inputList = [gridList[0], waterAreaList[0]]
                    print("the input list:\n {}".format(inputList))

                    output = os.path.join(self.outputGDB, "Water_area_" + state)
                    print("The out path is: {}".format(output))

                    if arcpy.Exists(output):
                        print("file exits, skipping")

                    else:


                        try:

                            arcpy.Intersect_analysis(inputList, output)
                            print(arcpy.GetMessages(0))


                        except arcpy.ExecuteError:
                            msg = arcpy.GetMessages(2)
                            arcpy.AddError(msg)
                            print(msg)
                            print("FIPS: {}\nInput List: {}\nMessage: {}".format(state, inputList, msg))


        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)


    def erase_water_blocks_from_coverage(self, lte_table_output_folder):


        try:

            stateList = get_path.pathFinder.make_fips_list()

            infeature = get_path.pathFinder()
            infeature.env_0 = self.inputGDB

            erasefeature = get_path.pathFinder()
            erasefeature.env_0 = path_links.water_blocks_gdb

            for state in stateList:

                erasewildcard = "*_"+state
                erasefeatureList = erasefeature.get_file_path_with_wildcard_from_gdb(erasewildcard)

                pidList = get_path.pathFinder.query_provider_by_FIPS(os.path.join(lte_table_output_folder,
                                                                           path_links.LTE5_table_path), str(int(state)))

                for provider in pidList:

                    print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx state: {} xxxx prividor id: {} xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n\n".format(state, provider))
                    infeatureWildcard = "*_{}_{}".format(state, provider)

                    infeatureList = infeature.get_file_path_with_wildcard_from_gdb(infeatureWildcard)



                    if len(infeatureList) ==0 or len(erasefeatureList)==0:
                        print("one or more feature classes are mising for state: {}".format(state))
                    else:

                        print("\n\nIn feature class is {}\nErase feature class is {}".format(os.path.basename(infeatureList[0]), os.path.basename(erasefeatureList[0])))

                        outfeature = os.path.join(self.outputGDB, os.path.basename(infeatureList[0]))

                        if arcpy.Exists(outfeature):
                            print("\nthe feature class exists, Skipping!!!!!!!!!!!!!!!!!!!!!!!!!!")

                        else:
                            print("\n\nerasing, hold your horses")

                            arcpy.Erase_analysis(infeatureList[0],erasefeatureList[0], outfeature)
                            print(arcpy.GetMessages(0))
                            print()

        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)

    def add_field_for_all_fc(self, field_name, field_type, field_length):


        fcObj = get_path.pathFinder()
        fcObj.env_0 = self.inputGDB

        fcList = fcObj.get_path_for_all_feature_from_gdb()

        for fc in fcList:

            try:
                print("\nadding field")
                arcpy.AddField_management(fc, field_name, field_type, field_length)
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



    def calculate_area_in_meters(self, field_name):


        fc = get_path.pathFinder()
        fc.env_0 = self.inputGDB

        fcList = fc.get_path_for_all_feature_from_gdb()

        for x in fcList:
            try:

                print("\nlooking into {}".format(os.path.basename(x)))

                exp = "!SHAPE.geodesicArea@SQUAREMETERS!"
                arcpy.CalculateField_management(x, field_name, exp, "PYTHON_10.5")
                print("calculated!!!")


            except:
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
                arcpy.AddError(pymsg)
                arcpy.AddError(msgs)
                print(pymsg)
                print(msgs)


    def drop_diminimus_area(self):


        fcObj = get_path.pathFinder()
        fcObj.env_0 = self.inputGDB

        fcList = fcObj.get_path_for_all_feature_from_gdb()

        for fc in fcList:

            in_features = fc
            print("\n\nIn Feature: {}".format(os.path.basename(fc)))
            out_path = self.outputGDB
            out_name = os.path.basename(fc)

            where_clause = "area > {}".format(225 * 225)

            try:
                arcpy.FeatureClassToFeatureClass_conversion(in_features, out_path, out_name, where_clause)
                print(arcpy.GetMessages(0))


            except arcpy.ExecuteError:
                msg = arcpy.GetMessages(2)
                arcpy.AddError(msg)
                print(msg)


    def merge_ineligible_coverages(self):

        merge = get_path.pathFinder()
        merge.env_0 = self.inputGDB

        stateList = merge.make_fips_list()

        for state in stateList:

            wildcard = "*_"+state+"_*"
            print("\t\t\t\txxxxxxxxxxx state: {}; Wildcard: {} xxxxxxxxxxxxxx\n".format(state, wildcard))
            mergeList = merge.get_file_path_with_wildcard_from_gdb(wildcard)
            print(mergeList)

            outfeature = os.path.join(self.outputGDB, "_merged_"+state)

            if arcpy.Exists(outfeature):
                print("file already Exists, Skipping !!!!!!!!!!!!!!!!!\n")

            elif len(mergeList) ==0:
                print("merged list is zero, skipping!!!!")

            else:

                try:
                    print("Merging files")
                    arcpy.Merge_management(mergeList,outfeature)
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



    def erase_coverages_from_state_boundary(self):

        eraseFeature = get_path.pathFinder()
        eraseFeature.env_0 = self.inputGDB
        stateList = eraseFeature.make_fips_list()

        for state in stateList:
            wildcard = "*_"+state
            print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx state: {} xxxx wildcard: {} xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n\n".format(
                    state, wildcard))
            eraseFeatureList = eraseFeature.get_file_path_with_wildcard_from_gdb(wildcard)
            inputFeatureList = get_path.pathFinder.get_shapefile_path_wildcard(path_links.raw_state_grid,wildcard)

            outFeature = os.path.join(self.outputGDB,"eligible_area_"+state)

            if arcpy.Exists(outFeature):
                print("this file already exists, skipping !!!!!!!!!!!!!!!!!!")

            else:

                if len(eraseFeatureList) == 0 or len(inputFeatureList)==0:
                    print("The erase feature or input feature is empty")
                else:

                    try:

                        arcpy.Erase_analysis(inputFeatureList[0],eraseFeatureList[0],outFeature)
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


    def erase_water_blocks_from_eligible_area(self):


        try:

            stateList = get_path.pathFinder.make_fips_list()

            infeature = get_path.pathFinder()
            infeature.env_0 = self.inputGDB

            erasefeature = get_path.pathFinder()
            erasefeature.env_0 = path_links.water_blocks_gdb

            for state in stateList:

                erasewildcard = "*_"+state
                erasefeatureList = erasefeature.get_file_path_with_wildcard_from_gdb(erasewildcard)

                infeatureList = infeature.get_file_path_with_wildcard_from_gdb(erasewildcard)



                print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx state: {} xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n\n".format(state))


                if len(infeatureList) ==0 or len(erasefeatureList)==0:
                    print("one or more feature classes are mising for state: {}\n\n".format(state))
                else:

                    print("\n\nIn feature class is: {}\nErase feature class is: {}".format(os.path.basename(infeatureList[0]), os.path.basename(erasefeatureList[0])))

                    outfeature = os.path.join(self.outputGDB, os.path.basename(infeatureList[0]))

                    if arcpy.Exists(outfeature):
                        print("\nthe feature class exists, Skipping!!!!!!!!!!!!!!!!!!!!!!!!!!")

                    else:
                        print("\n\nerasing, hold your horses")

                        arcpy.Erase_analysis(infeatureList[0],erasefeatureList[0], outfeature)
                        print(arcpy.GetMessages(0))
                        print()

        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)



    def diceLTE5Coverages(self):

        try:

            fc = get_path.pathFinder(env_0=self.inputGDB)
            fcList  = fc.get_path_for_all_feature_from_gdb()

            for x in fcList:

                print("Dicing:\n{}\n".format(os.path.basename(x)))

                outfeature = os.path.join(self.outputGDB, "diced_"+os.path.basename(x))
                vertxLimit = 10000

                if arcpy.Exists(outfeature):
                    print("this file exits, skipping !!!!\n")

                else:

                    print("Dicing files, please wait !!\n")
                    arcpy.Dice_management(x,outfeature,vertxLimit)
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

