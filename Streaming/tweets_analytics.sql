CREATE EXTERNAL TABLE 
streaming(user_id string, contestant string,sentiment string, user_location string,  created_at string)
row format delimited fields terminated by '\054'
    lines terminated by '\n'
    location '/user/cloudera/data/';


select contestant, LOWER(user_location) as location, substr(created_at, 4, 7) as time, count(*) as number
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


-- output select result to local 


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



