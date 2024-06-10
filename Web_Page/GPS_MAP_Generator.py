import requests
import threading
import datetime
import time
import ftplib
import json
import codecs
from PIL import Image, ImageDraw, ImageFont
from math import log, pi, cos, tan
from staticmap import StaticMap


# 緯度経度ピクセル変換
def lon_to_pixel(lon, m):
    # 経度からタイル番号
    if not (-180 <= lon <= 180):
        lon = (lon + 180) % 360 - 180
    x = ((lon + 180.) / 360) * pow(2, m.zoom)
    # タイル番号からキャンバスの座標
    pixel = (x - m.x_center) * m.tile_size + m.width / 2
    return round(pixel) - 25


def lat_to_pixel(lat, m):
    # 緯度からタイル番号
    if not (-90 <= lat <= 90):
        lat = (lat + 90) % 180 - 90
    y = (1 - log(tan(lat * pi / 180) + 1 / cos(lat * pi / 180)) / pi) / 2 * pow(2, m.zoom)
    # タイル番号からキャンバスの座標
    pixel = (y - m.y_center) * m.tile_size + m.height / 2
    return round(pixel) - 32


# スピード計算
def calculate_speed(lat1, lat2, lon1, lon2, time1, time2):
    from math import radians, sin, cos, sqrt, atan2
    # 緯度経度距離変換
    # 緯度経度をラジアンに変換
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    # 地球の半径（単位: メートル）
    radius = 6371.0 * 1000
    # 2点間の距離（単位: メートル）
    distance = radius * c
    # 時間計算
    # 時間の差を計算
    time_difference = time1 - time2
    # 差を秒単位に変換
    time_difference_in_seconds = time_difference.total_seconds()
    # スピード計算
    speed = distance / time_difference_in_seconds
    return round(speed, 1)


# 角度計算
def calculate_angle(xa, xb, ya, yb):
    from math import atan2, degrees
    # ベクトルの計算
    dx = xb - xa
    dy = yb - ya
    # atan2を使用して角度を計算
    angle_radians = atan2(dy, dx)
    # ラジアンを度数法に変換
    angle_degrees = degrees(angle_radians)
    return int(angle_degrees)


# 座標補正用関数(事前にマップを歩き、誤差が大きかったところを定数で補正する)
def plot_correct(lat, lon, x, y):
    # 第1補正エリア
    if 40.492719 <= lat <= 40.492994 and 141.448082 <= lon <= 141.448651:
        correct_plot_x = x + 20
        correct_plot_y = y - 0
    # 第2補正エリア
    elif 40.491758 <= lat <= 40.492177 and 141.447960 <= lon <= 141.448146:
        correct_plot_x = x + 0
        correct_plot_y = y + 10
    # 第3補正エリア
    elif 40.491623 <= lat <= 40.491757 and 141.447381 <= lon <= 141.447944:
        correct_plot_x = x + 20
        correct_plot_y = y + 0
    # 第4補正エリア
    elif 40.491091 <= lat <= 40.491482 and 141.445955 <= lon <= 141.446541:
        correct_plot_x = x - 15
        correct_plot_y = y + 0
    # 第5補正エリア
    elif 40.491428 <= lat <= 40.491559 and 141.448240 <= lon <= 141.448481:
        correct_plot_x = x + 15
        correct_plot_y = y + 0
    # 第6補正エリア
    elif 40.492009 <= lat <= 40.492284 and 141.449966 <= lon <= 141.450132:
        correct_plot_x = x + 0
        correct_plot_y = y + 15
    # 第7補正エリア
    elif 40.491998 <= lat <= 40.492689 and 141.449338 <= lon <= 141.449623:
        correct_plot_x = x + 0
        correct_plot_y = y + 10
    # 第8補正エリア
    elif 40.492684 <= lat <= 40.492982 and 141.449075 <= lon <= 141.449367:
        correct_plot_x = x + 0
        correct_plot_y = y + 30
    # 第9補正エリア
    elif 40.492948 <= lat <= 40.493082 and 141.448790 <= lon <= 141.449266:
        correct_plot_x = x + 15
        correct_plot_y = y + 0
    # 第10補正エリア
    elif 40.492132 <= lat <= 40.492777 and 141.448687 <= lon <= 141.448942:
        correct_plot_x = x + 0
        correct_plot_y = y + 40
    else:
        correct_plot_x = x
        correct_plot_y = y
    return correct_plot_x, correct_plot_y


# 地図生成
def map_gene(deg1, deg2, deg3, RP1_info_txt, RP2_info_txt, RP3_info_txt, RP1_Lost, RP2_Lost,
             RP3_Lost):
    print("地図生成開始")
    # グローバル宣言
    global now
    global map_gene_flag
    map_gene_flag = True

    # ピン設定
    RP1_pin = "./img/pin_rp1.png"
    RP2_pin = "./img/pin_rp2.png"
    RP3_pin = "./img/pin_rp3.png"
    Dead_pin = "./img/pin_dead.png"
    RP1_lost_pin = "./img/pin_rp1_lost.png"
    RP2_lost_pin = "./img/pin_rp2_lost.png"
    RP3_lost_pin = "./img/pin_rp3_lost.png"
    Dead_lost_pin = "./img/pin_dead_lost.png"

    # 地図用ピン
    RP1_map_pin = RP1_pin
    RP2_map_pin = RP2_pin
    RP3_map_pin = RP3_pin

    # 地図設定
    WIDTH, HEIGHT = 1000, 800
    PIN_IMAGE_SIZE1 = (60, 60)
    PIN_IMAGE_SIZE2 = (60, 60)
    PIN_IMAGE_SIZE3 = (60, 60)
    FONT_SIZE = 20
    FONT_SIZE2 = 25
    FONT = 'meiryo.ttc'
    COPYRIGHT_TEXT = '©国土地理院(簡易航空写真)'

    # エリア設定(八戸高専)
    MAP_CENTER = [141.448, 40.49165]

    # ステータスチェック(ピンの画像変更に用いる)
    status_url1 = "http://iaei0.starfree.jp/GPS-SPY/json/Status_RP1.json"
    response1 = requests.get(status_url1)
    s_data1 = response1.json()
    time.sleep(1)
    status_url2 = "http://iaei0.starfree.jp/GPS-SPY/json/Status_RP2.json"
    response2 = requests.get(status_url2)
    s_data2 = response2.json()
    time.sleep(1)
    status_url3 = "http://iaei0.starfree.jp/GPS-SPY/json/Status_RP3.json"
    response3 = requests.get(status_url3)
    s_data3 = response3.json()
    time.sleep(1)

    # ロストピン位置情報修正定数初期化
    lost1x = lost1y = lost2x = lost2y = lost3x = lost3y = 0

    # ピン決定
    # RP1
    if s_data1 == "Dead":
        if RP1_Lost:
            RP1_map_pin = Dead_lost_pin
            PIN_IMAGE_SIZE1 = (30, 30)
            deg1 = 0
            lost1x = 12
            lost1y = 12
        else:
            RP1_map_pin = Dead_pin
    else:
        if RP1_Lost:
            RP1_map_pin = RP1_lost_pin
            PIN_IMAGE_SIZE1 = (30, 30)
            deg1 = 0
            lost1x = 12
            lost1y = 12
    # RP2
    if s_data2 == "Dead":
        if RP2_Lost:
            RP2_map_pin = Dead_lost_pin
            PIN_IMAGE_SIZE2 = (30, 30)
            deg2 = 0
            lost2x = 12
            lost2y = 12
        else:
            RP2_map_pin = Dead_pin
    else:
        if RP2_Lost:
            RP2_map_pin = RP2_lost_pin
            PIN_IMAGE_SIZE2 = (30, 30)
            deg2 = 0
            lost2x = 12
            lost2y = 12
    # RP3
    if s_data3 == "Dead":
        if RP3_Lost:
            RP3_map_pin = Dead_lost_pin
            PIN_IMAGE_SIZE3 = (30, 30)
            deg3 = 0
            lost3x = 12
            lost3y = 12
        else:
            RP3_map_pin = Dead_pin
    else:
        if RP3_Lost:
            RP3_map_pin = RP3_lost_pin
            PIN_IMAGE_SIZE3 = (30, 30)
            deg3 = 0
            lost3x = 12
            lost3y = 12

    # 地図生成
    static_map = StaticMap(WIDTH, HEIGHT,
                           url_template='https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg')
    image = static_map.render(zoom=18, center=MAP_CENTER).convert('RGBA')

    # RP1
    pin_image1 = Image.open(RP1_map_pin).convert('RGBA').resize(PIN_IMAGE_SIZE1).rotate(deg1)
    time.sleep(0.3)
    img_clear1 = Image.new("RGBA", image.size, (255, 255, 255, 0))
    x1 = lat_to_pixel(RP1_lat, static_map)
    y1 = lon_to_pixel(RP1_lon, static_map)
    correct_x1, correct_y1 = plot_correct(RP1_lat, RP1_lon, x1, y1)
    img_clear1.paste(pin_image1, (correct_y1 + lost1y, correct_x1 + lost1x))
    image1 = Image.alpha_composite(image, img_clear1)

    # RP2
    pin_image2 = Image.open(RP2_map_pin).convert('RGBA').resize(PIN_IMAGE_SIZE2).rotate(deg2)
    time.sleep(0.3)
    img_clear2 = Image.new("RGBA", image1.size, (255, 255, 255, 0))
    x2 = lat_to_pixel(RP2_lat, static_map)
    y2 = lon_to_pixel(RP2_lon, static_map)
    correct_x2, correct_y2 = plot_correct(RP2_lat, RP2_lon, x2, y2)
    img_clear2.paste(pin_image2, (correct_y2 + lost2y, correct_x2 + lost2x))
    image2 = Image.alpha_composite(image1, img_clear2)

    # RP3
    pin_image3 = Image.open(RP3_map_pin).convert('RGBA').resize(PIN_IMAGE_SIZE3).rotate(deg3)
    time.sleep(0.3)
    img_clear3 = Image.new("RGBA", image2.size, (255, 255, 255, 0))
    x3 = lat_to_pixel(RP3_lat, static_map)
    y3 = lon_to_pixel(RP3_lon, static_map)
    correct_x3, correct_y3 = plot_correct(RP3_lat, RP3_lon, x3, y3)
    img_clear3.paste(pin_image3, (correct_y3 + lost3y, correct_x3 + lost3x))
    image3 = Image.alpha_composite(image2, img_clear3)

    # Drawオブジェクトの生成
    draw = ImageDraw.Draw(image3)

    # コピーライト描画
    font = ImageFont.truetype(FONT, FONT_SIZE)
    draw.multiline_text((WIDTH - 10, HEIGHT - 10), COPYRIGHT_TEXT, fill=(255, 255, 255), font=font, anchor='rs')

    # 速度情報、更新情報
    font2 = ImageFont.truetype(FONT, FONT_SIZE2)
    draw.multiline_text((20, HEIGHT - 95), RP1_info_txt, fill=(255, 255, 255), font=font2)
    draw.multiline_text((20, HEIGHT - 65), RP2_info_txt, fill=(255, 255, 255), font=font2)
    draw.multiline_text((20, HEIGHT - 35), RP3_info_txt, fill=(255, 255, 255), font=font2)

    # 出力
    image3.save(f'./GPS_Map/Location_Map.png')
    # 画像軽量化
    time.sleep(1)
    img = Image.open(f'./GPS_Map/Location_Map.png')
    img_p = img.convert('P')
    img_p.save(f'./GPS_Map/Location_Map.png')
    # サーバー送信
    host = ****
    username = ****
    password = ****
    port = 21
    timeout = 50
    with ftplib.FTP() as ftp:
        ftp.connect(host=host, port=port, timeout=timeout)
        ftp.set_pasv(True)
        ftp.login(username, password)
        # 位置情報のアップロード
        AM_path = "./GPS_Map/Location_Map.png"
        # アップロード先
        AM_up_path = "STOR /GPS-SPY/GPS_Map/c2058eca-f77f-4b63-bdf0-3962e5516ffa.png"
        # アップロード
        with open(AM_path, 'rb') as fp:
            ftp.storbinary(AM_up_path, fp)
        # 更新日時のアップロード
        AMj_path = "./json/Map_Admin.json"
        # アップロード先
        AMj_up_path = "STOR /GPS-SPY/json/Map_Admin.json"
        # アップロード
        with open(AMj_path, 'rb') as fp:
            ftp.storbinary(AMj_up_path, fp)
        ftp.close()
    time.sleep(1)
    print("サーバー送信")
    map_gene_flag = False


# 更新情報、時刻情報
time1_old = datetime.datetime.strptime("2023-1-1 0:0:0.0", '%Y-%m-%d %H:%M:%S.%f')
time1_new = datetime.datetime.strptime("2023-1-1 0:0:0.0", '%Y-%m-%d %H:%M:%S.%f')
lat1_old = lat1_new = 0
lon1_old = lon1_new = 0
time2_old = datetime.datetime.strptime("2023-1-1 0:0:0.0", '%Y-%m-%d %H:%M:%S.%f')
time2_new = datetime.datetime.strptime("2023-1-1 0:0:0.0", '%Y-%m-%d %H:%M:%S.%f')
lat2_old = lat2_new = 0
lon2_old = lon2_new = 0
time3_old = datetime.datetime.strptime("2023-1-1 0:0:0.0", '%Y-%m-%d %H:%M:%S.%f')
time3_new = datetime.datetime.strptime("2023-1-1 0:0:0.0", '%Y-%m-%d %H:%M:%S.%f')
lat3_old = lat3_new = 0
lon3_old = lon3_new = 0

# 速度情報、更新情報、方向情報
RP1_info_txt = "No Data"
RP2_info_txt = "No Data"
RP3_info_txt = "No Data"
deg1 = deg2 = deg3 = 0

# 現在時代入
update_admin_time = datetime.datetime.now()

# 地図生成中フラグ
map_gene_flag = False

# メインループ
while True:
    # データ取得不能時用ブール関数
    RP1_notget = False
    RP2_notget = False
    RP3_notget = False

    # GPS座標取得
    # RP1
    now_map1 = datetime.datetime.now()
    try:
        gps_url = "http://iaei0.starfree.jp/GPS-SPY/json/GPS_RP1.json"
        response_gps = requests.get(gps_url)
        gps_data = response_gps.json()
        RP1_lat = gps_data["Lat"]
        RP1_lon = gps_data["Lon"]
        RP1_dateTime = datetime.datetime.strptime(gps_data["Time"], '%Y-%m-%d %H:%M:%S.%f')
        time.sleep(1)
    except:
        RP1_lat = 0
        RP1_lon = 0
        RP1_dateTime = datetime.datetime.strptime("2023-1-1 0:0:0.0", '%Y-%m-%d %H:%M:%S.%f')
        RP1_notget = True
    # RP2
    now_map2 = datetime.datetime.now()
    try:
        gps_url = "http://iaei0.starfree.jp/GPS-SPY/json/GPS_RP2.json"
        response_gps = requests.get(gps_url)
        gps_data = response_gps.json()
        RP2_lat = gps_data["Lat"]
        RP2_lon = gps_data["Lon"]
        RP2_dateTime = datetime.datetime.strptime(gps_data["Time"], '%Y-%m-%d %H:%M:%S.%f')
        time.sleep(1)
    except:
        RP2_lat = 0
        RP2_lon = 0
        RP2_dateTime = datetime.datetime.strptime("2023-1-1 0:0:0.0", '%Y-%m-%d %H:%M:%S.%f')
        RP2_notget = True
    # RP3
    now_map3 = datetime.datetime.now()
    try:
        gps_url = "http://iaei0.starfree.jp/GPS-SPY/json/GPS_RP3.json"
        response_gps = requests.get(gps_url)
        gps_data = response_gps.json()
        RP3_lat = gps_data["Lat"]
        RP3_lon = gps_data["Lon"]
        RP3_dateTime = datetime.datetime.strptime(gps_data["Time"], '%Y-%m-%d %H:%M:%S.%f')
        time.sleep(1)
    except:
        RP3_lat = 0
        RP3_lon = 0
        RP3_dateTime = datetime.datetime.strptime("2023-1-1 0:0:0.0", '%Y-%m-%d %H:%M:%S.%f')
        RP3_notget = True

    # 更新情報
    # RP1
    if RP1_notget or (now_map1 - RP1_dateTime).total_seconds() >= 60:
        info_time1 = "LOST"
        RP1_Lost = True
    elif (now_map1 - RP1_dateTime).total_seconds() >= 20:
        info_time1 = f"{int((now_map1 - RP1_dateTime).total_seconds())}秒前に更新"
        RP1_Lost = True
    else:
        info_time1 = "リアルタイム"
        RP1_Lost = False
    # RP2
    if RP2_notget or (now_map2 - RP2_dateTime).total_seconds() >= 60:
        info_time2 = "LOST"
        RP2_Lost = True
    elif (now_map2 - RP2_dateTime).total_seconds() >= 20:
        info_time2 = f"{int((now_map2 - RP2_dateTime).total_seconds())}秒前に更新"
        RP2_Lost = True
    else:
        info_time2 = "リアルタイム"
        RP2_Lost = False
    # RP3
    if RP3_notget or (now_map3 - RP3_dateTime).total_seconds() >= 60:
        info_time3 = "LOST"
        RP3_Lost = True
    elif (now_map3 - RP3_dateTime).total_seconds() >= 20:
        info_time3 = f"{int((now_map3 - RP3_dateTime).total_seconds())}秒前に更新"
        RP3_Lost = True
    else:
        info_time3 = "リアルタイム"
        RP3_Lost = False
    # 速度情報、方向情報
    # RP1
    # データの最終更新時刻がtime1_newと違う場合、RP1_notgetがTrueの場合を除いて実行
    if time1_new != RP1_dateTime and not RP1_notget:
        time1_old = time1_new
        time1_new = RP1_dateTime
        lat1_old = lat1_new
        lat1_new = RP1_lat
        lon1_old = lon1_new
        lon1_new = RP1_lon
        # スピード計算(lat1_oldが0の場合を除き実行)
        if lat1_old != 0:
            speed1 = calculate_speed(lat1_new, lat1_old, lon1_new, lon1_old, time1_new, time1_old)
            info_speed1 = f"{speed1}[m/s]"
            deg1 = calculate_angle(lat1_new, lat1_old, lon1_new, lon1_old)
            print("Get 1")
        else:
            info_speed1 = "--[m/s]"
        RP1_info_txt = f"赤 : {info_time1},{info_speed1}"
    # RP2
    # データの最終更新時刻がtime2_newと違う場合とRP2_notgetがTrueの場合を除いて実行
    if time2_new != RP2_dateTime and not RP2_notget:
        time2_old = time2_new
        time2_new = RP2_dateTime
        lat2_old = lat2_new
        lat2_new = RP2_lat
        lon2_old = lon2_new
        lon2_new = RP2_lon
        # スピード計算(lat2_oldが0の場合を除き実行)
        if lat2_old != 0:
            speed2 = calculate_speed(lat2_new, lat2_old, lon2_new, lon2_old, time2_new, time2_old)
            info_speed2 = f"{speed2}[m/s]"
            deg2 = calculate_angle(lat2_new, lat2_old, lon2_new, lon2_old)
            print("Get 2")
        else:
            info_speed2 = "--[m/s]"
        RP2_info_txt = f"青 : {info_time2},{info_speed2}"
    # RP3
    # データの最終更新時刻がtime3_newと違う場合とRP3_notgetがTrueの場合を除いて実行
    if time3_new != RP3_dateTime and not RP3_notget:
        time3_old = time3_new
        time3_new = RP3_dateTime
        lat3_old = lat3_new
        lat3_new = RP3_lat
        lon3_old = lon3_new
        lon3_new = RP3_lon
        # スピード計算(lat3_oldが0の場合を除き実行)
        if lat3_old != 0:
            speed3 = calculate_speed(lat3_new, lat3_old, lon3_new, lon3_old, time3_new, time3_old)
            info_speed3 = f"{speed3}[m/s]"
            deg3 = calculate_angle(lat3_new, lat3_old, lon3_new, lon3_old)
            print("Get 3")
        else:
            info_speed3 = "--[m/s]"
        RP3_info_txt = f"黄 : {info_time3},{info_speed3}"
    # マップデータ更新
    now = datetime.datetime.now()
    if (now - update_admin_time).seconds >= 20 and not map_gene_flag:
        # 更新時刻データ
        map_admin_str = now.strftime("%H:%M.%S")
        map_admin_txt = {"LastUpdateTime": map_admin_str}
        with codecs.open('./json/Map_Admin.json', 'w', 'utf-8') as f:
            json.dump(map_admin_txt, f, ensure_ascii=False, indent=3)
            f.close()
        thread_map = threading.Thread(target=map_gene, args=(
            deg1, deg2, deg3, RP1_info_txt, RP2_info_txt, RP3_info_txt, RP1_Lost, RP2_Lost, RP3_Lost))
        thread_map.start()
        update_admin_time = now
    time.sleep(3)
