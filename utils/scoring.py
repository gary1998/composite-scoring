# utils/scoring.py
"""
Defines functions to compute BLEU, ROUGE, METEOR, and Composite scores on DataFrame.
"""
import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from nltk.translate.meteor_score import meteor_score
from nltk.tokenize import word_tokenize

# Smooth BLEU to handle short texts
SMOOTHER = SmoothingFunction().method1


def compute_all_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Iterate over DataFrame rows, compute BLEU, ROUGE, METEOR, and Composite.
    Expects columns: 'reference', 'generated', optional 'human_score' (0-1 scale).
    Returns new DataFrame with added columns.
    """
    bleu_list, rouge_list, meteor_list, composite_list = [], [], [], []

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    for _, row in df.iterrows():
        ref = row['reference']
        cand = row['generated']
        human_score = float(row.get('human_score', 0.5))  # Default mid-score if missing

        # Tokenize for metrics
        ref_tokens = word_tokenize(ref.lower())
        cand_tokens = word_tokenize(cand.lower())

        # BLEU with smoothing
        bleu = sentence_bleu([ref_tokens], cand_tokens, smoothing_function=SMOOTHER)

        # ROUGE-L F1 measure
        rouge_scores = scorer.score(ref, cand)
        rouge_l = rouge_scores['rougeL'].fmeasure

        # METEOR (tokenized)
        meteor = meteor_score([ref_tokens], cand_tokens)

        # Composite weighted average
        auto_avg = (bleu + rouge_l + meteor) / 3
        
        # Weights for composite score
        # Adjust these weights based on your preference
        alpha = 0.4
        beta = 0.6
        composite = alpha * auto_avg + beta * human_score

        # Append scores
        bleu_list.append(bleu)
        rouge_list.append(rouge_l)
        meteor_list.append(meteor)
        composite_list.append(composite)

    # Add new columns to DataFrame
    df = df.copy()
    df['BLEU'] = bleu_list
    df['ROUGE-L'] = rouge_list
    df['METEOR'] = meteor_list
    df['COMPOSITE'] = composite_list
    return df