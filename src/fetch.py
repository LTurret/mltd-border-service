async def GetNewest(session):
    async with session.get("https://api.matsurihi.me/mltd/v1/events") as response:
        try:
            data = await response.json()
            return data[-1]
        except Exception as e:
            print(f"exception occur: {e}")
            return {}

async def Search(evtid, session):
    async with session.get(f"https://api.matsurihi.me/mltd/v1/events/{evtid}") as response:
        try:
            data = await response.json()
            return data
        except Exception as e:
            print(f"exception occur: {e}")
            return {}
    
async def FetchBorder(evtid, session):
    async with session.get(f"https://api.matsurihi.me/mltd/v1/events/{evtid}/rankings/borderPoints") as response:
        try:
            data = await response.json()
            return data
        except Exception as e:
            print(f"exception occur: {e}")
            return {}

async def FetchCover(session, evtid):
    async with session.get(f"https://storage.matsurihi.me/mltd/event_bg/{evtid:0>4,d}.png") as response:
        try:
            with open(f"{evtid:0>4,d}.png", "wb") as file:
                file.write(await response.read())
                return 0
        except Exception as e:
            print(f"exception occur: {e}")
            return 1
