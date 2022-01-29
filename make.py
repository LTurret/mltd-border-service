import json

async def makefile(file:json, filename:str):
    try:
        with open(f"{filename}.json", mode="w", encoding="utf-8") as data:
            data = json.dump(file, data, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"issue occur: {e}")
    finally:
        print(f'file "{filename}.json" created.')

if __name__ == "__main__":
    print('using "main.py" instead.')