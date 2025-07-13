# Gemini ROS

`gemini_ros`は、Google Gemini APIと連携して、ROS2上で大規模言語モデル（LLM）とのチャット機能を提供するパッケージです。画像や音声ファイルをLLMへの入力として使用することも可能です。

## インストール

1.  **依存関係のインストール**:
    ```bash
    sudo apt update
    pip3 install -q -U google-genai
    ```

2.  **ROS2パッケージのビルド**:
    ```bash
    cd colcon_ws/src
    git clone https://github.com/TeamSOBITS/gemini_ros.git
    cd ..
    colcon build --packages-select gemini_ros
    source install/setup.bash
    ```

## 使用方法

### 1. Geminiサーバーの起動
```bash
ros2 launch gemini_ros gemini_server.launch.py
```
Gemini APIキーを設定し、事前プロンプトファイルを指定して、Geminiサーバーを起動します。
  * `api_key`: Gemini APIキーを指定します。
  * `prompt_file`: 事前プロンプトを定義したYAMLファイルのパスを指定します。デフォルトは`base_prompt.yaml`です。

### 2. アクションクライアントからのリクエスト

`sobits_interfaces/action/ChatLlmRecognition`アクションを使用して、Geminiサーバーにリクエストを送信します。

| 項目         | フィールド名          | 型                     | 説明                                           |
| :----------- | :-------------------- | :--------------------- | :--------------------------------------------- |
| **アクション名** |                       |                        | `gemini_action`                                |
| **Goal** | `room_name`           | string                 | 会話履歴を管理するための任意の部屋の名前         |
|              | `request`             | string                 | ユーザーからのテキストメッセージ               |
|              | `image`               | sensor_msgs/Image[]    | 送信する画像メッセージのリスト                 |
|              | `sound_file_path`     | string[]               | 送信する音声ファイルのパスのリスト             |
|              | `model_name`          | string                 | 使用するGeminiモデルの名前 (例: "gemini-2.0-flash") |
|              | `is_stack`            | bool                   | 現在の会話を会話履歴にスタックするかどうか       |
| **Result** | `result`              | string                 | Geminiからの応答テキスト                       |
