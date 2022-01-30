from email.policy import default
import aiohttp
import argparse
import asyncio
import os
from fetch import GetNewestEvent, SearchEvent, FetchBorder, FetchCover
from make import makefile
from image import makeimg

parser = argparse.ArgumentParser(
    description="Generator that fetches hosting event information and border datasets then generates border image."
)
parser.add_argument("-S", "--search_id", nargs=1, type=int, metavar="",
                    required=False,
                    help="Search specific event with unique ID"
                )
parser.add_argument("-O", "--output_path", nargs=1, type=str, metavar="",
                    required=False,
                    default="./img-output",
                    help='Image generate ouput path, default is "./img-output"'
                )
parser.add_argument("-T", "--type", nargs="+", type=str, metavar="",
                    required=False,
                    help="Select fetches border type",
                    choices=["pt", "hs", "lp"]
                )
group = parser.add_mutually_exclusive_group()
group.add_argument("--checksum",
                    action="store_true",
                    help=f"Don't generate any folder to disk, test API response"
                )
group.add_argument("--dryrun",
                    action="store_true",
                    help=f"Don't generate image and output folder to disk"
                )
opt = parser.parse_args()

async def main(datatype, output_path, checksum, dryrun, search_id):
    async with aiohttp.ClientSession() as session:
        if search_id is not None:
            tasks = [
                asyncio.create_task(SearchEvent(search_id[0], session)),
                asyncio.create_task(FetchBorder(search_id[0], session))
            ]
        else:
            evtID = await GetNewestEvent(session)
            evtID = evtID["id"]
            tasks = [
                asyncio.create_task(SearchEvent(evtID, session)),
                asyncio.create_task(FetchBorder(evtID, session))
            ]
        await asyncio.gather(*tasks)
        information = tasks[0].result()
        border = tasks[1].result()
        print("fetch data complete.")

        if checksum:
            print("checksum complete.")
            pass
        else: 
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

            if dryrun:
                print("dryrun complete.")
                pass
            else:
                os.chdir("../")
                if os.path.isdir(f"{output_path}"):
                    pass
                else:
                    os.mkdir(f"{output_path}")

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
    loop.run_until_complete(main(opt.type, opt.output_path, opt.checksum, opt.dryrun, opt.search_id))