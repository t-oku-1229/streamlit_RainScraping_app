from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import os
 
class RainDataExtractor:


    def __init__(self, ID, start_year, end_year):
        self.ID = int(ID)
        self.start_year = int(start_year)
        self.end_year = int(end_year)
 
 
    def singleyear(self):
        date_arr, hourly_rain = [], []
 
        for year in range(self.start_year, self.end_year + 1):
            start_datetime = datetime(year, 1, 1, 1, 0)
            end_datetime = datetime(year, 12, 31, 23, 59)
            current_datetime = start_datetime
 
            for imonth in range(1, 13):
                if imonth < 10:
                    month = '0' + str(imonth)
                else:
                    month = str(imonth)
 
                url = f'http://www1.river.go.jp/cgi-bin/DspRainData.exe?KIND=2&ID={self.ID}&BGNDATE={year}{month}01&ENDDATE=20231231&KAWABOU=NO'
 
                res = requests.get(url)
 
                soup = BeautifulSoup(res.content, "html.parser", from_encoding='shift_jis')
                _discharge = soup.find_all('td')
 
                for i in range(9, len(_discharge) - 1):
                    discharge = _discharge[i].get_text()
                    hourly_rain.append(discharge)
                    date_arr.append(current_datetime.strftime('%Y-%m-%d %H:%M'))
                    current_datetime += timedelta(hours=1)
 
        # データフレームの作成
        data = {"日付": date_arr, "雨量": hourly_rain}
        df = pd.DataFrame(data)
 
        return df
 
 
    def multiyear(self):
        date_arr, hourly_rain = [], []
 
        for year in range(self.start_year, self.end_year + 1):
            start_datetime = datetime(year, 1, 1, 1, 0)
            end_datetime = datetime(year, 12, 31, 23, 59)
            current_datetime = start_datetime
 
            # filename = f'{point_name}_{year}.csv'
            # f = open(filename, 'w', encoding='shift_jis')
 
            for imonth in range(1, 13):
                if imonth < 10:
                    month = '0' + str(imonth)
                else:
                    month = str(imonth)
 
                url = f'http://www1.river.go.jp/cgi-bin/DspRainData.exe?KIND=2&ID={self.ID}&BGNDATE={year}{month}01&ENDDATE={year}{month}31&KAWABOU=NO'
 
                res = requests.get(url)
 
                soup = BeautifulSoup(res.content, "html.parser", from_encoding='shift_jis')
                _discharge = soup.find_all('td')
 
                for i in range(9, len(_discharge) - 1):
                    discharge = _discharge[i].get_text()
                    hourly_rain.append(discharge)
                    date_arr.append(current_datetime.strftime('%Y-%m-%d %H:%M'))
                    current_datetime += timedelta(hours=1)
 
        # データフレームの作成
        data = {"日付": date_arr, "雨量": hourly_rain}
        df = pd.DataFrame(data)
 
        return df.to_csv(index=False).encode('shift_jis')
 
 
def main():
    # タイトルと説明
    st.title('水文水質DB 雨量取得Webアプリ')
    st.text('水文水質データベースの雨量取得を行うためのWebアプリケーションを作成してみました。\n雨量情報を取得する機会があればぜひお使いください。')
 
    st.markdown("""
    ### 本アプリについて
    水文水質DBの雨量値を年単位で取得できるWebアプリです。
 
    ### 取得手順
    1. 単年で取得するか、複数年を一括で取得するか選択してください。複数年の場合はcsvファイルのダウンロードになります。
    2. 取得したい"観測所記号"を調べます。[例）厳木ダム](http://www1.river.go.jp/cgi-bin/SiteInfo.exe?ID=109021289922040)
    3. 取得したい年数を入力します。予め取得できる年数を確認しておくことをお勧めします。
    """)
 
    # ラジオボタンで単年と複数年を選択
    data_type = st.radio("データの種類を選択", ["単年", "複数年"])
 
    if data_type == "単年":

        ID_single = st.text_input('観測所のコード：例）109021289922040  ※厳木ダムの場合')
        start_year_single = st.text_input('取得年：例）2020')
        end_year_single = start_year_single
        submit_btn_single = st.button('結果表示')
        if submit_btn_single:
            extractor_single = RainDataExtractor(ID_single, start_year_single, end_year_single)
            df_single = extractor_single.singleyear()
            st.dataframe(df_single)
 
    elif data_type == "複数年":
 
        ID_multi = st.text_input('観測所のコード：例）109021289922040  ※厳木ダムの場合')
        start_year_multi = st.text_input('開始年：例）2020')
        end_year_multi = st.text_input('終了年：例）2022')
 
        submit_btn_multi = st.button('取得開始')
        if submit_btn_multi:
            extractor_multi = RainDataExtractor(ID_multi, start_year_multi, end_year_multi)
            st.text('csvデータを作成中です...')
            csvdata = extractor_multi.multiyear()
            st.text('csvデータの作成が完了しました')
            st.download_button(
               "CSVダウンロード",
               csvdata,
               "result.csv",
               "text/csv",
               key='download-csv'
            ) 
 
if __name__ == '__main__':
    main()
