# Honeypot Grapher
This project was a university course project, it was about Attacking Behavior Co-Relation Using Honeypot.

This project uses [WetFTP](https://github.com/ohmyadd/wetftp) as a high interaction honeypot and converts the logs generated by the tool into a graph using neo4j database.

## Project Functionalities
- Collecting logs
- Convert the logs into a json format that can be imported to neo4j using (apoc.import.json) procedure call
- View the graph in neo4j with two different type of graphs (Timeline, Overview)

## Graph Example
### Overview Graph
![Overview Graph](https://github.com/LonelyWolf-MQ/graphit-ftphoneypot/blob/main/example/overview.png)
### Timeline Graph
![Timeline Graph](https://github.com/LonelyWolf-MQ/graphit-ftphoneypot/blob/main/example/timeline.png)

## To run the project what you need is:
- Having python3 -_-.
- Install the latest Neo4j database version.
- Install the latest APOC plugins (So you can call the apoc.import.json procedure).
- Additional: ```pip3 install py2neo```, then modify bolt port and username/password of neo4j database if you wish to run the neo4j cypher queries within the python script.
- Run: ```python3 main.py -h```
- Example: ```python3 main.py --logpath cmd.log --mode timeline --jsonoutput timeline.json --neo4j --neo4juri bolt://localhost:11003 --neo4juser neo4j --neo4jpasswd neo4j --label Node```

## Future work
### Short period goal:
- Understand Neo4j structure more and more (lol).
- Develop the log2json convertor.

### Long period goal:
- Create my own honeypots for multiple services such as HTTP/SSH/SMB/...
- Use Provenance so we can correlate the attacker behaviour more using framework such as ![SPADE](https://github.com/ashish-gehani/SPADE)
- Convert this project to a framework with real time monitoring.


if you noticed any mistake or have any suggestion reached me at my Twitter/LinkedIn account:
- [![Twitter](https://img.shields.io/twitter/follow/MHMDQi?style=social)](https://twitter.com/intent/follow?screen_name=MHMDQi)
- [![Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mhmdqi/)
