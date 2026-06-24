FROM osrf/ros:jazzy-desktop-full

RUN apt-get update && apt-get install -y \
    git \
    ros-jazzy-demo-nodes-cpp \
    build-essential \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/ros2_ws

ENV ROS_DOMAIN_ID=0
ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp

RUN echo "source /opt/ros/jazzy/setup.bash" >> /etc/bash.bashrc

CMD ["bash"]