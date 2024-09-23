import streamlit as st
import nest_asyncio
nest_asyncio.apply()

import pandas as pd
import numpy as np
import re
import os
import csv

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from bs4 import BeautifulSoup
from langchain_community.document_loaders.sitemap import SitemapLoader

from gensim import corpora, models

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import networkx as nx
from pyvis.network import Network

import matplotlib.pyplot as plt
import seaborn as sns

import base64

# ------------------------------
# Initialization and Setup
# ------------------------------

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# ------------------------------
# Helper Functions
# ------------------------------

def preprocess_text(text):
    """
    Preprocesses the input text by:
    - Converting to lowercase
    - Removing URLs
    - Removing non-alphabetic characters
    - Tokenizing
    - Removing stopwords and lemmatizing
    """
    if not isinstance(text, str):
        return ''
    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove non-alphabetic characters
    text = re.sub(r'[^a-z\s]', '', text)

    # Tokenize
    tokens = text.split()

    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    # Join tokens back to string
    cleaned_text = ' '.join(tokens)

    return cleaned_text

def extract_headings(content: BeautifulSoup) -> str:
    """
    Extracts text from h1, h2, h3, and p tags in the HTML content.
    """
    headings = content.find_all(['h1', 'h2', 'h3', 'p'])
    return "\n".join([heading.get_text() for heading in headings])

def assign_depth(G):
    """
    Assigns depth to each node based on BFS starting from the root node.
    """
    if 'Trimmed_Source' not in df.columns or df['Trimmed_Source'].empty:
        return {}
    root = df['Trimmed_Source'].iloc[0]
    depths = {}
    for node in G.nodes():
        try:
            depths[node] = nx.shortest_path_length(G, source=root, target=node)
        except nx.NetworkXNoPath:
            depths[node] = None
    return depths

def get_table_download_link(df, filename, text):
    """
    Generates a download link for a DataFrame as a CSV file.
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def make_unique_trimmed_source(series):
    """
    Ensures that all entries in the Trimmed_Source series are unique by appending an index to duplicates.
    """
    counts = {}
    unique = []
    for item in series:
        if item in counts:
            counts[item] += 1
            unique.append(f"{item}_{counts[item]}")
        else:
            counts[item] = 1
            unique.append(item)
    return unique

# ------------------------------
# Streamlit App Layout
# ------------------------------

st.title('Semantic Analysis of Website Content')

st.markdown("""
This app performs semantic analysis on website content by:
1. Loading and processing sitemap data.
2. Performing topic modeling.
3. Computing cosine similarity between pages.
4. Constructing and visualizing a semantic network.
5. Allowing downloads of all results.
""")

# ------------------------------
# User Inputs
# ------------------------------

st.sidebar.header('Input Parameters')

# Sitemap URL Input
sitemap_url = st.sidebar.text_input('Enter Sitemap URL', 'https://example.com/sitemap.xml')

# Cosine Similarity Threshold
cosine_threshold = st.sidebar.slider('Set Cosine Similarity Threshold', min_value=0.0, max_value=1.0, value=0.5, step=0.01)

# Number of Topics for LDA
num_topics = st.sidebar.number_input('Number of Topics for LDA', min_value=1, max_value=1000, value=10, step=1)

# ------------------------------
# Sitemap Loading and Caching
# ------------------------------

@st.cache_data(show_spinner=False)
def load_sitemap(url):
    """
    Loads the sitemap using SitemapLoader with XML parser.
    Saves the sitemap data to 'sitemap_docs.csv'.
    """
    sitemap_loader = SitemapLoader(web_path=url, parsing_function=extract_headings)
    docs = sitemap_loader.load()
    return docs

# Button to Run Analysis
if st.sidebar.button('Run Analysis'):

    st.info('Starting analysis...')

    # ------------------------------
    # Load Sitemap
    # ------------------------------
    try:
        with st.spinner('Loading sitemap...'):
            docs = load_sitemap(sitemap_url)
    except Exception as e:
        st.error(f"Error loading sitemap: {e}")
        st.stop()

    if not docs:
        st.warning('No documents found in the sitemap.')
        st.stop()

    st.success(f'Loaded {len(docs)} documents from sitemap.')

    # Save sitemap to CSV
    sitemap_csv = 'sitemap_docs.csv'
    with st.spinner('Saving sitemap to CSV...'):
        df_sitemap = pd.DataFrame({
            'Source': [doc.metadata.get('source', '') for doc in docs],
            'Location': [doc.metadata.get('loc', '') for doc in docs],
            'Last Modified': [doc.metadata.get('lastmod', '') for doc in docs],
            'Page Content': [doc.page_content.replace("\n", " ").replace("\r", "").replace("Skip to main content Skip to footer Contact","") for doc in docs]
        })
        df_sitemap.to_csv(sitemap_csv, index=False)
    st.success(f'Sitemap saved to `{sitemap_csv}`.')

    # ------------------------------
    # Process Documents
    # ------------------------------
    with st.spinner('Processing documents...'):
        # Read the saved sitemap CSV
        df = pd.read_csv(sitemap_csv)

        # Clean the 'Source' column to remove the base URL
        BASE_URL = sitemap_url.replace('sitemap.xml', '')

        def trim_url(url):
            if url.startswith(BASE_URL):
                return url[len(BASE_URL):]
            else:
                return url

        df['Trimmed_Source'] = df['Source'].apply(trim_url)

        # Make Trimmed_Source unique
        df['Trimmed_Source'] = make_unique_trimmed_source(df['Trimmed_Source'])

    st.success('Documents processed successfully.')

    # ------------------------------
    # Preprocess Text
    # ------------------------------
    with st.spinner('Preprocessing text...'):
        df['cleaned_content'] = df['Page Content'].apply(preprocess_text)
        df['tokens'] = df['cleaned_content'].apply(lambda x: x.split())

    st.success('Text preprocessing completed.')

    # ------------------------------
    # Topic Modeling
    # ------------------------------
    with st.spinner('Performing topic modeling...'):
        dictionary = corpora.Dictionary(df['tokens'])
        dictionary.filter_extremes(no_below=2, no_above=0.5)
        corpus = [dictionary.doc2bow(text) for text in df['tokens']]
        NUM_TOPICS = int(num_topics)
        lda_model = models.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=10, random_state=42)

    st.success('Topic modeling completed.')

    # Display the topics
    st.header('Topics Discovered')
    topics = lda_model.print_topics(num_words=5)
    topics_data = []
    for topic in topics:
        st.write(f'Topic {topic[0]}: {topic[1]}')
        topics_data.append({'Topic': topic[0], 'Keywords': topic[1]})

    # ------------------------------
    # Assign Dominant Topics
    # ------------------------------
    with st.spinner('Assigning dominant topics to documents...'):
        def format_topics_sentences(ldamodel, corpus, texts):
            topic_details = []

            for i, row in enumerate(ldamodel[corpus]):
                row = sorted(row, key=lambda x: (x[1]), reverse=True)
                for j, (topic_num, prop_topic) in enumerate(row):
                    if j == 0:  # dominant topic
                        wp = ldamodel.show_topic(topic_num)
                        topic_keywords = ", ".join([word for word, prop in wp])
                        topic_details.append([int(topic_num), round(prop_topic, 4), topic_keywords, texts[i]])
                    else:
                        break

            sent_topics_df = pd.DataFrame(topic_details, columns=['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords', 'Text'])
            return sent_topics_df

        df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=df['cleaned_content'])

    st.success('Dominant topics assigned to documents.')

    # ------------------------------
    # Compute Cosine Similarity
    # ------------------------------
    with st.spinner('Computing cosine similarity...'):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(df['cleaned_content'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        similarity_df = pd.DataFrame(cosine_sim, index=df['Trimmed_Source'], columns=df['Trimmed_Source'])

    st.success('Cosine similarity computed.')

    # ------------------------------
    # Semantic Network Construction
    # ------------------------------
    with st.spinner('Constructing semantic network...'):
        SIMILARITY_THRESHOLD = float(cosine_threshold)
        G_semantic = nx.Graph()

        # Add nodes with trimmed source
        for source in df['Trimmed_Source']:
            G_semantic.add_node(source)

        # Add edges based on similarity threshold
        for i in range(len(df)):
            for j in range(i+1, len(df)):
                sim_score = cosine_sim[i][j]
                if sim_score >= SIMILARITY_THRESHOLD:
                    source_node = df['Trimmed_Source'].iloc[i]
                    target_node = df['Trimmed_Source'].iloc[j]
                    G_semantic.add_edge(source_node, target_node, weight=sim_score)

    st.success(f'Semantic network constructed with {G_semantic.number_of_nodes()} nodes and {G_semantic.number_of_edges()} edges.')

    # ------------------------------
    # Interactive Visualization using pyvis
    # ------------------------------
    st.header('Semantic Network Visualization')
    with st.spinner('Generating semantic network visualization...'):
        net = Network(height='750px', width='100%', notebook=False)
        net.barnes_hut()

        # Add nodes with labels as trimmed sources
        for node in G_semantic.nodes():
            net.add_node(node, label=node)

        # Add edges with weights
        for source, target, data in G_semantic.edges(data=True):
            weight = data['weight']
            net.add_edge(source, target, value=weight)

        # Generate the interactive network
        net.show_buttons(filter_=['physics'])
        net.save_graph('semantic_network.html')

    st.success('Semantic network visualization generated.')

    # Display the interactive network
    with st.spinner('Displaying semantic network...'):
        HtmlFile = open('semantic_network.html', 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        st.components.v1.html(source_code, height=750, scrolling=True)
        st.write("Interactive semantic network displayed.")

    # ------------------------------
    # Save Outputs and Provide Download Links
    # ------------------------------
    st.header('Download Results')
    with st.spinner('Preparing files for download...'):
        prefix = "Semantic_Analysis"  # Customize as needed

        # 1. Cosine Similarity Matrix (Wide Format)
        SIMILARITY_CSV = f"{prefix}_cosine_similarity.csv"
        similarity_df.to_csv(SIMILARITY_CSV)
        st.markdown(get_table_download_link(similarity_df, SIMILARITY_CSV, 'Download Cosine Similarity Matrix'), unsafe_allow_html=True)

        # 2. Semantic Network Edges (Long Format)
        semantic_edges = pd.DataFrame(
            [(u, v, data['weight']) for u, v, data in G_semantic.edges(data=True)],
            columns=['Source', 'Target', 'Similarity']
        )
        SEMANTIC_EDGES_CSV = f"{prefix}_semantic_network_edges.csv"
        semantic_edges.to_csv(SEMANTIC_EDGES_CSV, index=False)
        st.markdown(get_table_download_link(semantic_edges, SEMANTIC_EDGES_CSV, 'Download Semantic Network Edges CSV'), unsafe_allow_html=True)

        # 3. Topic Modeling Results
        topic_modeling_csv = f"{prefix}_topic_modeling.csv"
        df_topic_sents_keywords.to_csv(topic_modeling_csv, index=False)
        st.markdown(get_table_download_link(df_topic_sents_keywords, topic_modeling_csv, 'Download Topic Modeling CSV'), unsafe_allow_html=True)

        # 4. Nodes with Depth Information
        node_depths = assign_depth(G_semantic)
        nodes_depth_df = pd.DataFrame(list(node_depths.items()), columns=['Node', 'Depth'])
        NODES_DEPTH_CSV = f"{prefix}_nodes_with_depth.csv"
        nodes_depth_df.to_csv(NODES_DEPTH_CSV, index=False)
        st.markdown(get_table_download_link(nodes_depth_df, NODES_DEPTH_CSV, 'Download Nodes with Depth CSV'), unsafe_allow_html=True)

        # 5. Semantic Network Visualization HTML
        with open('semantic_network.html', 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:text/html;base64,{b64}" download="semantic_network.html">Download Semantic Network HTML</a>'
            st.markdown(href, unsafe_allow_html=True)

    st.success('All files are ready for download.')

    # ------------------------------
    # Display Outputs
    # ------------------------------

    st.header('Topic Modeling Results')
    st.dataframe(df_topic_sents_keywords)

    st.header('Cosine Similarity Matrix')
    st.dataframe(similarity_df)
