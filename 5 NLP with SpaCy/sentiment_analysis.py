import spacy 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from spacytextblob.spacytextblob import SpacyTextBlob

# Function to perform setiment analysis by using TextBlob
def analyze_sentiment(text):
    polarity = nlp(text)._.blob.polarity  # Sentiment score between -1 and 1

# Text required to be slight stronger tendency to classify as positve or negative
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    else:
        return "Neutral"
        
# Function to presprocessing text
def preprocess_text(text):
    doc = nlp(text.lower().strip().strip('"'))  # Convert to lowercase and remove whitespace
    tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]  # Remove stopwords & non-alphabetic words
    return " ".join(tokens)

# Setting up spaCy with textblob library
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("spacytextblob")

df = pd.read_csv('amazon_product_reviews.csv')

# Removing unused column
df.drop(['dateAdded',
         'dateUpdated',
         'asins',
         'categories',
         'imageURLs',
         'keys',
         'reviews.didPurchase',
         'reviews.dateSeen',
         'reviews.id',
         'reviews.sourceURLs',
         'reviews.username',
         'reviews.doRecommend',
         'reviews.numHelpful',
         'sourceURLs'
        ],axis=1, inplace=True)

print("Distribution of reviews rating")
print(df.loc[:,['id','reviews.rating']].groupby('reviews.rating').count())

# Removing any data with empty "reviews" and extrating review data
df.dropna(subset=['reviews.text'])

# Cleansing reviews.text column
df['reviews.text.cleaned'] = df["reviews.text"].apply(preprocess_text)

# Applying sentiment analysis and stored in sentiment column
df['sentiment'] = df['reviews.text.cleaned'].apply(analyze_sentiment)

# Printing first 5 comment text, review score and sentiment score to verify the model
for i in range(0,5):
    print('Review text: ', df["reviews.text"][i])
    print('Review Score: ', df['reviews.rating'][i])
    print('Sentiment Score: ', df['sentiment'][i])

# Showing relation between reviews and sentiment . Saving plot into files
custom_palette = {
    'Negative': 'grey',
    'Neutral': 'orange',
    'Positive': 'green'
}
hue_order = ['Negative', 'Neutral', 'Positive']
sns.countplot(df[df['reviews.rating'] < 4], x='reviews.rating', hue='sentiment', palette=custom_palette)
plt.xlabel("Reviews rating")
plt.ylabel("Number of review")
plt.title('Reviwes rating 1 to 3')
plt.savefig('rating_plot_1to3.png')
plt.close()

# Sapreated rating 4 to 5 into seprate graph since quantity is mush larger than rated 1 to 3
plt.title('Reviwes rating 4 to 5')
sns.countplot(df[df['reviews.rating'] >= 4], x='reviews.rating', hue='sentiment', palette=custom_palette)
plt.xlabel("Reviews rating")
plt.ylabel("Number of review")
plt.savefig('rating_plot_4to5.png')
plt.close()

# Printing result for some outlier review
outlier = df.loc[(df['reviews.rating'] == 5) & (df['sentiment'] == 'Negative')]
outlier_text= outlier['reviews.text'].values
print('Printing unexpected review (rated 5 but sentiment is Negative):')
for i in range(0,5):
    print(outlier_text[i])

#Testing sentiment analysis score with following sentence
print('Buying this product never cannot go wrong')
print('Sentiment Score : ',nlp("Buying this product never cannot go wrong")._.blob.polarity)

# Testing similarity
reviews_text_cleaned = df['reviews.text.cleaned'].values
print("Testing for similarity")
for i in range(0,5):
    saved = nlp(reviews_text_cleaned[i])
    for k in range(0,5):
        sim = saved.similarity(nlp(reviews_text_cleaned[k]))
        print(sim)

# Note: Using en_core_web_sm, a small model, is not recommended on doing similarity