# https://player-stage-manual.readthedocs.io/en/latest/

define UTM-30LX ranger
(
  # https://www.hokuyo-aut.co.jp/search/single.php?serial=21
  sensor(                         
    range [ 0.0  30.0 ]
    fov 270.25
    samples 1081
  )
  # generic model properties
  color "black"
  size [ 0.06 0.06 0.09 ]
)

define YDLIDAR_X4 ranger
(
  # https://www.ydlidar.com/products/view/5.html
  sensor(                         
    range [ 0.12  10.0 ]
    fov 360
    samples 720
  )
  # generic model properties
  color "black"
  size [ 0.07 0.07 0.352 ]
)

define IMX219_D160 camera
(
  # https://www.waveshare.com/imx219-d160.htm
  resolution [ 1280 720 ]
  range [ 0.2 20.0 ]
  fov [ 155.1263859 147.2783641 ]
  pantilt [ 0.0 0.0 ]

  # model properties
  size [ 0.01 0.025 0.025 ]
  color "green"
)

define antenna model(
  size [0.05 0.025 0.1]
  color "black"
)

define robot position
(
  size   [0.23 0.23 0.132]
  origin [-0.05 0 0 0] # move rotation center forward
  gui_nose 1
  drive "diff"
  YDLIDAR_X4(pose [ 0.03 0 -0.0894 0 ])
  IMX219_D160(pose [ 0.03 0 -0.03075 0 ])
  antenna(pose [ 0.01  0.10 0 0 ])
  antenna(pose [ 0.01 -0.10 0 0 ])
  velocity_bounds     [-1.2 1.2 0 0 0 0 -270 270]
  acceleration_bounds [-1.2 1.2 0 0 0 0 -270 270]
)
