from scrapper import scrape_google
from tabulate import tabulate
from db import Db


def insert_data_to_db(urls):
    print("inserting data to database from scrapper. . .")
    create_table = Db()
    create_table_cursor = create_table.cursor()
    create_table_cursor.execute(
        """
        DROP TABLE IF EXISTS `event_urls`;
        CREATE TABLE `event_urls` (
            `id` int unsigned NOT NULL AUTO_INCREMENT,
            `type` varchar(255) NOT NULL,
            `url` varchar(255) NOT NULL,
            PRIMARY KEY (`id`)
        );
    """
    )

    insert_data = Db()
    insert_data_cursor = insert_data.cursor()
    query = """
        INSERT INTO `event_urls`
        (type, url)
        VALUES (%s, %s)
    """
    values = [("impressions", x) for x in urls] * 5
    insert_data_cursor.executemany(query, values)
    insert_data.commit()


def get_final_data():
    get_data = Db()
    get_data_cursor = get_data.cursor()
    get_data_cursor.execute(
        """
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
    """
    )

    return get_data_cursor.fetchall()


print("start populating data. . .")
scraping_data = scrape_google("advertising") + scrape_google("latest news in indonesia")
insert_data_to_db(scraping_data)
print("====================")
print("Show final data after processing \n")
print(tabulate(get_final_data(), headers=["Domain", "Impressions"]))
