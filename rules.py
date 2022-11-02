import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from main import *

# skfuzzy interpolation with simple test (last digit in each line defines
# test case
height_level_lo = fuzz.interp_membership(x_height, height_lo, 25)
height_level_md = fuzz.interp_membership(x_height, height_md, 25)
height_level_hi = fuzz.interp_membership(x_height, height_hi, 25)
temp_level_lo = fuzz.interp_membership(x_temp, temp_lo, 20)
temp_level_md = fuzz.interp_membership(x_temp, temp_md, 20)
temp_level_hi = fuzz.interp_membership(x_temp, temp_hi, 20)
daytime_level_lo = fuzz.interp_membership(x_daytime, daytime_lo, 2)
daytime_level_hi = fuzz.interp_membership(x_daytime, daytime_hi, 2)

# Set of rules migrated from Excel into numpy
rule1 = np.fmin(np.fmin(np.fmin(height_level_lo, temp_level_lo), daytime_level_lo), intensity_md)
rule2 = np.fmin(np.fmin(np.fmin(height_level_lo, temp_level_md), daytime_level_lo), intensity_md)
rule3 = np.fmin(np.fmin(np.fmin(height_level_lo, temp_level_hi), daytime_level_lo), intensity_lo)
rule4 = np.fmin(np.fmin(np.fmin(height_level_md, temp_level_lo), daytime_level_lo), intensity_hi)
rule5 = np.fmin(np.fmin(np.fmin(height_level_md, temp_level_md), daytime_level_lo), intensity_md)
rule6 = np.fmin(np.fmin(np.fmin(height_level_md, temp_level_hi), daytime_level_lo), intensity_lo)
rule7 = np.fmin(np.fmin(np.fmin(height_level_hi, temp_level_lo), daytime_level_lo), intensity_hi)
rule8 = np.fmin(np.fmin(np.fmin(height_level_hi, temp_level_md), daytime_level_lo), intensity_hi)
rule9 = np.fmin(np.fmin(np.fmin(height_level_hi, temp_level_hi), daytime_level_lo), intensity_md)
rule10 = np.fmin(np.fmin(temp_level_lo, daytime_level_hi), intensity_lo)
rule11 = np.fmin(np.fmin(temp_level_md, daytime_level_hi), intensity_none)
rule12 = np.fmin(np.fmin(temp_level_hi, daytime_level_hi), intensity_none)

# Rules aggregated into each level of our output
int_activation_none = np.fmax(rule12, rule11)
int_activation_low = np.fmax(np.fmax(rule3, rule6), rule10)
int_activation_md = np.fmax(np.fmax(np.fmax(rule1, rule2), rule5), rule9)
int_activation_hi = np.fmax(np.fmax(rule4, rule7), rule8)
int0 = np.zeros_like(x_intensity)

# Visualize this
fig, ax0 = plt.subplots(figsize=(8, 3))

# Specification of graph
ax0.fill_between(x_intensity, int0, int_activation_none, facecolor='y', alpha=0.7)
ax0.plot(x_intensity, int_activation_none, 'y', linewidth=0.5, linestyle='--')
ax0.fill_between(x_intensity, int0, int_activation_low, facecolor='b', alpha=0.7)
ax0.plot(x_intensity, int_activation_low, 'b', linewidth=0.5, linestyle='--', )
ax0.fill_between(x_intensity, int0, int_activation_md, facecolor='g', alpha=0.7)
ax0.plot(x_intensity, int_activation_md, 'g', linewidth=0.5, linestyle='--')
ax0.fill_between(x_intensity, int0, int_activation_hi, facecolor='r', alpha=0.7)
ax0.plot(x_intensity, int_activation_hi, 'r', linewidth=0.5, linestyle='--')
ax0.set_title('Output membership activity')

# Turn off top/right axes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

# Showing our graph
plt.tight_layout()
plt.show()


