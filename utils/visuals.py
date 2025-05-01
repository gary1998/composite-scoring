# utils/visuals.py
"""
Visualization utilities for evaluation scores.
"""
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for server environments
import matplotlib.pyplot as plt
import os
from sklearn.metrics import precision_recall_curve, auc

STATIC_DIR = 'static'


def ensure_static():
    os.makedirs(STATIC_DIR, exist_ok=True)
    
def plot_delta_histogram(df, output_path='static/delta_hist.png'):
    """
    Plots histogram of Composite - Auto_Avg to visualize how often composite score outperforms traditional scores.
    """
    delta = df['COMPOSITE'] - df['auto_avg']
    plt.figure(figsize=(8, 5))
    plt.hist(delta, bins=10, color='#2980b9', edgecolor='black')
    plt.axvline(delta.mean(), color='red', linestyle='--', label=f'Mean Δ = {delta.mean():.2f}')
    plt.title('Distribution of Composite Score Advantage')
    plt.xlabel('Composite Score - Average(BLEU, ROUGE, METEOR)')
    plt.ylabel('Number of Responses')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path

def plot_scores(df, output_path='static/avg_scores.png'):
    """
    Plots a bar chart of the average BLEU, ROUGE, METEOR, and Composite scores across the dataset.
    
    Args:
        df (pd.DataFrame): DataFrame containing 'BLEU', 'ROUGE', 'METEOR', 'Composite' columns.
        output_path (str): Path where the plot image will be saved.

    Returns:
        str: File path to the saved image.
    """
    metric_names = ['BLEU', 'ROUGE-L', 'METEOR', 'COMPOSITE']
    averages = [df[m].mean() for m in metric_names]

    colors = ['#2980b9', '#27ae60', '#f39c12', '#8e44ad']

    plt.figure(figsize=(8, 5))
    bars = plt.bar(metric_names, averages, color=colors)

    # Annotate bars with values
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.01, f"{yval:.2f}", ha='center', va='bottom', fontsize=10)

    plt.title("Average Metric Scores Across Dataset")
    plt.ylabel("Score (0 to 1)")
    plt.ylim(0, 1.1)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # Ensure static directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path

def plot_avg_scores(df):
    ensure_static()
    metrics = ['BLEU', 'ROUGE-L', 'METEOR', 'COMPOSITE']
    avgs = [df[m].mean() for m in metrics]
    fig, ax = plt.subplots(figsize=(6,4))
    bars = ax.bar(metrics, avgs)
    ax.set_title('Average Metric Scores')
    ax.set_ylim(0,1)
    for b in bars:
        ax.text(b.get_x()+0.3, b.get_height()+0.02, f"{b.get_height():.2f}")
    path = os.path.join(STATIC_DIR, 'avg_scores.png')
    fig.savefig(path); plt.close(fig)
    return path


def plot_metric_correlations(df):
    ensure_static()
    import scipy.stats as st
    metrics = ['BLEU','ROUGE-L','METEOR','COMPOSITE']
    cors = [st.pearsonr(df[m], df['human_score'])[0] for m in metrics]
    fig, ax = plt.subplots(figsize=(6,4))
    bars = ax.bar(metrics, cors, color='green')
    ax.set_title('Correlation with Human Scores')
    ax.set_ylim(0,1)
    for b in bars:
        ax.text(b.get_x()+0.3, b.get_height()+0.02, f"{b.get_height():.2f}")
    path = os.path.join(STATIC_DIR, 'correlations.png')
    fig.savefig(path); plt.close(fig)
    return path


def plot_score_variability(df):
    ensure_static()
    metrics = ['BLEU','ROUGE-L','METEOR','COMPOSITE']
    stds = [df[m].std() for m in metrics]
    fig, ax = plt.subplots(figsize=(6,4))
    bars = ax.bar(metrics, stds, color='orange')
    ax.set_title('Score Variability (Std Dev)')
    for b in bars:
        ax.text(b.get_x()+0.3, b.get_height()+0.02, f"{b.get_height():.2f}")
    path = os.path.join(STATIC_DIR, 'variability.png')
    fig.savefig(path); plt.close(fig)
    return path


def plot_precision_recall(df, threshold=0.7):
    ensure_static()
    y_true = (df['human_score'] >= threshold).astype(int)
    y_scores = df['COMPOSITE']
    precision, recall, _ = precision_recall_curve(y_true, y_scores)
    pr_auc = auc(recall, precision)
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(recall, precision, lw=2)
    ax.set_title(f'Precision-Recall (AUC={pr_auc:.2f})')
    ax.set_xlabel('Recall'); ax.set_ylabel('Precision')
    path = os.path.join(STATIC_DIR, 'pr_curve.png')
    fig.savefig(path); plt.close(fig)
    return path
