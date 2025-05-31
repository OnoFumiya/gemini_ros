import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # model_name_arg = DeclareLaunchArgument(
    #     "model_name",
    #     default_value="gemini-2.0-flash",
    #     description="Name of the Gemini model to use",
    # )

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

    # use_crispe_arg = DeclareLaunchArgument(
    #     "use_crispe",
    #     default_value="True",
    #     description="Enable/Disable CRISPE context",
    # )

    # use_history_arg = DeclareLaunchArgument(
    #     "use_history",
    #     default_value="True",
    #     description="Whether to store interaction history",
    # )

    # history_length_arg = DeclareLaunchArgument(
    #     "history_length",
    #     default_value="10",
    #     description="Maximum number of past interactions to store",
    # )

    # crispe_framework_path = os.path.join(
    #     get_package_share_directory("gemini_ros"),
    #     "config",
    #     "crispe_framework.yaml"
    # )

    gemini_action_server_node = Node(
        package="gemini_ros",
        executable="gemini_action_server",
        name="gemini_action_server",
        output="screen",
        parameters=[
            # crispe_framework_path,
            {
                # "model_name": LaunchConfiguration("model_name"),
                "api_key": LaunchConfiguration("api_key"),
                "prompt_file": LaunchConfiguration("prompt_file"),
                "max_output_tokens": LaunchConfiguration("max_output_tokens"),
                # "use_crispe": LaunchConfiguration("use_crispe"),
                # "use_history": LaunchConfiguration("use_history"),
                # "history_length": LaunchConfiguration("history_length"),
            }
        ],
    )

    return LaunchDescription(
        [
            # model_name_arg,
            api_key_arg,
            prompt_file_arg,
            max_output_tokens_arg,
            # use_crispe_arg,
            # use_history_arg,
            # history_length_arg,
            gemini_action_server_node,
        ]
    )