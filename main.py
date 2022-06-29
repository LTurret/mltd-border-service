import aiohttp
import argparse
import asyncio
import os

from src.fetch import GetNewest, Search, FetchBorder, FetchCover
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
parser.add_argument("-I", "--identify", nargs=1, type=int, metavar="",
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
                    help="Don't generate border-image and output folder to disk"
                )
group.add_argument("--checksum",
                    action="store_true",
                    help="Don't generate any file or folder, test API response"
                )
group.add_argument("--static",
                    action="store_true",
                    help="Used for debugging"
)
opt = parser.parse_args()

async def main(output_type:list, output_path:str, checksum:bool=False, dryrun:bool=False, static:bool=False, identify:int=None):

    check_identified = lambda identify: True if (identify is not None and type(identify) is int and identify > 0) else 1
    identify_maximun = lambda identify, idmax: True if (identify is not None and identify > idmax) else 2
    matchtype = lambda typecode: ([3, 4, 5, 11, 13, 16].count(typecode)) == 1

    tasks = []
    announcement = ""

    if not static:
        async with aiohttp.ClientSession() as session:
            eventdata = await GetNewest(session)
            identify = eventdata["id"]

            if check_identified(identify):
                if matchtype(eventdata["type"]):
                    tasks.append(asyncio.create_task(FetchBorder(identify, session)))
                else:
                    announcement = "This event is inborderable."
            else:
                identify = eventdata["id"]
                if matchtype(eventdata["type"]):
                    tasks.append(asyncio.create_task(FetchBorder(identify, session)))
            await asyncio.gather(*tasks)
            if matchtype(eventdata["type"]):
                border = tasks[0].result()
            print("fetch data complete.")

    if checksum:
        print("checksum complete.")
    else:
        if not os.path.isdir("./dataset"):
            os.mkdir("./dataset")
        os.chdir("./dataset")
        tasks = [
            asyncio.create_task(makefile(eventdata, "information"))
        ]
        if matchtype(eventdata["type"]):
            tasks.append(asyncio.create_task(makefile(border, "border")))
        await asyncio.gather(*tasks)
        os.chdir("../")

        if dryrun:
            print("dryrun complete.")
        else:
            if not os.path.isdir(output_path):
                os.mkdir(output_path)

            tasks = []
            for category in output_type:
                tasks.append(makeimg(category, output_path))
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(opt.output_type, opt.output_path, opt.checksum, opt.dryrun, opt.static, opt.search_id))
