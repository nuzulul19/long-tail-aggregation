# Long Tail Aggregation
Long Tail Aggregation example with `Python` and `Mysql` with dummy data from scrapping url from search query `Google`. This program will executed single SQL query that shows lists Top 10 significant domains with impressions count and additional “Others” row with all the long tail aggregated.

Main query that will be used:
```
(
    SELECT IF(
        CHARACTER_LENGTH(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(url, "www.", ""), '/', 3), '://', -1), '?', 1), '.', -2)) > 6,
        SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(url, "www.", ""), '/', 3), '://', -1), '.', -2), '?', 1),
        SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(url, "www.", ""), '/', 3), '://', -1), '.', -3), '?', 1)
    ) AS domain,
    COUNT(id) AS impressions
    FROM `event_urls`
    GROUP BY domain
    ORDER BY impressions DESC
    LIMIT 10
)
UNION ALL
(
    SELECT 'Others' AS domain, SUM(impressions)
    FROM
    (
        SELECT IF(
            CHARACTER_LENGTH(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(url, "www.", ""), '/', 3), '://', -1), '?', 1), '.', -2)) > 6,
            SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(url, "www.", ""), '/', 3), '://', -1), '.', -2), '?', 1),
            SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(url, "www.", ""), '/', 3), '://', -1), '.', -3), '?', 1)
        ) AS domain,
        COUNT(id) AS impressions
        FROM `event_urls`
        GROUP BY domain
        ORDER BY impressions DESC
        LIMIT 10, 18446744073709551615
    ) AS others
)
```

Another idea for the query:
```
SELECT
    ROW_NUMBER() OVER (ORDER BY CASE WHEN otherDomain = 'Others' THEN 1 ELSE 0 END, SUM(n) DESC) AS nr,
    otherDomain,
    SUM(n)
FROM (
    SELECT
        CASE WHEN nr >= 11 THEN 'Others' ELSE domain END AS otherDomain,
        n
    FROM ( 
        SELECT 
            ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS nr, 
            IF(
		        CHARACTER_LENGTH(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(url, "www.", ""), '/', 3), '://', -1), '?', 1), '.', -2)) > 6,
		        SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(url, "www.", ""), '/', 3), '://', -1), '.', -2), '?', 1),
		        SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(url, "www.", ""), '/', 3), '://', -1), '.', -3), '?', 1)
		    	) AS domain,
            COUNT(id) AS n
        FROM
            event_urls
        GROUP BY
        	domain
    ) AS x
) AS y
GROUP BY
    otherDomain
ORDER BY
    CASE WHEN otherDomain = 'Others' THEN 1 ELSE 0 END,
    SUM(n) DESC
```

## How to run the program
Need at least `Python 3.9` and already installed `Mysql` database on local machines.
### Copy `settings.py.example` into `settings.py`
**Note**:
Overriding all the credentials are **required**.
### Installing all needed requirements
```
pip install -r requirements.txt
```
### Execute the program
```
python main.py
```
