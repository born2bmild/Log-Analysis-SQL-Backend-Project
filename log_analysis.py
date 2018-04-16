#!/usr/bin/env python3
import psycopg2

DBNAME = "news"

def get_most_popular_articles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select path, count(path)
                  from log
                  group by path
                  order by count(path) desc''')
    most_popular_articles = c.fetchall()
    db.close()
    return most_popular_articles

def total_articles_by_author():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select au.name,
                 count(ar.title) as total
                 from authors au
                 join articles ar
                 on au.id = ar.author
                 group by au.name''')
    total_by_author = c.fetchall()
    db.close()
    return total_by_author

def get_most_errors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''SELECT
                    t2.error_date, 
                    error_percentage||'%' AS error_percentage
                FROM
                (
                SELECT 
                    t1.error_date, 
                    round(100 * SUM(t1.error_count) / SUM(views),2) AS error_percentage
                FROM
                (
                    SELECT 
                        t.error_date, SUM(error_count) AS error_count, 
                        SUM(error_count + non_error_count) AS views
                    FROM
                    (
                    SELECT 
                        time::DATE AS error_date , 
                        CASE WHEN status LIKE '4%'
                        THEN 1
                        ELSE 0
                        END AS error_count,
                
                        CASE WHEN status NOT LIKE '4%'
                        THEN 1 
                        ELSE 0
                        END AS non_error_count
                    FROM LOG
                
                    )T
                GROUP BY 1
                )t1
                GROUP BY 1
                )t2
                WHERE t2.error_percentage > 1''')
    error_data = c.fetchall()
    db.close()
    return error_data

#print(get_most_popular_articles())
#print(total_articles_by_author())
#print(get_most_errors())
    

