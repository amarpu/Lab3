from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

```
# Declare arguments
declared_arguments = []
declared_arguments.append(
    DeclareLaunchArgument(
        "description_package",
        default_value="metafly_description",
        description="Description package of the metafly",
    )
)
declared_arguments.append(
    DeclareLaunchArgument(
        "prefix",
        default_value='""',
        description="Prefix of the joint names",
    )
)

# Initialize arguments
description_package = LaunchConfiguration("description_package")
prefix = LaunchConfiguration("prefix")

# Get URDF via xacro
robot_description_content = Command(
    [
        PathJoinSubstitution([FindExecutable(name="xacro")]),
        " ",
        PathJoinSubstitution(
            [FindPackageShare(description_package), "urdf", "metafly.urdf.xacro"]
        ),
        " ",
        "prefix:=",
        prefix,
        " ",
    ]
)

robot_description = {"robot_description": robot_description_content}

# Metafly TF publisher (makes it fly)
metafly_tf_pub_node = Node(
    package="metafly_tf_pub",
    executable="metafly_tf_pub",
    name="metafly_tf_pub",
    output="both",
)

# Joint state publisher (fixes wings)
joint_state_publisher_node = Node(
    package="joint_state_publisher",
    executable="joint_state_publisher",
    name="joint_state_publisher",
    output="both",
    parameters=[robot_description, {'zeros.joint1': 0.707, 'zeros.joint2': -0.707}],
)

# Robot state publisher
robot_state_publisher_node = Node(
    package="robot_state_publisher",
    executable="robot_state_publisher",
    name="robot_state_publisher",
    output="both",
    parameters=[robot_description],
)

# RViz (NO config file — clean launch)
rviz_node = Node(
    package="rviz2",
    executable="rviz2",
    name="rviz2",
    output="both",
)

return LaunchDescription(
    declared_arguments
    + [
        metafly_tf_pub_node,
        joint_state_publisher_node,
        robot_state_publisher_node,
        rviz_node,
    ]
)
```

