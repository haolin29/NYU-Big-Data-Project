# Predicting US Election of 2016 using Social media

## Data source
1. Twitter Streaming API
2. Primary Election 
3. Twitter REST API

## ETL
### Crawl the data

1.pip module
`sudo easy_install pip`
`sudo python setup.py install`

2.tweepy modules
install it from source, download the source from http://pypi.python.org/pypi/tweepy then run something like:

```
tar -xzvf tweepy-1.7.1.tar.gz

cd tweepy-1.7.1

python setup.py install
```

### Store to HDFS
```
$ hdfs dfs -mkdir hiveInput

// create a hive external table for oldTweets
$ beeline -u jdbc:hive2://quickstart:10000/default -n cloudera -d org.apache.hive.jdbc.HiveDriver
hive> create external table tweets (
    username string,
    date string,
    retweets int,
    favorites int,
    text string,
    geo string,
    mentions string,
    hashtags string,
    id string,
    permalink string)
    row format delimited fields terminated by '\073'
    lines terminated by '\n'
    location '/user/hj836/hiveInput/';

hive> show tables;
hive> describe tweets;

// create table for primary results
hive> create external table primary (
    state string,
    state_abbreviation string,
    county string,
    fips int,
    party string,
    candidate string,
    votes int,
    fraction_votes string)
    row format delimited fields terminated by '\073'
    lines terminated by '\n'
    location '/user/hj836/primary/';

// create table for streaming data

 create external table stream(userid string, user string, time string, tweet string) row format delimited fields terminated by '\073' lines terminated by '\n' location '/user/cloudera/streamTweets/';

```



## How to Query

We use Hive to query data.

Why Hive?
Additionally, some of the fields may be arbitrarily complex. The hashtags field is an array of all the hashtags present in the tweets, but most RDBMS’s do not support arrays as a column type. 
This semi-structured quality of the data makes the data very difficult to query in a traditional RDBMS. Hive can handle this data much more gracefully.




