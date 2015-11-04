from odbAccess import *
import sys
import re
class history(object):
    "all die auspraegungen"

    
    def __init__(self, argument):
#        self.batch    = argument.batch
        self.interactive = argument.interactive
        if (self.interactive):
            self.batch = False
        else:
            self.batch = True

        self.arg_odb  = str(argument.odb)
        self.odb      = self._getodb(self.arg_odb)

        
        self.arg_stepname, self.step     = self._getstep(str(argument.stepname))

        self.arg_region, self.region     = self._getregion(str(argument.region))
        
# feststellen des koordinatensystems
#        self.arg_coordsys, self.coordsys = self._getcoordsys(str(argument.coordsys))

# self.history enthaelt nur die histories fuer die ermittelte region
        self.arg_history, self.history   = self._gethistory(str(argument.history))
        self.arg_output, self.output     = self._getoutput(str(argument.output))

        self.arg_postfunction, self.postfunction = self._getpostfunction(str(argument.postfunction))

        self.result = self._getresult()

    def print_args(self):
        for attribute, value in self.__dict__.iteritems():
            print attribute, value
            
    def check_odb_update_required(self):
        if isUpgradeRequiredForOdb(self.odbfile):
            print "The database is from a previous release of Abaqus."
            print "Run abaqus -upgrade -job <newFileName> -odb <oldOdbFileName> to upgrade it."
            sys.exit()
        else:
            print "no update is required for odb-File "+self.odbfile

# =============================
# Method: ermittlung des odb-objektes
# =============================
    def _getodb(self, odbfile):
        if isUpgradeRequiredForOdb(odbfile):
            print "The database is from a previous release of Abaqus."
            print "Run abaqus -upgrade -job <newFileName> -odb <oldOdbFileName> to upgrade it."
            sys.exit()
        else:
            if (self.batch == False):
                print "no update is required for odb-File "+odbfile
            
            odb=openOdb(odbfile, readOnly=True)
            return(odb)

# =============================
# Method: ermittlung des step-objektes
# =============================
    def _getstep(self, stepname):
        # feststellen ob stepname in odb vorhanden ist
        # wenn nicht, dann im --batch-Modus aussteigen und qualifizierte Meldung machen
        # wenn nicht, dann im interaktiv-Modus den Step abfragen
        odb = self.odb
        try:
            odb.steps[stepname]
        except KeyError:
            if (self.batch):
                print "stepname '"+stepname+"' does not exist in odb '"+odb.name+"'"
                sys.exit()
            else:
                print "======="
                print "These steps are available in " + odb.name# + str(odb.sectionCategories)
                print "-------"
                stepNames = odb.steps.keys()

                stepNr = 0
                for stepName in stepNames:
                    print "(" + str(stepNr) + ") " + stepName
                    stepNr+=1
                print "-------"

                # User Abfrage
                desired_step_nr = raw_input("Please specify step: ")
                while ((re.search('\D', str(desired_step_nr))) or ((len(stepNames)-1) < int(desired_step_nr)) or (int(desired_step_nr)) < 0):
                    desired_step_nr = raw_input("impermissible choice - please use an index mentioned above: ")

                stepname = str(stepNames[int(desired_step_nr)])
                print "You've chosen step '" + stepname + "'"
                return (stepname, odb.steps[stepname])

        return (stepname, odb.steps[stepname])

# =============================
# Method: ermittlung der historyregion
# =============================
    def _getregion(self, region):

        try:
            self.step.historyRegions[region]
        except KeyError:
            if (self.batch):
                print "historyRegion '"+region+"' does not exist in odb '"+self.odb.name+"'"
                sys.exit()
            else:
                print "======="
                print "These historyRegions are available in " + self.odb.name
                print "-------"
                historyregionNames = self.step.historyRegions.keys()

                historyregionNr = 0

                for historyregionName in historyregionNames:
                    print "(" + str(historyregionNr) + ") " + historyregionName
                    historyregionNr+=1
                print "-------"

                # User Abfrage
                desired_historyregion_nr = raw_input("Please specify historyRegion: ")
                while ((re.search('\D', str(desired_historyregion_nr))) or ((len(historyregionNames)-1) < int(desired_historyregion_nr)) or (int(desired_historyregion_nr)) < 0):
                    desired_historyregion_nr = raw_input("impermissible choice - please use an index mentioned above: ")

                historyregionname = str(historyregionNames[int(desired_historyregion_nr)])
                print "You've chosen historyRegion '" + historyregionname + "'"
                return (historyregionname, self.step.historyRegions[historyregionname])

        return (region, self.step.historyRegions[region])

# =============================
# Method: ermittlung der historyOutputs
# =============================
    def _gethistory(self, history):

        try:
            self.region.historyOutputs[history]
        except KeyError:
            if (self.batch):
                print "historyOutput '"+history+"' does not exist in odb '"+self.odb.name+"'"
                sys.exit()
            else:
                print "======="
                print "These historyOutputs are available in " + self.odb.name
                print "-------"
                historyoutputNames = self.region.historyOutputs.keys()

                historyoutputNr = 0

                for historyoutputName in historyoutputNames:
                    print "(" + str(historyoutputNr) + ") " + historyoutputName
                    historyoutputNr+=1
                print "-------"

                # User Abfrage
                desired_historyoutput_nr = raw_input("Please specify historyOutput: ")
                while ((re.search('\D', str(desired_historyoutput_nr))) or ((len(historyoutputNames)-1) < int(desired_historyoutput_nr)) or (int(desired_historyoutput_nr)) < 0):
                    desired_historyoutput_nr = raw_input("impermissible choice - please use an index mentioned above: ")

                historyoutputname = str(historyoutputNames[int(desired_historyoutput_nr)])
                print "You've chosen historyOutput '" + historyoutputname + "'"
                return (historyoutputname, self.region.historyOutputs[historyoutputname])

        return (history, self.region.historyOutputs[history])

# =============================
# Method: ermittlung des output-objektes
# =============================
    def _getoutput(self, outputname):

        output = None
        try:
#            output_array = []

            if (outputname == "None"):
                raise

            for attr in dir(self.history):     # dir() erzeugt eine liste aller moeglichen attribute des uebergebenen objektes
#                print attr

                if (str(attr) == outputname):
#                    print "YIPEEEE "+str(attr)+" is "+outputname
                    output = (getattr(self.history, outputname))
            
            if (output == None):
#                print "SHIT"
                raise
            
#                output_array.append(getattr(value, outputname))
#            odb.steps[self.stepname].frames
#            odb.steps[str(stepNames[desired_step_nr])].frames
#        except KeyError or TypeError:
        except:
            if (self.batch):
                print "output '"+outputname+"' does not exist in historyOutput '"+self.history.name+"'"
                sys.exit()
            else:
                print "======="
                print "These outputs are available: "
#                print "(example result) is from the first value of actual region: "
                print "-------"

                attrs = dir(self.history)
                selected_attrs = []                              #eine gefilterte liste erstellen (ohne __blabla__ etc)
                for attr in attrs:
                    if (re.match('[^_]', str(attr)) and str(attr) != "addData" and str(attr) != "conjugateData"):
                        selected_attrs.append(attr)
                
                outputNr = 0
                for selected_attr in selected_attrs:
                    try:
                        result = getattr(self.history, selected_attr)
                        print "(" + str(outputNr) + ") " + selected_attr + " ("+str(result)+")"
                        outputNr+=1
                    except:
                        pass
#                        print "(" + str(outputNr) + ") " + selected_attr + " = "+str(result)
                print "-------"

                # User Abfrage
                desired_output_nr = raw_input("Please specify output: ")
                while ((re.search('\D', str(desired_output_nr))) or ((len(selected_attrs)-1) < int(desired_output_nr)) or (int(desired_output_nr)) < 0):
#                    print desired_output_nr
                    desired_output_nr = raw_input("impermissible choice - please use an index mentioned above: ")

#                field = frame.fieldOutputs[fieldKeys[int(desired_output_nr)]].getSubset(region=self.region)
                outputname = str(selected_attrs[int(desired_output_nr)])
                print "You've chosen output '" +outputname+ "'"
                
                # bei nodeSets und elementSets gibt es mehrere Ergebnisdaten, deshalb ein array
                output = getattr(self.history, outputname)
                return (outputname, output)

        return (outputname, output)


# =============================
# Method: ermittlung der postfunction
# =============================
    def _getpostfunction(self, postfunction):

        postfunctions = ("none", "time,value", "value,time", "stepname,time,value", "steptime,time,value", "steptime+time,value")
        
        try: # feststellen, ob es die postfunction ueberhaupt gibt
            if (postfunction not in postfunctions):
                raise ('unknown postfunction '+ postfunction)
            else:
                return (postfunction, postfunction) 
            
        except:
            if (self.batch):
                print "error: unknown postfunction "+postfunction
                sys.exit()
            else:
                print "======="
                print "These postfunctions are available "
                print "If you don't know - try 'none' first"
                print "-------"

                postfunctionNr = 0
                
                for postfunction in postfunctions:
                    print "(" + str(postfunctionNr) + ") " + postfunction
                    postfunctionNr +=1
                print "-------"

                # User Abfrage
                desired_postfunction_nr = raw_input("Please specify postfunction: ")
                while ((re.search('\D', str(desired_postfunction_nr))) or ((len(postfunctions)-1) < int(desired_postfunction_nr)) or (int(desired_postfunction_nr)) < 0):
#                    print desired_coordsys_nr
                    desired_postfunction_nr = raw_input("impermissible choice - please use an index mentioned above: ")

                postfunction = postfunctions[int(desired_postfunction_nr)]
                print "You've chosen postfunction '" +postfunction+ "'"
                
                return (postfunction, postfunction)

# =============================
# Method: ermittlung des results
# =============================
    def _getresult(self):

#        for output in output_array:
#            search = re.search('[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?\s*,\s*[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?\s*,\s*[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?', str(output))
##           search = re.search('\(.+\)', str(output))
##            search2 = re.search('[^\[\]]', search.group())
#            if (search):
#                array = search.group()
#                output = array
##                print str(array)
#            print str(output)
        ergebnis = self.output
        output_array_to_iterate = []
#        print type(output_array_to_iterate)
        if ((type(self.output) == tuple) or (type(self.output) == list)):
            output_array_to_iterate = self.output
#            print "ist ein tuple oder list"
        else:
            output_array_to_iterate.append(self.output)
#            print "ist kein tuple oder list"

        for output_array_item in output_array_to_iterate:

            if self.postfunction == "none":
                ergebnis = str(output_array_item)

            elif self.postfunction == "time,value":
                search = re.search('^\((.+)\)$', str(output_array_item))
                if (search):
                    ergebnis = str(search.group(1))
                else:
                    ergebnis = "output '"+str(output_array_item)+"' doesn't match pattern used in postfunction 'time,value'"

            elif self.postfunction == "value,time":
                search = re.search('^\((.+),\s*(.+)\)$', str(output_array_item))
                if (search):
                    ergebnis_time = str(search.group(1))
                    ergebnis_value = str(search.group(2))
                    ergebnis = ergebnis_value+", "+ergebnis_time
                else:
                    ergebnis = "output '"+str(output_array_item)+"' doesn't match pattern used in postfunction 'value,time'"

            elif self.postfunction == "stepname,time,value":
                search = re.search('^\((.+)\)$', str(output_array_item))
                if (search):
                    ergebnis = str(self.step.name)+", "+str(search.group(1))
                else:
                    ergebnis = "output '"+str(output_array_item)+"' doesn't match pattern used in postfunction 'stepname,time,value'"

            elif self.postfunction == "steptime,time,value":
                search = re.search('^\((.+)\)$', str(output_array_item))
                if (search):
                    ergebnis = str(self.step.totalTime)+", "+str(search.group(1))
                else:
                    ergebnis = "output '"+str(output_array_item)+"' doesn't match pattern used in postfunction 'steptime,time,value'"

            elif self.postfunction == "steptime+time,value":
                search = re.search('^\((.+),\s*(.+)\)$', str(output_array_item))
                if (search):
                    ergebnis_time = str(search.group(1))
                    ergebnis_value = str(search.group(2))
                    ergebnis_steptime_plus_time = self.step.totalTime + float(ergebnis_time)
                    ergebnis = str(ergebnis_steptime_plus_time)+", "+ergebnis_value
                else:
                    ergebnis = "output '"+str(output_array_item)+"' doesn't match pattern used in postfunction 'steptime+time,value'"

# ausgabe des ergebniswertes
            print ergebnis

#        print self.output

        if (self.batch == False):
# um die datenmoeglichkeiten zu sehen, die folgende zeile einkommentieren
#            print dir(self.step)
# falls in den einzelnen parametern blanks vorkommen, werden diese maskiert mit anfuehrungszeichen
            arg_region_evtl_mit_anfuehrungszeichen = self.arg_region
            search = re.search('[\s;]+', self.arg_region)
            if (search):
                arg_region_evtl_mit_anfuehrungszeichen = "\""+self.arg_region+"\""
            
            arg_history_evtl_mit_anfuehrungszeichen = self.arg_history
            search = re.search('[\s;]+', str(self.arg_history))
            if (search):
                arg_history_evtl_mit_anfuehrungszeichen = "\""+self.arg_history+"\""
            
            print "To get the same information in batch mode, call:"
            command = "abaqus python "+sys.argv[0]+" --odb "+self.arg_odb+" --stepname "+self.arg_stepname+" --region "+arg_region_evtl_mit_anfuehrungszeichen+" --history "+arg_history_evtl_mit_anfuehrungszeichen+" --output "+self.arg_output+" --postfunction "+self.arg_postfunction
            print command
