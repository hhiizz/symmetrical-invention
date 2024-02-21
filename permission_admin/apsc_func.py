import datetime
from myApp.models import getjob
from mysql_member.models import Member
from user.models import Notice
from dateutil.relativedelta import relativedelta


def check_mysql_connect():
    Member.objects.filter()
    return True
def remove_job_table():
    today = datetime.date.today()
    twoweek = datetime.timedelta(weeks=2)
    deleteday = today-twoweek
    getjob.objects.filter(date__lte=deleteday).delete()
    return True
def remove_notice():
    today = datetime.date.today()
    twoweek = datetime.timedelta(days=60)
    deleteday = today-twoweek
    Notice.objects.filter(Notice_date__lte=deleteday).delete()
    return True

def remove_user_two_year():
    today = datetime.date.today()
    twoyear = datetime.timedelta(years = 2)
    deletuser = today-twoyear
    Member.objects.filter(last_login__lte=deletuser).delete()
def remove_user_two_year():
    today = datetime.date.today()
    twoyear = relativedelta(years = 2)
    deletuser = today-twoyear
    Member.objects.filter(last_login__lte=deletuser).delete()
