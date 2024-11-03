import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as anim
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

else:
    if filename.__contains__('.emt'):
        utils.emt_to_csv(filename)
        filename = filename.replace('.emt', '.csv')
    df = pd.read_csv(filename)

print(df.columns.tolist())
print(df)


mintime = df[time_col].min()
maxtime = df[time_col].max()

fig, ax = plt.subplots(figsize=(16, 9))

ax.set_xlim(mintime, maxtime)
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
        ax.plot(df[time_col], local_x_acc, color='red', label='X')
    if cog.plot_y:
        ax.plot(df[time_col], local_y_acc, color='green', label='Y')
    if cog.plot_z:
        ax.plot(df[time_col], local_z_acc, color='blue', label='Z')
    ax.set_title('Free Acceleration')
else:
    if cog.plot_x:
        ax.plot(df[time_col], df[x_acc_col], color='red', label='X')
    if cog.plot_y:
        ax.plot(df[time_col], df[y_acc_col], color='green', label='Y')
    if cog.plot_z:
        ax.plot(df[time_col], df[z_acc_col], color='blue', label='Z')
    ax.set_title('Acceleration (Sensor relative)')
plt.grid(True, which='both')

events_x = []
events_y = []
def onclick(event):
    if event.inaxes:
        events_x.append(event.xdata)
        events_y.append(event.ydata)

        print(f'clicked at: {event.xdata}, {event.ydata}')

def animate(frame):
    ax.scatter(events_x, events_y, c='black', zorder=10)


ax.set_xlabel('Time')
ax.set_ylabel('Acceleration')
ax.legend()

fig.canvas.mpl_connect('button_press_event', onclick)
a = anim.FuncAnimation(fig, animate, interval=(1000 / 20), blit=False, save_count=0, cache_frame_data=False)

plt.show()