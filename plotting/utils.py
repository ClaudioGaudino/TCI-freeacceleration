from scipy.spatial.transform import Rotation as R


def convert_to_local(angles, acc, gyro=None):
    rotation = R.from_euler('xyz', angles, degrees=True)

    local_acc = rotation.apply(acc)

    if gyro is not None:
        local_gyro = rotation.apply(gyro)
        return local_acc, local_gyro

    else:
        return local_acc
