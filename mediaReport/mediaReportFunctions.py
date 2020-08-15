import pandas as pd
import numpy as np
import torch
import pickle
import transformers as ppb # pytorch transformers
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def read_file(filename):
    df = pd.read_excel(filename)
    #df['Content'] = df['Content'].str.replace('.',' ').astype(str)
    for i, tup in df.iterrows():
        if (len(tup['Content']) > 500):
            df.at[i, 'Content'] = tup['Content'][:500]
    return df


def to_DistilBert(df):
    model_class, tokenizer_class, pretrained_weights = (ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-uncased')
    tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights)
    tokenized = df['Content'].apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))
    max_len = 500
    # for i in tokenized.values:
    #     if len(i) > max_len:
    #         max_len = len(i)
    padded = np.array([i + [0]*(max_len-len(i)) for i in tokenized.values])
    attention_mask = np.where(padded != 0, 1, 0)
    input_ids = torch.tensor(padded)
    attention_mask = torch.tensor(attention_mask)
    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)


    features = last_hidden_states[0][:,0,:].numpy()
    labels = df['Feedback']

    return features, labels

def logistic_with_training(features, labels):
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels)
    print(len(train_features), len(test_features))
    lr_clf = LogisticRegression()
    lr_clf.fit(train_features, train_labels)
    print(lr_clf.score(test_features, test_labels))
    filename = 'log_model.sav'
    pickle.dump(lr_clf, open(filename, 'wb'))


def predict(features, df):
    filename = 'log_model.sav'
    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(features)
    df['Feedback'] = result.tolist()
    return df




