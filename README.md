# Predicting US Election of 2016 using Social media

## Data source
1. Twitter Streaming API
2. Primary Election 
3. Twitter REST API

## ETL
~~Flume

Why Flume?
Flume is a highly reliable, distributed, and configurable tool. It is principally designed to copy streaming data (log data) from various web servers to HDFS.

Here are the advantages of using Flume:

- Using Apache Flume we can store the data in to any of the centralized stores (HBase, HDFS).

- When the rate of incoming data exceeds the rate at which data can be written to the destination, Flume acts as a mediator between data producers and the centralized stores and provides a steady flow of data between them.

- Flume provides the feature of contextual routing.

- The transactions in Flume are channel-based where two transactions (one sender and one receiver) are maintained for each message. It guarantees reliable message delivery.

- Flume is reliable, fault tolerant, scalable, manageable, and customizable.

![](http://www.tutorialspoint.com/apache_flume/images/apache_flume.jpg)


_Some of the notable features of Flume are as follows_ 

- Flume ingests log data from multiple web servers into a centralized store (HDFS, HBase) efficiently.

- Using Flume, we can get the data from multiple servers immediately into Hadoop.

- Along with the log files, Flume is also used to import huge volumes of event data produced by social networking sites like Facebook and Twitter, and e-commerce websites like Amazon and Flipkart.

- Flume supports a large set of sources and destinations types.

- Flume supports multi-hop flows, fan-in fan-out flows, contextual routing, etc.

- Flume can be scaled horizontally.~~

### Crawl the data

1.pip module
`sudo easy_install pip`
`sudo python setup.py install`

2.tweepy modules
install it from source, download the source from http://pypi.python.org/pypi/tweepy then run something like:

```
tar xzvf tweepy-1.7.1.tar.gz

cd tweepy-1.7.1

python setup.py install
```

### Store to HDFS
```
$ hdfs dfs -mkdir hiveInput
$ hdfs dfs -mkdir impalaInput

// Get data ready for Hive tests
$ hdfs dfs -put smallWeather1.txt hiveInput
$ hdfs dfs -ls hiveInput 
$ hdfs dfs -cat hiveInput/smallWeather1.txt

// create a hive external table
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
hive> describe w1;



```




## How to Query

We use Hive to query data.

Why Hive?
Additionally, some of the fields may be arbitrarily complex. The hashtags field is an array of all the hashtags present in the tweets, but most RDBMS’s do not support arrays as a column type. 
This semi-structured quality of the data makes the data very difficult to query in a traditional RDBMS. Hive can handle this data much more gracefully.




