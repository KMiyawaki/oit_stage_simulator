#!/bin/bash

function install_desktop_entry(){
    local -r DST=${1}
    local -r SRC=${2}
    local -r DESKTOP_FILE="${SRC}.desktop"
    local -r FILENAME=${DESKTOP_FILE##*/}
    cp "${SRC}" "${DESKTOP_FILE}"
    sed -i "s@<<HOME>>@${HOME}@g" "${DESKTOP_FILE}"
    
    desktop-file-install --dir="${DST}" ${DESKTOP_FILE}
    chmod u+x "${DST}/${FILENAME}"

    rm ${DESKTOP_FILE}
}

function main(){
    local -r APPS=${HOME}/.local/share/applications
    local -r ICONS=${HOME}/.icons
    local -r DESK=${HOME}/Desktop
    if [ ! -e ${ICONS} ]; then
        mkdir ${ICONS}
    fi
    cp ./icons/*.png ${ICONS}
    
    install_desktop_entry ${DESK} ./desktop_templates/oit_stage_navigation
    install_desktop_entry ${DESK} ./desktop_templates/oit_stop_all
    install_desktop_entry ${APPS} ./desktop_templates/oit_stage_navigation 
    install_desktop_entry ${APPS} ./desktop_templates/oit_stop_all
    echo "Add panel from lanchbar menu"
}

main "$@"
