![Windrecorder](https://github.com/Antonoko/Windrecorder/blob/main/__assets__/product-header-cn.jpg)
<h1 align="center"> 🦝 Windrecorder | 捕風記錄儀</h1>
<p align="center"> Windows 上での Rewind の代替ツールで、メモリクーを取り戻すのに役立ちます。</p>

<p align="center"> <a href="https://github.com/Antonoko/Windrecorder/blob/main/__assets__/README-en.md">English</a>  | <a href="https://github.com/Antonoko/Windrecorder/blob/main/README.md">简体中文</a> | <a href="https://github.com/Antonoko/Windrecorder/blob/main/__assets__/README-ja.md">日本語</a> </p>

---
> Rewind App は何ですか？: https://www.rewind.ai/

これは、画面のキャプチャを継続的に記録し、キーワード検索などを使用して関連するメモリをいつでも取り戻すためのツールです。

**すべての機能（録画、認識処理、バックトレースの保存など）は完全にローカルで実行され、インターネットに接続する必要はありません。データはアップロードされず、必要なことだけが行われます。**

![Windrecorder](https://github.com/Antonoko/Windrecorder/blob/main/__assets__/product-preview-cn.jpg)


# 🦝 インストール

- [ffmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) をダウンロードし、その中の bin ディレクトリから ffmpeg.exe を `C:\Windows\System32`（または PATH にある他のディレクトリ）に解凍します。

- [Git](https://git-scm.com/downloads)、[Python](https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe)（インストール時に Add python.exe to PATH を選択）、[Pip](https://pip.pypa.io/en/stable/installation/) をインストールします。

- このツールをインストールしたいディレクトリに移動します（容量のあるパーティションに配置することをお勧めします）。ターミナルで `git clone https://github.com/Antonoko/Windrecorder` コマンドを実行して、ツールをダウンロードします。

    - インストールしたいフォルダを開き、パスバーに `cmd` と入力し、Enter キーを押して現在のディレクトリのターミナルに移動し、上記のコマンドを貼り付けて実行します。

- ディレクトリ内の `install_update_setting.bat` を開き、ツールのインストールと設定を行います。成功すれば、使用を開始できます。


# 🦝 使い方

- ディレクトリ内の `start_record.bat` を実行して画面の記録を開始します。

> 注意: 記録するためには、ターミナルウィンドウを最小化してバックグラウンドで実行する必要があります。同様に、記録を一時停止する場合は、ターミナルウィンドウを閉じるだけです。

- ディレクトリ内の `start_webui.bat` を実行して、メモリのトレース、検索、設定を行います。

> ベストプラクティス: webui で `start_record.bat` を自動起動に設定しておくと、すべてを自動的に記録できます。コンピュータがアイドル状態で誰も使用していない場合、`start_record.bat` は自動的に記録を一時停止し、古いビデオを圧縮・クリーンアップします。設定して忘れるだけです！

---
### ロードマップ:
- [x] 小さなファイルサイズで安定した画面の録画
- [x] 変更のあった画面のみを認識し、インデックスをデータベースに保存
- [x] グラフィカルなユーザーインターフェース（webui）
- [x] ワードクラウド、タイムライン、ライトボックス、スキャッタープロットによるデータの要約
- [x] セグメントの録画後に自動的に認識し、アイドル時にビデオをメンテナンス、クリーンアップ、圧縮する
- [x] 多言語サポート：i18n サポートによるインターフェースと OCR 認識の完了。
- [ ] プロセスの最適化とパフォーマンスの向上
- [ ] データベースの暗号化機能の追加
- [ ] フォアグラウンドプロセス名と OCR 単語の位置の記録を検索時に線索として表示
- [ ] マルチスクリーンの記録サポートの追加（pyautogui の将来の機能追加に依存）
- [ ] 画面モーダルの認識の追加により、画面の内容の記述を検索できるようにする
- [ ] 単語埋め込みインデックス、ローカル LLM クエリの追加
- [ ] 🤔


# 🧡
Powered by these amazing projects:

- [https://github.com/DayBreak-u/chineseocr_lite](https://github.com/DayBreak-u/chineseocr_lite)

- [https://github.com/zh-h/Windows.Media.Ocr.Cli](https://github.com/zh-h/Windows.Media.Ocr.Cli)


---

🧡 このツールが気に入ったら、[長瀬有花](https://www.youtube.com/channel/UCf-PcSHzYAtfcoiBr5C9DZA) のだつりょくよい音楽をYouTubeやストリーミング音楽プラットフォームでお楽しみください。ありがとうございます！

> "Your tools suck, check out my girl Yuka Nagase, she's amazing, I code 10 times faster when listening to her." -- @jpswing
