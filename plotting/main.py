import pandas as pd
import matplotlib.pyplot as plot
import matplotlib.animation as anim
import numpy as np
import time
from scipy.spatial.transform import Rotation as R

filename = ('data\\data.csv')
time_col = 'SampleTimeFine'
x_acc_col = 'Acc_X'
y_acc_col = 'Acc_Y'
z_acc_col = 'Acc_Z'

x_rot_col = 'Euler_X'
y_rot_col = 'Euler_Y'
z_rot_col = 'Euler_Z'

df = pd.read_csv(filename)


df[time_col] = pd.to_numeric(df[time_col], errors='coerce')
df.sort_values(time_col)

mintime = df[time_col].min()
maxtime = df[time_col].max()

plot.figure(figsize=(16, 9), dpi=100)
plot.xlim(mintime, maxtime)
plot.plot(df[time_col], df[x_acc_col], color='red', label='X')
plot.plot(df[time_col], df[y_acc_col], color='green', label='Y')
plot.plot(df[time_col], df[z_acc_col], color='blue', label='Z')
plot.grid(True, which='both')
plot.title('Acceleration (Sensor relative)')
plot.xlabel('Time')
plot.ylabel('Acceleration')
plot.legend()
plot.show()


# rotate frame of reference to be Local


def convert_to_local(angles, acc, gyro=None):
    rotation = R.from_euler('xyz', angles, degrees=True)

    local_acc = rotation.apply(acc)

    if gyro is not None:
        local_gyro = rotation.apply(gyro)
        return local_acc, local_gyro

    else:
        return local_acc

def get_reading_local():
    for _i, row in df.iterrows():

        x_acc = row[x_acc_col]
        y_acc = row[y_acc_col]
        z_acc = row[z_acc_col]

        x_rot = row[x_rot_col]
        y_rot = row[y_rot_col]
        z_rot = row[z_rot_col]

        time = row[time_col]

        x, y, z = convert_to_local([x_rot, y_rot, z_rot], [x_acc, y_acc, z_acc])

        yield x, y, z, time


local_x_acc = []
local_y_acc = []
local_z_acc = []

times = []

secs = 60*1

gen = get_reading_local()
def animate(frame):
    lx, ly, lz, time = next(gen)

    local_x_acc.append(lx)
    local_y_acc.append(ly)
    local_z_acc.append(lz)

    times.append(frame)

    if len(local_x_acc) >= secs:
        local_x_acc.pop(0)
    if len(local_y_acc) >= secs:
        local_y_acc.pop(0)
    if len(local_z_acc) >= secs:
        local_z_acc.pop(0)
    if len(times) >= secs:
        times.pop(0)

    print(len(times))

    ax.plot(frame, lx, color='red', label='X')
    ax.plot(frame, ly, color='green', label='Y')
    ax.plot(frame, lz, color='blue', label='Z')


fig, ax = plot.subplots()
ax.grid(True, which='both')
ax.set_title('Acceleration (Local)')
ax.set_xlabel('Time')
ax.set_ylabel('Acceleration')
ax.legend()
a = anim.FuncAnimation(fig, animate, interval=(1000/60), blit=False, save_count=0, cache_frame_data=False)

plot.show()

#print(np.mean(times))