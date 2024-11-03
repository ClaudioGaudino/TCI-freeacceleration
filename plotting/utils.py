from scipy.spatial.transform import Rotation as R
import pandas as pd

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


def emt_to_csv(path: str):
    data = ''
    with open(path, 'r') as file:
        blanks = 0
        for line in file:
            if blanks < 3:
                if line == '\n':
                    blanks += 1
                    continue
            else:
                if line == '\n' or line == '':
                    break
                else:
                    row = line.split()
                    for d in row:
                        data += d.strip() + ','
                    data += '\n'
    with open(path.replace('.emt', '.csv'), 'w') as csv_file:
        csv_file.write(data)
    return

class Config:
    def __init__(self):
        self.ang_vel_time = None
        self.ang_time = None
        self.acc_time = None
        self.time = None
        self.plot_z = None
        self.plot_y = None
        self.plot_x = None
        self.free_acc = None
        self.z_ang_vel_col = None
        self.y_ang_vel_col = None
        self.x_ang_vel_col = None
        self.z_rot_col = None
        self.y_rot_col = None
        self.x_rot_col = None
        self.z_acc_col = None
        self.y_acc_col = None
        self.file = None
        self.x_acc_col = None
        self.multifile = False
        self.file_angles = None
        self.file_acceleration = None
        self.file_angular_velocity = None

    def setup(self, path: str):
        with open(path, 'r') as ini:
            value = None
            for line in ini:
                if line.startswith('#'):
                    continue

                if line.startswith('file multipli='):
                    value = eval(line.split('=')[1].strip())
                    print(value)
                    self.multifile = value

                if self.multifile:
                    if line.startswith('file accelerazioni='):
                        self.file_acceleration = line.split('=')[1].strip()
                    if line.startswith('file angoli='):
                        self.file_angles = line.split('=')[1].strip()
                    if line.startswith('file velocita angolari='):
                        self.file_angular_velocity = line.split('=')[1].strip()
                else:
                    if line.startswith('file dati='):
                        self.file = line.split('=')[1].strip()
                
                if line.startswith('accelerazione asse x='):
                    self.x_acc_col = line.split('=')[1].strip()
                elif line.startswith('accelerazione asse y='):
                    self.y_acc_col = line.split('=')[1].strip()
                elif line.startswith('accelerazione asse z='):
                    self.z_acc_col = line.split('=')[1].strip()
                elif line.startswith('angolazioni asse x='):
                    self.x_rot_col = line.split('=')[1].strip()
                elif line.startswith('angolazioni asse y='):
                    self.y_rot_col = line.split('=')[1].strip()
                elif line.startswith('angolazioni asse z='):
                    self.z_rot_col = line.split('=')[1].strip()
                elif line.startswith('velocita angolare asse x='):
                    self.x_ang_vel_col = line.split('=')[1].strip()
                elif line.startswith('velocita angolare asse y='):
                    self.y_ang_vel_col = line.split('=')[1].strip()
                elif line.startswith('velocita angolare asse z='):
                    self.z_ang_vel_col = line.split('=')[1].strip()
                elif line.startswith('free acceleration='):
                    self.free_acc = eval(line.split('=')[1].strip())
                elif line.startswith('asse x='):
                    self.plot_x = eval(line.split('=')[1].strip())
                elif line.startswith('asse y='):
                    self.plot_y = eval(line.split('=')[1].strip())
                elif line.startswith('asse z='):
                    self.plot_z = eval(line.split('=')[1].strip())
                elif line.startswith('tempo generale='):
                    self.time = line.split('=')[1].strip()
                elif line.startswith('tempo accelerazioni='):
                    self.acc_time = line.split('=')[1].strip()
                elif line.startswith('tempo angolazioni='):
                    self.ang_time = line.split('=')[1].strip()
                elif line.startswith('tempo velocita angolari='):
                    self.ang_vel_time = line.split('=')[1].strip()
                