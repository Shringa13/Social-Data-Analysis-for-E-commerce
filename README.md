# Social-Data-Analysis-for-E-commerce

					
Everyday E-commerce sites like Amazon,eBay ,flipkart increasing their services in every field and
trying to catch each and every activity of customers.By messages, mails ,facebook page and 
tweets this retail companies always ready with their support services. 

In this project I am analysing E-commerce support services through twitter.Most suitable service 
provider junction nowadays is twitter, just tag provider username (like :@Amazonhelp) and 
write your query, experiences, about the product you purchased or anything and you will get 
instant replies.We look after the data for 3 retail sites i.e. Amazon,eBay and Flipkart
support services through twitter and pulled its data followers,tweets and user ids.

There are 4 steps through which we have done some analysis on this data:

1) collect.py : In this file we have pulled data from twitter like user ids ,followers detail and
total of around 4000+ tweets from the above mentioned retail sites.Using Maxi_id and since_id we 
can able to pull more and more tweets for our analysis.Now, user and its followers data get dumped
into a CSV file known as Followers.csv  and tweets data for its respective retail sites gets stored in
individual text files AmazonHelp.txt, AskeBay.txt, flipkartsupport.txt

2) cluster.py : In this file we are clustering data in to 4 clusters on he basis of their common followers.
As per our data there are now 1 user which is following all the support services and many users who follow 
either 2 of the retail services.I have used newman girvan algorithm for calculating clusters ans use jaccard
coefficient betweenusers and their followers. In the end I have created a weighted graph using jaccard coefficient
value.From this Communities.txt file is created which stores data of communitites created from given data and their average users.

3) classify.py : In this file I have performed sentiment analysis on tweets data and found positive and negative tweets
about the service provider.From this analysis we can able to look after which retail sites provides better support services
through twitter. I have used AFINN words list  to do sentiment analysis by comapring each word from tweet 
with the words list provided by AFINN. Calculates its Positive and negative scores which helps to find count of Positive and
negative terms present in tweet.Complete data from above code gets stored in Sentiment.csv file conating Labels (Positivie/Negative),
Positive score, Negative score,tweet and user details.

4) summarize.py : In this file I am creating new text file summary.txt which pulls data from all the files created above and paste into
 this file as per the asked format.

Analysis:- From the above analysis we have found that for all the three retail services there are more negative tweets than positive one 
but again we cannot say that the services are not good but can be improved.We also found that there is only one single user who follows all
the 3 support services on twitter means till now this has not been much used in general. From this analysis I can understand that how online analysis 
has been done by using general data to predict future services or for improving it.
