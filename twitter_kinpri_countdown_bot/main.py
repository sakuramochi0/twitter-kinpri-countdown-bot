#!/usr/bin/env python3
import datetime
import argparse

from dateutil.parser import parse

from get_tweepy import get_api


# if now is 00:00:00, remaining days would be greater than 1 day
# so we must minus 1
RELEASE_DATE = parse('2017-06-10') - datetime.timedelta(seconds=1)
RELEASE_DATETIME = parse('2017-06-10 00:00') - datetime.timedelta(seconds=1)


def get_remaining_days(now=None):
    if now is None:
        now = datetime.datetime.now()
    delta = RELEASE_DATE - now
    remaining = delta.days + 1
    return remaining


def get_remaining_hours(now=None):
    if now is None:
        now = datetime.datetime.now()
    # see the same hour if within 30 min.
    delta = RELEASE_DATETIME - now
    if delta >= datetime.timedelta(0):
        delta += datetime.timedelta(minutes=30)
    else:
        delta -= datetime.timedelta(minutes=30)
    remaining = int(delta.total_seconds() / 3600)
    return remaining


def tweet(screen_name='kinpricountdown'):
    api = get_api(screen_name)
    days = get_remaining_days()
    hours = get_remaining_hours()
    text = get_text(days, hours)
    img = get_img(days)
    if not is_hours_countdown(hours) and img:
        res = api.update_with_media(img, status=text)
    else:
        res = api.update_status(text)
    return res


def tweet_second(screen_name='kinpricountdown'):
    api = get_api(screen_name)
    days = get_remaining_days()
    hours = get_remaining_hours()
    text = get_text(days, hours)
    res = api.update_status(text)
    return res


def get_img(days):
    # prepare images if 0 <= days <= 5
    if 0 <= days <= 5:
        img = 'img/kinpri-countdown-{}.png'.format(days)
    else:
        img = None
    return img


def is_hours_countdown(hours):
    return hours % 24 != 0


def get_text(days, hours):
    # 「○日経過しました」ではなく、「○日目です」とツイートするための修正。
    # これによって、公開日以前が正しくなくなってしまっている。
    days -= 1
    
    # make the number of exclamation marks different
    # depanding on the remaining days
    if 0 < days <= 10:
        exclamation_num = 3
    elif days % 10 == 0:
        exclamation_num = 2
    else:
        exclamation_num = 1
    exclamation = '！' * exclamation_num
    exclamation_ko = '!' * exclamation_num

    # 100の倍数の時にクラッカーを鳴らす🎉✨
    if days % 100 == 0:
        celebration = '👑🌹🎉🌈✨'
    else:
        celebration = ''

    # add an additinal space characters
    # to avoid a duplicate status restriction
    # there are 4 cases: 0-6 / 6-12 / 12-18 / 18-24
    space = ' ' * (datetime.datetime.now().hour // 6 % 4)

    if args.second:
        text = ('『KING OF PRISM -PRIDE the HERO-』\n'
                '7/22(土)上映開始劇場での公開まで\n'
                'あと {days} 日です{exclamation}\n'
                '#kinpri #prettyrhythm').format(
                    days=days,
                    exclamation=exclamation,
                    exclamation_ko=exclamation_ko,
                )
    elif days > 0:
        if is_hours_countdown(hours):
            text = ('『KING OF PRISM -PRIDE the HERO-』\n'
                    '公開まで、あと {hours} 時間です{exclamation}\n'
                    '공개까지 앞으로 {hours} 시간입니다{exclamation_ko}\n'
                    '#kinpri #prettyrhythm').format(
                        hours=hours,
                        exclamation=exclamation,
                        exclamation_ko=exclamation_ko,
                    )
        else:
            text = ('『KING OF PRISM -PRIDE the HERO-』\n'
                    '公開まで、あと {days} 日です{exclamation}\n'
                    '공개까지 앞으로 {days} 일입니다{exclamation_ko}\n'
                    '{space}#kinpri #prettyrhythm').format(
                        days=days,
                        exclamation=exclamation,
                        exclamation_ko=exclamation_ko,
                        space=space)
    elif days == 0:
        text = ('✨🎉🌈 『KING OF PRISM -PRIDE the HERO-』 🌈🎉✨\n'
                '公開日です！！！！！\n'
                '공개 일입니다!!!!!\n'
                '{space}#kinpri #prettyrhythm').format(space=space)
    else:
        days *= -1
        text = ('{celebration}\n'
                '『KING OF PRISM -PRIDE the HERO-』\n'
                '今日は公開 {days} 日目です{exclamation}\n'
                '오늘은 공개 {days} 일째입니다{exclamation_ko}\n'
                '{space}#kinpri #prettyrhythm').format(
                    days=days,
                    celebration=celebration,
                    exclamation=exclamation,
                    exclamation_ko=exclamation_ko,
                    space=space)

    return text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--second', action='store_true')
    args = parser.parse_args()

    if args.second:
        # make release date 2017/07/22
        RELEASE_DATE += datetime.timedelta(days=42)
        RELEASE_DATETIME += datetime.timedelta(days=42)
        if args.debug:
            tweet_second('sakuramochi_pre')
        else:
            tweet_second()
    else:
        if args.debug:
            tweet('sakuramochi_pre')
        else:
            tweet()
