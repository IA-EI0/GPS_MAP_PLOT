<?php
  $g_jsonData = file_get_contents('./json/Game.json');
  $g_data = json_decode($g_jsonData, true);
  $game = $g_data['Game'];
  // GitHub用にプレイ中の画面を表示
  $game = "Start";
  if ($game == 'End') {
        ?>
        <!-- ゲーム開始前、または終了 -->
        <!DOCTYPE HTML PUBLIC>
        <html lang="ja">
          <head>
            <meta name=”robots” content=”noindex”>
            <meta http-equiv="Cache-Control" content="no-store">
            <meta http-equiv="refresh" content="10">
            <link rel="stylesheet" type="text/css" href="./style/css.css">
            <meta http-equiv="content-type" content="text/html; charset=utf-8">
            <meta http-equiv="Content-Script-Type" content="text/javascript">
            <title>管理者用GPSマップ</title>
          </head>
          <script src="./style/function_Admin.js"></script>
          <br>
          <body style="margin: 0; padding: 0; background: #191919; width:1100;  margin-right:auto; margin-left:auto;line-height:0px;">
            <center>
              <p style="color:white; font-size: 40px;">管理者用GPSマップ</p>
              <div style="padding: 10px; margin-bottom: 5px; border: 13px double #00bfff; border-radius: 13px;">
                <p>
                <a style="color:white; font-size: 25px">ゲーム開始前か、終了しています。
                </a>
              </p>
            </div>
            <p></p>
            <div style="padding: 10px; margin-bottom: 5px; border: 6px double #ffa07a; border-radius: 6px;">
              <a style="color:white; font-size:30px; margin-bottom: 0; line-height:1.5">位置情報最終更新時間
              </a>
              <br>
            <div class="boxSP">
              <div style="padding: 10px; margin-bottom: 10px; border: 3px solid #ffffff; width: auto; height:auto;">
                <a style="color:red; font-size:30px; margin-bottom: 0; line-height:1.3">赤(RP1)
                </a>
                <div>
                  <a style="font-size:32px; color:white; margin-bottom: 0; line-height:1.3">
                  <b id="red_gps">--</b>
                  </a>
                </div>
              </div>
            </div>
            <div class="boxSP">
              <div style="padding: 10px; margin-bottom: 10px; border: 3px solid #ffffff; width: auto; height:auto;">
                <a style="color:cyan; font-size:30px; margin-bottom: 0; line-height:1.3">青(RP2)
                </a>
                <div>
                  <a style="font-size:32px; color:white; margin-bottom: 0; line-height:1.3">
                  <b id="blue_gps">--</b>
                  </a>
                </div>
              </div>
            </div>
            <div class="boxSP">
              <div style="padding: 10px; margin-bottom: 10px; border: 3px solid #ffffff; width: auto; height:auto;">
                <a style="color:yellow; font-size:30px; margin-bottom: 0; line-height:1.3">黄(RP3)
                </a>
                <div>
                  <a style="font-size:32px; color:white; margin-bottom: 0; line-height:1.3">
                  <b id="yellow_gps">--</b>
                  </a>
                </div>
              </div>
            </div>
            </center>
          </body>
        </html>
<?php
    } else {
        $ua = $_SERVER['HTTP_USER_AGENT'];
        $browser = ((strpos($ua, 'iPhone') !== false) || (strpos($ua, 'iPod') !== false) || (strpos($ua, 'Android')) !== false);
            if ($browser == true) {
                $browser = 'sp';
            }
        if ($browser == 'sp') {
            ?>
        <!-- ゲーム中 -->
        <!DOCTYPE HTML PUBLIC>
        <html lang="ja">
          <head>
            <meta name=”robots” content=”noindex”>
            <meta http-equiv="Cache-Control" content="no-store">
            <meta http-equiv="refresh" content="10">
            <link rel="stylesheet" type="text/css" href="./style/css.css">
            <meta http-equiv="content-type" content="text/html; charset=utf-8">
            <meta http-equiv="Content-Script-Type" content="text/javascript">
            <title>GPSマップ</title>
          </head>
          <script src="./style/function_Admin.js"></script>
          <br>
          <body style="margin: 0; padding: 0; background: #191919; width:1100;  margin-right:auto; margin-left:auto;line-height:0px;">
            <center>
              <p style="color:white; font-size: 60px;">GPSマップ</p>
              <div style="padding: 10px; margin-bottom: 5px; border: 13px double #00bfff; border-radius: 13px;">
                <p>　</p>
                <p>
                <a style="color:white; font-size: 45px">最終更新 :
                </a>
                <a id="LastUpdate_A" style="color:white; font-size: 45px">--:--.--
                </a>
              </p>
              <p>　</p>
                <img src="./GPS_Map/For_GitHub.png?t=<?php echo time(); ?>" width="auto" id="Map"></img>
              </div>
              <p></p>
              <div style="padding: 10px; margin-bottom: 5px; border: 6px double #ffa07a; border-radius: 6px;">
                <a style="color:white; font-size:40px; margin-bottom: 0; line-height:1.5">位置情報最終更新時間
                </a>
                <br>
              <div class="boxSP">
                <div style="padding: 10px; margin-bottom: 10px; border: 3px solid #ffffff; width: auto; height:auto;">
                  <a style="color:red; font-size:30px; margin-bottom: 0; line-height:1.3">赤(RP1)
                  </a>
                  <div>
                    <a style="font-size:32px; color:white; margin-bottom: 0; line-height:1.3">
                    <b id="red_gps">--</b>
                    </a>
                  </div>
                </div>
              </div>
              <div class="boxSP">
                <div style="padding: 10px; margin-bottom: 10px; border: 3px solid #ffffff; width: auto; height:auto;">
                  <a style="color:cyan; font-size:30px; margin-bottom: 0; line-height:1.3">青(RP2)
                  </a>
                  <div>
                    <a style="font-size:32px; color:white; margin-bottom: 0; line-height:1.3">
                    <b id="blue_gps">--</b>
                    </a>
                  </div>
                </div>
              </div>
              <div class="boxSP">
                <div style="padding: 10px; margin-bottom: 10px; border: 3px solid #ffffff; width: auto; height:auto;">
                  <a style="color:yellow; font-size:30px; margin-bottom: 0; line-height:1.3">黄(RP3)
                  </a>
                  <div>
                    <a style="font-size:32px; color:white; margin-bottom: 0; line-height:1.3">
                    <b id="yellow_gps">--</b>
                    </a>
                  </div>
                </div>
              </div>
            </div>
            </center>
          </body>
        </html>
        <?php
            } else {
                ?>
                <!DOCTYPE HTML PUBLIC>
                <html lang="ja">
                  <head>
                    <meta name=”robots” content=”noindex”>
                    <meta http-equiv="Cache-Control" content="no-store">
                    <meta http-equiv="refresh" content="10">
                    <link rel="stylesheet" type="text/css" href="./style/css.css">
                    <meta http-equiv="content-type" content="text/html; charset=utf-8">
                    <meta http-equiv="Content-Script-Type" content="text/javascript">
                    <title>GPSマップ</title>
                  </head>
                  <script src="./style/function_Admin.js"></script>
                  <br>
                  <body style="margin: 0; padding: 0; background: #191919; width:1100;  margin-right:auto; margin-left:auto;line-height:0px;">
                    <center>
                      <p style="color:white; font-size: 40px;">GPSマップ</p>
                      <div style="padding: 10px; margin-bottom: 5px; border: 13px double #00bfff; border-radius: 13px;">
                        <p>
                        <a style="color:white; font-size: 25px">最終更新 :
                        </a>
                        <a id="LastUpdate_A" style="color:white; font-size: 25px">--:--.--
                        </a>
                      </p>
                        <br>
                        <img src="./GPS_Map/Location_Map(GitHub).png?t=<?php echo time(); ?>" height="85%" id="Map"></img>
                      </div>
                      <p></p>
                      <div style="padding: 10px; margin-bottom: 5px; border: 6px double #ffa07a; border-radius: 6px;">
                        <a style="color:white; font-size:30px; margin-bottom: 0; line-height:1.5">位置情報最終更新時間
                        </a>
                        <br>
                      <div class="boxSP">
                        <div style="padding: 10px; margin-bottom: 10px; border: 3px solid #ffffff; width: auto; height:auto;">
                          <a style="color:red; font-size:30px; margin-bottom: 0; line-height:1.3">赤(RP1)
                          </a>
                          <div>
                            <a style="font-size:32px; color:white; margin-bottom: 0; line-height:1.3">
                            <b id="red_gps">--</b>
                            </a>
                          </div>
                        </div>
                      </div>
                      <div class="boxSP">
                        <div style="padding: 10px; margin-bottom: 10px; border: 3px solid #ffffff; width: auto; height:auto;">
                          <a style="color:cyan; font-size:30px; margin-bottom: 0; line-height:1.3">青(RP2)
                          </a>
                          <div>
                            <a style="font-size:32px; color:white; margin-bottom: 0; line-height:1.3">
                            <b id="blue_gps">--</b>
                            </a>
                          </div>
                        </div>
                      </div>
                      <div class="boxSP">
                        <div style="padding: 10px; margin-bottom: 10px; border: 3px solid #ffffff; width: auto; height:auto;">
                          <a style="color:yellow; font-size:30px; margin-bottom: 0; line-height:1.3">黄(RP3)
                          </a>
                          <div>
                            <a style="font-size:32px; color:white; margin-bottom: 0; line-height:1.3">
                            <b id="yellow_gps">--</b>
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                    </center>
                  </body>
                </html>
<?php
    }
}
        ?>
