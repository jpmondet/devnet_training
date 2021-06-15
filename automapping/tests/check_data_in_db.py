# /usr/bin/env python3


from pymongo import MongoClient, ASCENDING

# https://pymongo.readthedocs.io/en/stable/tutorial.html

AUTOMAPPING_DB = "mongodb://localhost:27017/"

client = MongoClient(AUTOMAPPING_DB)

db = client.automapping

#print("\n\n\n\INDEX")
#print(list(db.index_seq.find()))
#print("\n\n\n\nNODES")
#print(list(db.nodes.find()))
#print("\n\n\n\nLINKS")
#print(list(db.links.find()))
#print("\n\n\n\nSTATS")
#print(list(db.stats.find()))
#print("\n\n\n\nUTILIZATION")
#print(list(db.utilization.find()))



#db.nodes.delete_many({})
#db.links.delete_many({})
#db.stats.delete_many({})
#db.utilization.delete_many({})

#print("\n\n\n\nNODES")
#for node in db.nodes.find():
#    print(node)
#print("\n\n\n\nLINKS")
#for link in db.links.find():
#    print(link)
#print("\n\n\n\nSTATS")
#for stat in db.stats.find():
#    print(stat)
print("\n\n\n\nUTILIZATION")
for utilization in db.utilization.find():
    print(utilization)
print(list(db.links.find({'device_name': 'fake_device_stage6_16', 'iface_name': '0/16'})))
l = list(db.stats.find({'device_name': 'fake_device_stage6_16', 'iface_name': '0/16'}))
print(l)
print(l[-1])