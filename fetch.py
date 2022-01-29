from datetime import datetime

async def getID(session, rcode:bool=False):
    print(f"fetching event id at: {str(datetime.now()):0.22}")
    async with session.get("https://api.matsurihi.me/mltd/v1/events") as response:
        if rcode:
            print(f"response code: {response.status}")
        if response.status == 200:
            try:
                data =  await response.json()
                return data[-1]["id"]
            except Exception as e:
                print(f"exception occur: {e}")
        else:
            print(f"bad response status: \n{response.status}")
    
async def getEventInfo(evtid, session, rcode:bool=False):
    async with session.get(f"https://api.matsurihi.me/mltd/v1/events/{evtid}") as response:
        print(f"fetching event information at: {str(datetime.now()):0.22}")
        if rcode:
            print(f"response code: {response.status}")
        if response.status == 200:
            try:
                data = await response.json()
                return data
            except Exception as e:
                print(f"exception occur: {e}")
        else:
            print(f"bad response status: \n{response.status}")
        if rcode:
            print(f"response code: {response.status}")
    
async def getRankBorder(evtid, session, rcode:bool=False):
    async with session.get(f"https://api.matsurihi.me/mltd/v1/events/{evtid}/rankings/borderPoints") as response:
        print(f"fetching event border at: {str(datetime.now()):0.22}")
        if rcode:
            print(f"response code: {response.status}")
        if response.status == 200:
            try:
                data = await response.json()
                return data
            except Exception as e:
                print(f"exception occur: {e}")
        else:
            print(f"bad response status: \n{response.status}")
        if rcode:
            print(f"response code: {response.status}")
    
async def fetchCover(session, evtid, rcode:bool=False):
    print(f"fetching event cover image at: {str(datetime.now()):0.22}")
    async with session.get(f"https://storage.matsurihi.me/mltd/event_bg/{evtid:0>4,d}.png") as response:
        if rcode:
            print(f"response code: {response.status}")
        if response.status == 200:
            try:
                with open(f"{evtid:0>4,d}.png", "wb") as file:
                    file.write(await response.read())
            except Exception as e:
                print(f"exception occur: {e}")
        else:
            print(f"bad response status: \n{response.status}")
        if rcode:
            print(f"response code: {response.status}")

if __name__ == "__main__":
    print('using "main.py" instead.')