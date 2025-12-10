#!/usr/bin/env python3

"""
Launch file for spawning the robot in Gazebo
Launches the robot model in the Gazebo simulation environment
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import xacro
import os


def generate_launch_description():
    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    robot_name = LaunchConfiguration('robot_name', default='humanoid_robot')
    world = LaunchConfiguration('world', default='digital_twin_world.world')

    # Path to URDF file
    pkg_path = FindPackageShare('digital_twin_description')
    urdf_path = PathJoinSubstitution([pkg_path, 'urdf', 'humanoid_robot.urdf'])

    # Process the URDF file
    robot_description_content = xacro.process_file(
        os.path.join(
            FindPackageShare('digital_twin_description').find('digital_twin_description'),
            'urdf',
            'humanoid_robot.urdf'
        )
    ).toprettyxml(indent='  ')

    robot_description = {'robot_description': robot_description_content}

    # Robot State Publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': use_sim_time}]
    )

    # Spawn entity node
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', robot_name,
            '-x', '0', '-y', '0', '-z', '1.0'  # Spawn 1m above ground
        ],
        output='screen'
    )

    # Joint state broadcaster
    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    # Robot controller
    robot_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
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
                world
            ])
        }.items()
    )

    # Event handler to start controllers after spawn
    load_joint_state_broadcaster = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_entity,
            on_exit=[joint_state_broadcaster],
        )
    )

    load_robot_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_broadcaster,
            on_exit=[robot_controller],
        )
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),
        DeclareLaunchArgument(
            'robot_name',
            default_value='humanoid_robot',
            description='Name of the robot to spawn'
        ),
        DeclareLaunchArgument(
            'world',
            default_value='digital_twin_world.world',
            description='Choose one of the world files from `/digital_twin_gazebo/worlds`'
        ),
        gazebo,
        robot_state_publisher,
        spawn_entity,
        load_joint_state_broadcaster,
        load_robot_controller
    ])