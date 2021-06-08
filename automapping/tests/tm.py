# /usr/bin/env python3

import re
from random import randint
from time import time
from pymongo import MongoClient, ASCENDING, UpdateMany

# https://pymongo.readthedocs.io/en/stable/tutorial.html

TEST_DB = "mongodb://localhost:27017/"

client = MongoClient(TEST_DB)
db = client.automapping

#print("\n\n\n\nNODES")
#print(list(db.nodes.find()))
#print("\n\n\n\nIFACES")
#print(list(db.ifaces.find()))
#print("\n\n\n\nLINKS")
#print(list(db.links.find()))
#print("\n\n\n\nSTATS")
#print(list(db.stats.find()))
#print("\n\n\n\nUTILIZATIONS")
#print(list(db.utilization.find()))
#print("\n\n\n\INDEX")
#print(list(db.index_seq.find()))

# print(db.nodes.find_one({ 'device_name': 'sw1.iou'}))
# print(list(db.stats.find({ 'device_name': 'n9k.local.lab'})))
#print(list(db.stats.find({ 'device_name': '192.168.77.1'})))
#for res in db.stats.find({ 'device_name': 'rtr1.iou'}):
#    try:
#       print(res["device_name"], res['iface_name'], res["speed"], res['in_bytes'], res['out_bytes'])
#    except:
#       print(res["device_name"], res['iface_name'], res['in_bytes'], res['out_bytes'])
#print(list(db.ifaces.find({ 'device_name': 'sw1.iou'})))
#print(list(db.ifaces.find({ 'device_name': 'sw1.iou', "iface_name": "Et0/1"})))
#or_res = db.stats.find({"$or":[ {"device_name": "sw1.iou"}, {"device_name":"sw2.iou"}]})
#for res in db.links.find({"$or":[ {"device_name": "sw1.iou"}, {"neighbor_name":"sw1.iou"}]}):
#    print(res["device_name"], res['neighbor_name'], res["iface_name"])
#for res in db.stats.distinct("iface_name", {"device_name" : "sw1.iou"}):
#    print(res)
    #print(res["device_name"], res['neighbor_name'], res["iface_name"])
# print(list(db.nodes.find({ 'device_name': re.compile('sw', re.IGNORECASE)})))
# print(db.nodes.find_one({ 'device_name': re.compile('^' + 'cpt' + '$', re.IGNORECASE)}))
#print(db.ifaces.find_one({ 'device_name': "sw1.iou", re.compile('^' + 'Eth' + '$', re.IGNORECASE)}))
#print(db.ifaces.find_one({ 'device_name': "sw1.iou", "iface_name": "Et0/0"}))
#print(list(db.ifaces.find({ "device_name": "sw1.iou", "iface_name": "Et0/1" }))[-1]["speed"])

#db.nodes.create_index([("device_name", ASCENDING)], unique=True)
#db.nodes.insert_one({"device_name": "name", "device_id": 1})
#db.nodes.insert_one({"device_name": "name", "device_id": 1, "iface": "a"})
#db.nodes.insert_one({"device_name": "name", "device_id": 3})
#db.nodes.insert_one({"device_name": "name", "device_id": 4})
#db.nodes.update_many({'device_name': 'name2'}, {"$set": {"device_name": "name", "device_id": 1} })
#db.nodes.update_many({'device_name': 'name'}, {"$set": {"device_name": "name", "device_id": 2} })
#db.nodes.update_many({'device_name': 'name'}, {"$set": {"device_name": "name", "device_id": 3} })
#db.nodes.update_many({'device_id': 3}, {"$set": {"device_id": 3, 'device_name': 'name'}})
#db.nodes.update_many({}, {"$set": [{"device_id": 2, 'device_name': 'name2'}, {"device_id": 1, 'device_name': 'name'}]})
#db.nodes.update({}, {"$set": [{"device_id": 2, 'device_name': 'name2'}, {"device_id": 1, 'device_name': 'name'}]})
#req = [UpdateMany({'device_name': 'name','device_id': 4}, {"$set": {"device_id": 4, 'device_name': 'name4'}}),
#        UpdateMany({'device_name': 'name', 'device_id': 1}, {"$set": {"device_id": 1, 'device_name': 'name1'}})]
#req = [UpdateMany({'device_name': 'sw1.iou'}, {'$set': {'device_name': 'sw1.iou'}}, True), UpdateMany({'device_name': 'sw4.iou'}, {'$set': {'device_name': 'sw4.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr1.iou'}, {'$set': {'device_name': 'rtr1.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr2.iou'}, {'$set': {'device_name': 'rtr2.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw2.iou'}, {'$set': {'device_name': 'sw2.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw4.iou'}, {'$set': {'device_name': 'sw4.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr8.iou'}, {'$set': {'device_name': 'rtr8.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr7.iou'}, {'$set': {'device_name': 'rtr7.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw3.iou'}, {'$set': {'device_name': 'sw3.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw1.iou'}, {'$set': {'device_name': 'sw1.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr1.iou'}, {'$set': {'device_name': 'rtr1.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw1.iou'}, {'$set': {'device_name': 'sw1.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr2.iou'}, {'$set': {'device_name': 'rtr2.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw1.iou'}, {'$set': {'device_name': 'sw1.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw2.iou'}, {'$set': {'device_name': 'sw2.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr4.iou'}, {'$set': {'device_name': 'rtr4.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr3.iou'}, {'$set': {'device_name': 'rtr3.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw1.iou'}, {'$set': {'device_name': 'sw1.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw3.iou'}, {'$set': {'device_name': 'sw3.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr8.iou'}, {'$set': {'device_name': 'rtr8.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw4.iou'}, {'$set': {'device_name': 'sw4.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr7.iou'}, {'$set': {'device_name': 'rtr7.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw4.iou'}, {'$set': {'device_name': 'sw4.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw3.iou'}, {'$set': {'device_name': 'sw3.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr5.iou'}, {'$set': {'device_name': 'rtr5.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr6.iou'}, {'$set': {'device_name': 'rtr6.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw4.iou'}, {'$set': {'device_name': 'sw4.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw2.iou'}, {'$set': {'device_name': 'sw2.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr4.iou'}, {'$set': {'device_name': 'rtr4.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw2.iou'}, {'$set': {'device_name': 'sw2.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr3.iou'}, {'$set': {'device_name': 'rtr3.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw2.iou'}, {'$set': {'device_name': 'sw2.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr5.iou'}, {'$set': {'device_name': 'rtr5.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw3.iou'}, {'$set': {'device_name': 'sw3.iou'}}, False, None, None, None), UpdateMany({'device_name': 'rtr6.iou'}, {'$set': {'device_name': 'rtr6.iou'}}, False, None, None, None), UpdateMany({'device_name': 'sw3.iou'}, {'$set': {'device_name': 'sw3.iou'}}, False, None, None, None)]
#
#db.nodes.bulk_write(req)

#print(list(db.nodes.find()))
# db.nodes.delete_one({'device_name': 'name'})
# print(db.nodes.count_documents({}))

# db.nodes.delete_many({})
# db.links.delete_many({})
# db.stats.delete_many({})
# db.utilization.delete_many({})




def add_lots_of_nodes():

    for i in range(10):
        db.nodes.insert_one({"device_name": f"fake_device{str(i)}"})
        for j in range(10):
            down_device = str((i+1) * 10 + j)
            db.nodes.insert_one({"device_name": f"down_fake_device{down_device}"})

def add_lots_of_links():

    for i in range(4):
        for j in range(10):
            # Connects rtr.iou devices with first 10 'fake_devices'
            db.links.insert_one({'device_name': f"rtr{str(i+1)}.iou", 
            'iface_name': f'100/{str(j)}', 'neighbor_iface': '0/0', 'neighbor_name': f"fake_device{str(j)}"})
            db.links.insert_one({'device_name': f"fake_device{str(j)}",
            'iface_name': '0/0', 'neighbor_iface': f'100/{str(j)}', 'neighbor_name': f"rtr{str(i+1)}.iou"})
    for i in range(10):
        for j in range(10):
            # Connects first 10 'fake_devices' with 10 more down_fake_devices each
            down_device = str((i+1) * 10 + j)
            db.links.insert_one({'device_name': f"fake_device{str(i)}",
            'iface_name': f'1/{down_device}', 'neighbor_iface': '0/0', 'neighbor_name': f"down_fake_device{down_device}"})
            db.links.insert_one({'device_name': f"down_fake_device{down_device}",
            'iface_name': '0/0', 'neighbor_iface': f'1/{down_device}', 'neighbor_name': f"fake_device{str(i)}"})
    
def add_lots_of_utilizations():

    for i in range(4):
        for j in range(10):
            db.utilization.insert_one({'device_name': f"rtr{str(i+1)}.iou", 
                'iface_name': f'100/{str(j)}', 'last_utilization': randint(0,1250000)})
            db.utilization.insert_one({'device_name': f"fake_device{str(j)}", 
                'iface_name': f'0/0', 'last_utilization': randint(0,1250000)})
    for i in range(10):
        for j in range(10):
            down_device = str((i+1) * 10 + j)
            db.utilization.insert_one({'device_name': f"fake_device{str(i)}",
                'iface_name': f'1/{down_device}', 'last_utilization': randint(0,1250000)})
            db.utilization.insert_one({'device_name': f"down_fake_device{down_device}", 
                'iface_name': f'0/0', 'last_utilization': randint(0,1250000)})

def add_lots_of_stats():

    for i in range(4):
        for j in range(10):
            db.stats.insert_one({'device_name': f"rtr{str(i+1)}.iou", 
                'iface_name': f'100/{str(j)}', 'timestamp': int(time()),
                'mtu': 1500, 'mac': '', 'speed': 10, 'in_discards': 0, 
                'in_errors': 0, 'out_discards': 0, 'out_errors': 0, 'in_bytes': randint(0,1250000),
                'in_ucast_pkts': 0, 'in_mcast_pkts': 0, 'in_bcast_pkts': 0,
                'out_bytes': randint(0,1250000), 'out_ucast_pkts': 0, 'out_mcast_pkts': 0, 'out_bcast_pkts': 0}
                )
            db.stats.insert_one({'device_name': f"fake_device{str(j)}", 
                'iface_name': f'0/0', 'timestamp': int(time()),
                'mtu': 1500, 'mac': '', 'speed': 10, 'in_discards': 0, 
                'in_errors': 0, 'out_discards': 0, 'out_errors': 0, 'in_bytes': randint(0,1250000),
                'in_ucast_pkts': 0, 'in_mcast_pkts': 0, 'in_bcast_pkts': 0,
                'out_bytes': randint(0,1250000), 'out_ucast_pkts': 0, 'out_mcast_pkts': 0, 'out_bcast_pkts': 0}
                )
    for i in range(10):
        for j in range(10):
            down_device = str((i+1) * 10 + j)
            db.stats.insert_one({'device_name': f"fake_device{str(i)}",
                'iface_name': f'1/{down_device}', 'timestamp': int(time()),
                'mtu': 1500, 'mac': '', 'speed': 10, 'in_discards': 0, 
                'in_errors': 0, 'out_discards': 0, 'out_errors': 0, 'in_bytes': randint(0,1250000),
                'in_ucast_pkts': 0, 'in_mcast_pkts': 0, 'in_bcast_pkts': 0,
                'out_bytes': randint(0,1250000), 'out_ucast_pkts': 0, 'out_mcast_pkts': 0, 'out_bcast_pkts': 0}
                )
            db.stats.insert_one({'device_name': f"down_fake_device{down_device}", 
                'iface_name': f'0/0', 'timestamp': int(time()),
                'mtu': 1500, 'mac': '', 'speed': 10, 'in_discards': 0, 
                'in_errors': 0, 'out_discards': 0, 'out_errors': 0, 'in_bytes': randint(0,1250000),
                'in_ucast_pkts': 0, 'in_mcast_pkts': 0, 'in_bcast_pkts': 0,
                'out_bytes': randint(0,1250000), 'out_ucast_pkts': 0, 'out_mcast_pkts': 0, 'out_bcast_pkts': 0}
                )

def main():
    #db.nodes.delete_many({})
    #db.links.delete_many({})
    #db.stats.delete_many({})
    #db.utilization.delete_many({})
    #add_lots_of_nodes()
    #add_lots_of_links()
    #add_lots_of_utilizations()
    add_lots_of_stats()
    for res in db.nodes.find():
       print(res)

if __name__ == "__main__":
    main()
