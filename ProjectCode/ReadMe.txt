1.Historical Data Extract(Java):
This program uses HttpRequest to extract historical Twitter data,you can specific searching keywords,date range,username and maximum volume. The downloaded data will be saved to multiple small csv files, which are used as input files for the python mapReduce program.
 
Program Path: “./OldTweets/”
“./OldTweets/libs/*” is the external jar files for the program,
“./src/*” is the program files, 
“./src/main/Exporter3.java” is the main class.

Running Command:
$ cd OldTweets/src
$ javac -cp ../libs/commons-logging-1.1.1.jar:../libs/httpclient-4.3.6.jar:../libs/httpcore-4.3.jar:../libs/json-20140107.jar:../libs/jsoup-1.8.1.jar main/Exporter3.java manager/TweetManager.java manager/TwitterCriteria.java model/Tweet.java

$ java -cp ../libs/commons-logging-1.1.1.jar:../libs/httpclient-4.3.6.jar:../libs/httpcore-4.3.jar:../libs/json-20140107.jar:../libs/jsoup-1.8.1.jar:. main/Exporter3



2.Sentiment Analysis and MapReduce for historical Data (Python):
This program combined NLTK sentiment analysis with MapReduce in Python, to analyzed the sentiment of each tweets and calculate the positive and negative tweets count for each candidates in each month.

Program Path: “./SentimentAnalysis_MapReduce”
“training_set.txt” is the training input file for Mapper.py.

Below is how to run program in Dumbo:
(1)Change python version to 2,7:
$ module load python/gnu/2.7.11
(2)Download nltk data:
>>>import nltk>>>nltk.download()Downloader>d punkt
(3)Copy the resources above to the work path :
$ cp -r ./nltk_data/tokenizers ./MapReduce_WorkPath
(4)Running command:
$ hadoop jar /opt/cloudera/parcels/CDH-5.4.5-1.cdh5.4.5.p0.7/jars/hadoop-streaming-2.6.0-cdh5.4.5.jar -files"Mapper.py,Reducer.py,training_set.txt,./tokenizers/" -mapper Mapper.py -reducer Reducer.py -input/user/netID/input -output /user/netId/output

3. Calculate tweets volume:
We use hive to calculate the data volume about each candidate in each month.
Query path:”./TweetsVolume.txt”

4.Streaming Data:
This program can get real-time twitter data by using Twitter Streaming API and analysis the sentiment by nltk, save the results into csv files and load into hdfs.
And then use Hive to count the positive and negative tweets for each candidate.

Program Path: “./Analysis”

Running Command:
(1) install module:
$ pip install tweedy
$ pip install unirest
(2)Run the scripts:
nohup python Hillary.py
nohup python Trump.py
nohup python Bernie Sanders.py
nohup python John Kasich.py
nohup python Ted.py
(3) Hive Query:
path:”./Analysis/tweets_analytics.sql”

5.Primary Results:
Use Hive to calculate the average support rate of each candidate based on Primary_results

path:”./Primary/hive”



