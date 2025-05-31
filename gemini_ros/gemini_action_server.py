import os
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
import time
import datetime
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from sobits_interfaces.action import ChatLlmRecognition
from google import genai
import yaml

## MODEL Example : 'gemini-2.0-flash'

class GeminiActionServer(Node):
    def __init__(self):
        super().__init__('gemini_action_server')

        self.bridge = CvBridge()

        self.declare_parameter('api_key', '')
        self.declare_parameter('max_output_tokens', 256)

        self.declare_parameter('prompt_file', '')

        self.api_key = self.get_parameter('api_key').get_parameter_value().string_value
        self.max_output_tokens = self.get_parameter('max_output_tokens').get_parameter_value().integer_value

        self.prompt_file = self.get_parameter('prompt_file').get_parameter_value().string_value
        self.yaml_folder_path = "/".join(self.prompt_file.split("/")[:-1]) +"/"

        with open(self.prompt_file, "r") as file:
            self.prompt = yaml.safe_load(file)

        if self.api_key == '':
            self.get_logger().error('API key not set')
            return

        self.client = genai.Client(api_key=self.api_key)

        self.chat_messages = {}
        self.build_prompt()

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
        feedback = ChatLlmRecognition.Feedback()
        response = ChatLlmRecognition.Result()
        response.elapsed_time = 0.0
        response.result = ""
        print("===============================================", flush=True)
        if ((goal_handle.request.room_name in self.chat_messages.keys()) != True):
            self.chat_messages[goal_handle.request.room_name] = []

        self.chat_messages[goal_handle.request.room_name] += [{'role': 'user', 'parts': [{"text": goal_handle.request.request}]}]

        dt_now = datetime.datetime.now()
        for i in range(len(goal_handle.request.image)):
            img = goal_handle.request.image[i]
            image = self.bridge.imgmsg_to_cv2(img)

            if img.encoding == 'bgr8':
                pass
            elif img.encoding == 'bgra8':
                image     = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
            elif img.encoding == 'rgba8':
                image     = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
            elif img.encoding == 'rgb8':
                image     = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                print("\033[31mEncoding ERROR\033[0m")
                return response

            save_file_name = self.yaml_folder_path + "result_" + str(dt_now.year) + "_" + str(dt_now.month) + "_" + str(dt_now.day) + "_" + str(dt_now.hour) + "_" + str(dt_now.minute) + "_" + str(dt_now.second) + "_label" + str(i) + ".png"
            cv2.imwrite(save_file_name, image)
            uploaded_file = self.client.files.upload(file=save_file_name)
            self.chat_messages[goal_handle.request.room_name][-1]["parts"] += [{"file_data": {"mime_type": uploaded_file.mime_type, "file_uri": uploaded_file.uri}}]

        for i in range(len(goal_handle.request.sound_file_path)):
            sound_file = goal_handle.request.sound_file_path[i]
            if (os.path.isfile(sound_file)):
                uploaded_file = self.client.files.upload(file=sound_file)
                self.chat_messages[goal_handle.request.room_name][-1]["parts"] += [{"file_data": {"mime_type": uploaded_file.mime_type, "file_uri": uploaded_file.uri}}]
            else:
                print("\033[31mNo File Path\033[0m")

        feedback.end_flag = False
        feedback.wip_result = ""
        starting_time = time.time()

        for chunk in self.client.models.generate_content_stream(
            model=goal_handle.request.model_name,
            contents=self.chat_messages[goal_handle.request.room_name]):

            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                print('\033[31mGoal canceled\033[0m', flush=True)
                return response

            feedback.wip_result += chunk.text
            print(feedback.wip_result, flush=True)
            goal_handle.publish_feedback(feedback)

        feedback.end_flag = True
        goal_handle.publish_feedback(feedback)

        response.elapsed_time = time.time() - starting_time
        response.result = feedback.wip_result

        if goal_handle.request.is_stack:
            self.chat_messages[goal_handle.request.room_name] += [{'role': 'model', 'parts': [{"text": response.result}]}]
        else:
            self.chat_messages[goal_handle.request.room_name] = self.chat_messages[goal_handle.request.room_name][:-1]

        goal_handle.succeed()
        return response


    def build_prompt(self):
        self.chat_messages = {}
        for rn in self.prompt.keys():
            self.chat_messages[str(rn)] = []
            for talk in self.prompt[rn]:
                if ("user" in list(talk.keys())):
                    self.chat_messages[str(rn)] += [{"role": "user", "parts": [{"text": talk["user"]}]}]
                else:
                    self.chat_messages[str(rn)] += [{"role": "model", "parts": [{"text": talk["model"]}]}]

                if ("files" in list(talk.keys())):
                    for f in talk["files"]:
                        if (f[0] == "/"):
                            uploaded_file = self.client.files.upload(file=f)
                        else:
                            uploaded_file = self.client.files.upload(file=self.yaml_folder_path + f)
                        self.chat_messages[str(rn)][-1]["parts"] += [{"file_data": {"mime_type": uploaded_file.mime_type, "file_uri": uploaded_file.uri}}]



def main(args=None):
    rclpy.init(args=args)
    node = GeminiActionServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
