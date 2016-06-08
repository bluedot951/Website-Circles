import json

myFile = open("websites.txt", "r")


def cleanJson(json_list):
	print("CLEANING: \t" + str(json_list))
	if(len(json_list['children']) == 0):
		del json_list['children']
	else:
		for i in range(len(json_list['children'])):
			json_list['children'][i] = cleanJson(json_list['children'][i])

depth = 0
root = { "name": "root", "children": [] }
parents = []
node = root
for line in myFile:
    line = line.rstrip()
    newDepth = len(line) - len(line.lstrip()) + 1
    # print newDepth, line
    # if the new depth is shallower than previous, we need to remove items from the list
    if newDepth < depth:
        parents = parents[:newDepth]
    # if the new depth is deeper, we need to add our previous node
    elif newDepth == depth + 1:
        parents.append(node)
    # levels skipped, not possible
    elif newDepth > depth + 1:
        raise Exception("Invalid file")
    depth = newDepth

    strpLine = line.strip()
    data = strpLine.split(",")
    if(len(data) == 2):
    	node = {"name": "", "children": [{"name": data[0], "link": data[1], "size" : 100}], "size" : 100}
    else:
    	node = {"name": data[0], "size": 100}

    # create the new node
    # node = {"name": line.strip(), "children":[]}
    # add the new node into its parent's children
    if(("children" not in parents[-1].keys())):
    	parents[-1]["children"] = []
    	parents[-1].pop("size")
    parents[-1]["children"].append(node)

json_list = root["children"]

master = {"name" : "", "children": json_list}

outputfile = open("flare.json", "w")
outputfile.write(json.dumps(master, sort_keys=True, indent=3, separators=(',', ': ')))
