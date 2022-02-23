import aiohttp
import argparse
import asyncio
import os

from src.fetch import GetNewestEvent, SearchEvent, FetchBorder, FetchCover
from src.make import makefile
from src.image import makeimg

parser = argparse.ArgumentParser(
    description="Generator that fetches hosting event information and border datasets then generates border image."
)
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
    def typematch(typeid:int):
        manifest = [3, 4, 11, 13, 16]
        return manifest.count(typeid)

    async with aiohttp.ClientSession() as session:
        if search_id:
            eventData = await SearchEvent(search_id[0], session)
            tasks = []
            if (typematch(eventData["type"])):
                tasks.append(asyncio.create_task(FetchBorder(search_id[0], session)))
        else:
            eventData = await GetNewestEvent(session)
            evtID = eventData["id"]
            tasks = []
            if (typematch(eventData["type"])):
                tasks.append(asyncio.create_task(FetchBorder(evtID, session)))
        await asyncio.gather(*tasks)
        information = eventData
        if (typematch(eventData["type"])):
            border = tasks[0].result()
        print("fetch data complete.")

        if checksum:
            print("checksum complete.")
            pass
        else:
            if not os.path.isdir("./dataset"):
                os.mkdir("./dataset")
            os.chdir("./dataset")
            tasks = [
                asyncio.create_task(makefile(information, "information"))
            ]
            if (typematch(eventData["type"])):
                tasks.append(asyncio.create_task(makefile(border, "border")))
            await asyncio.gather(*tasks)

            if (dryrun or not(typematch(eventData["type"]))):
                pass
            else:
                os.chdir("../")
                if os.path.isdir(f"{output_path}"):
                    pass
                else:
                    os.mkdir(f"{output_path}")

                tasks = []
                for category in datatype:
                    manifest = {
                        "pt": "eventPoint",
                        "hs": "highScore",
                        "lp": "loungePoint"
                    }
                    tasks.append(makeimg(manifest[category], output_path))
                await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(opt.type, opt.output_path, opt.checksum, opt.dryrun, opt.search_id))