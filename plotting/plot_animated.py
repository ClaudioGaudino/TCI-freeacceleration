import pandas as pd
import matplotlib.pyplot as plot
import matplotlib.animation as anim
import time as t
from utils import convert_to_free

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


def get_reading(local=True):
    for _i, row in df.iterrows():

        x_acc = row[x_acc_col]
        y_acc = row[y_acc_col]
        z_acc = row[z_acc_col]

        x_rot = row[x_rot_col]
        y_rot = row[y_rot_col]
        z_rot = row[z_rot_col]

        time = row[time_col]
        if local:
            x, y, z = convert_to_free([x_rot, y_rot, z_rot], [x_acc, y_acc, z_acc])

            yield x, y, z, time
        else:
            yield x_acc, y_acc, z_acc, time
    return None, None, None, None


local_x_acc = []
local_y_acc = []
local_z_acc = []

times = []

secs = 60 * 1

gen = get_reading(local=True)


def animate(frame):
    if frame % secs == 0:
        print(t.time())

    lx, ly, lz, time = next(gen)

    if lx is not None and ly is not None and lz is not None and time is not None:
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

        min_x = min(local_x_acc)
        max_x = max(local_x_acc)
        min_y = min(local_y_acc)
        max_y = max(local_y_acc)
        min_z = min(local_z_acc)
        max_z = max(local_z_acc)

        tot_min = min(min_x, min_y, min_z)
        tot_max = max(max_x, max_y, max_z)

        ax.plot(times[-secs:], local_x_acc[-secs:], color='red', label='X')
        ax.plot(times[-secs:], local_y_acc[-secs:], color='green', label='Y')
        ax.plot(times[-secs:], local_z_acc[-secs:], color='blue', label='Z')

        ax.set_ylim(tot_min - 1, tot_max + 1)
        ax.set_xlim(min(times), max(times))


fig, ax = plot.subplots()
ax.grid(True, which='both')
ax.set_title('Acceleration (Local)')
ax.set_xlabel('Time')
ax.set_ylabel('Acceleration')
ax.legend()
a = anim.FuncAnimation(fig, animate, interval=(1000 / 60), blit=False, save_count=0, cache_frame_data=False)

plot.show()
