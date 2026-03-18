import os

import numpy as np
import rclpy
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from transforms3d.euler import euler2quat


class MetaflyTfPublisher(Node):
    def __init__(self):
        super().__init__('metafly_tf_publisher')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.broadcast_tf)

        package_share_dir = get_package_share_directory('metafly_tf_pub')
        csv_file = os.path.join(package_share_dir, 'resource', 'mocap_data.csv')
        data = np.genfromtxt(csv_file, delimiter=',', skip_header=1)

        self.x = data[:, 1]
        self.y = data[:, 2]
        self.z = data[:, 3]

        self.roll = np.deg2rad(data[:, 4])
        self.pitch = np.deg2rad(data[:, 5])
        self.yaw = np.deg2rad(data[:, 6])

        self.i = 0
        self.data_length = len(self.x)

    def broadcast_tf(self):
        tf = TransformStamped()

        tf.header.stamp = self.get_clock().now().to_msg()
        tf.header.frame_id = 'world'
        tf.child_frame_id = 'base_link'

        tf.transform.translation.x = float(self.x[self.i])
        tf.transform.translation.y = float(self.y[self.i])
        tf.transform.translation.z = float(self.z[self.i])

        q = euler2quat(self.pitch[self.i], self.roll[self.i], self.yaw[self.i])
        tf.transform.rotation.w = float(q[0])
        tf.transform.rotation.x = float(q[1])
        tf.transform.rotation.y = float(q[2])
        tf.transform.rotation.z = float(q[3])

        self.tf_broadcaster.sendTransform(tf)

        self.i += 1
        self.i %= self.data_length


def main(args=None):
    rclpy.init(args=args)
    node = MetaflyTfPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
