import os
import datetime
import calendar
from datetime import date
from datetime import timedelta
from random import randint
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def gen_random_time(_date, _hour, _minute, rand_offset):
    return datetime.datetime.combine(
        _date,
        datetime.time(hour=_hour, minute=_minute+randint(0,rand_offset))
        ).timestamp()

def cal_abbr(month):
    return calendar.month_abbr[month]

OAUTH_TOKEN = "SLACK_SDK_OAUTH_TOKEN"
TEST_CHANNEL_NAME = "#slack_sdk_bot_testing"
OLD_CHANNEL_NAME = "#teamchat"
TARGET_CHANNEL_NAME = "#35-party-people"
SLACK_CHANNEL = TARGET_CHANNEL_NAME

client = WebClient(token=os.environ[OAUTH_TOKEN])

if __name__ == '__main__':
    file = open("./teamchat_scheduled_msg_log.txt", "a")
    log_str = ""
    try:
        #for i in range(1,6):
        sch_date= date.today() + timedelta(days=1)
        if sch_date.weekday() <= 3 or sch_date.weekday() == 6: #Mon, Tue, Wed, Thu, Sat
            log_str = "{0} Msg scheduled to {4} for {1}, msg: {2} {3} PDY".format(
                datetime.datetime.now(),
                sch_date,
                (sch_date + timedelta(days=1)).day, 
                cal_abbr((sch_date + timedelta(days=1)).month),
                SLACK_CHANNEL
            )
            print(log_str)
            response = client.chat_scheduleMessage(
                channel= SLACK_CHANNEL,
                post_at= gen_random_time(_date=sch_date, _hour=17, _minute=50, rand_offset=9),
                as_user= True,
                text= "{0} {1} PDY".format(
                    (sch_date + timedelta(days=1)).day, 
                    cal_abbr((sch_date + timedelta(days=1)).month)
                )
            )
            file.write(log_str+"\n")
        else:
            log_str= "{0} no Msg scheduled to {1} for {2}".format(
                datetime.datetime.now(),
                SLACK_CHANNEL,
                (sch_date + timedelta(days=1)).day
            ) 
            print(log_str)
            file.write(log_str+"\n")
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
        file.write("Got an error: {}".format(e.response['error']))
        # Also receive a corresponding status_code
        assert isinstance(e.response.status_code, int)
        print(f"Received a response status_code: {e.response.status_code}")
        file.write("Received a response status_code: {}".format(e.response.status_code))
    file.close()