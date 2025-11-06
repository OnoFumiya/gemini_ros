import os
import datetime
import cv2
import yaml
from google import genai
from google.genai import types

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup

import ament_index_python
from cv_bridge import CvBridge

from sensor_msgs.msg import Image
from sobits_interfaces.action import ChatLlmRecognition


class GeminiActionServer(Node):
    def __init__(self):
        super().__init__('gemini_action_server')
        self.declare_parameter('api_key', '')
        self.declare_parameter('rooms_file', '')
        self.declare_parameter('genai.temperature', 0.5)
        self.declare_parameter('genai.thinking_budget', 0)
        self.declare_parameter('genai.response_mime_type', 'application/json')

        self.api_key = self.get_parameter('api_key').get_parameter_value().string_value
        self.room_file = self.get_parameter('rooms_file').get_parameter_value().string_value
        self.pkg_path = ament_index_python.get_package_share_directory('gemini_ros')
        self.config_path = os.path.join(self.pkg_path, 'config/')
        self.genai={
            'temperature': self.get_parameter('genai.temperature').get_parameter_value().double_value,
            'thinking_budget': self.get_parameter('genai.thinking_budget').get_parameter_value().integer_value,
            'response_mime_type': self.get_parameter('genai.response_mime_type').get_parameter_value().string_value
        }

        # Print out parameters for debugging
        self.get_logger().info(f'API Key: {"[HIDDEN]" if self.api_key else "[NOT SET]"}')
        self.get_logger().info(f'Room File: {self.room_file}')
        self.get_logger().info(f'GenAI Temperature: {self.genai["temperature"]}')
        self.get_logger().info(f'GenAI Thinking Budget: {self.genai["thinking_budget"]}')
        self.get_logger().info(f'GenAI Response Mime Type: {self.genai["response_mime_type"]}')

        if self.api_key == '':
            self.get_logger().error('API Key is not set. Please set the `api_key` parameter.')
            return

        with open(self.room_file, "r") as file:
            self.rooms = yaml.safe_load(file)

        self.genai_client = genai.Client(api_key=self.api_key)
        self.genai_config = types.GenerateContentConfig(
            temperature=self.genai['temperature'],
            thinking_config=types.ThinkingConfig(thinking_budget=self.genai['thinking_budget']),
            response_mime_type=self.genai['response_mime_type']
        )
        self.chat_messages = {}
        self.build_prompt()

        self.bridge = CvBridge()

        self.action_server_ = ActionServer(self, ChatLlmRecognition, "gemini_action",
            execute_callback=self.gemini_callback, callback_group=ReentrantCallbackGroup(),
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)

        self.get_logger().info('Gemini Server is ready and waiting for action requests.')  


    def goal_callback(self, goal_request):
        """Accept or reject a client request to begin an action."""
        # This server allows multiple goals in parallel
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT


    def cancel_callback(self, goal_handle):
        """Accept or reject a client request to cancel an action."""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT


    def gemini_callback(self, goal_handle):
        self.get_logger().info('Executing goal')

        response = ChatLlmRecognition.Result()
        response.elapsed_time = -1.0
        response.result = ""

        # print("===============================================", flush=True)
        if ((goal_handle.request.room_name in self.chat_messages.keys()) != True):
            self.chat_messages[goal_handle.request.room_name] = []

        self.chat_messages[goal_handle.request.room_name] += [{'role': 'user', 'parts': [{"text": goal_handle.request.request}]}]

        dt_now = datetime.datetime.now()
        for i in range(len(goal_handle.request.image)):
            img_msg = goal_handle.request.image[i]
            img_cv = self.bridge.imgmsg_to_cv2(img_msg)

            if img_msg.encoding == 'bgr8':
                pass
            elif img_msg.encoding == 'bgra8':
                img_cv     = cv2.cvtColor(img_cv, cv2.COLOR_RGBA2RGB)
            elif img_msg.encoding == 'rgba8':
                img_cv     = cv2.cvtColor(img_cv, cv2.COLOR_BGRA2RGB)
            elif img_msg.encoding == 'rgb8':
                img_cv     = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            else:
                self.get_logger().error('Unsupported image encoding: %s' % img_msg.encoding)
                goal_handle.canceled()
                return response

            save_file_name = os.path.join(
                self.config_path,
                "result_" + str(dt_now.year) + "_" + \
                str(dt_now.month) + "_" + \
                str(dt_now.day) + "_" + \
                str(dt_now.hour) + "_" + \
                str(dt_now.minute) + "_" + \
                str(dt_now.second) + "_" + \
                "label" + str(i) + ".png")
            cv2.imwrite(save_file_name, img_cv)

            uploaded_file = self.genai_client.files.upload(file=save_file_name)
            self.chat_messages[goal_handle.request.room_name][-1]["parts"] += \
                [{"file_data": {
                    "mime_type": uploaded_file.mime_type,
                    "file_uri": uploaded_file.uri
                }}]

        for i in range(len(goal_handle.request.sound_file_path)):
            sound_file = goal_handle.request.sound_file_path[i]
            if (os.path.isfile(sound_file)):
                uploaded_file = self.genai_client.files.upload(file=sound_file)
                self.chat_messages[goal_handle.request.room_name][-1]["parts"] += \
                    [{"file_data": {
                        "mime_type": uploaded_file.mime_type,
                        "file_uri": uploaded_file.uri
                    }}]
            else:
                self.get_logger().error('Sound file not found: %s' % sound_file)
                goal_handle.canceled()
                return response

        feedback = ChatLlmRecognition.Feedback()
        feedback.wip_result = ""
        feedback.end_flag = False

        starting_time = self.get_clock().now()

        for chunk in self.genai_client.models.generate_content_stream(
            model=goal_handle.request.model_name,
            contents=self.chat_messages[goal_handle.request.room_name],
            config=self.genai_config,
        ):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return response

            self.get_logger().debug('Received chunk: %s' % chunk.text)
            feedback.wip_result += chunk.text
            self.get_logger().debug('Published feedback: %s' % feedback.wip_result)
            goal_handle.publish_feedback(feedback)

        ending_time = self.get_clock().now()
        feedback.end_flag = True
        goal_handle.publish_feedback(feedback)

        response.elapsed_time = (ending_time - starting_time).nanoseconds / 1e9
        response.result = feedback.wip_result

        if goal_handle.request.is_stack:
            self.chat_messages[goal_handle.request.room_name] += \
                [{
                    'role': 'model',
                    'parts': [{
                        "text": response.result
                    }]
                }]
        else:
            self.chat_messages[goal_handle.request.room_name] = self.chat_messages[goal_handle.request.room_name][:-1]

        goal_handle.succeed()
        return response


    def build_prompt(self):
        self.chat_messages = {}
        for room_name in self.rooms.keys():
            self.chat_messages[str(room_name)] = []
            for talk in self.rooms[room_name]:
                if ("user" in list(talk.keys())):
                    self.chat_messages[str(room_name)] += \
                        [{
                            "role": "user",
                            "parts": [{
                                "text": talk["user"]
                            }]
                        }]
                if ("model" in list(talk.keys())):
                    self.chat_messages[str(room_name)] += \
                        [{
                            "role": "model",
                            "parts": [{
                                "text": talk["model"]
                            }]
                        }]
                if ("files" in list(talk.keys())):
                    for f in talk["files"]:
                        if (f[0] == "/"):
                            uploaded_file = self.genai_client.files.upload(file=f)
                        else:
                            uploaded_file = self.genai_client.files.upload(file=self.config_path + f)
                        self.chat_messages[str(room_name)][-1]["parts"] += \
                            [{
                                "file_data": {
                                    "mime_type": uploaded_file.mime_type,
                                    "file_uri": uploaded_file.uri
                                }
                            }]


def main(args=None):
    rclpy.init(args=args)

    genai_action_server_node = GeminiActionServer()

    rclpy.spin(genai_action_server_node)


if __name__ == '__main__':
    main()
