import csv
import re, os
from collections import Counter
from sklearn.model_selection import train_test_split

#This function takes data and the sentiment of which the text is to 
# be sperated
def getText(data, sentiment):
    extracted = ''
    count = 0
    #test_list = []
    for row in data:
        if row[1] == sentiment:
            extracted += row[0]+ ' '
            #test_list.append(row[0])
            count += 1
    return extracted, count


#Actual Naive Bayes Logic
def NaiveBayes(review, class_word_dict, closs_prob, no_reviews_in_class):
    prediction = 1.0
    sentence_words = Counter(re.split("\s+",review))
    for word in sentence_words:
        #The one is added to avoid the zero factor 
        prediction *= sentence_words.get(word) * ((class_word_dict.get(word, 0)+1) / float(sum(class_word_dict.values())+len(class_word_dict) ))
    return prediction * closs_prob 

#This function only run nive bayes for each sentence and return classification
def Predict(sentence, negative_words, positive_words, negative_probab, positive_probab, no_negative_sentences, no_positive_sentences):
    neg_prob = NaiveBayes(sentence,negative_words,negative_probab, no_negative_sentences)
    pos_prob = NaiveBayes(sentence,positive_words,positive_probab, no_positive_sentences)
    if(neg_prob > pos_prob):  
        return 0
    else:   
        return 1

def getPrediction(sentence):
    #Opening all files
    dataset_file = open('dataset.csv', 'r')

    ## This two lines return list of tuples [review, sentiment]
    dataset = list(csv.reader(dataset_file))

    #Split data into training and testing 0.7:0.3
    # train_data = dataset[:int(len(dataset)*0.8)]
    # test_data = dataset[int(len(dataset)*0.8):]
    train_data, test_data = train_test_split(dataset, test_size=0.2)


    #calculate number of total sentences
    total_sentence_train = len(train_data)

    #Seperating data into two classes negative and positive
    ## Return -ve and +ve along with their counts
    negative_text, no_negative_sentences = getText(train_data, '0')
    positive_text, no_positive_sentences = getText(train_data, '1')
    # print(negative_text, no_negative_sentences)

    # \s+ = split when one or more space
    ## The function return key value pairs (Dictionary)
    ## This gives unique -ve and +ve words along with count {word:count}
    negative_words = Counter(re.split('\s+', negative_text))
    positive_words = Counter(re.split('\s+', positive_text))

    # Now we calculate probabilites of both -ve and poitive words in train data
    negative_probab = no_negative_sentences / float(total_sentence_train)
    positive_probab = no_positive_sentences / float(total_sentence_train)
    # print(negative_probab, positive_probab)

    #Lets now predict with test data
    predictions = Predict(sentence, negative_words, positive_words, negative_probab, positive_probab, no_negative_sentences, no_positive_sentences)
    return predictions


    #Close All Files
    dataset_file.close()