from rules import *

aggregated = np.fmax(np.fmax(int_activation_none, int_activation_low),
                     np.fmax(int_activation_md, int_activation_hi))

# Calculate defuzzified result
tip = fuzz.defuzz(x_intensity, aggregated, 'centroid')
tip_activation = fuzz.interp_membership(x_intensity, aggregated, tip)  # for plot

# Visualize this
fig, ax0 = plt.subplots(figsize=(8, 4))

ax0.plot(x_intensity, intensity_lo, 'b', linewidth=0.5, linestyle='--', )
ax0.plot(x_intensity, intensity_none, 'y', linewidth=0.5, linestyle='--', )
ax0.plot(x_intensity, intensity_md, 'g', linewidth=0.5, linestyle='--')
ax0.plot(x_intensity, intensity_hi, 'r', linewidth=0.5, linestyle='--')
ax0.fill_between(x_intensity, int0, aggregated, facecolor='Orange', alpha=0.7)
ax0.plot([tip, tip], [0, tip_activation], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Aggregated membership and result (line)')

# Turn off top/right axes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()

plt.show()