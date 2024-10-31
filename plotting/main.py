import pandas as pd
import matplotlib.pyplot as plt
import utils

cog = utils.Config()
cog.setup('setup.ini')

multifile = cog.multifile

filename = cog.
fileAccelerations ='data\\accelerazione.emt'
fileAngles ='data\\Angoli.emt'

join_col = 'Frame'
time_col = 'Time'

x_acc_col = 'GSensor.X'
y_acc_col = 'GSensor.Y'
z_acc_col = 'GSensor.Z'

x_rot_col = 'GSensor.X'
y_rot_col = 'GSensor.Y'
z_rot_col = 'GSensor.Z'

local = True

df = None
if multifile:
    if fileAccelerations.__contains__('.emt'):
        utils.emt_to_csv(fileAccelerations)
        fileAccelerations = fileAccelerations.replace('.emt', '.csv')
    if fileAngles.__contains__('.emt'):
        utils.emt_to_csv(fileAngles)
        fileAngles = fileAngles.replace('.emt', '.csv')

    df_acc = pd.read_csv(fileAccelerations)
    df_ang = pd.read_csv(fileAngles)
    df_ang.drop(time_col, axis=1)

    df = pd.merge(df_acc, df_ang, left_on=join_col, right_on=join_col, how='inner')
    if x_acc_col == x_rot_col:
        x_acc_col += '_x'
        x_rot_col += '_y'
    if y_acc_col == y_acc_col:
        y_acc_col += '_x'
        y_rot_col += '_y'
    if z_acc_col == z_rot_col:
        z_acc_col += '_x'
        z_rot_col += '_y'
    time_col += '_x'

else:
    df = pd.read_csv(filename)

print(df)


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

        lx, ly, lz = utils.convert_to_free([x_rot, y_rot, z_rot], [x_acc, y_acc, z_acc])

        local_x_acc.append(lx)
        local_y_acc.append(ly)
        local_z_acc.append(lz)

    plt.plot(df[time_col], local_x_acc, color='red', label='X')
    #plt.plot(df[time_col], local_y_acc, color='green', label='Y')
    #plt.plot(df[time_col], local_z_acc, color='blue', label='Z')
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

# Function to get data coordinates from plot coordinates