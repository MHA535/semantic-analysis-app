
# Semantic Analysis of Website Content

## Overview
This project is a web application built with **Streamlit** for performing **semantic analysis** on website content. It allows users to load website sitemaps, analyze content, and visualize relationships between pages based on semantic similarity. The app includes features for topic modeling, cosine similarity calculations, and network visualizations.

### LDA Topic Modeling

**Latent Dirichlet Allocation (LDA)** is a statistical method for identifying abstract topics in a collection of documents. It assumes that each document is a mixture of a few topics, and each topic is a mixture of words. LDA helps identify key topics across a website's content.

#### Benefits of LDA for Website Content Analysis:
- **Content Themes**: Discover the main topics discussed on the website and check if they align with user intent.
- **SEO Improvement**: Identify content gaps and optimize topics for better search engine rankings.
- **Content Organization**: Group similar content into silos for better SEO and user navigation.

### Cosine Similarity

**Cosine Similarity** measures how similar two documents are by calculating the cosine of the angle between two vectors in multi-dimensional space. These vectors are created using TF-IDF (Term Frequency-Inverse Document Frequency) scores. A similarity score of 1 means identical content, while 0 means no similarity.

#### Uses of Cosine Similarity in Website Content Analysis:
- **Duplicate Content Detection**: Identify similar pages to avoid search engine penalties for duplicate content.
- **Content Gap Analysis**: Discover gaps between related topics and create new content accordingly.
- **Internal Linking**: Link pages with high similarity to enhance SEO and improve user navigation.

### Application Benefits

- **Topic Optimization**: Align your content with important topics to boost user engagement and SEO.
- **Content Strategy Refinement**: Identify underrepresented topics and combine high-similarity pages to prevent content cannibalization.
- **SEO and User Flow Improvement**: Use semantic relationships to build better internal linking and enhance the site's structure.

### Visualization Features
- **Semantic Network**: Interactive graph displaying relationships between pages based on their semantic similarity.
- **Topics Discovered**: Displays the topics identified across website content.

### Downloadable Outputs
The app provides several downloadable files:
- **Cosine Similarity Matrix**: A CSV file containing similarity scores between pages.
- **Semantic Network Edges**: A CSV file representing relationships between pages.
- **Topic Modeling Results**: A CSV file showing topics assigned to each page.
- **Nodes with Depth**: A CSV of nodes and their depth in the semantic network.
- **Semantic Network Visualization**: An HTML file of the interactive graph.

## Features
- Load and process **sitemap data** from a website.
- Perform **LDA topic modeling** to discover key topics.
- Calculate **cosine similarity** between website pages.
- Build an **interactive semantic network** using **Pyvis**.
- Download analysis results, including cosine similarity matrices, topic models, and semantic network edges.

## Dependencies
To run this project, you'll need the following libraries:
- **Streamlit**: Web app framework.
- **Nest Asyncio**: Allows running asyncio event loops in notebooks.
- **NLTK**: For text preprocessing, including stopwords and lemmatization.
- **BeautifulSoup**: For HTML parsing.
- **Gensim**: For LDA topic modeling.
- **Scikit-learn**: For cosine similarity calculations.
- **NetworkX**: For graph construction.
- **Pyvis**: For graph visualization.
- **Matplotlib & Seaborn**: For data visualization.
- **Pandas**: For data manipulation.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MHA535/semantic-analysis-app.git
   cd semantic-analysis-app
   ```

2. Install the dependencies:
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
- **Number of Topics**: Specify the number of topics for LDA topic modeling (default: 10). For websites, this should match the number of articles on the site.

### 2. Running Analysis
After setting the inputs, click the **Run Analysis** button to begin.

### 3. Analysis Steps
- **Sitemap Loading**: Load website URLs from the sitemap and extract headings.
- **Text Preprocessing**: Clean and process content by removing stopwords, URLs, and performing lemmatization.
- **Topic Modeling**: Use LDA to identify topics across the website.
- **Cosine Similarity**: Measure similarity between pages based on their TF-IDF vectors.
- **Semantic Network**: Create a graph where nodes represent pages, and edges represent high cosine similarity.

## License
This project is licensed under the MIT License.
































