#
# The constants module is a convenience place for teams to hold robot-wide
# numerical or boolean constants. Don't use this for any other purpose!
#

import math

# Motors
kLeftMotor1Port = 0
kRightMotor1Port = 1


# Encoders
kLeftEncoderPorts = (4, 5)
kRightEncoderPorts = (6, 7)
kLeftEncoderReversed = False
kRightEncoderReversed = True

kEncoderCPR = 1024
kWheelDiameterInches = 6
# Assumes the encoders are directly mounted on the wheel shafts
kEncoderDistancePerPulse = (kWheelDiameterInches * math.pi) / kEncoderCPR


# Physical parameters  - in meters on the romi?
ksVolts = 0.929
kvVoltSecondsPerInch = 6.33
kaVoltSecondsSquaredPerInch = 0.1 # 0.0175
kDriveTrainMotorCount = 2
kTrackWidth = 0.14
kGearingRatio = 8
kWheelRadius = 0.0508

# kEncoderResolution = -
