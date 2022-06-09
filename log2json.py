import time
from py2neo import Graph
disabledlogs = ['PORT', 'USER', 'PASS', 'OPTS', 'TYPE']


def timeline(nodelabel, path):
    countRelation = 0
    countNode = 0
    loggedInSessions = {}
    logs = []
    label = nodelabel
    with open(path) as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            logline = line.strip()
            timestamp = logline.split()[0]
            ipAddr = logline.split()[1]
            command = logline.split()[2]
            args = ""
            if 3 < len(logline.split()):
                args = logline.split()[3]
            if command in str(disabledlogs):
                continue
            countRelation += 1
            countNode += 1
            uploadFile = {
                "ftpcommand": "STOR",
                "usercommand": "put",
                "description": "User Uploaded a File To FTP Server",
                "parameter": args
            }
            createDirectory = {
                "ftpcommand": "MKD",
                "usercommand": "mkdir",
                "description": "User Created a New Directory",
                "parameter": args
            }
            removeDirectory = {
                "ftpcommand": "RMD",
                "usercommand": "rmdir",
                "description": "User Removed a Directory",
                "parameter": args
            }
            getFile = {
                "ftpcommand": "RETR",
                "usercommand": "get",
                "description": "User Downloaded a File From FTP Server",
                "parameter": args
            }
            listDirectory = {
                "ftpcommand": "LIST",
                "usercommand": ["ls", "dir"],
                "description": "User Listed The Current Directory.",
                "parameter": args,
                "listed": ["/"]
            }
            getPath = {
                "ftpcommand": "PWD",
                "usercommand": "pwd",
                "description": "User Printed The Current Directory Path."
            }
            changeDirectory = {
                "ftpcommand": "CWD",
                "usercommand": "cd",
                "description": "User Moved To Another Directory.",
                "parameter": args
            }
            endSession = {
                "ftpcommand": "QUIT",
                "usercommand": ["quit", "exit", "bye"],
                "description": "User Exited The Current Session."
            }
            newSession = {
                "ftpcommand": "SYST",
                "usercommand": "ftp <machine ip>",
                "description": "User Has Opened A New Session."
            }
            if newSession["ftpcommand"] in logline:
                if len(loggedInSessions) == 0:
                    node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"NS{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                        countNode, label, ipAddr, countNode,
                        newSession["description"], newSession["usercommand"],
                        newSession["ftpcommand"], ipAddr, timestamp)
                    loggedInSessions[countNode] = ipAddr
                    logs.append(node)
                elif len(loggedInSessions) > 0:
                    for v in list(loggedInSessions.values()):
                        if str(ipAddr) in v:
                            break
                        elif str(ipAddr) not in v:
                            countNode += 1
                            node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"NS{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                                countNode, label, ipAddr, countNode,
                                newSession["description"],
                                newSession["usercommand"],
                                newSession["ftpcommand"], ipAddr, timestamp)
                            loggedInSessions[countNode] = ipAddr 
                            logs.append(node)

            if listDirectory["ftpcommand"] in logline:
                if listDirectory["parameter"] == '':
                    listDirectory["parameter"] = listDirectory['listed'][-1]
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"LD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, listDirectory["parameter"], countNode,
                    listDirectory["description"], listDirectory["usercommand"],
                    listDirectory["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"ListingDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, countNode - 1, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if getPath["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"Get Path of {}","actionid":"GP{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, listDirectory["listed"][-1], countNode,
                    getPath["description"], getPath["usercommand"],
                    getPath["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"GetPath","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, countNode - 1, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if createDirectory["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"CD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, createDirectory["parameter"], countNode,
                    createDirectory["description"],
                    createDirectory["usercommand"],
                    createDirectory["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"CreateDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, countNode - 1, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if changeDirectory["ftpcommand"] in logline:
                savedir = listDirectory['listed'] 
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"CWD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, changeDirectory["parameter"], countNode,
                    changeDirectory["description"],
                    changeDirectory["usercommand"],
                    changeDirectory["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"ChangeDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, countNode - 1, label, countNode, label)
                dirctory = changeDirectory["parameter"]
                savedir.append(dirctory) 
                logs.append(node)
                logs.append(relation)

            if removeDirectory["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"RD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, removeDirectory["parameter"], countNode,
                    removeDirectory["description"],
                    removeDirectory["usercommand"],
                    removeDirectory["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"RemoveDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, countNode - 1, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if getFile["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"GF{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, getFile["parameter"], countNode,
                    getFile["description"], getFile["usercommand"],
                    getFile["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"DownloadedFile","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, countNode - 1, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if uploadFile["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"UF{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, uploadFile["parameter"], countNode,
                    uploadFile["description"], uploadFile["usercommand"],
                    uploadFile["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"UploadedFile","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, countNode - 1, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if endSession["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"Session Ended","actionid":"ES{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, countNode, endSession["description"],
                    endSession["usercommand"], endSession["ftpcommand"],
                    ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"EndSession","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, countNode - 1, label, countNode, label)
                logs.append(node)
                logs.append(relation)
    return logs


def overview(nodelabel, path):
    countRelation = 0
    countNode = 0
    loggedInSessions = {}
    logs = []
    label = nodelabel
    with open(path) as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            logline = line.strip()
            timestamp = logline.split()[0]
            ipAddr = logline.split()[1]
            command = logline.split()[2]
            args = ""
            if 3 < len(logline.split()):
                args = logline.split()[3]
            if command in str(disabledlogs):
                continue
            countRelation += 1
            countNode += 1
            uploadFile = {
                "ftpcommand": "STOR",
                "usercommand": "put",
                "description": "User Uploaded a File To FTP Server",
                "parameter": args
            }
            createDirectory = {
                "ftpcommand": "MKD",
                "usercommand": "mkdir",
                "description": "User Created a New Directory",
                "parameter": args
            }
            removeDirectory = {
                "ftpcommand": "RMD",
                "usercommand": "rmdir",
                "description": "User Removed a Directory",
                "parameter": args
            }
            getFile = {
                "ftpcommand": "RETR",
                "usercommand": "get",
                "description": "User Downloaded a File From FTP Server",
                "parameter": args
            }
            listDirectory = {
                "ftpcommand": "LIST",
                "usercommand": ["ls", "dir"],
                "description": "User Listed The Current Directory.",
                "parameter": args,
                "listed": ["/"]
            }
            getPath = {
                "ftpcommand": "PWD",
                "usercommand": "pwd",
                "description": "User Printed The Current Directory Path."
            }
            changeDirectory = {
                "ftpcommand": "CWD",
                "usercommand": "cd",
                "description": "User Moved To Another Directory.",
                "parameter": args
            }
            endSession = {
                "ftpcommand": "QUIT",
                "usercommand": ["quit", "exit", "bye"],
                "description": "User Exited The Current Session."
            }
            newSession = {
                "ftpcommand": "SYST",
                "usercommand": "ftp <machine ip>",
                "description": "User Has Opened A New Session."
            }

            if newSession["ftpcommand"] in logline:
                if len(loggedInSessions) == 0:
                    node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"NS{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                        countNode, label, ipAddr, countNode,
                        newSession["description"], newSession["usercommand"],
                        newSession["ftpcommand"], ipAddr, timestamp)
                    loggedInSessions[countNode] = ipAddr
                    logs.append(node)
                elif len(loggedInSessions) > 0:
                    for v in list(loggedInSessions.values()):
                        if str(ipAddr) in v:
                            break
                        elif str(ipAddr) not in v:
                            countNode += 1
                            node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"NS{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                                countNode, label, ipAddr, countNode,
                                newSession["description"],
                                newSession["usercommand"],
                                newSession["ftpcommand"], ipAddr, timestamp)
                            loggedInSessions[countNode] = ipAddr
                            logs.append(node)


            for k,v in list(loggedInSessions.items()):
                if v == str(ipAddr):
                    startrelation = k

            if listDirectory["ftpcommand"] in logline:
                if listDirectory["parameter"] == '':
                    listDirectory["parameter"] = listDirectory['listed'][-1]
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"LD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, listDirectory["parameter"], countNode,
                    listDirectory["description"], listDirectory["usercommand"],
                    listDirectory["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"ListingDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, startrelation, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if getPath["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"Get Path of {}","actionid":"GP{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, listDirectory["listed"][-1], countNode,
                    getPath["description"], getPath["usercommand"],
                    getPath["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"GetPath","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, startrelation, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if createDirectory["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"CD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, createDirectory["parameter"], countNode,
                    createDirectory["description"],
                    createDirectory["usercommand"],
                    createDirectory["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"CreateDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, startrelation, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if changeDirectory["ftpcommand"] in logline:
                savedir = listDirectory['listed']
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"CWD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, changeDirectory["parameter"], countNode,
                    changeDirectory["description"],
                    changeDirectory["usercommand"],
                    changeDirectory["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"ChangeDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, startrelation, label, countNode, label)
                dirctory = changeDirectory["parameter"]
                savedir.append(dirctory)
                logs.append(node)
                logs.append(relation)

            if removeDirectory["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"RD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, removeDirectory["parameter"], countNode,
                    removeDirectory["description"],
                    removeDirectory["usercommand"],
                    removeDirectory["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"RemoveDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, startrelation, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if getFile["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"GF{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, getFile["parameter"], countNode,
                    getFile["description"], getFile["usercommand"],
                    getFile["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"DownloadedFile","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, startrelation, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if uploadFile["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"UF{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, uploadFile["parameter"], countNode,
                    uploadFile["description"], uploadFile["usercommand"],
                    uploadFile["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"UploadedFile","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, startrelation, label, countNode, label)
                logs.append(node)
                logs.append(relation)

            if endSession["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"Session Ended","actionid":"ES{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                    countNode, label, countNode, endSession["description"],
                    endSession["usercommand"], endSession["ftpcommand"],
                    ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"EndSession","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(
                    countRelation, startrelation, label, countNode, label)
                logs.append(node)
                logs.append(relation)
    return logs


def json2neo4j(label, uri, userName, password, jsonpath):
    g = Graph(uri, auth=(userName, password))
    cqlCommand0 = "CREATE CONSTRAINT ON (n:{}) assert n.neo4jImportId IS UNIQUE;".format(
        label)
    cqlCommand1 = "CALL apoc.import.json('file:///{}');".format(jsonpath)
    g.run(cqlCommand0)
    g.run(cqlCommand1)