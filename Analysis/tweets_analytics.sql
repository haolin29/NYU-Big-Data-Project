CREATE EXTERNAL TABLE 
streaming(user_id string, contestant string,sentiment string, user_location string,  created_at string)
row format delimited fields terminated by '\054'
    lines terminated by '\n'
    location '/user/cloudera/data/';


select contestant, LOWER(user_location), substr(created_at, 4, 7), count(*)
from streaming
where created_at is not null and user_location != 'undefined' and lower(sentiment)='positive'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)
;

select contestant, LOWER(user_location), substr(created_at, 4, 7), count(*)
from streaming
where created_at is not null and user_location != 'undefined' and lower(sentiment)='negative'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)
;

select contestant, LOWER(user_location), substr(created_at, 4, 7), count(*)
from streaming
where created_at is not null and user_location != 'undefined'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)
;

select contestant, trim(substr(created_at, 4, 7)), trim(substr(created_at, 11, 3)), LOWER(sentiment), count(*)
from streaming
where created_at is not null
group by contestant, substr(created_at, 4, 7), substr(created_at, 11, 3), LOWER(sentiment)
;


-- output select result to local 

INSERT OVERWRITE LOCAL DIRECTORY '/home/cloudera/Desktop/Share/hive' 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
select contestant, LOWER(user_location), substr(created_at, 4, 7), count(*)
from streaming
where created_at is not null and user_location != 'undefined' and lower(sentiment)='positive'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)
;


hive -e "select contestant, LOWER(user_location), substr(created_at, 4, 7), count(*) from streaming where created_at is not null and user_location != 'undefined' and lower(sentiment)='positive' group by contestant, LOWER(user_location), substr(created_at, 4, 7)"| sed 's/[\t]/,/g'  >> outputfile.csv

