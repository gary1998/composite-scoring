
# 🧠 Conversational AI Evaluation Wizard

**A Unified Framework for Evaluating Conversational AI Outputs Using Composite Scoring**

---

## 📌 About the Project

This project is a practical implementation of the master's thesis:

> **"A Comparative Study of Evaluation Metrics for Conversational AI: Toward a Unified Framework"**  
> 👨‍🎓 **Author**: Gaurav Goswami  
> 🏛️ M.Tech, Meerut Institute of Engineering & Technology  
> 📘 Roll No: 2300680105005  
> 📅 Year: 2025

The tool offers an interactive wizard-style web application to help researchers, developers, and evaluators analyze the quality of chatbot or conversational AI outputs using traditional metrics and a novel **Composite Score**.

---

## ❓ Motivation

Traditional NLP evaluation metrics like BLEU, ROUGE, and METEOR are widely used for machine translation and summarization. However, in **Conversational AI**, they often fall short because:

- BLEU penalizes paraphrasing and ignores context.
- ROUGE overemphasizes n-gram recall but misses tone.
- METEOR improves on synonyms but remains surface-level.
- Human feedback is subjective and not scalable.

### 🎯 Our Solution

We propose a **Composite Score** that integrates:

- BLEU  
- ROUGE-L  
- METEOR  
- Human Feedback Score (optional)  

Using tunable weights (α and β), the composite score better aligns with **human judgment** while remaining automatable.

---

## 🚀 Features

- Wizard-based, step-by-step interface
- Support for CSV uploads or synthetic data generation
- Automatic scoring using:
  - **BLEU**
  - **ROUGE-L**
  - **METEOR**
  - **Composite Score**
- In-depth visual analytics:
  - Average Scores
  - Correlation with Human Feedback
  - Variability (Std. Dev.)
  - Precision-Recall Curve
  - Composite vs Traditional Delta Histogram
- Detailed visual explanations
- Sample datasets (positive and negative)
- Sticky badges for author credit and restarting wizard

---

## 🛠️ Tech Stack

| Layer        | Tools/Libraries                        |
|--------------|----------------------------------------|
| Backend      | Python, Flask                          |
| Frontend     | HTML, CSS, Jinja2                      |
| NLP Metrics  | `nltk`, `rouge_score`, `scikit-learn`  |
| Visualization| `matplotlib`, `seaborn`                |
| Others       | `pandas`, `numpy`                      |

---

## 📂 Project Structure

```
project-root/
│
├── app.py                     # Flask application entry point
├── templates/
│   ├── index.html             # Landing page
│   ├── step1.html             # Upload / generate data
│   ├── step2.html             # Preview data
│   ├── step3.html             # Scoring
│   └── step4.html             # Visualization
│
├── utils/
│   ├── scoring.py             # BLEU, ROUGE, METEOR, Composite computation
│   ├── sample.py              # Synthetic data generation (positive/negative)
│   └── visuals.py             # Graph generation
│
├── static/
│   └── *.png                  # Generated chart images
│
├── datasets/
│   ├── sample_positive.csv    # High semantic match, low metric overlap
│   └── sample_negative.csv    # Poor semantic match, deceptive scores
│
├── README.md                  # ← YOU ARE HERE
└── requirements.txt           # Python dependencies
```

---

## 🧪 Dataset Types

### ✅ Positive Dataset
Pairs with high human_score (≥ 0.88) but where traditional metrics underperform due to rephrasings, synonyms, or reordered phrases.

### ❌ Negative Dataset
Pairs with **poor semantic match** but **misleadingly decent metric scores** due to surface n-gram overlap or structure, flagged by human_score (< 0.25).

---

## 📊 Composite Score Formula

```text
Composite = α * ((BLEU + ROUGE + METEOR)/3) + β * human_score
Where:
- α + β = 1
- α ∈ [0.6, 0.8], β ∈ [0.2, 0.4] (configurable)
```

This formula balances traditional metrics and human feedback, making it ideal for subjective conversational evaluations.

---

## 🧭 Usage Instructions

### 🔧 Install Dependencies

```bash
pip install -r requirements.txt
```

### 🚀 Start the Flask App

```bash
python app.py
```

Then open your browser and go to:

```
http://localhost:5000/
```

### 📝 Step-by-Step Flow

1. **Step 1** – Upload your own CSV or generate synthetic data  
2. **Step 2** – Preview dataset and validate columns  
3. **Step 3** – Compute BLEU, ROUGE, METEOR, Composite  
4. **Step 4** – View interactive analytics & metric comparison  

---

## 🧩 Customization

- Modify weights `α` and `β` in `scoring.py`
```python
# Weights for composite score
# Adjust these weights based on your preference
alpha = 0.4
beta = 0.6
```
---
