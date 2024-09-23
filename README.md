
# Semantic Analysis of Website Content

## Overview
This project is a web-based application built with **Streamlit** for performing **semantic analysis** on website content. It allows users to load website sitemaps, analyze the content, and visualize relationships between pages based on their semantic similarity. The app provides features for topic modeling, cosine similarity calculations, and network visualizations.


### LDA Topic Modeling

**Latent Dirichlet Allocation (LDA)** is a statistical model used for identifying abstract topics that occur in a collection of documents. It assumes that each document is a mixture of a few topics, and each topic is a mixture of words. By analyzing word patterns, LDA identifies topics across the content.

#### How LDA Helps with Website Content Analysis:
- **Understanding Content Themes**: LDA helps identify key topics discussed on the website and whether they align with user intent.
- **Improving SEO**: Recognizing frequently discussed topics allows content optimization and identification of content gaps.
- **Content Organization**: Grouping content by topics assists in creating content silos, improving user experience and SEO.

### Cosine Similarity

**Cosine Similarity** is a metric used to measure how similar two documents are, based on their content. It calculates the cosine of the angle between two vectors in multi-dimensional space, where the vectors represent the TF-IDF (Term Frequency-Inverse Document Frequency) of the text. A cosine similarity score of 1 indicates identical content, while a score of 0 indicates no similarity.

#### How Cosine Similarity Helps with Website Content Analysis:
- **Detecting Duplicate Content**: Identifying similar pages helps prevent duplicate content penalties from search engines.
- **Content Gap Analysis**: Lower similarity scores between related topics indicate opportunities to bridge content gaps.
- **Internal Linking Strategy**: Pages with high similarity should be internally linked to improve SEO and user navigation.

### How These Techniques Aid Website Content Analysis:

- **Identify and optimize key topics**: Ensure your content aligns with important topics to improve engagement and SEO.
- **Refine content strategy**: Address underrepresented topics or combine pages with high similarity to avoid content cannibalization.
- **Improve internal linking and user experience**: Linking similar content improves the website's structure, enhancing SEO performance and user flow.
- **Enhance SEO**: Reducing duplicate content and improving keyword relevance aids in better rankings and search engine understanding of the website's content.


### 4. Visualizing Results
- **Semantic Network**: View an interactive semantic network graph that displays relationships between pages based on their similarity.
- **Topics Discovered**: The app shows the topics discovered in the website content.

### 5. Downloadable Outputs
The app generates several downloadable files:
- **Cosine Similarity Matrix**: A CSV of similarity scores between pages.
- **Semantic Network Edges**: A CSV file of the relationships between pages based on similarity.
- **Topic Modeling Results**: CSV containing the topics assigned to each page.
- **Nodes with Depth**: CSV of nodes and their depth in the semantic network.
- **Semantic Network Visualization**: An HTML file of the interactive network visualization.
- 
## Features
- Load and process website **sitemap data**.
- Perform **topic modeling** using Latent Dirichlet Allocation (LDA).
- Compute **cosine similarity** between website pages to measure their semantic closeness.
- Build an **interactive semantic network** visualization using **Pyvis**.
- Download results, including cosine similarity matrices, topic modeling outputs, and semantic network edges.

## Dependencies
The project requires the following libraries:
- **Streamlit**: Web app framework.
- **Nest Asyncio**: For running asyncio event loops in notebooks.
- **NLTK**: For text processing (stopwords, lemmatization).
- **BeautifulSoup**: For parsing HTML content.
- **Gensim**: For topic modeling.
- **Scikit-learn**: For cosine similarity calculations.
- **NetworkX**: For graph construction.
- **Pyvis**: For interactive graph visualization.
- **Matplotlib & Seaborn**: For plotting.
- **Pandas**: For data manipulation.

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage

### 1. Input Parameters
- **Sitemap URL**: Provide a sitemap URL (e.g., `https://example.com/sitemap.xml`).
- **Cosine Similarity Threshold**: Set the threshold to filter page similarity connections (default: 0.5).
- **Number of Topics**: Define the number of topics for LDA topic modelling (default: 10), for Website make it equal to no of Article on the website.

### 2. Running Analysis
- Press the **Run Analysis** button to start the analysis after setting your inputs.

### 3. Analysis Process
The app performs the following steps:
- **Sitemap Loading**: Loads website URLs from the provided sitemap and extracts headings.
- **Text Preprocessing**: Cleans and processes the page content by removing stopwords, URLs, and lemmatizing the text.
- **Topic Modeling**: Uses LDA to identify topics across the website content.
- **Cosine Similarity**: Measures semantic similarity between pages based on TF-IDF vectors.
- **Semantic Network**: Constructs a graph where nodes are pages, and edges represent high cosine similarity between them.




## License
This project is licensed under the MIT License.

AI Disclaimer:This Readme is rewritten with the help of AI
