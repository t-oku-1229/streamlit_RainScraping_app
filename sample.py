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
        self.date_arr = []
        self.hourly_rain = []


    def loadurl(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser", from_encoding='shift_jis')
        arr = soup.find_all('td')

        return arr


    def convertmonth(self, imonth):
        if imonth < 10:
            month = '0' + str(imonth)
        else:
            month = str(imonth)

        return month


    def createdf(self, header):
        data = {"日付": self.date_arr, str(header): self.hourly_rain}
        return pd.DataFrame(data)


    def rainsingleyear(self):
        for year in range(self.start_year, self.end_year + 1):
            start_datetime = datetime(year, 1, 1, 1, 0)
            end_datetime = datetime(year, 12, 31, 23, 59)
            current_datetime = start_datetime

            for imonth in range(1, 13):
                month = self.convertmonth(imonth)

                url = f'http://www1.river.go.jp/cgi-bin/DspRainData.exe?KIND=2&ID={self.ID}&BGNDATE={year}{month}01&ENDDATE={year}{month}31&KAWABOU=NO'
                _discharge = self.loadurl(url)

                for i in range(9, len(_discharge)):
                    discharge = _discharge[i].get_text()
                    if discharge=='黒字：確定値　青字：暫定値':
                        continue
                    self.hourly_rain.append(discharge)
                    self.date_arr.append(current_datetime.strftime('%Y-%m-%d %H:%M'))
                    current_datetime += timedelta(hours=1)

        # データフレームの作成
        return self.createdf('雨量')


    def rainmultiyear(self):
        for year in range(self.start_year, self.end_year + 1):
            start_datetime = datetime(year, 1, 1, 1, 0)
            end_datetime = datetime(year, 12, 31, 23, 59)
            current_datetime = start_datetime

            for imonth in range(1, 13):
                month = self.convertmonth(imonth)

                url = f'http://www1.river.go.jp/cgi-bin/DspRainData.exe?KIND=2&ID={self.ID}&BGNDATE={year}{month}01&ENDDATE={year}{month}31&KAWABOU=NO'
                _discharge = self.loadurl(url)

                for i in range(9, len(_discharge)):
                    discharge = _discharge[i].get_text()
                    if discharge=='黒字：確定値　青字：暫定値':
                        continue
                    self.hourly_rain.append(discharge)
                    self.date_arr.append(current_datetime.strftime('%Y-%m-%d %H:%M'))
                    current_datetime += timedelta(hours=1)

        # データフレームの作成
        return self.createdf('雨量').to_csv(index=False).encode('shift_jis')


    def wlsingleyear(self):
        for year in range(self.start_year, self.end_year + 1):
            start_datetime = datetime(year, 1, 1, 1, 0)
            end_datetime = datetime(year, 12, 31, 23, 59)
            current_datetime = start_datetime

            for imonth in range(1, 13):
                month = self.convertmonth(imonth)

                # 荒瀬 309061289901060
                url = f'http://www1.river.go.jp/cgi-bin/DspWaterData.exe?KIND=2&ID={self.ID}&BGNDATE={year}{month}01&ENDDATE={year}{month}31&KAWABOU=NO'
                _discharge = self.loadurl(url)

                for i in range(9, len(_discharge)):
                    discharge = _discharge[i].get_text()
                    if discharge=='黒字：確定値　青字：暫定値':
                        continue
                    self.hourly_rain.append(discharge)
                    self.date_arr.append(current_datetime.strftime('%Y-%m-%d %H:%M'))
                    current_datetime += timedelta(hours=1)

        # データフレームの作成
        return self.createdf('水位')


    def wlmultiyear(self):
        for year in range(self.start_year, self.end_year + 1):
            start_datetime = datetime(year, 1, 1, 1, 0)
            end_datetime = datetime(year, 12, 31, 23, 59)
            current_datetime = start_datetime

            for imonth in range(1, 13):
                month = self.convertmonth(imonth)

                url = f'http://www1.river.go.jp/cgi-bin/DspWaterData.exe?KIND=2&ID={self.ID}&BGNDATE={year}{month}01&ENDDATE={year}{month}31&KAWABOU=NO'
                _discharge = self.loadurl(url)

                for i in range(9, len(_discharge)):
                    discharge = _discharge[i].get_text()
                    if discharge=='黒字：確定値　青字：暫定値':
                        continue
                    self.hourly_rain.append(discharge)
                    self.date_arr.append(current_datetime.strftime('%Y-%m-%d %H:%M'))
                    current_datetime += timedelta(hours=1)

        # データフレームの作成
        return self.createdf('水位').to_csv(index=False).encode('shift_jis')


    def dischargesingleyear(self):
        for year in range(self.start_year, self.end_year + 1):
            start_datetime = datetime(year, 1, 1, 1, 0)
            end_datetime = datetime(year, 12, 31, 23, 59)
            current_datetime = start_datetime

            for imonth in range(1, 13):
                month = self.convertmonth(imonth)

                # 日の出橋 309011289902050
                url = f'http://www1.river.go.jp/cgi-bin/DspWaterData.exe?KIND=6&ID={self.ID}&BGNDATE={year}{month}01&ENDDATE={year}{month}31&KAWABOU=NO'
                _discharge = self.loadurl(url)

                for i in range(9, len(_discharge)):
                    discharge = _discharge[i].get_text()
                    if discharge=='黒字：確定値　青字：暫定値':
                        continue
                    self.hourly_rain.append(discharge)
                    self.date_arr.append(current_datetime.strftime('%Y-%m-%d %H:%M'))
                    current_datetime += timedelta(hours=1)

        # データフレームの作成
        return self.createdf('流量')


    def dischargemultiyear(self):
        for year in range(self.start_year, self.end_year + 1):
            start_datetime = datetime(year, 1, 1, 1, 0)
            end_datetime = datetime(year, 12, 31, 23, 59)
            current_datetime = start_datetime

            for imonth in range(1, 13):
                month = self.convertmonth(imonth)

                url = f'http://www1.river.go.jp/cgi-bin/DspWaterData.exe?KIND=6&ID={self.ID}&BGNDATE={year}{month}01&ENDDATE={year}{month}31&KAWABOU=NO'
                _discharge = self.loadurl(url)

                for i in range(9, len(_discharge)):
                    discharge = _discharge[i].get_text()
                    if discharge=='黒字：確定値　青字：暫定値':
                        continue
                    self.hourly_rain.append(discharge)
                    self.date_arr.append(current_datetime.strftime('%Y-%m-%d %H:%M'))
                    current_datetime += timedelta(hours=1)

        # データフレームの作成
        return self.createdf('流量').to_csv(index=False).encode('shift_jis')


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

    # プルダウンでデータの種類を選択
    data_type = st.selectbox("データの種類を選択", ["雨量", "流量", "水位"])

    # ラジオボタンで単年と複数年を選択
    year_type = st.radio("データの種類を選択", ["単年", "複数年"])


    if data_type == "雨量" and year_type == "単年":
        ID_single = st.text_input('観測所のコード：例）厳木ダム 109021289922040')
        start_year_single = st.text_input('取得年')
        end_year_single = start_year_single
        submit_btn_single = st.button('結果表示')
        if submit_btn_single:
            extractor_single = RainDataExtractor(ID_single, start_year_single, end_year_single)
            # df_single = extractor_single.rainsingleyear()
            df_single = extractor_single.dischargesingleyear()
            st.dataframe(df_single)


    elif data_type == "雨量" and year_type == "複数年":
        ID_multi = st.text_input('観測所のコード：例）厳木ダム 109021289922040')
        start_year_multi = st.text_input('開始年')
        end_year_multi = st.text_input('終了年')
        submit_btn_multi = st.button('取得開始')
        if submit_btn_multi:
            extractor_multi = RainDataExtractor(ID_multi, start_year_multi, end_year_multi)
            text_placeholder = st.text('csvデータを作成中です...')
            csvdata = extractor_multi.rainmultiyear()
            new_text = 'csvデータの作成が完了しました'
            text_placeholder.text(new_text)
            st.download_button(
               "CSVダウンロード",
               csvdata,
               "result.csv",
               "text/csv",
               key='download-csv'
            )


    elif data_type == "水位" and year_type == "単年":
        ID_single = st.text_input('観測所のコード：例）荒瀬 309061289901060')
        start_year_single = st.text_input('取得年')
        end_year_single = start_year_single
        submit_btn_single = st.button('結果表示')
        if submit_btn_single:
            extractor_single = RainDataExtractor(ID_single, start_year_single, end_year_single)
            # df_single = extractor_single.rainsingleyear()
            df_single = extractor_single.wlsingleyear()
            st.dataframe(df_single)


    elif data_type == "水位" and year_type == "複数年":
        ID_multi = st.text_input('観測所のコード：例）荒瀬 309061289901060')
        start_year_multi = st.text_input('開始年')
        end_year_multi = st.text_input('終了年')
        submit_btn_multi = st.button('取得開始')
        if submit_btn_multi:
            extractor_multi = RainDataExtractor(ID_multi, start_year_multi, end_year_multi)
            text_placeholder = st.text('csvデータを作成中です...')
            csvdata = extractor_multi.wlmultiyear()
            new_text = 'csvデータの作成が完了しました'
            text_placeholder.text(new_text)
            st.download_button(
               "CSVダウンロード",
               csvdata,
               "result.csv",
               "text/csv",
               key='download-csv'
            )


    elif data_type == "流量" and year_type == "単年":
        ID_single = st.text_input('観測所のコード：例）日の出橋 309011289902050')
        start_year_single = st.text_input('取得年')
        end_year_single = start_year_single
        submit_btn_single = st.button('結果表示')
        if submit_btn_single:
            extractor_single = RainDataExtractor(ID_single, start_year_single, end_year_single)
            # df_single = extractor_single.rainsingleyear()
            df_single = extractor_single.dischargesingleyear()
            st.dataframe(df_single)


    elif data_type == "流量" and year_type == "複数年":
        ID_multi = st.text_input('観測所のコード：例）日の出橋 309011289902050')
        start_year_multi = st.text_input('開始年')
        end_year_multi = st.text_input('終了年')
        submit_btn_multi = st.button('取得開始')
        if submit_btn_multi:
            extractor_multi = RainDataExtractor(ID_multi, start_year_multi, end_year_multi)
            text_placeholder = st.text('csvデータを作成中です...')
            csvdata = extractor_multi.dischargemultiyear()
            new_text = 'csvデータの作成が完了しました'
            text_placeholder.text(new_text)
            st.download_button(
               "CSVダウンロード",
               csvdata,
               "result.csv",
               "text/csv",
               key='download-csv'
            )


if __name__ == '__main__':
    main()
