import json

async def makefile(file:list, filename:str):
    try:
        with open(f"{filename}.json", mode="w", encoding="utf-8") as data:
            data = json.dump(file, data, indent=4, ensure_ascii=False)
    except Exception as exception:
        print(f"issue occur: {exception}")
    else:
        print(f'"{filename}.json" created.')