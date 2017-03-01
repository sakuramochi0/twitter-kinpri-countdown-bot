#!/usr/bin/env python3
import datetime

from dateutil.parser import parse

from get_tweepy import get_api


# if now is 00:00:00, remaining days would be greater than 1 day
# so we must minus 1
RELEASE_DATE = parse('2017-06-10') - datetime.timedelta(seconds=1)


def get_remaining_days(now=None):
    if now is None:
        now = datetime.datetime.now()
    delta = RELEASE_DATE - now
    remaining = delta.days + 1
    return remaining


def tweet(screen_name='kinpricountdown'):
    api = get_api(screen_name)
    days = get_remaining_days()
    text = get_text(days)
    return api.update_status(text)


def get_text(days):
    if days % 10 == 0 or abs(days) < 10:
        exclamation_num = 2
    else:
        exclamation_num = 1
    exclamation = '！' * exclamation_num

    if days > 0:
        text = ('『KING OF PRISM -PRIDE the HERO-』公開まで、'
                'あと {days} 日です{exclamation} #kinpri').format(
                    days=days, exclamation=exclamation)
    elif days == 0:
        text = '🎉🌈 今日は『KING OF PRISM -PRIDE the HERO-』の公開日です！！！ 🌈🎉 #kinpri'
    else:
        days *= -1
        text = ('『KING OF PRISM -PRIDE the HERO-』公開から、'
                '{days} 日が経過しました{exclamation} #kinpri').format(
                    days=days, exclamation=exclamation)
    return text


if __name__ == '__main__':
    tweet()
