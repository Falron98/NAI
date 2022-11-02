import numpy as np
import skfuzzy as fuzz
from matplotlib import pyplot as plt

# Range of input arrays
x_height = np.arange(0, 61, 1)
x_temp = np.arange(0, 51, 1)
x_daytime = np.arange(0, 3, 1)
x_intensity = np.arange(0, 101, 1)

print(x_height)
print(x_temp)
print(x_daytime)

# Defining the division of the input arrays into segments
# (with trapmf(4 arguments) and trimf(3 arguments))
height_lo = fuzz.trapmf(x_height, [0, 0, 0, 15])
height_md = fuzz.trapmf(x_height, [10, 15, 20, 30])
height_hi = fuzz.trapmf(x_height, [20, 40, 60, 60])
temp_lo = fuzz.trapmf(x_temp, [-18, 0, 18, 23])
temp_md = fuzz.trapmf(x_temp, [20, 27, 33, 37])
temp_hi = fuzz.trapmf(x_temp, [30, 50, 50, 50])
daytime_lo = fuzz.trimf(x_daytime, [0, 0, 1])
daytime_hi = fuzz.trimf(x_daytime, [1, 2, 2])
intensity_none = fuzz.trimf(x_intensity, [0, 0, 0])
intensity_lo = fuzz.trimf(x_intensity, [1, 1, 50])
intensity_md = fuzz.trimf(x_intensity, [1, 50, 100])
intensity_hi = fuzz.trimf(x_intensity, [50, 100, 100])

# Visualize this
fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, figsize=(8, 9))

# Graph specification for each array and each level of it
ax0.plot(x_height, height_lo, 'b', linewidth=1.5, label='Low')
ax0.plot(x_height, height_md, 'g', linewidth=1.5, label='Medium')
ax0.plot(x_height, height_hi, 'r', linewidth=1.5, label='High')
ax0.set_title('Height of bulb')
ax0.legend()

ax1.plot(x_temp, temp_lo, 'b', linewidth=1.5, label='Low')
ax1.plot(x_temp, temp_md, 'g', linewidth=1.5, label='Medium')
ax1.plot(x_temp, temp_hi, 'r', linewidth=1.5, label='High')
ax1.set_title('Temperature inside')
ax1.legend()

ax2.plot(x_daytime, daytime_lo, 'b', linewidth=1.5, label='Day')
ax2.plot(x_daytime, daytime_hi, 'r', linewidth=1.5, label='Night')
ax2.set_title('Time of day')
ax2.legend()

ax3.plot(x_intensity, intensity_none, 'y', linewidth=1.5, label='None')
ax3.plot(x_intensity, intensity_lo, 'b', linewidth=1.5, label='Low')
ax3.plot(x_intensity, intensity_md, 'g', linewidth=1.5, label='Medium')
ax3.plot(x_intensity, intensity_hi, 'r', linewidth=1.5, label='High')
ax3.set_title('Intensity')
ax3.legend()

# Turn off top/right axes
for ax in (ax0, ax1, ax2, ax3):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

# Showing our graph
plt.tight_layout()
plt.show()
