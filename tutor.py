from static.data.spData import dataRec, busNeedToDeliverable, busNeedToSolution
import json
knowledge = []
knowledgeList = []
count = 0

#dict2 = {'LeafTemps': '\xff\xff\xff\xff',}
json1 = json.dumps(busNeedToDeliverable, ensure_ascii=False)
json2 = json.dumps(busNeedToSolution, ensure_ascii=False)
print(json1)
print(json2)

"""
for value in busNeedToDeliverable['Collaboration']:
    print value
"""