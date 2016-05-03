# Predicting US Election of 2016 with Twitter

Team member:

Haolin Ju(hj836)

Weijing Wei(ww893)

Ailing Cui(ac5443)



## Data source

1. Historical Tweets (March&April)
2. Twitter Streaming API
3. Primary Election




## Streaming Data

### Crawl the data

1.pip module
`sudo easy_install pip`
`sudo python setup.py install`



2.modules

install it from source, download the source from http://pypi.python.org/pypi/tweepy then run something like:

```
pip install tweepy
pip install unirest

```



3.run the scripts

```
cd Streaming
nohup python Hillary.py
nohup python Trump.py
nohup python Bernie Sanders.py
nohup python John Kasich.py
nohup python Ted.py
```

Move all the results to `data/` folder.

### Store to HDFS

```
$ hdfs dfs -mkdir hiveInput

// create a hive external table for oldTweets
$ beeline -u jdbc:hive2://quickstart:10000/default -n cloudera -d org.apache.hive.jdbc.HiveDriver
hive> CREATE EXTERNAL TABLE 
streaming(user_id string, contestant string,sentiment string, user_location string,  created_at string)
row format delimited fields terminated by '\054'
    lines terminated by '\n'
    location '/user/cloudera/data/';


hive> show tables;
hive> describe tweets;
```



### query data

```
select contestant, LOWER(user_location) as location, substr(created_at, 4, 7) as time, count(*) as number
from streaming
where created_at is not null and user_location != 'undefined' and lower(sentiment)='positive'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)
;

select contestant, LOWER(user_location) as location, substr(created_at, 4, 7) as time, count(*) as count
from streaming
where created_at is not null and user_location != 'undefined' and lower(sentiment)='negative'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)
;

select contestant, LOWER(user_location) as location, substr(created_at, 4, 7) as time, count(*) as count
from streaming
where created_at is not null and user_location != 'undefined'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)
;

select contestant, trim(substr(created_at, 4, 7)) as date, trim(substr(created_at, 11, 3)) as time, LOWER(sentiment) as sentiment, count(*) as count
from streaming
where created_at is not null
group by contestant, substr(created_at, 4, 7), substr(created_at, 11, 3), LOWER(sentiment)
;


select contestant, trim(substr(created_at,4,7)) as date, count(*) as count
from streaming
where created_at is not null
group by contestant, substr(created_at, 4, 7)
;

select contestant, trim(substr(created_at,4,7)) as date, lower(sentiment) as sentiment, count(*) as count
from streaming
where created_at is not null
group by contestant, substr(created_at, 4, 7), lower(sentiment)
;

```



### output data to csv

```
hive -e "select contestant, LOWER(user_location), substr(created_at, 4, 7), count(*) from streaming where created_at is not null and user_location != 'undefined' and lower(sentiment)='positive' group by contestant, LOWER(user_location), substr(created_at, 4, 7)"| sed 's/[\t]/,/g'  >> positive.csv

hive -e "select contestant, LOWER(user_location), substr(created_at, 4, 7), count(*)
from streaming
where created_at is not null and user_location != 'undefined' and lower(sentiment)='negative'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)" | sed 's/[\t]/,/g'  >> negative.csv

hive -e "select contestant, LOWER(user_location), substr(created_at, 4, 7), count(*)
from streaming
where created_at is not null and user_location != 'undefined'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)" | sed 's/[\t]/,/g'  >> all.csv

hive -e "select contestant, trim(substr(created_at, 4, 7)), trim(substr(created_at, 11, 3)), LOWER(sentiment), count(*)
from streaming
where created_at is not null
group by contestant, substr(created_at, 4, 7), substr(created_at, 11, 3), LOWER(sentiment)
" | sed 's/[\t]/,/g'  >> sentiment.csv

```



## Old tweets

1.Historical Data Extract(Java):
This program uses HttpRequest to extract historical Twitter data,you can specific searching keywords,date range,username and maximum volume. The downloaded data will be saved to multiple small csv files, which are used as input files for the python mapReduce program.

Program Path: 

“./OldTweets/”
“./OldTweets/libs/*” is the external jar files for the program,
“./src/*” is the program files, 
“./src/main/Exporter3.java” is the main class.

Running Command:
`$ cd OldTweets/src`
`$ javac -cp ../libs/commons-logging-1.1.1.jar:../libs/httpclient-4.3.6.jar:../libs/httpcore-4.3.jar:../libs/json-20140107.jar:../libs/jsoup-1.8.1.jar main/Exporter3.java manager/TweetManager.java manager/TwitterCriteria.java model/Tweet.java`

`$ java -cp ../libs/commons-logging-1.1.1.jar:../libs/httpclient-4.3.6.jar:../libs/httpcore-4.3.jar:../libs/json-20140107.jar:../libs/jsoup-1.8.1.jar:. main/Exporter3`



2.Sentiment Analysis and MapReduce for historical Data (Python):
This program combined NLTK sentiment analysis with MapReduce in Python, to analyzed the sentiment of each tweets and calculate the positive and negative tweets count for each candidates in each month.

Program Path: “./SentimentAnalysis_MapReduce”
“training_set.txt” is the training input file for Mapper.py.

Below is how to run program in Dumbo:
(1)Change python version to 2,7:
$ module load python/gnu/2.7.11
(2)Download nltk data:

```
import nltk

nltk.download()

Downloader>d punkt

(3)Copy the resources above to the work path :

$ cp -r ./nltk_data/tokenizers ./MapReduce_WorkPath

(4)Running command:

$ hadoop jar /opt/cloudera/parcels/CDH-5.4.5-1.cdh5.4.5.p0.7/jars/hadoop-streaming-2.6.0-cdh5.4.5.jar -files

"Mapper.py,Reducer.py,training_set.txt,./tokenizers/" -mapper Mapper.py -reducer Reducer.py -input

/user/netID/input -output /user/netId/output

```

3.Calculate tweets volume:
We use hive to calculate the data volume about each candidate in each month.
Query path:”./TweetsVolume.txt”



## Primary results

```
$ hdfs dfs -mkdir primary
$ hdfs dfs -put primary_results.csv primary

$ beeline -u jdbc:hive2://quickstart:10000/default -n cloudera -d org.apache.hive.jdbc.HiveDriver
0: jdbc:hive2://quickstart:10000/default> create external table primary_result(state string, state_abbr string, county string, fips int, party string, candidate string, votes int, fraction_votes double) 
	row format delimited fields terminated by ',' 
	location '/user/cloudera/primary/'; 


hive> create table candidate_rate as select candidate, sum(fraction_votes)*1.0/count(candidate) as rate 
	from primary_result 
	group by candidate 
	order by rate desc;

hive> select * from candidate_rate;

hive>  create table party_candidate as select party, candidate 
	from primary_result 
	group by party, candidate;

hive>  select * from party_candidate;


hive> create table party_candidate_rate as select party, candidate_rate.candidate, rate 
	from party_candidate, candidate_rate 
	where party_candidate.candidate=candidate_rate.candidate 
	order by party, rate desc;
hive>  select * from party_candidate_rate;

```












