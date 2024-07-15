import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize
import csv
import os


# Function to count syllables in a word
def count_syllables(word):
    vowels = 'aeiouy'
    count = 0
    previous_char_was_vowel = False
    for char in word.lower():
        if char in vowels:
            if not previous_char_was_vowel:
                count += 1
                previous_char_was_vowel = True
        else:
            previous_char_was_vowel = False
    # Adjust count for words ending with 'e'
    if word.lower().endswith('e'):
        count -= 1
    # Ensure count is at least 1
    return max(count, 1)



# Load stop words from text files
stop_words_files = [
    "StopWords_Auditor.txt",
    "StopWords_Currencies.txt",
    "StopWords_DatesandNumbers.txt",
    "StopWords_Generic.txt",
    "StopWords_GenericLong.txt",
    "StopWords_Geographic.txt",
    "StopWords_Names.txt"
]

stop_words = []
for file_name in stop_words_files:
    with open(file_name, "r", encoding="latin1") as file:
        stop_words.extend(file.read().split())

# Load positive words from text file
positive_words_file = "positive-words.txt"
with open(positive_words_file, "r", encoding="latin1") as file:
    positive_words = file.read().split()

# Load negative words from text file
negative_words_file = "negative-words.txt"
with open(negative_words_file, "r", encoding="latin1") as file:
    negative_words = file.read().split()




# Function to perform textual analysis
def analyze_text_file(file_name):
    # Read text from file
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()

    # Calculate scores and variables
    positive_score = sum(1 for word in word_tokenize(text.lower()) if word in positive_words)
    negative_score = sum(1 for word in word_tokenize(text.lower()) if word in negative_words)
    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    words = [word for word in word_tokenize(text.lower()) if word not in stop_words]
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)
    sentences = sent_tokenize(text)
    avg_sentence_length = sum(len(word_tokenize(sentence)) for sentence in sentences) / len(sentences)
    complex_words = [word for word in words if count_syllables(word) > 2]
    percentage_complex_words = (len(complex_words) / len(words)) * 100
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = len(words) / len(sentences)
    complex_word_count = len(complex_words)
    word_count = len(words)
    total_syllables = sum(count_syllables(word) for word in words)
    syllables_per_word = total_syllables / len(words)
    personal_pronouns = sum(1 for word in words if word.lower() in ["i", "we", "my", "ours", "us"])
    avg_word_length = sum(len(word) for word in words) / len(words)

    return [positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_length,
            percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count, word_count,
            syllables_per_word, personal_pronouns, avg_word_length]


# List to store results
results = []

# Loop through each text file
for i in range(1, 101):
    file_name = f"blackassign{str(i).zfill(4)}.txt"
    if os.path.exists(file_name):
        analysis_result = analyze_text_file(file_name)
        results.append(analysis_result)

# Write results to CSV file
with open("analysis_results.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["File", "Positive Score", "Negative Score", "Polarity Score", "Subjectivity Score",
                     "Average Sentence Length", "Percentage of Complex Words", "Fog Index",
                     "Average Number of Words Per Sentence", "Complex Word Count", "Word Count",
                     "Syllables Per Word", "Personal Pronouns", "Average Word Length"])
    for i, result in enumerate(results, start=1):
        writer.writerow([f"blackassign{str(i).zfill(4)}"] + result)