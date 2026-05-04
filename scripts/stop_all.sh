#!/bin/bash

function main(){
    local -r PACKAGE="oit_stage_simulator"
    local -r USER_HOME=$(getent passwd $USER | cut -d: -f6)
    local -r DIST=`${USER_HOME}/ros2_ws/src/${PACKAGE}/get_ros_distro.sh`
    source /opt/ros/${DIST}/setup.bash
    source ${USER_HOME}/ros2_ws/install/setup.bash
    export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
    export ROS_DOMAIN_ID=0
    
    echo "Kill all ros nodes!"
    ros2 daemon stop > /dev/null 2>&1
    local ROS_PROCS=$(pgrep -f "ros2|__node:=|_ros2_daemon")
    if [ -n "${ROS_PROCS}" ]; then
        echo "Active ROS 2 nodes found. Sending SIGINT..."
        echo "${ROS_PROCS}" | xargs -r kill -INT
        
        echo "Waiting for node cleanup..."
        sleep 2
    fi

    if command -v fastdds &> /dev/null; then
        fastdds shm clean > /dev/null 2>&1
    fi
    
    echo "All ROS 2 nodes stopped."
    return 0
}

main "$@"