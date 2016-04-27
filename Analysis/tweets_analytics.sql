CREATE EXTERNAL TABLE 
streamming_analysis(user_id string, user_location string, contestant string, created_at string, sentiment string)
row format delimited fields terminated by '\073'
    lines terminated by '\n'
    location '/user/hj836/hiveInput/';


select contestant, LOWER(user_location), substr(created_at, 4, 7), count(*)
from streamming_analysis
where created_at is not null and user_location != 'undefined' and lower(sentiment)='positive'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)
;

select contestant, LOWER(user_location), substr(created_at, 4, 7), count(*)
from streamming_analysis
where created_at is not null and user_location != 'undefined' and lower(sentiment)='negative'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)
;

select contestant, LOWER(user_location), substr(created_at, 4, 7), count(*)
from streamming_analysis
where created_at is not null and user_location != 'undefined'
group by contestant, LOWER(user_location), substr(created_at, 4, 7)
;

select contestant, trim(substr(created_at, 4, 7)), trim(substr(created_at, 11, 3)), LOWER(sentiment), count(*)
from streamming_analysis
where created_at is not null
group by contestant, substr(created_at, 4, 7), substr(created_at, 11, 3), LOWER(sentiment)
;
