import requests
import time
import pandas as pd
import matplotlib.pyplot as plt

###################

url = "https://api.opensea.io/api/v1/events?only_opensea=false&offset=0&limit=1&occurred_after=2021-10-16T20%3A35%3A43.511Z"
headers = {"Accept": "application/json"}
seenTokens = []


gatheringData = True

###### MatPlotLib Animation


######

def updateTable():
    global worksheet
    df = pd.DataFrame(columns = ['Name', 'fiveSecond', 'tenSecond', 'sixtySecond', 'tenMinute', 'thirtyMinute']) # Shorter time intervals to show frequency
    
    for x in nameCounterDict:
        df = df.append({'Name' : x, 'fiveSecond' : nameCounterDict[x][0], 'tenSecond' : nameCounterDict[x][1], 'sixtySecond' : nameCounterDict[x][2], 'tenMinute' : nameCounterDict[x][3], 'thirtyMinute' : nameCounterDict[x][4]}, 
                ignore_index = True)
    
    df.to_csv('real time nft sales.csv', mode='w', header = True, index=False)
    

    print(df.to_string(index=False))

######
keyQueue1 = []
keyQueue2 = []
keyQueue3 = []
keyQueue4 = []
keyQueue5 = []
targetTimes = [0]*5
timeNameDict = {}
nameCounterDict = {}
######


def beginGathering():
    global gatheringData
    while(gatheringData):
        response = requests.request("GET",url, headers=headers)
        

        data = response.json()
        for x in data['asset_events']:
            if (x['asset']['asset_contract']['name']!='OPENSTORE' and (x['asset']['token_id'] not in seenTokens) and x['asset']['asset_contract']['schema_name']=='ERC721'):
                
                name = x['asset']['asset_contract']['name']
                print(x['asset']['asset_contract']['address']+" "+ x['asset']['token_id'] +" "+ name)
                seenTokens.append(x['asset']['token_id'])
                ######
                currTime = time.time()
                keyQueue1.append(currTime)
                timeNameDict[currTime]=name
                
                if name in nameCounterDict:
                    nameCounterDict[name] = [x+1 for x in nameCounterDict[name]]
                else:
                    nameCounterDict[name] = [1,1,1,1,1]
                ######
            currentTime = time.time()
            if len(keyQueue1)>0:
                targetTimes[0] = keyQueue1[0]
                if targetTimes[0]+5<currentTime and targetTimes[0] in timeNameDict:
                    nameCounterDict[timeNameDict[targetTimes[0]]][0]-=1;
                    keyQueue2.append(keyQueue1.pop(0))
            if len(keyQueue2)>0:    
                targetTimes[1] = keyQueue2[0]
                if targetTimes[1]+10<currentTime and targetTimes[1] in timeNameDict:
                    nameCounterDict[timeNameDict[targetTimes[1]]][1]-=1;
                    keyQueue3.append(keyQueue2.pop(0))
            if len(keyQueue3)>0:    
                targetTimes[2] = keyQueue3[0]
                if targetTimes[2]+60<currentTime and targetTimes[2] in timeNameDict:
                    nameCounterDict[timeNameDict[targetTimes[2]]][2]-=1;
                    keyQueue4.append(keyQueue3.pop(0))
            if len(keyQueue4)>0:    
                targetTimes[3] = keyQueue4[0]
                if targetTimes[3]+600<currentTime and targetTimes[3] in timeNameDict:
                    nameCounterDict[timeNameDict[targetTimes[3]]][3]-=1;
                    keyQueue5.append(keyQueue4.pop(0))
            if len(keyQueue5)>0:
                targetTimes[4] = keyQueue5[0]
                if targetTimes[4]+1800<currentTime and targetTimes[4] in timeNameDict:
                    nameCounterDict[timeNameDict[targetTimes[4]]][4]-=1;
                    keyQueue5.pop(0)
                    if nameCounterDict[timeNameDict[targetTimes[4]]][4] == 0:
                        nameCounterDict.pop(timeNameDict[targetTimes[4]])
                    timeNameDict.pop(targetTimes[4])
        updateTable()

        
        print("Target Times for each minute comparison: "+str([targetTimes[0],targetTimes[1],targetTimes[2],targetTimes[3],targetTimes[4]]))

        print([keyQueue1,keyQueue2,keyQueue3,keyQueue4,keyQueue5])
        print(timeNameDict)
        print(nameCounterDict)
        
        time.sleep(1)

        


beginGathering()