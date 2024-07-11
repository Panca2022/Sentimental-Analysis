
<h1>Sentiment Analysis of Amazon Reviews for Intel Processors</h1>

<h2>Project Description</h2>
<p>This project conducts sentiment analysis on Amazon reviews for Intel processors using TextBlob, a Python NLP library. It categorizes reviews into Very Positive, Positive, Neutral, Negative, and Very Negative to provide insights for product improvement and marketing strategies. Visualizations highlight sentiment distribution to enhance understanding of customer feedback.</p>

<h2>Project Structure</h2>
<ul>
    <li><strong>data/</strong>: Contains the dataset of Amazon reviews in Excel format.</li>
    <li><strong>notebooks/</strong>: Jupyter notebooks for data analysis and visualization.</li>
    <li><strong>scripts/</strong>: Python scripts for sentiment analysis and generating visualizations.</li>
    <li><strong>results/</strong>: Output files including graphs and processed data.</li>
    <li><strong>README.md</strong>: Project overview and instructions.</li>
</ul>

<h2>Requirements</h2>
<p>Python 3.7+<br>
    pandas<br>
    matplotlib<br>
    textblob<br>
    jupyter</p>
<p>Install the required packages using:</p>
<pre><code>pip install pandas matplotlib textblob jupyter</code></pre>

<h2>Getting Started</h2>
<ol>
    <li>Clone the repository:
        <pre><code>git clone https://github.com/yourusername/sentiment-analysis-intel-reviews.git
cd sentiment-analysis-intel-reviews</code></pre>
    </li>
    <li>Place your data file (<code>sentiment_analysis_12gen_DesktopProcessor.xlsx</code>) in the <code>data/</code> directory.</li>
    <li>Open the Jupyter notebook:
        <pre><code>jupyter notebook notebooks/SentimentAnalysis.ipynb</code></pre>
    </li>
    <li>Run the cells in the notebook to perform the sentiment analysis and generate visualizations.</li>
</ol>

<h2>Usage</h2>
<h3>Sentiment Analysis Script</h3>
<p>To run the sentiment analysis script and generate a pie chart of sentiment distribution:</p>
<pre><code>python scripts/sentiment_analysis.py</code></pre>

<h3>Results</h3>
<p>The sentiment analysis results and visualizations are saved in the <code>results/</code> directory. You can find:</p>
<ul>
    <li><code>sentiment_distribution.png</code>: Pie chart showing the sentiment distribution of reviews.</li>
    <li>Processed data files with sentiment scores and categories.</li>
</ul>

<h2>Conclusion</h2>
<p>This project demonstrates how to use TextBlob for sentiment analysis of product reviews, providing valuable insights for product development and marketing. The visualizations help in understanding the sentiment trends and identifying key areas for improvement based on customer feedback.</p>

<p>Feel free to reach out if you have any questions or need further assistance with this project.</p>
