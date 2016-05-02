# Predicting US Election of 2016 using Social media



## Data source

1. Twitter Streaming API
2. Primary Election 
3. Twitter REST API



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
nohup python Hillary.py
nohup python Trump.py
nohup python Bernie Sanders.py
nohup python John Kasich.py
nohup python Ted.py

```





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








