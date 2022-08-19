import json
import datetime

from PIL import Image, ImageFont, ImageDraw

async def makeimg(category, path:str="image"):

    # Abbreviation to Chinese
    def categories(category):
        manifest = {
            "pt": "PT榜",
            "hs": "高分榜",
            "lp": "廳榜"
        }
        return manifest[category]

    # Abbreviation to fullform
    def fullform(abbreviation):
        manifest = {
            "pt": "eventPoint",
            "hs": "highScore",
            "lp": "loungePoint"
        }
        return manifest[abbreviation]

    # Event type convert
    def idtostring(typeid):
        manifest = {
            3:  "Theater",
            4:  "Tour",
            5:  "Anniversary",
            11: "Tune",
            13: "Tale",
            16: "Treasure"
        }
        return manifest[typeid]

    # Configurations
    with open("./config.json") as config:
        config = json.load(config)

        border_data = config["border_data"]
        data_eventinfo = config["data_eventinfo"]
        background = config["background"]

        font_event_title = config["font_event_title"]
        font_data_title = config["font_data_title"]
        font_subtitle = config["font_subtitle"]

    with open(border_data, mode="r", encoding='utf8') as file:
        borderData = json.load(file)
    with open(data_eventinfo, mode="r", encoding='utf8') as file:
        eventData = json.load(file)

    # Assign data
    eventName = eventData["name"]
    eventType = eventData["type"]
    beginDate = eventData["schedule"]["beginDate"]
    endDate = eventData["schedule"]["endDate"]
    boostDate = eventData["schedule"]["boostBeginDate"]
    timeSummaries = borderData[fullform(category)]["summaryTime"]

    # Formatting datetime
    beginDate = beginDate.replace("-", "/")[0:10]
    endDate = endDate.replace("-", "/")[0:10]
    boostDate = boostDate.replace("-", "/")[0:10]
    time_date = timeSummaries.replace("-","/")[0:10]
    time_date += f" {timeSummaries[11:16]}"

    # Remaining days ("BD" = "Begin Date", "ED" = "End Date")
    if eventType == 5:
        formatedBD = datetime.datetime(int(beginDate[0:4]), int(beginDate[5:7]), int(beginDate[8:10]), 15, 0, 0)
        formatedED = datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]), 20, 59, 59)
    else:
        formatedBD = datetime.datetime(int(beginDate[0:4]), int(beginDate[5:7]), int(beginDate[8:10]), 0, 0, 0)
        formatedED = datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]), 23, 59, 59)

    length_of_hours = (formatedED - formatedBD).days * 24 + (formatedED - formatedBD).seconds / 3600
    length_of_days = length_of_hours / 24

    # Configure current time with Japan Standard Time(GMT+9)
    current_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    current_time = current_time.astimezone(datetime.timezone(datetime.timedelta(hours=9)))

    # Special case for Annivaersary
    if eventType == 5:
        end_time = datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]), 23, 59, 59, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
    else:
        end_time = datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]), 21, 00, 00, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
    
    different_time = end_time - current_time
    different_hours = different_time.total_seconds() / 3600
    different_days = different_hours / 24

    total_hours = length_of_days * 24
    progress = (total_hours-different_hours) / total_hours

    # Pillow 畫布設定
    frame = Image.open(background)
    frame = frame.convert('RGBA')
    draw = ImageDraw.Draw(frame)

    # Pillow 設定
    score_x = 0
    y_globe = 290
    x_globe = 40

    # 字型設定
    event_title = ImageFont.truetype(font_event_title, 27)
    data_title = ImageFont.truetype(font_data_title, 25)
    subtitle = ImageFont.truetype(font_subtitle, 20)
    interval = ImageFont.truetype(font_subtitle, 30)

    # 圖片資訊產生
    draw.text((x_globe, 28), f"{eventName}", (2, 62, 125), font=event_title)

    if progress >= 100:
        draw.text((x_globe, 70), f"資料時間：{time_date} (100%)\n", (0, 40, 85), font=data_title)
    else:
        draw.text((x_globe, 70), f"資料時間：{time_date} ({progress:.2%})\n", (0, 40, 85), font=data_title)

    draw.text((x_globe, 105), f"活動期間：{beginDate} ~ {endDate} ({int(total_hours)}小時)\n", (92, 103, 125), font=subtitle)
    draw.text((x_globe, 130), f"後半期間：{boostDate} ~ {endDate}\n", (92, 103, 125), font=subtitle)

    if different_days <= 0:
        draw.text((x_globe, 155), f"剩下時間：已經結束囉～\n", (92, 103, 125), font=subtitle)
    else:
        draw.text((x_globe, 155), f"剩下時間：{different_days:.2f}天 ({different_hours:.1f}小時)\n", (92, 103, 125), font=subtitle)

    draw.text((x_globe, 180), f"榜線類型：{idtostring(eventType)} ({categories(category)})\n", (92, 103, 125), font=subtitle)

    # 圖片排名產生
    for data in borderData[fullform(category)]["scores"]:
        rank = data["rank"]
        score = data["score"]

        if score is not None:
            if (len(str(rank)) == 1):
                argx = 73
            elif (len(str(rank)) == 2):
                argx = 54
            elif (len(str(rank)) == 3):
                argx = 38
            elif (len(str(rank)) == 4):
                argx = 12
            else:
                argx = -6

            draw.text(
                xy=(x_globe + argx, y_globe),
                text=f"{rank:,.0f}",
                fill=(3, 83, 164),
                font=interval
            )
            draw.text(
                xy=(x_globe + 95, y_globe),
                text="位",
                fill=(3, 83, 164),
                font=interval
            )

            if len(str(score)) == 9:
                score_x = 230
            elif len(str(score)) == 8:
                score_x = 256.8
            elif len(str(score)) == 7:
                score_x = 274
            elif len(str(score)) == 6:
                score_x = 293
            elif len(str(score)) == 5:
                score_x = 319
            elif len(str(score)) == 4:
                score_x = 337

            draw.text(
                xy=(score_x, y_globe),
                text=f"{score:,.0f}",
                fill=(4, 102, 200),
                font=interval
            )

            y_globe += 40

    print(f"Generating border image: ./{path}/{categories(category)}.png")
    frame.save(f"./{path}/{categories(category)}.png")
