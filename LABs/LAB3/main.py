from sklearn.feature_extraction.text import CountVectorizer
##vectorizer =CountVectorizer(min_df=1)

##content = ["How to format my hard disk", " Hard disk format problems "]
##X = vectorizer.fit_transform(content)

##print(vectorizer.get_feature_names())
##print(X.toarray())

from sklearn.datasets import fetch_20newsgroups

categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics','sci.med']

twenty_train = fetch_20newsgroups(subset='train', categories=categories,shuffle=True, random_state=42)

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()

train_counts = vectorizer.fit_transform(twenty_train.data)

print(vectorizer.vocabulary_.get('algorithm'))
print(len(vectorizer.get_feature_names()))