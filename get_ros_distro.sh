#!/bin/bash

function main(){
    if [ -d /opt/ros/foxy ]; then
        echo "foxy"
    elif [ -d /opt/ros/humble ]; then
        echo "humble"
    elif [ -d /opt/ros/jazzy ]; then
        echo "jazzy"
    else
        echo "*** No supported ROS found ***"
    fi
}

main "$@"
