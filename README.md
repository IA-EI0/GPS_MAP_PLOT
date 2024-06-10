GPS MAP PLOT
====
令和5年度に制作した、指定の範囲内にある3台のRaspberryPiの位置をウェブサイトに表示させるプログラムです。「RaspberryPiとGNSS (Global Navigation Satellite System) 受信機を使って簡単なゲームシステムを開発する」という事を目的に制作しました。

サイトリンク : [こちらから](http://iaei0.starfree.jp/GPS-SPY/MAP_GitHub.php)

## Description
任意の範囲のマップに存在する3台のRaspberryPiからサーバーへ定期的にGNSS受信機で受信した位置情報のデータを送り、そのデータを管理者のパソコンで起動させているPythonで書かれたプログラムが読み込み、位置情報、速度、方向を記入したマップ画像を同サーバーへアップロードしサイトで表示させるものです。有料のレンタルサーバーではなく無料のレンタルサーバーで行ったため、Pythonをサーバー内で動かすことが出来ず、この方法をとる事とした。

<img width="50%" src="https://github.com/IA-EI0/GPS_MAP_PLOT/assets/86182861/3e092e42-801e-4f9b-b8c5-06bd26b4013d"></img>

①RaspberryPiがGNSS受信機から取得した位置情報をJSONファイルとしてサーバーにアップロードする。

②管理者のパソコンで起動させているPythonで書かれたプログラムがJSONファイルを読み込み、位置情報、速度、方向を記入したマップ画像を生成する。

③生成されたマップ画像を同サーバーへアップロードする。

④マップ画像をウェブに表示させる。

## Equipment Used
Raspberry Pi 4 Model B 8GB

GPS受信機 (AE-GNSS-EXTANT+ANT_SET)

## Licence
[Apache-2.0 license](https://github.com/IA-EI0/GPS_MAP_PLOT/blob/main/LICENSE)
