import csv
from collections import Counter
import pandas as pd

def main():

    dfr=pd.read_csv('Followers.csv')
    c = len(dfr['follows']) +3
    #print(len(c))  No. of users
    total_messages =[]
    searchQuery = ['flipkartsupport','AskeBay','AmazonHelp']
    for i in searchQuery:
        with open(i+'.txt', 'r') as f:
            my_list = [line.rstrip('\n') for line in f]
        total_messages.append(len(my_list))
    Messages = sum(total_messages) # Messages collected
    with open('Communities.txt', 'r') as f:
        Community = [line.rstrip('\n') for line in f]
    #print(Community[0],Community[1]) No. of clusters and average 
	
    df_sentiment=pd.read_csv('Sentiment.csv')
    cnt = Counter(df_sentiment['Labels'])
    Instances =[]
    for label,value in cnt.items():
        Instances.append([label,value])
    #print (Instances)
    df_sentiment_positive=df_sentiment[df_sentiment['Labels']=='POSITIVE'].head(1)
    #print(df_sentiment_positive['Tweet'].values)
    df_sentiment_negative=df_sentiment[df_sentiment['Labels']=='NEGATIVE'].head(1)
    #print(df_sentiment_negative['Tweet'].values)
    with open("summary.txt", 'w') as final:
        final.write ("Number of users collected: %d\n" %(c))
    with open("summary.txt", 'a') as final:
        final.write ("Number of messages collected: %d\n"%(Messages))
        final.write ("Number of communities discovered: %s\n"%(Community[0]))
        final.write ("Average number of users per community: %s\n"%(Community[1]))
        final.write ("Number of instances per class found: %s\n"%(Instances))
        final.write ("One example from each class:\n")
        final.write ("Positive: %s\n"%(df_sentiment_positive['Tweet'].values))
        final.write ("Negative: %s\n"%(df_sentiment_negative['Tweet'].values))
        
		
    
		
    

if __name__ == '__main__':
    main()