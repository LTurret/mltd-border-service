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
        font_body = config["font_body"]

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
    formatedBD = datetime.date(int(beginDate[0:4]), int(beginDate[5:7]), int(beginDate[8:10]))
    formatedED = datetime.date(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]))

    if eventType == 5:
        dayLength = (formatedED - formatedBD).days + 1
    else:
        dayLength = (formatedED - formatedBD).days

    # Configure current time with Japan Standard Time(GMT+9)
    current_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    current_time = current_time.astimezone(datetime.timezone(datetime.timedelta(hours=9)))

    # Special case for Annivaersary
    if eventType == 5:
        end_time = datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]), 22, 59, 59, 0, tzinfo=datetime.timezone.utc)
    else:
        end_time = datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]), 19, 59, 59, 0, tzinfo=datetime.timezone.utc)
    
    different_time = end_time - current_time
    different_hours = different_time.total_seconds() / 3600
    different_days = different_hours / 24
    total_hours = dayLength * 24
    progress = (total_hours-different_hours) / total_hours

    # Pillow 畫布設定
    frame = Image.open(background)
    frame = frame.convert('RGBA')
    draw = ImageDraw.Draw(frame)

    # Pillow 設定
    y_globe = 290
    y_accumulate = 40
    x_globe = 40
    length_adjust = 1
    adjust_x = 150

    # 字型設定
    event_title = ImageFont.truetype(font_event_title, 27)
    data_title = ImageFont.truetype(font_data_title, 25)
    subtitle = ImageFont.truetype(font_subtitle, 20)
    body = ImageFont.truetype(font_body, 30)
    interval = ImageFont.truetype(font_subtitle, 30)

    # 圖片資訊產生
    draw.text((x_globe,28), f"{eventName}", (2, 62, 125), font=event_title)

    if progress >= 100:
        draw.text((x_globe,70), f"資料時間：{time_date} (100%)\n", (0, 40, 85), font=data_title)
    else:
        draw.text((x_globe,70), f"資料時間：{time_date} ({progress:.1%})\n", (0, 40, 85), font=data_title)

    draw.text((x_globe,105), f"活動期間：{beginDate} ~ {endDate} ({dayLength*24}小時)\n", (92, 103, 125), font=subtitle)
    draw.text((x_globe,130), f"後半期間：{boostDate} ~ {endDate}\n", (92, 103, 125), font=subtitle)

    if different_days <= 0:
        draw.text((x_globe,155), f"剩下時間：已經結束囉～\n", (92, 103, 125), font=subtitle)
    else:
        draw.text((x_globe,155), f"剩下時間：{different_days:.2f}天 ({int(different_hours)}小時)\n", (92, 103, 125), font=subtitle)

    draw.text((x_globe,180), f"榜線類型：{idtostring(eventType)} ({categories(category)})\n", (92, 103, 125), font=subtitle)

    # 圖片排名產生
    for data in borderData[fullform(category)]["scores"]:
        rank = data["rank"]
        score = data["score"]
        if score is not None:
            if (length_adjust > 9):
                break
            elif (len(str(rank)) == 1):
                argx = 73
            elif (len(str(rank)) == 2):
                argx = 54
            elif (len(str(rank)) == 3):
                argx = 36
            elif (len(str(rank)) == 4):
                argx = 18
            else:
                argx = 0

            draw.text(
                xy=(x_globe + argx, y_globe),
                text=f"{rank}",
                fill=(3, 83, 164),
                font=interval
            )
            draw.text(
                xy=(x_globe + 95, y_globe),
                text="位",
                fill=(3, 83, 164),
                font=interval
            )

            if len(str(score)) == 8:
                adjust_x = 186.8
            elif len(str(score)) == 7:
                adjust_x = 204
            elif len(str(score)) == 6:
                adjust_x = 211.2

            draw.text(
                xy=(x_globe + adjust_x + 30, y_globe),
                text=f"{score:,.0f}",
                fill=(4, 102, 200),
                font=body
            )
            y_globe += y_accumulate
            length_adjust += 1
    print(f"Generating border image: ./{path}/{categories(category)}.png")
    frame.save(f"./{path}/{categories(category)}.png")
