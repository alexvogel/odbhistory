#!/usr/bin/python

import sys
import re

if len(sys.argv)!=2:
    print "call: abaqus python $scriptname $odbfile"
    sys.exit()

from odbAccess import *
from textRepr import *

odbfile = sys.argv[1]
if isUpgradeRequiredForOdb(odbfile):
    print "The database is from a previous release of Abaqus."
    print "Run abaqus -upgrade -job <newFileName> -odb <oldOdbFileName> to upgrade it."
    sys.exit()

odb=openOdb(odbfile)

#prettyPrint(odb,2)

#print "odbfile"

#from odbAccess import *
#from textRepr import *
#odb=openOdb('odbfile')

###############################
#
# Stepabfrage
#
###############################
print "======="
print "These steps are available in " + odb.name# + str(odb.sectionCategories)
print "-------"
stepNames = odb.steps.keys()

stepNr = 0
for stepName in stepNames:
    print "(" + str(stepNr) + ") " + stepName
    stepNr+=1
print "-------"

desired_step_nr = input("Please specify the step of desire: ")

while (((len(stepNames)-1) < desired_step_nr ) or (desired_step_nr < 0)):
    desired_step_nr = input("unknown choice - please use an index mentioned above: ")

step = str(stepNames[desired_step_nr])
print "You've chosen step '" + step + "'"

###############################
#
# Historyregionabfrage
#
###############################
print "======="
print "These historyRegions are available in " + step
print "-------"

historyregionNames = odb.steps[str(stepNames[desired_step_nr])].historyRegions.keys()
historyregionNr = 0

print historyregionNames
for historyregionName in historyregionNames:
    print "(" + str(historyregionNr) + ") " + historyregionName
    historyregionNr+=1
print "-------"

desired_historyregion_nr = input("Please specify the historyRegion of desire: ")

while (((len(historyregionNames)-1) < desired_historyregion_nr ) or (desired_historyregion_nr < 0)):
    desired_historyregion_nr = input("unknown choice - please use an index mentioned above: ")

historyregion = str(historyregionNames[desired_historyregion_nr])
print "You've chosen historyRegion '" + historyregion + "'"

###############################
#
# Historyoutput Abfrage
#
###############################
print "======="
print "These historyOutputs are available in " + historyregion
print "-------"


historyOutputNr = 0
historyOutputs = odb.steps[str(stepNames[desired_step_nr])].historyRegions[historyregion].historyOutputs.keys()

print historyOutputs

for historyOutput in historyOutputs:
    print "(" + str(historyOutputNr) + ") " + historyOutput
    historyOutputNr+=1
print "-------"

desired_historyoutput_nr = input("Please specify the historyOutput of desire: ")

while (((len(historyOutputs)-1) < desired_historyoutput_nr ) or (desired_historyoutput_nr < 0)):
    desired_historyoutput_nr = input("unknown choice - please use an index mentioned above: ")

historyOutput = historyOutputs[desired_historyoutput_nr]
print "You've chosen historyOutput '" + historyOutput + "'"

###############################
#
# Output Abfrage
#
###############################

print "======="
print "These outputs are available: "
print "(example result) is from the first value of actual region: "
print "-------"

# holen aller repositories in gewaehltem historyoutput
output = odb.steps[str(stepNames[desired_step_nr])].historyRegions[historyregion].historyOutputs[historyOutput]

# dir() erzeugt eine liste aller moeglichen attribute des uebergebenen objektes
attrs = dir(output)

# liste filtern: alle rausschmeissen, die mit "_" beginnen und "addData" und "conjugateData" auch raus.
#print attrs
selected_attrs = []
for attr in attrs:
    if (re.match('[^_]', str(attr)) and str(attr) != "addData" and str(attr) != "conjugateData"):
        selected_attrs.append(attr)

print selected_attrs

outputNr = 0
for selected_attr in selected_attrs:
    try:
        result = getattr(output, selected_attr)
    except:
        pass
#                        print "(" + str(outputNr) + ") " + selected_attr + " = "+str(result)
    print "(" + str(outputNr) + ") " + selected_attr + " ("+str(result)+")"
    outputNr+=1
print "-------"
                # User Abfrage
desired_output_nr = raw_input("Please specify output: ")
while ((re.search('\D', str(desired_output_nr))) or ((len(selected_attrs)-1) < int(desired_output_nr)) or (int(desired_output_nr)) < 0):
#                    print desired_output_nr
    desired_output_nr = raw_input("impermissible choice - please use an index mentioned above: ")

#                field = frame.fieldOutputs[fieldKeys[int(desired_output_nr)]].getSubset(region=self.region)
outputname = str(selected_attrs[int(desired_output_nr)])
print "You've chosen output '" +outputname+ "'"

print output.data
                # bei nodeSets und elementSets gibt es mehrere Ergebnisdaten, deshalb ein array
