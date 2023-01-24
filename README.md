# Long Tail Aggregation
Long Tail Aggregation example with `Python` and `Mysql` with dummy data from scrapping url from search query `Google`. This program will execurted single SQL query that shows lists Top 10 significant domains with impressions count and additional “Others” row with all the long tail aggregated.

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
