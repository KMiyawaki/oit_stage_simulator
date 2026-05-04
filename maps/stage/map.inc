# https://player-stage-manual.readthedocs.io/en/latest/

define floorplan model
(
  # sombre, sensible, artistic
  color "gray30"

  # most maps will need a bounding box
  boundary 1

  gui_nose 0
  gui_grid 0
  gui_move 0
  gui_outline 0
  gripper_return 0
  fiducial_return 0
  ranger_return 1
)

define rect_block model
(
  #size [0.5 0.5 1.5]
  #gui_nose 0
  size [0.5 0.2 1.7]
  block( 
  points 8
  point[0] [-0.25 0.05]
  point[1] [-0.25 -0.05]
  point[2] [-0.1 -0.1 ]
  point[3] [0.1 -0.1]
  point[4] [0.25 -0.05]
  point[5] [0.25 0.05]
  point[6] [0.1 0.1]
  point[7] [-0.1 0.1]
  z [0 1.7]
  )
)

define polygon_block model
(
  size [0.65 0.3 1.7]
  block( 
    points 8
    point[0] [0.13 0.05]
    point[1] [0.13 -0.05]
    point[2] [0.065 -0.1 ]
    point[3] [-0.065 -0.1]
    point[4] [-0.13 -0.05]
    point[5] [-0.13 0.05]
    point[6] [-0.065 0.1]
    point[7] [0.065 0.1]
    z [0 1.7]
  )
  block(
    points 8
    point[0] [0.35 0.175]
    point[1] [0.35 0.125]
    point[2] [0.325 0.1]
    point[3] [0.275 0.1]
    point[4] [0.25 0.125]
    point[5] [0.25 0.175]
    point[6] [0.275 0.2]
    point[7] [0.325 0.2]
    z [0 1.7]
  )
  block(
    points 8
    point[0] [-0.2 0.125]
    point[1] [-0.2 0.075]
    point[2] [-0.275 0.05 ]
    point[3] [-0.275 0.05]
    point[4] [-0.3 0.075]
    point[5] [-0.3 0.125]
    point[6] [-0.275 0.15]
    point[7] [-0.225 0.15]
    z [0 1.7]
  )
)

define low_block model
(
  #size [0.5 0.5 1.5]
  #gui_nose 0
  size [0.5 0.5 0.25]
)

define middle_block model
(
  #size [0.5 0.5 1.5]
  #gui_nose 0
  size [0.25 0.25 0.35]
)

define pin model
(
  size [0.05 0.05 0.1]
  block(
    points 4
      point[0] [-0.025 0.00]
      point[1] [0.00 0.025]
      point[2] [0.025 0.00]
      point[3] [0.00 -0.025]
      z [0 0.1]
  )
)
