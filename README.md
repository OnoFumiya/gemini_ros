<a name="readme-top"></a>

[JA](README.md) | [EN](README_en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]


# Gemini ROS

## 概要

`gemini_ros`は、Google Gemini APIと連携して、ROS2上で大規模言語モデル（LLM）とのチャット機能を提供するパッケージです。画像や音声ファイルをLLMへの入力として使用することも可能です。

### 環境条件

まず，以下の環境を整えてから，次のインストール段階に進んでください．

| System  | Version |
| --- | --- |
| Ubuntu | 24.04 (Noble Numbat) |
| ROS    | Jazzy Jalisco |
| Python | 3.12 |

> [!NOTE]
> `Ubuntu`や`ROS`のインストール方法に関しては，[SOBITS Manual](https://github.com/TeamSOBITS/sobits_manual#%E9%96%8B%E7%99%BA%E7%92%B0%E5%A2%83%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)に参照してください．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


### インストール方法


1. ROSの`src`フォルダに移動します．
```sh
$ cd ~/colcon_ws/src/
```

2. 本レポジトリをcloneします．
```sh
$ git clone https://github.com/TeamSOBITS/gemini_ros
```

3. レポジトリの中へ移動します．
```sh
$ cd gemini_ros/
```

4. 依存パッケージをインストールします．
```sh
$ bash install.sh
```

5. パッケージをコンパイルします．
```sh
$ cd ~/colcon_ws/
$ colcon build --symlink-install
$ source ~/colcon_ws/install/setup.sh
```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


## 実行・操作方法

1. Gemini APIキーをターミナル上で設定します．
```sh
export GEMINI_API_KEY=************
```

> [!NOTE]
> Gemini APIキーを獲得するために，こちらのサイトを参照してください．
> https://ai.google.dev/gemini-api/docs/api-key

2. [genai_config.yaml](./config/genai_config.yaml)上でモデルの設定を用途に応じて更新してください．
```yaml
genai:
  temperature: 0.5    # Lower: less open-ended or creative, higher: more diverse or creative
  thinking_budget: 0  # 0 is DISABLED. -1 is AUTOMATIC
  response_mime_type: "application/json"  # `text/plain` or `application/json`
```

3. [任意] [genai_room.yaml](./config/genai_room.yaml)上で，文脈エンジニアリングのためのルームを記述してください．
```yaml
# 例：自チームに関する紹介のチャットボット
team_introduce:               # team_introduceという別の部屋も準備している
  - {user : "私達のチームはSOBITSという学生チームを組んでいます！"}  # imageを入れない場合＝LLM
  - {model: "SOBITSという学生チームを組んでいるのですね！素晴らしいですね！どういったチームなのですか？"}
  - {user : "学部生・修士・博士と幅広く在籍し，40人います！"}
  - {model: "40人ものメンバーがいる大規模な学生チームなのですね！\n幅広い層の方が在籍されているとのこと、多様な視点や知識が集まって素晴らしいチームになりそうですね。"}
```

4. Gemini ROSのアクションサーバを起動します．
```sh
ros2 launch gemini_ros gemini_server.launch.py
```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


### サーバーへのリクエストの送信

`sobits_interfaces/action/ChatLlmRecognition`というアクションを用いて、Geminiサーバにリクエストを送信します。

| 項目              | フィールド名          | 型                     | 説明                                                |
| :---------------- | :-------------------- | :--------------------- | :-------------------------------------------------- |
| **アクション名**  |                       |                        | `gemini_action`                                     |
| **Goal**          | `room_name`           | string                 | 会話履歴を管理するための任意のルームの名前          |
|                   | `request`             | string                 | ユーザーからのテキストメッセージ                    |
|                   | `image`               | sensor_msgs/Image[]    | 送信する画像メッセージのリスト                      |
|                   | `sound_file_path`     | string[]               | 送信する音声ファイルのパスのリスト                  |
|                   | `model_name`          | string                 | 使用するGeminiモデルの名前 (例: "gemini-2.0-flash") |
|                   | `is_stack`            | bool                   | 現在の会話を会話履歴にスタックするかどうか          |
| **Result**        | `result`              | string                 | Geminiからの応答テキスト                            |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TeamSOBITS/gemini_ros.svg?style=for-the-badge
[contributors-url]: https://github.com/TeamSOBITS/gemini_ros/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TeamSOBITS/gemini_ros.svg?style=for-the-badge
[forks-url]: https://github.com/TeamSOBITS/gemini_ros/network/members
[stars-shield]: https://img.shields.io/github/stars/TeamSOBITS/gemini_ros.svg?style=for-the-badge
[stars-url]: https://github.com/TeamSOBITS/gemini_ros/stargazers
[issues-shield]: https://img.shields.io/github/issues/TeamSOBITS/gemini_ros.svg?style=for-the-badge
[issues-url]: https://github.com/TeamSOBITS/gemini_ros/issues
[license-shield]: https://img.shields.io/github/license/TeamSOBITS/gemini_ros.svg?style=for-the-badge
[license-url]: LICENSE
