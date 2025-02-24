import matplotlib.pyplot as plt
import numpy as np


def create_pie_chart(counter):
    filtered_counter = {k: v for k, v in counter.items() if v > 0}
    if not filtered_counter:
        print("No events to display.")
        return

    labels = list(filtered_counter.keys())
    sizes = list(filtered_counter.values())
    colors = plt.cm.tab20c(np.linspace(0, 1, len(labels)))

    plt.figure(figsize=(10, 7))
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        shadow=True
    )

    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')

    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')

    plt.axis('equal')
    plt.title("Event Distribution", fontsize=16, fontweight='bold', color='darkblue')
    plt.show()

