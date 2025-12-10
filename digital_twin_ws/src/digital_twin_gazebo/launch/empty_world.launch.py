#!/usr/bin/env python3

"""
Launch file for empty Gazebo world
Launches Gazebo with an empty world for the digital twin simulation
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Launch arguments
    world_arg = DeclareLaunchArgument(
        'world',
        default_value='empty',
        description='Choose one of the world files from `/digital_twin_gazebo/worlds`'
    )

    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            ])
        ]),
        launch_arguments={
            'world': PathJoinSubstitution([
                FindPackageShare('digital_twin_gazebo'),
                'worlds',
                LaunchConfiguration('world')
            ])
        }.items()
    )

    return LaunchDescription([
        world_arg,
        gazebo
    ])