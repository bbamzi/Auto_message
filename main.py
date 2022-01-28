import pandas as pd
import random
import requests
import datetime
import numpy as np
import smtplib
import os

from email.mime.text import MIMEText
user = os.environ.get('username')
password = os.environ.get('password')
recipient= os.environ.get('recipient')
smtp_detail = 'smtp.mail.yahoo.com'
SMTP_PORT = 587

def send_email(msg,EMAIL_SUBJECT):
    msg = MIMEText(msg)
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = user
    msg['To'] = recipient
    debuglevel = True
    mail = smtplib.SMTP(smtp_detail, SMTP_PORT)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(user, password)
    mail.sendmail(user, recipient, msg.as_string())
    mail.quit()

messages = {
    'b_day_msg': [f'The Lord your God is in your midst, a mighty one who will save; He will rejoice over you with '
                  'gladness; he will quiet you by his love; he will exult over you with loud singing.” – Zephaniah 3:17 '
                  'Happiest of birthdays to you, ###. May God hold His comforting hand over your life in the coming '
                  'year',
                  'May Jesus Christ continue to bless you abundantly and keep you safe in his loving care. On your '
                  "birthday, enjoy His divine presence in your life. Have a happy and holy birthday, ###. You mean"
                  " the world to us! Araba Baptist Church",
                  "Life by itself is a gift, so never forget to thank God for it. Moreover, never forget to make the most"
                  "of it. May God bless you on your birthday with abundant peace and joy. Happy birthday, ###. we "
                  "love you more than words can say. Araba Baptist Church",
                  "On your birthday, we wish you every ounce of happiness ###. We hope you bring glory to Jesus’s "
                  "name every day of the coming year. Have fun and a blessed day. we love you. Araba Baptist Church",
                  "God is always there to guide you, protect you and comfort you. You are never alone.He is always near. "
                  "May you have a lovely day and an even more beautiful year ahead. Happy Birthday. May God bless you "
                  "abundantly, ###! Araba Baptist Church",
                  "Wishing you a day filled with happy memories and a year with numerous reasons to be thankful about. "
                  "Happy Birthday ###. May God bless you. Araba Baptist Church",
                  "Happy birthday, ###. On your birthday I pray to God for your health and well-being. May Jesus gift you "
                  "all the success, pride, and prosperity. Have a great year ahead. Araba Baptist Church"],
    'wed_msg': ["Love that grows through time is such an inspiring thing. Congratulations on your ### years together."
                "Araba Baptist Church",
                "Having each other’s backs and taking care of one another’s souls for ### years, that’s a beautiful faith walk."
                "Happy Anniversary Araba Baptist Church",
                "Sharing in your happiness as you celebrate ### years of marriage. Today is your day to be in the "
                "spotlight…to celebrate all you’ve accomplished together…and to bask in all the admiration. "
                "Araba Baptist Church",
                "### years of marriage! It couldn’t have been easy every day, but you two make it look that way"
                "Araba Baptist Church."

                ]
}


def age(new):
    this_year = datetime.datetime.today().year
    age = this_year - new.year
    return age


def month_day(new):
    current_month = new.month
    day = new.day
    month_and_day = (current_month, day)
    return month_and_day


def wed_month_day(new):
    if new == pd.isnull(np.datetime64('NaT')):
        month_and_day = (0, 0)
    else:
        current_month = new.month
        day = new.day
        month_and_day = (current_month, day)
    return month_and_day


def month(new):
    current_month = new.month

    return current_month


sms_username = os.environ.get('sms_username')
sms_password = os.environ.get('sms_password')


class Sms():

    def __init__(self):
        self.url = f'https://portal.nigeriabulksms.com/api/?username={sms_username}&password={sms_password}&action=balance'

    def balance_getter(self):
        balance = int(requests.get(url=self.url).json()['balance'])
        return balance

    def sms_sender(self, sender, phone_numbers, message):
        url = f'https://portal.nigeriabulksms.com/api/?username={sms_username}&password={sms_password}&message={message}&' \
              f'sender={sender}&mobiles={phone_numbers}'
        send_sms = requests.post(url)
        return send_sms

    def numbers_counter(self, phone_numbers):
        splitter = phone_numbers.split(',')
        return len(splitter)


def title_adder(new):
    #     new['date_of_birth'] = pd.to_datetime(new['date_of_birth'], infer_datetime_format=True)
    new["gender"] = new["gender"]
    new["marital_status"] = new["marital_status"]
    if new.gender.lower() == 'male' and age(new.date_of_birth) >= 70:
        return 'Pa'
    elif new.gender.lower() == 'female' and age(new.date_of_birth) >= 70:
        return 'Ma'
    elif new.gender.lower() == 'female' and age(new.date_of_birth) >= 40 and new.marital_status == 'single':
        return 'Ms'
    elif new.gender.lower() == 'male' and age(new.date_of_birth) >= 40 and new.marital_status == 'single':
        return 'Mr'
    elif new.gender.lower() == 'female' and new.marital_status == 'married':
        return 'Mrs'
    elif new.gender.lower() == 'female' and new.marital_status == 'single':
        return 'Miss'
    elif new.gender.lower() == 'male' and new.marital_status == 'married':
        return 'Mr'
    elif new.gender.lower() == 'male' and new.marital_status == 'single':
        return 'Bro'

    else:
        pass


class Data:

    def __init__(self):
        self.engine = os.environ.get('sql')
        self.df = pd.read_sql('select * from Members', con=self.engine)
        self.df['wedding_date'] = pd.to_datetime(self.df['wedding_date'], errors='coerce')
        # self.df = pd.read_csv('/Users/akinbodebams/PycharmProjects/arabs/new.csv')
        self.df['gender'] = self.df["gender"].str.strip()
        self.df['age'] = self.df['date_of_birth'].apply(age)
        self.df['wedding_age'] = self.df['wedding_date'].apply(age)
        self.df["gender"] = self.df["gender"].str.lower()
        self.df["marital_status"] = self.df["marital_status"].str.lower()
        self.df['title'] = self.df.apply(title_adder, axis=1)
        self.df['month_and_day'] = self.df['date_of_birth'].apply(month_day)
        self.df['wed_month_day'] = self.df['wedding_date'].apply(wed_month_day)
        self.df['month'] = self.df['date_of_birth'].apply(month)
        self.df['wedding_date'] = pd.to_datetime(self.df['wedding_date'], errors='coerce')

    def month_birthday(self):
        today = datetime.datetime.today().date()
        month = today.month
        day = today.day
        celebrant_number = self.df[self.df.month == month].phone_number
        return celebrant_number

    def today_birthday(self):
        lst = []
        celebrants_info = {}
        # today = datetime.datetime.today().date()
        today = datetime.datetime(2020, 2, 1)
        month = today.month
        day = today.day
        celebrant_number = self.df[self.df.month_and_day == (month, day)].phone_number
        celebrant_name = self.df[self.df.month_and_day == (month, day)].first_name
        celebrant_title = self.df[self.df.month_and_day == (month, day)].title
        name = celebrant_title + " " + celebrant_name.str.title()
        new = zip(name, celebrant_number)
        return list(new)

    def today_wedding(self):
        lst = []
        celebrants_info = {}
        today = datetime.datetime.today().date()
        # today = datetime.datetime(2020, 2, 21)
        month = today.month
        day = today.day
        celebrant_number = self.df[self.df.wed_month_day == (month, day)].phone_number
        celebrant_name = self.df[self.df.wed_month_day == (month, day)].first_name
        celebrant_title = self.df[self.df.wed_month_day == (month, day)].title
        celebrant_year = self.df[self.df.wed_month_day == (month, day)].wedding_age

        name = celebrant_title + " " + celebrant_name.str.title()
        new = zip(name, celebrant_number, celebrant_year)
        return list(new)

    def b_day_checker(self):
        if len(self.today_birthday()) > 0:
            return True
        else:
            return False

    def wedding_checker(self):
        if len(self.today_wedding()) > 0:
            return True
        else:
            return False

    def b_day_message_picker(self, member):
        message_picked = random.choice(list(messages['b_day_msg']))
        hash_replace = message_picked.replace('###', member)
        return hash_replace

    def wed_message_picker(self, age):
        message_picked = random.choice(list(messages['wed_msg']))
        hash_replace = message_picked.replace('###', str(age))
        return hash_replace

    def messaging(self):
        if self.b_day_checker():
            message_details = {'names': [],
                               'messages': [],
                               'wed_names': []}
            sms = Sms()
            sender_name = 'Araba B.C'
            for i in self.today_birthday():
                phone_numbers = i[1]
                name = i[0]

                message = self.b_day_message_picker(name)
                message_details['names'].append(name)
                message_details['messages'].append(message)

                sms.sms_sender(sender=sender_name, phone_numbers=phone_numbers, message=message)
            messagess = f"bday message was sent to {message_details['names']}"
            subject= 'bday sent'
            send_email(messagess,subject)



        else:
            messagess = 'No Birthday Sms was sent today'
            subject = 'no bday'

            send_email(messagess, subject)

        if self.wedding_checker():
            message_details = {'names': [],
                               'messages': [],
                               'wed_names': []}
            sms = Sms()
            sender_name = 'Araba B.C'
            for i in self.today_wedding():
                phone_numbers = i[1]
                name = i[0]
                age = i[2]
                message = self.wed_message_picker(age)
                message_details['wed_names'].append(name)
                message_details['messages'].append(message)
                sms.sms_sender(sender=sender_name, phone_numbers=phone_numbers, message=message)

            messagess = f"wedding message was sent to {message_details['wed_names']}"
            subject = 'wedding sent'
            send_email(messagess, subject)
        else:
            messagess = "No Wedding Sms was sent today"
            subject = 'wedding not sent'
            send_email(messagess, subject)

if __name__ == '__main__':
    Data().messaging()
