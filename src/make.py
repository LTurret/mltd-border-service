import json

async def makefile(file:json, filename:str):
    try:
        with open(f"{filename}.json", mode="w", encoding="utf-8") as data:
            data = json.dump(file, data, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"makefile: {e}")
    else:
        print(f'file "{filename}.json" created.')
