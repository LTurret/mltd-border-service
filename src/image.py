import json

from src.informations import time_cluster
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
    def idtostr(typeid):
        manifest = {
            3:  "Theater",
            4:  "Tour",
            5:  "Anniversary",
            11: "Tune",
            13: "Tale",
            16: "Treasure"
        }
        return manifest[typeid]

    # Event informations initialize
    sets = time_cluster(fullform, category)

    borderData = sets["raw"]["borderData"]
    event_name = sets["raw"]["event_info"]["eventName"]
    event_type = sets["raw"]["event_info"]["eventType"]
    begin_date = sets["raw"]["event_date"]["beginDate"]
    end_date = sets["raw"]["event_date"]["endDate"]
    boost_date = sets["raw"]["event_date"]["boostDate"]
    update_time = sets["handled"]["dataset_updated_time"]
    difference_days = sets["handled"]["difference_days"]
    difference_hours = sets["handled"]["difference_hours"]
    total_hours = sets["handled"]["total_hours"]
    progress = sets["handled"]["progress"]

    # Configurations
    with open("./config.json") as config:

        config = json.load(config)

        background = config["background"]
        font_event_title = config["font_event_title"]
        font_data_title = config["font_data_title"]
        font_subtitle = config["font_subtitle"]

    # Pillow frame initialize
    frame = Image.open(background)
    frame = frame.convert('RGBA')
    draw = ImageDraw.Draw(frame)

    # Pillow px location adjusters initialize
    score_x = 0
    y_globe = 290
    x_globe = 40

    # Font settings
    event_title = ImageFont.truetype(font_event_title, 27)
    data_title = ImageFont.truetype(font_data_title, 25)
    subtitle = ImageFont.truetype(font_subtitle, 20)
    interval = ImageFont.truetype(font_subtitle, 30)

    # Image informations processing
    progress_overflow = lambda progress: f"資料時間：{update_time} (100%)\n" if (progress >= 100) else f"資料時間：{update_time} ({progress:.2%})\n"
    event_ended = lambda difference_days: f"剩下時間：已經結束囉～\n" if (difference_days <= 0) else f"剩下時間：{difference_days:.2f}天 ({difference_hours:.1f}小時)\n"
    draw.text((x_globe, 28), f"{event_name}", (2, 62, 125), font=event_title)
    draw.text((x_globe, 70), progress_overflow(progress), (0, 40, 85), font=data_title)
    draw.text((x_globe, 105), f"活動期間：{begin_date} ~ {end_date} ({int(total_hours)}小時)\n", (92, 103, 125), font=subtitle)
    draw.text((x_globe, 130), f"後半期間：{boost_date} ~ {end_date}\n", (92, 103, 125), font=subtitle)
    draw.text((x_globe, 155), event_ended(difference_days), (92, 103, 125), font=subtitle)
    draw.text((x_globe, 180), f"榜線類型：{idtostr(event_type)} ({categories(category)})\n", (92, 103, 125), font=subtitle)

    # Image ranking processing
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