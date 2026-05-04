#!/bin/bash

function main(){
    local -r USER_HOME=$(getent passwd $USER | cut -d: -f6)
    local -r PACKAGE="oit_stage_simulator"
    local -r DIST=`${USER_HOME}/ros2_ws/src/${PACKAGE}/get_ros_distoro.sh`
    source /opt/ros/${DIST}/setup.bash
    source ${USER_HOME}/ros2_ws/install/setup.bash
    export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
    export ROS_DOMAIN_ID=0
    ros2 run ${PACKAGE} select_map.py
}

main "$@"
