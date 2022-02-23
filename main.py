import argparse
import asyncio
import os

import aiohttp

from src.fetch import FetchBorder, FetchCover, GetNewestEvent, SearchEvent
from src.image import makeimg
from src.make import makefile

parser = argparse.ArgumentParser(description="MLTD event information and score border image generator.")

parser.add_argument("-O", "--output_path", nargs=1, type=str, metavar="",
                    required=False,
                    default="image",
                    help='Image generate ouput path, default is "./image"'
                )
parser.add_argument("-S", "--search_id", nargs=1, type=int, metavar="",
                    required=False,
                    help="Search specific event with unique ID"
                )
parser.add_argument("-T", "--type", nargs="+", type=str, metavar="",
                    required=True,
                    help="Select fetches border type",
                    choices=["pt", "hs", "lp"]
                )
group = parser.add_mutually_exclusive_group()
group.add_argument("--dryrun",
                    action="store_true",
                    help=f"Don't generate border-image and output folder to disk"
                )
group.add_argument("--checksum",
                    action="store_true",
                    help=f"Don't generate any file or folder, test API response"
                )
opt = parser.parse_args()

async def main(datatype, output_path, checksum, dryrun, search_id):
    def typematch(typeid):
        if typeid == (3 | 4 | 11 | 13 | 16):
            return True

    async with aiohttp.ClientSession() as session:
        if search_id is not None:
            eventData = await SearchEvent(search_id[0], session)
            tasks = []
            if typematch(eventData["type"]):
                tasks.append(asyncio.create_task(FetchBorder(search_id[0], session)))
        else:
            eventData = await GetNewestEvent(session)
            evtID = eventData["id"]
            tasks = []
            if typematch(eventData["type"]):
                tasks.append(asyncio.create_task(FetchBorder(evtID, session)))
        await asyncio.gather(*tasks)
        information = eventData
        if typematch(eventData["type"]):
            border = tasks[0].result()
        print("fetch data complete.")

        if checksum:
            print("checksum complete.")
        else: 
            if os.path.exists("./dataset"):
                if not os.path.isdir("./dataset"):
                    raise NotImplementedError() # EEXIST
            else:
                os.mkdir("./dataset")
            os.chdir("./dataset")
            tasks = [
                asyncio.create_task(makefile(information, "information"))
            ]
            if typematch(eventData["type"]):
                tasks.append(asyncio.create_task(makefile(border, "border")))
            await asyncio.gather(*tasks)

            if not dryrun and typematch(eventData["type"]):
                os.chdir("../")
                if os.path.exists(output_path):
                    if not os.path.isdir(output_path):
                        raise NotImplementedError() # EEXIST
                else:
                    os.mkdir(output_path)

                tasks = []
                for category in datatype:
                    manifest = {
                        "pt": "eventPoint",
                        "hs": "hightScore",
                        "lp": "loungePoint"
                    }
                    tasks.append(makeimg(category, output_path))
                await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(opt.type, opt.output_path, opt.checksum, opt.dryrun, opt.search_id))
