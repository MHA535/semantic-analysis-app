Semantic Analysis of Website Content
Overview
This project is a web-based application built with Streamlit for performing semantic analysis on website content. It allows users to load website sitemaps, analyze the content, and visualize relationships between pages based on their semantic similarity. The app provides features for topic modeling, cosine similarity calculations, and network visualizations.

Features
Load and process website sitemap data.
Perform topic modeling using Latent Dirichlet Allocation (LDA).
Compute cosine similarity between website pages to measure their semantic closeness.
Build an interactive semantic network visualization using Pyvis.
Download results, including cosine similarity matrices, topic modeling outputs, and semantic network edges.
Dependencies
The project requires the following libraries:

Streamlit: Web app framework
Nest Asyncio: For running asyncio event loops in notebooks
NLTK: For text processing (stopwords, lemmatization)
BeautifulSoup: For parsing HTML content
Gensim: For topic modeling
Scikit-learn: For cosine similarity calculations
NetworkX: For graph construction
Pyvis: For interactive graph visualization
Matplotlib & Seaborn: For plotting
Pandas: For data manipulation
Installation
Clone the repository:

bash
Copy code
git clone <repo-url>
cd <repo-directory>
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the app:

bash
Copy code
streamlit run app.py
Usage
1. Input Parameters
Sitemap URL: Provide a sitemap URL (e.g., https://example.com/sitemap.xml).
Cosine Similarity Threshold: Set the threshold to filter page similarity connections (default: 0.5).
Number of Topics: Define the number of topics for LDA topic modeling (default: 10).
2. Running Analysis
Press the Run Analysis button to start the analysis after setting your inputs.
3. Analysis Process
The app performs the following:

Sitemap Loading: Loads website URLs from the provided sitemap and extracts headings.
Text Preprocessing: Cleans and processes the page content by removing stopwords, URLs, and lemmatizing the text.
Topic Modeling: Uses LDA to identify topics across the website content.
Cosine Similarity: Measures semantic similarity between pages based on TF-IDF vectors.
Semantic Network: Constructs a graph where nodes are pages, and edges represent high cosine similarity between them.
LDA Topic Modeling
Latent Dirichlet Allocation (LDA) is a statistical model used for identifying abstract topics that occur in a collection of documents. It works by assuming that each document is a mixture of a few topics, and each topic is a mixture of words. By analyzing the words and patterns in the text, LDA identifies which topics are discussed across the content.

How LDA Helps with Website Content Analysis:
Understanding Content Themes: By applying LDA to website pages, you can identify the key topics that are prevalent across the entire site. This helps in understanding what your website focuses on and whether it aligns with the intended audience's needs.
Improving SEO: Knowing the topics that appear frequently can help optimize content for search engines. If certain important topics are missing, you can enrich your content by addressing those areas.
Content Organization: LDA can assist in grouping related content together, helping with the creation of content silos, which is crucial for improving user experience and search engine rankings.
Cosine Similarity
Cosine Similarity is a metric used to measure how similar two documents are, based on their content. It calculates the cosine of the angle between two vectors in a multi-dimensional space, where the vectors represent the TF-IDF (Term Frequency-Inverse Document Frequency) of the text. A cosine similarity score of 1 means that two pages are identical, while a score of 0 means they share no similarities.

How Cosine Similarity Helps with Website Content Analysis:
Detecting Duplicate Content: High cosine similarity scores between two pages may indicate duplicate or very similar content. Search engines penalize sites for duplicate content, so identifying and addressing these can improve your site's SEO.
Content Gap Analysis: By identifying pages with low cosine similarity, you can detect content gaps where different parts of your website may not cover the same topics, allowing you to create new content to bridge those gaps.
Internal Linking Strategy: Pages with high cosine similarity should be internally linked, as they share related topics. This helps with topic clustering, improving user navigation and potentially enhancing rankings for interconnected pages.
How These Techniques Aid Website Content Analysis
By using LDA topic modeling and cosine similarity together in website content analysis, you can:

Identify and optimize key topics: LDA helps you discover which topics are covered across the site, ensuring that your content is focused on the right themes.
Refine content strategy: You can enhance underrepresented topics or combine pages with high similarity to avoid content cannibalization.
Improve internal linking and user experience: Linking pages with similar content boosts the SEO performance and helps users find relevant information faster.
Enhance SEO: Both techniques enable you to reduce duplicate content and improve keyword relevance, helping search engines better understand and rank your site.
These insights lead to more cohesive content, better user experience, and improved search engine optimization for the website.

4. Visualizing Results
Semantic Network: View an interactive semantic network graph that displays relationships between pages based on their similarity.
Topics Discovered: The app shows the topics discovered in the website content.
5. Downloadable Outputs
The app generates several downloadable files:

Cosine Similarity Matrix: A CSV of similarity scores between pages.
Semantic Network Edges: A CSV file of the relationships between pages based on similarity.
Topic Modeling Results: CSV containing the topics assigned to each page.
Nodes with Depth: CSV of nodes and their depth in the semantic network.
Semantic Network Visualization: An HTML file of the interactive network visualization.
