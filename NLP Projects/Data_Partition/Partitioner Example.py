import pandas as pd         #python package for data analysis
import neattext as nt       #python package for text cleaning                                                   
import nltk                 #python package for text analysis
nltk.download('punkt')      #nltk dependency for sentence tokenization
import PyPDF2               #python package for extracting data from pdf 
import os                   #importing os to deal with system directories
import re                   #re-> to handle regular expressions
import tabula               #python package for tabular data extraction from pdf
from sklearn.feature_extraction.text import TfidfVectorizer        #sklearn function for TF-IDF
from sklearn.metrics.pairwise import cosine_similarity             #to find similarity among the chunks

partitions_similarity=[]           #creating storage for partitions similarity



def pre_processing(text):
    text=nt.fix_contractions(text)                   #I'm --> I am
    text=nt.remove_special_characters(text)
    text=nt.remove_stopwords(text)
    text=nt.remove_shortwords(text,3)
    text=nt.remove_numbers(text)
    text=nt.remove_urls(text)
    text=nt.remove_non_ascii(text)
    return text


def extract_tables(file_name):
    df = tabula.read_pdf(file_name,pages='all')
    return df


def extract_text(pdf_path):
    text=''
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfFileReader(f)
        # Get the number of pages in the PDF file
        num_pages = pdf_reader.getNumPages()
        for page_num in range(num_pages):
            # Get the page object
            page_obj = pdf_reader.getPage(page_num)
            # Extract the text from the page
            text += page_obj.extract_text()
    return text


    def split_into_chunks(pdf_text):
        # Split the input string into sentences
        sentences = nltk.sent_tokenize(pdf_text)
        # Split each sentence into chunks of at most 1600 characters
        chunks = []
        current_chunk = ''
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= 1600:
                current_chunk += ' ' + sentence
            else:
                if len(current_chunk) >= 100:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk += ' ' + sentence
        # Add the last chunk
        if len(current_chunk) >= 100:
            chunks.append(current_chunk.strip())
        return chunks
    
def merge_chunks(chunks, similarity_matrix, most_similar):
    merged_chunks = []
    merged_indices = set()
    
    for i in range(len(chunks)):
        if i not in merged_indices:
            current_chunk = chunks[i]
            merged_indices.add(i)
            j = most_similar[i]
            while j not in merged_indices and similarity_matrix[i][j] > 0.5:
                current_chunk += ' ' + chunks[j]
                merged_indices.add(j)
                j = most_similar[j]
            merged_chunks.append(current_chunk)
    
    return merged_chunks    
    
def get_paritions_similarity(partitions):
    # Use TfidfVectorizer to compute the TF-IDF matrix for the chunks
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(partitions)
    # Compute the cosine similarity matrix for the chunks
    similarity_matrix= cosine_similarity(tfidf_matrix)
    most_similar = similarity_matrix.argsort()[:, -2]
    merged_partitions = merge_chunks(partitions, similarity_matrix, most_similar)


    for i in range(len(partitions)):
        for j in range(len(partitions)):
            if i != j:
                similarity = similarity_matrix[i][j]
                partitions_similarity.append(f"Similarity between chunk {i+1} and chunk {j+1}: {similarity:.2f}")
    
    return partitions_similarity,merged_partitions
    
    
def merge_chunks(chunks, similarity_matrix, most_similar):
    merged_chunks = []
    merged_indices = set()

    for i in range(len(chunks)):
        if i not in merged_indices:
            current_chunk = chunks[i]
            merged_indices.add(i)
            j = most_similar[i]
            while j not in merged_indices and similarity_matrix[i][j] > 0.5:
                current_chunk += ' ' + chunks[j]
                merged_indices.add(j)
                j = most_similar[j]
            merged_chunks.append(current_chunk)

    return merged_chunks   
    
def save_partitions(partitions, file_path):
    file_dir, file_name = os.path.split(file_path)
    file_root, file_ext = os.path.splitext(file_name)
    for i, partition in enumerate(partitions):
        partition_file_name = f"{file_root}_part_{i+1}{file_ext}"
        partition_file_path = os.path.join(file_dir, partition_file_name)
        with open(partition_file_path, 'w', encoding='utf-8') as f:
            f.write(partition)   

    
        
##########################################################################################################
pdf_path ='3404555.3404559.pdf'
text = extract_text(pdf_path)
#######################################################################################################
tables=extract_tables(pdf_path)
for i,j in enumerate(tables):
    j.to_csv(f'tabl{i}.csv')      #saving the each table
#########################################################################################################
partitions = partition_text(text)
#########################################################################################################
#un-comment this code if you want to perform preprocessing on each partition
#for index,part in enumerate(partitions):
 #   partitions[index]=pre_processing(part)
#########################################################################################################
partitions_sim,merged_partitions=get_paritions_similarity(partitions)
#########################################################################################################
save_partitions(partitions,pdf_path)
####################################################################################################