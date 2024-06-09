GPS_MAP_PLOT
====
令和5年度に制作した、指定の範囲内にある3台のRaspberryPiの位置をウェブサイトに表示させるプログラムです。

サイトリンク : [こちらから](http://iaei0.starfree.jp/KOSEN-Program/DashBoard_WEB_Access.php)

## Description
天気予報、授業変更・休講情報、占いの情報を取得するプログラム(Python)をレンタルサーバー上でCronを用いて定期実行させ、それぞれの情報をまとめたJsonファイルをサーバーの指定のファイルに配置し、サイトがJsonファイルを読み込むことでデータを表示しています。

<img width="50%" src="https://github.com/IA-EI0/DashBoard_Web/assets/86182861/bdebd634-cd9f-4c0c-8dbf-6139eafc8e14"></img>

①Pythonで書かれたプログラムがAPIにアクセスし、情報を取得する。

②APIで取得した情報を整理し、それをJSONファイルとして指定のディレクトリに出力する。

③JavaScriptで書かれたプログラムがJSONファイルを読み込み、ウェブサイトの指定の場所にデータと表示させるようにする。

## Equipment used

## Licence
[Apache-2.0 license](https://github.com/IA-EI0/GPS_MAP_PLOT/blob/main/LICENSE)
