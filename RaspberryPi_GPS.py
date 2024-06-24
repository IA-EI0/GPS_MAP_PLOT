#!/usr/bin/env python3
# プログラムは1号機の例 #
import time
import datetime
import serial
from micropyGPS import MicropyGPS
import codecs
import json
import ftplib


def main():
    # シリアル通信設定
    uart = serial.Serial('/dev/ttyS0', 9600, timeout=10)
    # gps設定
    my_gps = MicropyGPS(9, 'dd')

    tm_last = 0
    while True:
        sentence = uart.readline()
        if len(sentence) > 0:
            for x in sentence:
                if 10 <= x <= 126:
                    stat = my_gps.update(chr(x))
                    if stat:
                        now = datetime.datetime.now()
                        tm = my_gps.timestamp
                        tm_now = (tm[0] * 3600) + (tm[1] * 60) + int(tm[2])
                        s_lat = str(my_gps.latitude[0])
                        s_lon = str(my_gps.longitude[0])
                        a, lat_n = s_lat.split('.')
                        a, lon_n = s_lon.split('.')
                        if 20 <= my_gps.latitude[0] <= 45 and 120 <= my_gps.longitude[0] <= 150 and len(lat_n) >= 10 and len(lon_n) >= 10:
                            time_txt = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(tm[0]) + ":" + str(tm[1]) + ":" + str(tm[2])
                            gps_rp1_txt = {"Lat": my_gps.latitude[0], "Lon": my_gps.longitude[0], "Time": time_txt}
                            gps_locate_txt = f"{my_gps.latitude[0]},{my_gps.longitude[0]}"
                            if (tm_now - tm_last) >= 3:
                                tm_last = (tm[0] * 3600) + (tm[1] * 60) + int(tm[2])
                                with codecs.open('./GPS_RP1.json', 'w', 'utf-8') as f:
                                    json.dump(gps_rp1_txt, f, ensure_ascii=False, indent=3) # 号機によって変更
                                f.close()
                                """
                                with open('./Locate_Data.txt', 'a') as f:
                                    print(gps_locate_txt, file=f)
                                f.close()
                                """
                                # サーバー送信
                                host = ****
                                username = ****
                                password = ****
                                port = 21
                                timeout = 50
                                try:
                                    with ftplib.FTP() as ftp:
                                        ftp.connect(host=host, port=port, timeout=timeout)
                                        ftp.set_pasv(True)
                                        ftp.login(username, password)
                                        Gj1_path = "./GPS_RP1.json" # 号機によって変更
                                        # アップロード先
                                        Gj1_up_path = "STOR /GPS-SPY/json/GPS_RP1.json" # 号機によって変更
                                        # アップロード
                                        with open(Gj1_path, 'rb') as fp:
                                            ftp.storbinary(Gj1_up_path, fp)
                                        ftp.close()
                                except:
                                    print("No NetWork")


if __name__ == "__main__":
    main()
