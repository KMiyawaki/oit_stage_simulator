#!/bin/bash

function main(){
    local -r SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
    cd "${SCRIPT_DIR}" || { echo "Error: Could not change directory to ${SCRIPT_DIR}. Exiting." >&2; exit 1; }
    
    if [ "$#" -ne 1 ]; then
        echo "Usage: ${0} <map_yaml_path>" >&2
        echo "Example: ${0} /path/to/my_map.yaml" >&2
        exit 1
    fi
    local -r MAP_YAML_PATH="${1}"
    local -r MAP_PGM_PATH="${MAP_YAML_PATH%.*}.pgm"
    python3 add_map_image_border.py "${MAP_PGM_PATH}"
    if [ $? -ne 0 ]; then
        echo "Error: add_border.py failed to add border to ${MAP_PGM_PATH}. Exiting." >&2
        exit 1
    fi
    python3 make_stage_world.py "${MAP_YAML_PATH}"
    if [ $? -ne 0 ]; then
        echo "Error: make_stage_world.py failed to generate world file for ${MAP_YAML_PATH}. Exiting." >&2
        exit 1
    fi
    echo "Stage world file successfully generated."
    ../build.sh
}

main "$@"
