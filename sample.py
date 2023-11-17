from bs4 import BeautifulSoup
import urllib.request as req
import requests
import time
from selenium import webdriver
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

def geturl(url):
    try:
        res = requests.get(str(url), timeout=5)
    except Timeout:
        error_code = 1
        getres = -9999
    else:
        error_code = 0
        getres = res
    return getres, error_code

def check(url):
    # print('Start connect!!')
    res, error_code = geturl(str(url))
    i = 0
    while True:
        if error_code == 0:
            # print('Success connect!!')
            break
        else:
            time.sleep(2)
            i += 1
            print('Retry connect!! : ' + str(i) + 'time...' )
            res, error_code = geturl(str(url))

    return res

def print_datetime_range(year):
    start_datetime = datetime(year, 1, 1, 1, 0)
    end_datetime = datetime(year, 12, 31, 23, 59)

    current_datetime = start_datetime
    while current_datetime <= end_datetime:
        print(current_datetime.strftime('%Y-%m-%d %H:%M'))
        current_datetime += timedelta(hours=1)


def create_csv(point_name, ID, start_year, end_year):
    # point_name = point_name_entry.get()
    # ID = id_entry.get()
    # start_year = int(start_year_entry.get())
    # end_year = int(end_year_entry.get())

    point_name = str(point_name)
    ID = int(ID)
    start_year = int(start_year)
    end_year = int(end_year)

    for year in range(start_year, end_year + 1):
        date_arr, hourly_rain = [], []
        filename = f'{point_name}_{year}.csv'
        # f = open(filename, 'w', encoding='shift_jis')

        start_datetime = datetime(year, 1, 1, 1, 0)
        end_datetime = datetime(year, 12, 31, 23, 59)
        current_datetime = start_datetime

        for imonth in range(1, 13):
            if imonth < 10:
                month = '0' + str(imonth)
            else:
                month = str(imonth)

            url = f'http://www1.river.go.jp/cgi-bin/DspRainData.exe?KIND=2&ID={ID}&BGNDATE={year}{month}01&ENDDATE=20231231&KAWABOU=NO'

            res = check(url)
            soup = BeautifulSoup(res.content, "html.parser", from_encoding='shift_jis')
            _discharge = soup.find_all('td')

            for i in range(9, len(_discharge) - 1):
                discharge = _discharge[i].get_text()
                hourly_rain.append(discharge)
                date_arr.append(current_datetime.strftime('%Y-%m-%d %H:%M'))
                # print(current_datetime.strftime('%Y-%m-%d %H:%M'))
                current_datetime += timedelta(hours=1)

        # for i in range(len(hourly_rain)):
        #     f.write(str(date_arr[i]))
        #     f.write(',')
        #     f.write(str(hourly_rain[i]))
        #     f.write('\n')

        # データフレームの作成
        data = {"日付": date_arr, "雨量": hourly_rain}
        df = pd.DataFrame(data)

        # print(f'{year}_end')
        # f.close()
        time.sleep(2)

    # try:
    #     # 既存の create_csv の実装をここに配置

    #     # 以下は create_csv の実行が成功したと仮定したメッセージ
    #     messagebox.showinfo("Success", "Data scraping completed successfully!")

    # except Exception as e:
    #     # エラーが発生した場合のメッセージ
    #     messagebox.showerror("Error", f"An error occurred: {str(e)}")



def create_df(ID, start_year):

    ID = int(ID)
    start_year = int(start_year)

    for year in range(start_year, start_year + 1):
        date_arr, hourly_rain = [], []

        start_datetime = datetime(year, 1, 1, 1, 0)
        end_datetime = datetime(year, 12, 31, 23, 59)
        current_datetime = start_datetime

        for imonth in range(1, 13):
            if imonth < 10:
                month = '0' + str(imonth)
            else:
                month = str(imonth)

            url = f'http://www1.river.go.jp/cgi-bin/DspRainData.exe?KIND=2&ID={ID}&BGNDATE={year}{month}01&ENDDATE=20231231&KAWABOU=NO'

            res = check(url)
            soup = BeautifulSoup(res.content, "html.parser", from_encoding='shift_jis')
            _discharge = soup.find_all('td')

            for i in range(9, len(_discharge) - 1):
                discharge = _discharge[i].get_text()
                hourly_rain.append(discharge)
                date_arr.append(current_datetime.strftime('%Y-%m-%d %H:%M'))
                # print(current_datetime.strftime('%Y-%m-%d %H:%M'))
                current_datetime += timedelta(hours=1)

        # データフレームの作成
        data = {"日付": date_arr, "雨量": hourly_rain}
        df = pd.DataFrame(data)

        # print(f'{year}_end')
        # f.close()

    return df


# 109021289922040

st.title('水文水質データベース 雨量取得ツール')
st.caption('試作品です')
st.text('水文水質データベースの雨量取得を行うためのWebアプリケーションを作成してみました。')
st.text('※観測所記号はこちらのようなコードのことです↓↓')

image = './ID_image.png'
st.image(image, width=600)

with st.form(key='input'):    

    ID = st.text_input('観測所のコード：例）厳木ダム 109021289922040')
    start_year = st.text_input('取得年')

    submit_btn = st.form_submit_button('取得')
    if submit_btn:
        df = create_df(ID, start_year)
        st.dataframe(df)

