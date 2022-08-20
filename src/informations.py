import datetime
import json

def time_cluster(fullform, category):

    with open("./config.json") as config:
        config = json.load(config)
        border_data = config["border_data"]
        data_eventinfo = config["data_eventinfo"]

    with open(border_data, mode="r", encoding='utf8') as file:
        borderData = json.load(file)
    with open(data_eventinfo, mode="r", encoding='utf8') as file:
        eventData = json.load(file)

    # Sort data
    eventName = eventData["name"]
    eventType = eventData["type"]
    beginDate = eventData["schedule"]["beginDate"]
    endDate = eventData["schedule"]["endDate"]
    boostDate = eventData["schedule"]["boostBeginDate"]
    summaryTime = borderData[fullform(category)]["summaryTime"]
    
    # Formate data
    beginDate = beginDate.replace("-", "/")[0:10]
    endDate = endDate.replace("-", "/")[0:10]
    boostDate = boostDate.replace("-", "/")[0:10]
    dataset_updated_time = summaryTime.replace("-","/")[0:10]
    dataset_updated_time += f" {summaryTime[11:16]}"

    # Remaining days ("BD" = "Begin Date", "ED" = "End Date")
    if eventType == 5:
        formatedBD = datetime.datetime(int(beginDate[0:4]), int(beginDate[5:7]), int(beginDate[8:10]), 0, 0, 0)
        formatedED = datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]), 23, 59, 59)
    else:
        formatedBD = datetime.datetime(int(beginDate[0:4]), int(beginDate[5:7]), int(beginDate[8:10]), 15, 0, 0)
        formatedED = datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]), 21, 0, 0)

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
    
    difference_time = end_time - current_time
    difference_hours = difference_time.total_seconds() / 3600
    difference_days = difference_hours / 24

    total_hours = length_of_days * 24
    progress = (total_hours - difference_hours) / total_hours

    sets = {
        "raw": {
            "borderData": borderData,
            "event_info": {
                "eventName": eventName,
                "eventType": eventType
            },
            "event_date": {
                "beginDate": beginDate,
                "endDate": endDate,
                "boostDate": boostDate
            }
        },
        "handled": {
            "dataset_updated_time": dataset_updated_time,
            "difference_days": difference_days,
            "difference_hours": difference_hours,
            "total_hours": total_hours,
            "progress": progress
        }
    }

    return sets