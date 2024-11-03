import pandas as pd
import matplotlib.pyplot as plt
import utils

cog = utils.Config()
cog.setup('setup.ini')

multifile = cog.multifile
print(cog.file_acceleration)
filename = cog.file
fileAccelerations = cog.file_acceleration
fileAngles = cog.file_angles

time_col = cog.time

x_acc_col = cog.x_acc_col
y_acc_col = cog.y_acc_col
z_acc_col = cog.z_acc_col

x_rot_col = cog.x_rot_col
y_rot_col = cog.y_rot_col
z_rot_col = cog.z_rot_col

df = None
if multifile:
    time_col = cog.acc_time
    if fileAccelerations.__contains__('.emt'):
        utils.emt_to_csv(fileAccelerations)
        fileAccelerations = fileAccelerations.replace('.emt', '.csv')
    if fileAngles.__contains__('.emt'):
        utils.emt_to_csv(fileAngles)
        fileAngles = fileAngles.replace('.emt', '.csv')

    df_acc = pd.read_csv(fileAccelerations)
    df_ang = pd.read_csv(fileAngles)
    #df_ang.drop(time_col, axis=1)

    df = pd.merge(df_acc, df_ang, left_on=cog.acc_time, right_on=cog.ang_time, how='inner')
    if x_acc_col == x_rot_col:
        x_acc_col += '_x'
        x_rot_col += '_y'
    if y_acc_col == y_acc_col:
        y_acc_col += '_x'
        y_rot_col += '_y'
    if z_acc_col == z_rot_col:
        z_acc_col += '_x'
        z_rot_col += '_y'
    #time_col += '_x'

else:
    if filename.__contains__('.emt'):
        utils.emt_to_csv(filename)
        filename = filename.replace('.emt', '.csv')
    df = pd.read_csv(filename)

print(df.columns.tolist())
print(df)


mintime = df[time_col].min()
maxtime = df[time_col].max()

plt.figure(figsize=(16, 9), dpi=100)
plt.xlim(mintime, maxtime)
if cog.free_acc:
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

        lx, ly, lz = utils.convert_to_free([x_rot, y_rot, z_rot], [x_acc, y_acc, z_acc])

        local_x_acc.append(lx)
        local_y_acc.append(ly)
        local_z_acc.append(lz)

    if cog.plot_x:
        plt.plot(df[time_col], local_x_acc, color='red', label='X')
    if cog.plot_y:
        plt.plot(df[time_col], local_y_acc, color='green', label='Y')
    if cog.plot_z:
        plt.plot(df[time_col], local_z_acc, color='blue', label='Z')
    plt.title('Free Acceleration')
else:
    if cog.plot_x:
        plt.plot(df[time_col], df[x_acc_col], color='red', label='X')
    if cog.plot_y:
        plt.plot(df[time_col], df[y_acc_col], color='green', label='Y')
    if cog.plot_z:
        plt.plot(df[time_col], df[z_acc_col], color='blue', label='Z')
    plt.title('Acceleration (Sensor relative)')
plt.grid(True, which='both')

plt.xlabel('Time')
plt.ylabel('Acceleration')
plt.legend()

plt.show()

# Function to get data coordinates from plot coordinates