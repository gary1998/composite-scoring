# app.py
"""
Flask Web App: Conversational AI Evaluation Wizard

This application guides users through a 4-step wizard:
1. Upload or generate sample conversation data (CSV).
2. Preview the uploaded/generated data.
3. Compute evaluation metrics (BLEU, ROUGE, METEOR, Composite) on the data.
4. Visualize average scores with explanatory charts.
"""
from flask import Flask, render_template, request, redirect, url_for, session
import os
import pandas as pd
from werkzeug.utils import secure_filename
from utils.scoring import compute_all_scores
from utils.visuals import plot_delta_histogram, plot_metric_correlations, plot_precision_recall, plot_score_variability

import nltk
nltk.download('punkt_tab')
nltk.download('wordnet')

# Initialize Flask app and configuration
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'a_secure_default_key')  # Use env var in production
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    """
    Landing page: Redirect to Step 1 of the wizard.
    """
    return render_template('index.html')


@app.route('/step1', methods=['GET', 'POST'])
def step1():
    """
    Step 1: Data Import
    - Option A: Upload a CSV file with columns ['reference', 'generated', 'human_score (optional)'].
    - Option B: Generate built-in sample data.
    """
    if request.method == 'POST':
        # Handle file upload
        if 'datafile' in request.files:
            file = request.files['datafile']
            if file and file.filename.lower().endswith('.csv'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                session['filepath'] = filepath
                return redirect(url_for('step2'))
        # Handle sample data generation
        elif request.form.get('generate') == 'yes':
            from utils.sample import generate_sample_data
            df = pd.DataFrame(generate_sample_data())
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'sample_data.csv')
            df.to_csv(filepath, index=False)
            session['filepath'] = filepath
            return redirect(url_for('step2'))

    # GET: render upload/generate options
    return render_template('step1.html')


@app.route('/step2')
def step2():
    """
    Step 2: Data Preview
    Displays first 10 rows of the loaded conversation dataset for sanity check.
    """
    filepath = session.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return redirect(url_for('step1'))

    df = pd.read_csv(filepath)
    return render_template('step2.html', tables=[df.to_html(classes='table table-striped')], titles=df.columns.values)


@app.route('/step3')
def step3():
    """
    Step 3: Compute Scores
    Runs automated metrics (BLEU, ROUGE, METEOR) and combines with human_score (if present).
    Saves scored CSV and displays top 10 scored entries.
    """
    filepath = session.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return redirect(url_for('step1'))

    df = pd.read_csv(filepath)

    # Compute scores for each row
    scored_df = compute_all_scores(df)

    # Persist scored results
    scored_path = filepath.replace('.csv', '_scored.csv')
    scored_df.to_csv(scored_path, index=False)
    session['scored_file'] = scored_path
    
    return render_template('step3.html', tables=[scored_df.to_html(classes='table table-bordered')], titles=scored_df.columns.values)


@app.route('/step4')
def step4():
    import pandas as pd
    from utils.visuals import plot_scores
    import matplotlib.pyplot as plt

    filepath = session.get('scored_file')
    if not filepath or not os.path.exists(filepath):
        return redirect(url_for('step1'))
    
    df = pd.read_csv(filepath)
    
    print(df.columns)
    # Calculate average of BLEU, ROUGE, METEOR
    df['auto_avg'] = df[['BLEU', 'ROUGE-L', 'METEOR']].mean(axis=1)

    # Compare composite to auto_avg for arrow icons
    df['delta_icon'] = df.apply(
        lambda row: '✅' if row['COMPOSITE'] >= row['auto_avg'] else '❌',
        axis=1
    )

    # Generate charts
    chart_delta = plot_delta_histogram(df)
    chart_avg = plot_scores(df)  # your avg bar chart
    chart_corr = plot_metric_correlations(df)
    chart_var = plot_score_variability(df)
    chart_pr = plot_precision_recall(df)

    # These should already be created by your chart generation functions.
    # If not, we can code them next.
    return render_template('step4.html',
                           chart_avg=chart_avg,
                           chart_corr=chart_corr,
                           chart_var=chart_var,
                           chart_pr=chart_pr,
                           chart_delta=chart_delta,
                           final_df=df.to_dict(orient='records'))


if __name__ == '__main__':
    port = os.getenv('PORT', 5000)
    # Run Flask development server
    app.run(host='0.0.0.0', port=port, debug=True)