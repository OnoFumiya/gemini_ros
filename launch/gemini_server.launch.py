import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    api_key_arg = DeclareLaunchArgument(
        "api_key",
        default_value="Your Gemini API Key",
        description="Gemini API Key",
    )

    prompt_file_arg = DeclareLaunchArgument(
        "prompt_file",
        default_value=os.path.join(get_package_share_directory("gemini_ros"), 'prompt', 'base_prompt.yaml'),
        description="Prompt data format file path",
    )

    max_output_tokens_arg = DeclareLaunchArgument(
        "max_output_tokens",
        default_value="256",
        description="Maximum number of output tokens for Gemini",
    )

    gemini_action_server_node = Node(
        package="gemini_ros",
        executable="gemini_action_server",
        name="gemini_action_server",
        output="screen",
        parameters=[
            {
                "api_key": LaunchConfiguration("api_key"),
                "prompt_file": LaunchConfiguration("prompt_file"),
                "max_output_tokens": LaunchConfiguration("max_output_tokens"),
            }
        ],
    )

    return LaunchDescription(
        [
            api_key_arg,
            prompt_file_arg,
            max_output_tokens_arg,
            gemini_action_server_node,
        ]
    )