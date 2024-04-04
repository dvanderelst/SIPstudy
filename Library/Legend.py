import matplotlib.pyplot as plt

class CustomLegend:
    def __init__(self):
        self.entries = []

    def add_entry(self, label, color=None, marker=None, linestyle=None, alpha=1.0):
        # Check if the label already exists
        if label in [entry['label'] for entry in self.entries]:
            #print(f"Entry with label '{label}' already exists.")
            return
        self.entries.append({
            'label': label,
            'color': color,
            'marker': marker,
            'linestyle': linestyle,
            'alpha': alpha
        })

    def draw_legend(self, loc='best'):
        legend_handles = []
        for entry in self.entries:
            kwargs = {}
            if entry['color'] is not None:
                kwargs['color'] = entry['color']
            if entry['marker'] is not None:
                kwargs['marker'] = entry['marker']
            if entry['linestyle'] is not None:
                kwargs['linestyle'] = entry['linestyle']
            if entry['alpha'] is not None:
                kwargs['alpha'] = entry['alpha']
            legend_handles.append(plt.Line2D([0], [0], **kwargs))

        labels = [entry['label'] for entry in self.entries]
        plt.legend(legend_handles, labels, loc=loc)

# # Example usage:
# # Create CustomLegend object
# custom_legend = CustomLegend()
#
# # Add legend entries with alpha level
# custom_legend.add_entry(label='Red Dot', color='red', marker='o', alpha=0.5)
# custom_legend.add_entry(label='Grey Line', color='grey', linestyle='-', alpha=0.7)
#
# # Draw the legend at a
