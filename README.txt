==== 概要 ====

jbovlaste の xml 辞書を OSX の 辞書.app やコンテキストメニューの「調べる」で使えるように変換する。

各項目は単語自体の他に rafsi （4文字も）や訳語で検索可能であり、元ファイルの note の内容も大体表示する。 keyword や glossword は検索キーにするだけで表示しないし、 user は無視。

特に対策してないけど、 rafsi と cmavo が被ったら cmavo が優先して表示されるようになってる気がする。

==== 使い方 ====

0. Dictionary Development Kit を持っていなければ本ファイル末尾の URL から Additional Tools for Xcode を入手
1. 本ファイル末尾の URL から最新版 xml をダウンロード
2. cd PATH/TO/THIS/FOLDER
3. make CONV_SRC_PATH=PATH/TO/XML DICT_BUILD_TOOL_DIR=PATH/TO/TOOL && make install
4. 辞書アプリの環境設定から辞書を有効化

※ ファイルパスは未指定の場合には以下を使う
PATH/TO/XML = "./日本語 - lojban.xml"
PATH/TO/TOOL = "/DevTools/Utilities/Dictionary Development Kit"

===== 注意事項等 =====

動作確認環境: macOS 11.1, python 2.7.16

このフォルダに
なお、このフォルダは既に2まで行った状態であり、フォルダ内の "日本語 - lojban.xml" （2021/01/10 現在で 1 に対応するファイル）を使用している。
xml が更新されていない、もしくは最新版でなくても構わない場合は 3 から行えばよい。

lxml がインストールされている場合はそちらを使用するため、パースでエラーが出た場合は入れたり消したりするとうまくいく可能性あり。


==== その他 ====

glossword は扱いがわかっていないので keyword と同じ扱いとした。

複数辞書（各言語とか）を作成して入れておきたい場合、 MyInfo.plist の CFBundleIdentifier を辞書ごとに変更しないと make install したときに辞書が上書きされるので注意。 CFBundleName も変更することを推奨する。


==== 参考 ====

* jbovlaste : http://jbovlaste.lojban.org/export/xml-export.html?lang=ja
* Dictionary Development Kit : https://developer.apple.com/download/more/
* 内蔵辞書の公式ドキュメント (かなり古い) : https://developer.apple.com/library/mac/documentation/UserExperience/Conceptual/DictionaryServicesProgGuide/Introduction/Introduction.html
