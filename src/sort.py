import json


ret = []
mn = 9

def checkName(name, obj):
        # for num, val in enumerate(ret):
        #     if val["name"] == name:
        #         ret[num]["tiers"].append(obj["tier"])
        #         return True
        #     else:
        #         return False

    for i in ret:
        if i["name"] == name:
            i["tiers"].append(obj["tier"])
            return True
    return False

with open('./assets/maps.json') as json_file:
    data = json.load(json_file)



    for d in data["maps"]:
        # check if name is already in list

        if checkName(d["name"], d):
            print("Found match")
        else:
            obj = {}
            obj["name"] = d["name"]
            obj["tiers"] = []
            obj["tiers"].append(d["tier"])
            obj["regions"] = []
            # ...New/Arena.png?scale=1&mn=9&mt=2
            icon = d["icon"].split("&mn={mn}&mt=".format(mn = mn))
            iconAppend = icon[0] + "&mn={mn}&mt=".format(mn = mn)
            obj["icon"] = iconAppend
            ret.append(obj)


with open('maps_tier_sorted.json', 'w') as outfile:
    obj = {}
    obj["maps"] = ret
    json.dump(obj, outfile)

