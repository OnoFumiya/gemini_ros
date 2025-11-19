<a name="readme-top"></a>

[JA](README.md) | [EN](README_en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]


# Gemini ROS

## Introduction

`gemini_ros` is a package that integrates with the Google Gemini API to provide chat functionality with Large Language Models (LLM) on ROS2. It is also possible to use image and audio files as input for the model.


## Getting Started

This section describes how to set up this repository.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Prerequisites

First, please prepare the following environment before proceeding to the next installation stage.

| System  | Version |
| --- | --- |
| Ubuntu | 24.04 (Noble Numbat) |
| ROS    | Jazzy Jalisco |
| Python | 3.12 |

> [!NOTE]
> For instructions on how to install `Ubuntu` or `ROS`, please refer to the [SOBITS Manual](https://github.com/TeamSOBITS/sobits_manual#%E9%96%8B%E7%99%BA%E7%92%B0%E5%A2%83%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6).

<p align="right">(<a href="#readme-top">Back to top</a>)</p>


### Installation

1. Navigate to the ROS `src` folder.
    ```sh
    $ cd ~/colcon_ws/src/
    ```

2. Clone this repository.
    ```sh
    $ git clone https://github.com/TeamSOBITS/gemini_ros
    ```

3. Navigate into the repository.
    ```sh
    $ cd gemini_ros/
    ```

4. Install dependent packages.
    ```sh
    $ bash install.sh
    ```

5. Compile the package.
    ```sh
    $ cd ~/colcon_ws/
    $ colcon build --symlink-install
    $ source ~/colcon_ws/install/setup.sh
    ```

<p align="right">(<a href="#readme-top">Back to top</a>)</p>


## Launch and Usage

1. Set the Gemini API key in the terminal.
    ```sh
    export GEMINI_API_KEY=************
    ```

> [!NOTE]
> To obtain a Gemini API key, please refer to the following site:
> https://ai.google.dev/gemini-api/docs/api-key

2. Update the model settings in [genai_config.yaml](./config/genai_config.yaml) according to your needs.
    ```yaml
    genai:
      temperature: 0.5    # Lower: less open-ended or creative, higher: more diverse or creative
      thinking_budget: 0  # 0 is DISABLED. -1 is AUTOMATIC
      response_mime_type: "application/json"  # `text/plain` or `application/json`
    ```

3. [Optional] Configure a room for context engineering in [genai_room.yaml](./config/genai_room.yaml).
    ```yaml
    # Example: Chatbot introducing our team
    team_introduce:               # Preparing a separate room called team_introduce
      - {user : "Our team is a student team called SOBITS!"}  # If no image is included = LLM
      - {model: "So you formed a student team called SOBITS! That's wonderful! What kind of team is it?"}
      - {user : "We have 40 members, ranging from undergraduates to masters and PhDs!"}
      - {model: "A large student team with 40 members! With such a wide range of members, it sounds like a wonderful team with diverse perspectives and knowledge gathered together."}
    ```

4. Launch the Gemini ROS action server.
    ```sh
    ros2 launch gemini_ros gemini_server.launch.py
    ```

<p align="right">(<a href="#readme-top">Back to top</a>)</p>


### Sending Requests to the Server

Send a request to the Gemini server using the action `sobits_interfaces/action/ChatLlmRecognition`.

| Item              | Field Name            | Type                   | Description                                         |
| :---------------- | :-------------------- | :--------------------- | :-------------------------------------------------- |
| **Action Name**   |                       |                        | `gemini_action`                                     |
| **Goal**          | `room_name`           | string                 | Arbitrary room name for managing conversation history |
|                   | `request`             | string                 | Text message from the user                          |
|                   | `image`               | sensor_msgs/Image[]    | List of image messages to send                      |
|                   | `sound_file_path`     | string[]               | List of paths to audio files to send                |
|                   | `model_name`          | string                 | Name of the Gemini model to use (e.g., "gemini-2.0-flash") |
|                   | `is_stack`            | bool                   | Whether to stack the current conversation in the conversation history |
| **Result**        | `result`              | string                 | Response text from Gemini                           |

<p align="right">(<a href="#readme-top">Back to top</a>)</p>


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
