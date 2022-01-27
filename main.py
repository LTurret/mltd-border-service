import aiohttp
import argparse
import asyncio
import os
from fetch import getID, getEventInfo, getRankBorder, fetchCover
from make import makefile
from image import makeimg

parser = argparse.ArgumentParser(description="Use choice to fetches different type of data.")
parser.add_argument("-t", "--type", nargs="+", type=str, metavar="", required=True,
                    help="select datatype",
                    choices=["pt", "hs", "lp"]
                )
opt = parser.parse_args()

async def main(datatype):
    async with aiohttp.ClientSession() as session:
        evtID = await getID(session)
        tasks = [
            asyncio.create_task(getEventInfo(evtID, session)),
            asyncio.create_task(getRankBorder(evtID, session))
        ]
        await asyncio.gather(*tasks)
        information = tasks[0].result()
        border = tasks[1].result()

        if os.path.isdir("./dataset"):
            pass
        else:
            os.mkdir("./dataset")
        os.chdir("./dataset")
        tasks = [
            asyncio.create_task(makefile(information, "information")),
            asyncio.create_task(makefile(border, "border"))
        ]
        await asyncio.gather(*tasks)

        os.chdir("../")
        if os.path.isdir("./img-output"):
            pass
        else:
            os.mkdir("./img-output")

        tasks = []
        for category in datatype:
            match category:
                case "pt":
                    category = "eventPoint"
                case "hs":
                    category = "highScore"
                case "lp":
                    category = "loungePoint"
            tasks.append(makeimg(category))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(opt.type))