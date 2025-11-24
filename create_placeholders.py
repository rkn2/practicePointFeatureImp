import matplotlib.pyplot as plt

def create_placeholder(filename, text):
    plt.figure(figsize=(10, 6))
    plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=20, wrap=True)
    plt.axis('off')
    plt.savefig(f'figures/{filename}', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created figures/{filename}")

if __name__ == "__main__":
    create_placeholder('questions.png', 'Research Questions\n(Placeholder Image)')
    create_placeholder('dataTypes.png', 'Data Types Overview\n(Placeholder Image)')
