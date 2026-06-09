import matplotlib.pyplot as plt
labels_100 = ['salty','Sweet']
sizes_50 = [19,31]
sizes_100 = [39,61]
sizes_500 = [226,274]
fig, axes = plt.subplots(1, 3, figsize=(10, 5))
colors = ['#1f77b4', '#ff7f0e']
explode = (0.05, 0)

# Top 50 graph
axes[0].pie(sizes_50, explode = explode, labels=labels_100, colors=colors, autopct='%1.1f%%', startangle=85, textprops={'fontsize': 12})
axes[0].set_title('Top 50 highest-rated', fontsize = 18)
# Top 100 graph
axes[1].pie(sizes_100, explode = explode, labels=labels_100, colors=colors, autopct='%1.1f%%', startangle=85, textprops={'fontsize': 12})
axes[1].set_title('Top 100 highest-rated', fontsize = 18)

# Top 500 graph
axes[2].pie(sizes_500, explode = explode, labels=labels_100, colors=colors, autopct='%1.1f%%', startangle=85, textprops={'fontsize': 12})
axes[2].set_title('Top 500 highest-rated', fontsize = 18)
plt.tight_layout()
plt.show()