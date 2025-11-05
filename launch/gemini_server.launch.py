import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    robot_name = "gemini_robot"

    api_key_arg = DeclareLaunchArgument(
        "api_key",
        default_value=os.getenv("GEMINI_API_KEY", ""),
        description="Gemini API Key",
    )

    prompt_file_arg = DeclareLaunchArgument(
        "prompt_file",
        default_value=os.path.join(get_package_share_directory("gemini_ros"), 'config', 'base_prompt.yaml'),
        description="Prompt data format file path",
    )

    gemini_action_server_node = Node(
        package="gemini_ros",
        executable="gemini_action_server",
        name="gemini_action_server",
        namespace=robot_name,
        output="screen",
        parameters=[
            {
                "api_key": LaunchConfiguration("api_key"),
                "prompt_file": LaunchConfiguration("prompt_file"),
            }
        ],
    )


    return LaunchDescription(
        [
            api_key_arg,
            prompt_file_arg,
            gemini_action_server_node,
        ]
    )
