import time

def ftplog2json():
    countRelation = 0
    countNode = 0
    countNodeMain = 0
    loggedInSessions = []
    logs = []
    nodelabel = input("Enter a Node Name: ")
    with open(r"D://ftpgraph//newcmd.log") as fp:
        while True:
            countRelation += 1
            countNode += 1
            line = fp.readline()
            logline = line.strip()
            timestamp = logline[0:15]
            ipAddr = logline[16:31].strip()
            additionalinput3 = logline[45:]
            additionalinput4 = logline[46:]

            uploadFile = {
                "ftpcommand": "STOR",
                "usercommand": "put",
                "description": "User Uploaded a File To FTP Server",
                "parameter": additionalinput4
            }
            createDirectory = {
                "ftpcommand": "MKD",
                "usercommand": "mkdir",
                "description": "User Created a New Directory",
                "parameter": additionalinput3,
            }
            removeDirectory = {
                "ftpcommand": "RMD",
                "usercommand": "rmdir",
                "description": "User Removed a Directory",
                "parameter": additionalinput3
            }
            getFile = {
                "ftpcommand": "RETR",
                "usercommand": "get",
                "description": "User Downloaded a File From FTP Server",
                "parameter": additionalinput4
            }
            listDirectory = {
                "ftpcommand": "LIST",
                "usercommand": ["ls", "dir"],
                "description": "User Listed The Current Directory.",
                "parameter": additionalinput4,
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
                "parameter": additionalinput3
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
            if not line:
                break

            if newSession["ftpcommand"] in logline:
                if len(loggedInSessions) == 0:
                    node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"NS{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                        countNodeMain,nodelabel, ipAddr, countNodeMain,
                        newSession["description"], newSession["usercommand"],
                        newSession["ftpcommand"], ipAddr, timestamp)
                    loggedInSessions.append(ipAddr)
                    # print(node)
                    logs.append(node)
                elif len(loggedInSessions) > 0:
                    for i in loggedInSessions:
                        if str(ipAddr) in i:
                            break
                        elif str(ipAddr) not in i:
                            countNodeMain +=1

                            node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"NS{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(
                                countNodeMain,nodelabel, ipAddr, countNodeMain,
                                newSession["description"],
                                newSession["usercommand"],
                                newSession["ftpcommand"], ipAddr, timestamp)
                            # print(node)
                            logs.append(node)



            if listDirectory["ftpcommand"] in logline:
                node= '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"LD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(countNode,nodelabel, listDirectory["parameter"], countNode,  listDirectory["description"], listDirectory["usercommand"],listDirectory["ftpcommand"], ipAddr, timestamp)
                relation= '{{"id":"{}","type":"relationship","label":"ListingDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(countRelation,countNodeMain, nodelabel,countNode,nodelabel)

                # print(node)
                # print(relation)
                logs.append(node)
                logs.append(relation)

            if getPath["ftpcommand"] in logline:

                node='{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"Get Path of {}","actionid":"GP{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(countNode, nodelabel,listDirectory["listed"][-1], countNode,
                            getPath["description"], getPath["usercommand"],
                            getPath["ftpcommand"], ipAddr, timestamp)

                relation = '{{"id":"{}","type":"relationship","label":"GetPath","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(countRelation, countNodeMain,nodelabel, countNode,nodelabel)


                # print(node)
                # print(relation)
                logs.append(node)
                logs.append(relation)


            if createDirectory["ftpcommand"] in logline:

                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"CD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(countNode, nodelabel,createDirectory["parameter"], countNode,
                            createDirectory["description"],
                            createDirectory["usercommand"],
                            createDirectory["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"CreateDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(countRelation, countNodeMain,nodelabel, countNode,nodelabel)
                # print(node)
                # print(relation)
                logs.append(node)
                logs.append(relation)


            if changeDirectory["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"CWD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(countNode,nodelabel, changeDirectory["parameter"], countNode,
                            changeDirectory["description"],
                            changeDirectory["usercommand"],
                            changeDirectory["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"ChangeDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(countRelation,countNodeMain,nodelabel,  countNode,nodelabel)

                # print(node)
                # print(relation)
                logs.append(node)
                logs.append(relation)


            if removeDirectory["ftpcommand"] in logline:
                node ='{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"RD{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(countNode, nodelabel,removeDirectory["parameter"], countNode,
                            removeDirectory["description"],
                            removeDirectory["usercommand"],
                            removeDirectory["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"RemoveDirectory","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(countRelation,countNodeMain, nodelabel,countNode, nodelabel)

                # print(node)
                # print(relation)
                logs.append(node)
                logs.append(relation)


            if getFile["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"GF{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(countNode, nodelabel,getFile["parameter"], countNode,
                            getFile["description"], getFile["usercommand"],
                            getFile["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"DownloadedFile","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(countRelation, countNodeMain,nodelabel, countNode,nodelabel)
                # print(node)
                # print(relation)
                logs.append(node)
                logs.append(relation)


            if uploadFile["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"{}","actionid":"UF{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(countNode,nodelabel, uploadFile["parameter"], countNode,
                            uploadFile["description"],
                            uploadFile["usercommand"],
                            uploadFile["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"UploadedFile","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(countRelation,countNodeMain,nodelabel, countNode, nodelabel)
                # print(node)
                # print(relation)
                logs.append(node)
                logs.append(relation)


            if endSession["ftpcommand"] in logline:
                node = '{{"type":"node","id":"{}","labels":["{}"],"properties":{{"actionname":"Session Ended","actionid":"ES{}","actiondescription":"{}","actioncommand":"{}","ftpcommand":"{}","actionip":"{}","timestamp":"{}"}}}}'.format(countNode,nodelabel, countNode, endSession["description"],
                            endSession["usercommand"],
                            endSession["ftpcommand"], ipAddr, timestamp)
                relation = '{{"id":"{}","type":"relationship","label":"EndSession","start":{{"id":"{}","labels":["{}"]}},"end":{{"id":"{}","labels":["{}"]}}}}'.format(countRelation,countNodeMain, nodelabel, countNode,nodelabel)
                # print(node)
                # print(relation)
                logs.append(node)
                logs.append(relation)

    return nodelabel,logs


def removelogs():
    logs = ['PORT', 'USER', 'PASS','RNTO','RNFR','OPTS','TYPE']
    with open('cmd.log') as oldfile, open('newcmd.log', 'w') as newfile:
        for line in oldfile:
            if not any(log in line for log in logs):
                newfile.write(line)

def json2neo4j(label):
    uri = "bolt://localhost:11003"
    userName = "neo4j"
    password = "toor"
    g = Graph(uri, auth=(userName, password))
    cqlCommand0 = "CREATE CONSTRAINT ON (n:{}) assert n.neo4jImportId IS UNIQUE;".format(label)
    cqlCommand1 = "CALL apoc.import.json('file:///D://ftpgraph//logs.json');"
    g.run(cqlCommand0)
    g.run(cqlCommand1)

if __name__ == "__main__":
    from py2neo import Graph
    removelogs()
    print("Converting FTP Logs")
    labels,jsonfile = ftplog2json()
    with open('D:\\ftpgraph\\logs.json', 'w') as f:
        for log in jsonfile:
            f.write("%s\n" % log)
    print("Converting to JSON completed successfully")
    print("Moving JSON to neo4j database")
    json2neo4j(labels)
