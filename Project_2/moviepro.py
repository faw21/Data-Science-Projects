import sqlite3 as lite
import csv
import re
import pandas as pd
con = lite.connect('cs1656.sqlite')

with con:
    cur = con.cursor() 

    cur.execute('DROP TABLE IF EXISTS Actors')
    cur.execute("CREATE TABLE Actors(aid INT, fname TEXT, lname TEXT, gender CHAR(6), PRIMARY KEY(aid))")

    cur.execute('DROP TABLE IF EXISTS Movies')
    cur.execute("CREATE TABLE Movies(mid INT, title TEXT, year INT, rank REAL, PRIMARY KEY(mid))")

    cur.execute('DROP TABLE IF EXISTS Directors')
    cur.execute("CREATE TABLE Directors(did INT, fname TEXT, lname TEXT, PRIMARY KEY(did))")

    cur.execute('DROP TABLE IF EXISTS Cast')
    cur.execute("CREATE TABLE Cast(aid INT, mid INT, role TEXT)")

    cur.execute('DROP TABLE IF EXISTS Movie_Director')
    cur.execute("CREATE TABLE Movie_Director(did INT, mid INT)")


    ########################################################################        
    ### READ DATA FROM FILES ###############################################
    ########################################################################        
    # actors.csv, cast.csv, directors.csv, movie_dir.csv, movies.csv

    with open('actors.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            eachrow = (row[0], row[1], row[2], row[3])
            sql = '''
            INSERT INTO Actors(aid, fname, lname, gender) VALUES(?, ?, ?, ?)
            '''
            cur.execute(sql, eachrow)

    with open('cast.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            eachrow = (row[0], row[1], row[2])
            sql = '''
            INSERT INTO Cast(aid, mid, role) VALUES(?, ?, ?)
            '''
            cur.execute(sql, eachrow)
        
    with open('movies.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            eachrow = (row[0], row[1], row[2], row[3])
            sql = '''
            INSERT INTO Movies(mid, title, year, rank) VALUES(?, ?, ?, ?)
            '''
            cur.execute(sql, eachrow)
        
    with open('directors.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            eachrow = (row[0], row[1], row[2])
            sql = '''
            INSERT INTO Directors(did, fname, lname) VALUES(?, ?, ?)
            '''
            cur.execute(sql, eachrow)
        
    with open('movie_dir.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            eachrow = (row[0], row[1])
            sql = '''
            INSERT INTO Movie_Director(did, mid) VALUES(?, ?)
            '''
            cur.execute(sql, eachrow)
        
    con.commit()



    ########################################################################        
    ### QUERY SECTION ######################################################
    ########################################################################        
    queries = {}


    # DEBUG: all_movies ########################
    queries['all_movies'] = '''
SELECT * FROM Movies
'''    
    # DEBUG: all_actors ########################
    queries['all_actors'] = '''
SELECT * FROM Actors
'''    
    # DEBUG: all_cast ########################
    queries['all_cast'] = '''
SELECT * FROM Cast
'''    
    # DEBUG: all_directors ########################
    queries['all_directors'] = '''
SELECT * FROM Directors
'''    
    # DEBUG: all_movie_dir ########################
    queries['all_movie_dir'] = '''
SELECT * FROM Movie_Director
'''    


    # Q01 ########################        
    queries['q01'] = '''
    SELECT a.fname, a.lname FROM Cast AS c
    INNER JOIN Actors AS a ON c.aid = a.aid
    WHERE a.aid in (SELECT c2.aid FROM Cast AS c2
                    INNER JOIN Movies AS m2 ON m2.mid = c2.mid
                    WHERE m2.year <= 1990 AND m2.year >= 1980)
        AND a.aid in (SELECT c2.aid FROM Cast AS c2
                    INNER JOIN Movies AS m2 ON m2.mid = c2.mid
                    WHERE m2.year >= 2000)
    GROUP BY a.aid
    ORDER BY a.lname, a.fname
'''    
    
    # Q02 ########################        
    queries['q02'] = '''
    SELECT title, year FROM Movies
    WHERE rank > (SELECT rank FROM Movies
                  WHERE title = "Rogue One: A Star Wars Story")
        AND year IN (SELECT year FROM Movies 
                     WHERE title = "Rogue One: A Star Wars Story")
    ORDER BY title
'''    

    # Q03 ########################        
    queries['q03'] = '''
    SELECT a.fname, a.lname, COUNT(m.mid) AS movieNum
    FROM Actors AS a
    INNER JOIN Cast AS c ON a.aid = c.aid
    INNER JOIN Movies AS m ON m.mid = c.mid
    WHERE m.title LIKE '%Star Wars%'
    GROUP BY a.aid
    ORDER BY m.mid DESC
'''    

    # Q04 ########################        
    queries['q04'] = '''
    SELECT a.fname, a.lname FROM Actors AS a
    WHERE NOT a.aid IN (SELECT a2.aid FROM Movies AS m2
                        INNER JOIN Cast AS c2 ON m2.mid = c2.mid
                        INNER JOIN Actors AS a2 ON a2.aid = c2.aid
                        WHERE m2.year >= 1985)
    ORDER BY a.lname, a.fname
'''    

    # Q05 ########################        
    queries['q05'] = '''
    SELECT d.fname, d.lname, COUNT(md.mid) AS num FROM Directors as d
    INNER JOIN Movie_Director as md ON d.did = md.did
    GROUP BY d.did
    ORDER BY num DESC
    LIMIT 20
'''    

    # Q06 ########################        
    queries['q06'] = '''
    SELECT m.title, COUNT(c.aid) AS castSize FROM Movies AS m
    INNER JOIN Cast AS c ON m.mid = c.mid
    GROUP BY m.mid
    ORDER BY castSize DESC
'''    

    # Q07 ########################        
    queries['q07'] = '''
    SELECT m.title, IFNULL(WOMEN.womenNum, 0) AS num_women, IFNULL(MEN.menNum, 0) AS num_men
    FROM Movies AS m
    INNER JOIN Cast AS c ON c.mid = m.mid
    INNER JOIN Actors AS a ON c.aid = a.aid
    LEFT JOIN (SELECT c2.mid, COUNT(*) AS menNum FROM Cast AS c2
               INNER JOIN Actors AS a2 ON c2.aid = a2.aid
               WHERE a2.gender = "Male"
               GROUP BY c2.mid) AS MEN ON MEN.mid = m.mid
    LEFT JOIN (SELECT c3.mid, COUNT(*) AS womenNum FROM Cast AS c3
               INNER JOIN Actors AS a3 ON c3.aid = a3.aid
               WHERE a3.gender = "Female"
               GROUP BY c3.mid) AS WOMEN ON WOMEN.mid = m.mid
    WHERE num_men < num_women
    GROUP BY m.mid
    ORDER BY m.title
'''    

    # Q08 ######################## 
    queries['q08'] = '''
    SELECT a.fname, a.lname, COUNT(DISTINCT md.did) AS directorsNum
    FROM Actors AS a
    INNER JOIN Cast AS c ON a.aid = c.aid
    INNER JOIN Movie_Director AS md ON md.mid = c.mid
    INNER JOIN Directors AS d ON md.did = d.did AND d.lname <> a.lname AND d.fname <> a.fname
    GROUP BY a.aid
    HAVING directorsNum >= 7
    ORDER BY directorsNum DESC
    
'''    

    # Q09 ########################        
    queries['q09'] = '''
    SELECT a.fname, a.lname, COUNT(m.mid) AS moviesNum
    FROM Actors AS a
    INNER JOIN Cast AS c ON a.aid = c.aid
    INNER JOIN Movies AS m ON c.mid = m.mid
    WHERE SUBSTR(a.fname, 1, 1) = 'T'
        AND m.mid IN (SELECT m2.mid
                      FROM Actors AS a2
                      INNER JOIN Cast AS c2 ON a2.aid = c2.aid
                      INNER JOIN Movies AS m2 ON c2.mid = m2.mid
                      WHERE m.year = (SELECT MIN(m3.year)
                                      FROM Actors AS a3
                                      INNER JOIN Cast AS c3 ON a3.aid = c3.aid
                                      INNER JOIN Movies AS m3 ON c3.mid = m3.mid
                                      WHERE a3.aid = a.aid))
    GROUP BY a.aid
    ORDER BY moviesNum DESC
'''    

    # Q10 ########################        
    queries['q10'] = '''
    SELECT a.lname, m.title
    FROM Actors AS a
    INNER JOIN Cast AS c ON a.aid = c.aid
    INNER JOIN Movies AS m ON c.mid = m.mid
    INNER JOIN Movie_Director AS md ON c.mid = md.mid
    INNER JOIN Directors AS d ON d.did = md.did
    WHERE a.lname = d.lname AND a.fname <> d.fname
    ORDER BY a.lname
'''    

    # Q11 ########################        
    queries['q11'] = '''
'''    

    # Q12 ########################        
    queries['q12'] = '''
    SELECT a.fname, a.lname, COUNT(m.mid), AVG(m.rank) AS score
    FROM Movies AS m
    INNER JOIN Cast AS c ON c.mid = m.mid
    INNER JOIN Actors AS a ON a.aid = c.aid
    GROUP BY a.aid
    ORDER BY score DESC
    LIMIT 20
'''    


    ########################################################################        
    ### SAVE RESULTS TO FILES ##############################################
    ########################################################################        
  
    for (qkey, qstring) in sorted(queries.items()):
        try:
            cur.execute(qstring)
            all_rows = cur.fetchall()
            
            print ("=========== ",qkey," QUERY ======================")
            print (qstring)
            print ("----------- ",qkey," RESULTS --------------------")
            for row in all_rows:
                print (row)
            print (" ")

            save_to_file = (re.search(r'q0\d', qkey) or re.search(r'q1[012]', qkey))
            if (save_to_file):
                with open(qkey+'.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(all_rows)
                    f.close()
                print ("----------- ",qkey+".csv"," *SAVED* ----------------\n")
        
        except lite.Error as e:
            print ("An error occurred:", e.args[0])

    
