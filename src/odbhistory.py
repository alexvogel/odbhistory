import sys
import os
odbhistory_version = "[% version %]"
odbhistory_date = "[% date %]"

# 0.01    09.02.2012    Erste Version bei BMW
# 0.02    10.02.2012    Dev. Korrekturen bei postfunctions
# 0.03    27.03.2012    Wenn ein ";" in historyRegion oder historyOutput vorkommt, wird der Namen in Anfuehrungszeichen eingeschlossen

#print "Script dir: ", os.path.realpath(os.path.dirname(sys.argv[0]))

external_lib = os.path.realpath(os.path.dirname(sys.argv[0])) + "/../lib"
sys.path.append(external_lib)
#print sys.path
import argparse
from history import *

# Definieren der Kommandozeilenparameter
parser = argparse.ArgumentParser(description='a tool for obtaining information (history output) from an abaqus output database file (odb).',
                                 epilog='author: alexander.vogel@prozesskraft.de | version: '+odbhistory_version+' | date: '+odbhistory_date)
parser.add_argument('--odb', metavar='ODBFILE', type=str, required=True,
                   help='abaqus output database file')
parser.add_argument('--stepname', metavar='STEPNAME', action='store',
                   help='name of step')
parser.add_argument('--history', metavar='HISTORY', action='store',
                   help='name of history variable. e.G. U3, RF, CF etc.')
parser.add_argument('--output', metavar='OUTPUT', action='store',
                   help='name of output variable. e.G. data, name')
parser.add_argument('--region', metavar='REGION', action='store',
                   help='name of history region. e.G. "Node PART-1-1.66078689"')
#parser.add_argument('--coordsys', metavar='COORDINATESYSTEM', action='store',
#                   help='name of coordinate system.')
parser.add_argument('--postfunction', metavar='POSTFUNCTION', action='store',
                   help='name of function to manipulate retrieved values.')
parser.add_argument('--interactive', "-i", action='store_true', default=False,
                   help='interactive mode.')
#parser.add_argument('--batch', "-b", action='store_true', default=False,
#                   help='non-interactive mode.')

# Exklusivgruppen der Parameter
#group_2 = parser.add_mutually_exclusive_group()
#group_2.add_argument('--elset', metavar='ELSETNAME', action='store',
#                   help='name of element set. regular expressions may be used. opening and closing anchors are set implicitly')
#group_2.add_argument('--nset', metavar='NSETNAME', action='store',
#                   help='name of node set. regular expressions may be used. opening and closing anchors are set implicitly')
#group_2.add_argument('--nid', metavar='NID', action='store',
#                   help='node id')
#group_2.add_argument('--eid', metavar='EID', action='store',
#                   help='element id')

args = parser.parse_args()
#print args

#print(args.accumulate(args.integers))
#print str(args)
ergebniswert = history(args)
