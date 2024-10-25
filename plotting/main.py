import pandas as pd
import matplotlib.pyplot as plt
from utils import convert_to_free


filename = ('data\\lean_on_faces.csv')
time_col = 'SampleTimeFine'
x_acc_col = 'Acc_X'
y_acc_col = 'Acc_Y'
z_acc_col = 'Acc_Z'

x_rot_col = 'Euler_X'
y_rot_col = 'Euler_Y'
z_rot_col = 'Euler_Z'

local = True

df = pd.read_csv(filename)


df[time_col] = pd.to_numeric(df[time_col], errors='coerce')
df.sort_values(time_col)

mintime = df[time_col].min()
maxtime = df[time_col].max()

plt.figure(figsize=(16, 9), dpi=100)
plt.xlim(mintime, maxtime)
if local:
    local_x_acc = []
    local_y_acc = []
    local_z_acc = []

    for _, row in df.iterrows():
        x_acc = row[x_acc_col]
        y_acc = row[y_acc_col]
        z_acc = row[z_acc_col]

        x_rot = row[x_rot_col]
        y_rot = row[y_rot_col]
        z_rot = row[z_rot_col]

        lx, ly, lz = convert_to_free([x_rot, y_rot, z_rot], [x_acc, y_acc, z_acc])

        local_x_acc.append(lx)
        local_y_acc.append(ly)
        local_z_acc.append(lz)

    plt.plot(df[time_col], local_x_acc, color='red', label='X')
    plt.plot(df[time_col], local_y_acc, color='green', label='Y')
    plt.plot(df[time_col], local_z_acc, color='blue', label='Z')
    plt.title('Free Acceleration')
else:
    plt.plot(df[time_col], df[x_acc_col], color='red', label='X')
    plt.plot(df[time_col], df[y_acc_col], color='green', label='Y')
    plt.plot(df[time_col], df[z_acc_col], color='blue', label='Z')
    plt.title('Acceleration (Sensor relative)')
plt.grid(True, which='both')

plt.xlabel('Time')
plt.ylabel('Acceleration')
plt.legend()
plt.show()


