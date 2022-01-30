from datetime import datetime

async def GetNewestEvent(session):
    print(f"fetching event id at: {str(datetime.now()):0.22}")
    async with session.get("https://api.matsurihi.me/mltd/v1/events") as response:
        try:
            data = await response.json()
            return data[-1]
        except Exception as e:
            print(f"exception occur: {e}")

async def SearchEvent(evtid, session):
    async with session.get(f"https://api.matsurihi.me/mltd/v1/events/{evtid}") as response:
        print(f"fetching event information at: {str(datetime.now()):0.22}")
        try:
            data = await response.json()
            return data
        except Exception as e:
            print(f"exception occur: {e}")
    
async def FetchBorder(evtid, session):
    async with session.get(f"https://api.matsurihi.me/mltd/v1/events/{evtid}/rankings/borderPoints") as response:
        print(f"fetching event border at: {str(datetime.now()):0.22}")
        try:
            data = await response.json()
            return data
        except Exception as e:
            print(f"exception occur: {e}")

async def FetchCover(session, evtid):
    async with session.get(f"https://storage.matsurihi.me/mltd/event_bg/{evtid:0>4,d}.png") as response:
        print(f"fetching event cover image at: {str(datetime.now()):0.22}")
        try:
            with open(f"{evtid:0>4,d}.png", "wb") as file:
                file.write(await response.read())
        except Exception as e:
            print(f"exception occur: {e}")

if __name__ == "__main__":
    print('using "main.py" instead.')