# predict-keiba
競馬のG1レースの順位予測を行うモデル

過去のG1レースのデータを利用して順位予測を行います。出力はどの場淳の馬が何位になる確率が最も高いか、となります。
データはhttps://sports.yahoo.co.jp/keiba/schedule/monthly/ のサイトをスクレイピングして作成します。

予測を行うモデルがpredict_keiba.pyになります。

データをスクレイピングするプログラムがscraping_training_data.pyです。

予測するレースデータをスクレイピングするプログラムがscraping_race_data.pyです。

 （2022年10月5日変更：scraping_training_data.pyは動くようになりました。race_dataのほうは未対応）

作成したデータはkeiba_result{year}.csvとなります。（yearには年数が入ります）

予測するレースデータはrace_data.csvとなります。
