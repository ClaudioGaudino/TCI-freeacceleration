from scipy.spatial.transform import Rotation as R

g = 9.80665

def convert_to_free(angles, acc, gyro=None):
    rotation = R.from_euler('xyz', angles, degrees=True)

    local_acc = rotation.apply(acc)
    local_acc[2] -= g
    if gyro is not None:
        local_gyro = rotation.apply(gyro)
        return local_acc, local_gyro

    else:
        return local_acc
