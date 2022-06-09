from log2json import *
import argparse
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-lp','--logpath', type=open, required=True, help="FTP Log Path")
parser.add_argument('-jo','--jsonoutput', type=argparse.FileType('w', encoding='latin-1'), help="JSON Output", required=True)
parser.add_argument('-m','--mode',required=True, choices=['overview', 'timeline'])
parser.add_argument('-nl','--label',help="The Node Label", required=True)
parser.add_argument('--neo4j',help="create the graph in neo4j automatically",action='store_true',default='False')
parser.add_argument('--neo4juri',help="Specify the Neo4j URI Ex. bolt://localhost:11003",default='bolt://localhost:11003')
parser.add_argument('--neo4juser',help="Specify the Neo4j User, Default: neo4j",default='neo4j')
parser.add_argument('--neo4jpasswd',help="Specify the Neo4j Password",default='neo4j')
args = parser.parse_args()

label = args.label
logpath = args.logpath.name
uri = args.neo4juri
user = args.neo4juser
passwd = args.neo4jpasswd
jpath = args.jsonoutput.name
jpath = Path(jpath).absolute()
jpath = str(jpath)
jsonpath = jpath.replace("\\","\\\\")
print("Converting FTP Logs To JSON")
if args.mode == 'timeline':
    jsonfile = timeline(args.label,args.logpath.name)
    with open(args.jsonoutput.name, 'w') as f:
        for log in jsonfile:
            f.write("%s\n" % log)
    print("Converting to JSON completed successfully")

if args.mode == 'overview':
    jsonfile = overview(args.label,args.logpath.name)
    with open(args.jsonoutput.name, 'w') as f:
        for log in jsonfile:
            f.write("%s\n" % log)
    print("Converting to JSON completed successfully")

if args.neo4j == True and (uri and user and passwd) != "":
    json2neo4j(label,uri,user,passwd,jsonpath)
    print("Node Has Been Created")
    print("Visit http://localhost:11004/browser/ to view the graph")