import json
import datetime
from PIL import Image, ImageFont, ImageDraw

async def makeimg(category, path:str="image"):
   
    # 轉為中文
    def categories(category):
        manifest = {
            "pt": "PT榜",
            "hs": "高分榜",
            "lp": "廳榜"
        }
        return manifest[category]

    # 轉為全名
    def fullform(abbreviation):
        manifest = {
            "pt": "eventPoint",
            "hs": "highScore",
            "lp": "loungePoint"
        }
        return manifest[abbreviation]

    # 活動類型轉譯
    def idtostring(typeid):
        manifest = {
            3:  "Theater",
            4:  "Tour",
            11: "Tune",
            13: "Tale",
            16: "Treasure"
        }
        return manifest[typeid]

    # 檔案設定
    with open("./config.json") as config:
        config = json.load(config)
        background = "./components/AnnaFrame.png"
        data_border = "./dataset/border.json"
        data_eventinfo = "./dataset/information.json"
        font_filepath = "./components/jf-openhuninn-1.1.ttf"
        title_font_filepath = "./components/ChiuKongGothic-CL-Regular.otf"

    with open(data_border, mode="r", encoding='utf8') as file:
        borderData = json.load(file)
    with open(data_eventinfo, mode="r", encoding='utf8') as file:
        eventData = json.load(file)

    # 指定資料
    eventName = eventData["name"]
    eventType = eventData["type"]
    beginDate = eventData["schedule"]["beginDate"]
    endDate = eventData["schedule"]["endDate"]
    boostDate = eventData["schedule"]["boostBeginDate"]
    timeSummaries = borderData[fullform(category)]["summaryTime"]

    # 格式化日期
    beginDate = beginDate.replace("-", "/")[0:10]
    endDate = endDate.replace("-", "/")[0:10]
    boostDate = boostDate.replace("-", "/")[0:10]
    time_date = timeSummaries.replace("-","/")[0:10]
    time_date += f" {timeSummaries[11:16]}"

    # 活動天數
    formatedBD = datetime.date(int(beginDate[0:4]), int(beginDate[5:7]), int(beginDate[8:10]))
    formatedED = datetime.date(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]))
    dayLength = (formatedED - formatedBD).days

    # 新增台灣時間，方便觀察
    current_time = datetime.datetime(2022, 1, 23, 15, 31, 0, 0)
    end_time = datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]), 19, 59, 59, 0)
    different_time = end_time - current_time
    different_hours = different_time.total_seconds() / 3600
    different_days = different_hours / 24
    total_hours = dayLength*24
    progress = (total_hours-different_hours) / total_hours

    # Pillow 畫布設定
    AnnaFrame = Image.open(background)
    AnnaFrame = AnnaFrame.convert('RGBA')
    draw = ImageDraw.Draw(AnnaFrame)

    # Pillow 設定
    y_globe = 290
    y_accumulate = 40
    x_globe = 40
    length_adjust = 1
    adjust_x = 150

    # 字型設定
    broadcasting = ImageFont.truetype(font_filepath, 30)
    title = ImageFont.truetype(title_font_filepath, 27)
    fetchtime = ImageFont.truetype(font_filepath, 25)
    body = ImageFont.truetype(font_filepath, 20)

    # 圖片資訊產生
    draw.text((x_globe,28), f"{eventName}", (2, 62, 125), font=title)
    draw.text((x_globe,70), f"資料時間：{time_date} ({progress:.1%})\n", (0, 40, 85), font=fetchtime)
    draw.text((x_globe,105), f"活動期間：{beginDate} ~ {endDate} ({dayLength*24}小時)\n", (92, 103, 125), font=body)
    draw.text((x_globe,130), f"後半期間：{boostDate} ~ {endDate}\n", (92, 103, 125), font=body)
    draw.text((x_globe,155), f"剩下時間：{different_days:.2}天 ({int(different_hours)}小時)\n", (92, 103, 125), font=body)
    draw.text((x_globe,180), f"榜線類型：{idtostring(eventType)} ({categories(category)})\n", (92, 103, 125), font=body)
    
    # 圖片排名產生
    try:
        for data in borderData[fullform(category)]["scores"]:
            rank = data["rank"]
            score = data["score"]
            if score is not None:
                if (length_adjust <= 3):
                    argx = 73
                elif (length_adjust == 4):
                    argx = 36
                elif (length_adjust > 4 and length_adjust < 7):
                    argx = 18
                elif (length_adjust > 9):
                    break
                else:
                    argx = 0

                draw.text(
                    xy=(x_globe + argx, y_globe),
                    text=f"{rank}",
                    fill=(3, 83, 164),
                    font=broadcasting
                )
                draw.text(
                    xy=(x_globe + 95, y_globe),
                    text="位",
                    fill=(3, 83, 164),
                    font=broadcasting
                )

                if len(str(score)) == 8:
                    adjust_x = 176.8
                elif len(str(score)) == 7:
                    adjust_x = 194

                draw.text(
                    xy=(x_globe + adjust_x + 30, y_globe),
                    text=f"{score:,.0f}",
                    fill=(4, 102, 200),
                    font=broadcasting
                )
                y_globe += y_accumulate
                length_adjust += 1
        print(f"makeimg: {categories(category)}.png")
        AnnaFrame.save(f"./{path}/{categories(category)}.png")
    except Exception as e:
        print(f"makeimg {e}")