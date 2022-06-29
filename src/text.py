import datetime

class event:
    def __init__(self):
        self.status = []

    async def GetNewest(session):
        URL = "https://api.matsurihi.me/mltd/v1/events"
        async with session.get(URL) as response:
            try:
                data = await response.json()
                return data[-1]
            except Exception as exception:
                print(f"event.GetNewest exception occured,\n{exception}")
                return 1

    async def Search(identify:int, session):
        URL = f"https://api.matsurihi.me/mltd/v1/events/{identify}"
        async with session.get(URL) as response:
            try:
                data = await response.json()
                return data
            except Exception as exception:
                print(f"event.Search exception occured,\n{exception}")
                return 1

    async def FetchBorder(identify:int, session):
        URL = f"https://api.matsurihi.me/mltd/v1/events/{identify}/rankings/borderPoints"
        async with session.get(URL) as response:
            try:
                data = await response.json()
                return data
            except Exception as exception:
                print(f"event.FetchBorder exception occured,\n{exception}")
                return 1
    
    async def bordergenerator(event_data:list, border_data:list, score_type:int=0):

        typeselector = lambda mode: ["eventPoint", "highScore", "loungePoint"][mode]

        # Specified information forms
        title = event_data["name"]
        beginDate = event_data["schedule"]["beginDate"]
        endDate = event_data["schedule"]["endDate"]
        boostDate = ""
        timeSummaries = border_data[typeselector(score_type)]["summaryTime"]

        # Formate forms
        beginDate = beginDate.replace("-", "/")[0:10]
        endDate = endDate.replace("-", "/")[0:10]
        time_date = timeSummaries.replace("-","/")[0:10]
        time_date += f" {timeSummaries[11:16]}"

        # Special case handle
        if "boostBeginDate" in event_data["schedule"]:
            boostDate = event_data["schedule"]["boostBeginDate"]
            boostDate = boostDate.replace("-", "/")[0:10]

        # Event days left calculations
        converted_begin_date = datetime.date(int(beginDate[0:4]), int(beginDate[5:7]), int(beginDate[8:10]))
        converted_end_date = datetime.date(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]))
        day_length = (converted_end_date - converted_begin_date).days

        # Datetime calculations
        current_time = datetime.datetime.now()
        end_time = datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]), 19, 59, 59, 0)
        different_time = end_time - current_time
        different_hours = different_time.total_seconds() / 3600
        different_days = different_hours / 24
        total_hours = day_length * 24
        progress = (total_hours - different_hours) / total_hours
        taipei_time = int(timeSummaries[11:13]) - 1
        taipei_time = f"{int(taipei_time)}{timeSummaries[13:16]}"

        # Text-mode initialization
        overprogess = lambda progress: 1 if (progress>=100) else progress
        result = "```"
        result += f"{title}\n"
        result += f"活動期間：{beginDate} ~ {endDate} ({day_length*24}小時)\n"
        result += f"更新時間：{time_date} ({overprogess(progress):.1%})\n"

        # Special case handle
        if len(boostDate) > 0:
            result += f"後半期間：{boostDate} ~ {endDate}\n"
        if different_days > 0:
            result += f"剩下時間：{different_days:.2}天 ({different_hours:.3}小時)\n"

        result += f"\n"

        for data in border_data[typeselector(score_type)]["scores"]:
            rank = data["rank"]
            score = data["score"]

            if score is not None:
                result += f"排名：{rank:<10,d}分數：{score:>10,.0f}\n"

        result = f"{result}```"
        return result