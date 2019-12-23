from neo4j import GraphDatabase, basic_auth

#connection with authentication
#driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "12345678"), encrypted=False)

#connection without authentication
driver = GraphDatabase.driver("bolt://localhost", encrypted=False)
f = open("output.txt", "w")
session = driver.session()
transaction = session.begin_transaction()


f.write("### Q1 ###\n")
result = transaction.run("""
MATCH (a:Actor) -[:ACTS_IN]-> (:Movie)
RETURN a.name, count(*) AS films_count
ORDER BY films_count DESC LIMIT 20
;""")
for record in result:
    f.write(("%s, %d\n" %(record['a.name'], record['films_count'])))


f.write("\n### Q2 ###\n")
result = transaction.run("""
MATCH (:Person)-[r:RATED]->(m:Movie)
WHERE r.stars <= 3
RETURN m.title
;""")
for record in result:
    f.write(("%s\n" %(record['m.title'])))


f.write("\n### Q3 ###\n")
result = transaction.run("""MATCH (:Person)-[:RATED]->(m:Movie)<-[:ACTS_IN]-(a:Actor)
WITH m, count(distinct a) as actor_count
RETURN m.title, actor_count
ORDER BY actor_count DESC
LIMIT 1
;""")
for record in result:
    f.write(("%s, %d\n" %(record['m.title'], record['actor_count'])))

f.write("\n### Q4 ###\n")
result = transaction.run("""
MATCH (a:Actor) -[:ACTS_IN]-> (m:Movie) <-[:DIRECTED]- (d:Director)
WITH a, count(distinct d.name) AS director_count
WHERE director_count >= 3
RETURN distinct a.name, director_count
;""")
for record in result:
   f.write(("%s, %d\n" %(record['a.name'], record['director_count'])))


f.write("\n### Q5 ###\n")
result = transaction.run("""
MATCH (kb:Actor{name:"Kevin Bacon"})-[:ACTS_IN]->(:Movie)<-[:ACTS_IN]-(a1:Actor)
MATCH (a1)-[:ACTS_IN]->(:Movie)<-[:ACTS_IN]-(a2:Actor)
WHERE not exists ((kb)-[:ACTS_IN]->(:Movie)<-[:ACTS_IN]-(a2)) and a2.name<>"Kevin Bacon"
RETURN distinct a2.name
ORDER BY a2.name
;""")
for record in result:
   f.write(("%s\n" %(record['a2.name'])))


f.write("\n### Q6 ###\n")
result = transaction.run("""
MATCH (:Actor{name: "Tom Hanks"})-[:ACTS_IN]->(m:Movie)
RETURN distinct m.genre
;""" )
for record in result:
   f.write(("%s\n" %(record['m.genre'])))


f.write("\n### Q7 ###\n")
result = transaction.run("""
MATCH (d:Director)-[:DIRECTED]->(m:Movie)
WITH d.name AS d_name, count(distinct m.genre) AS genre_count
WHERE genre_count >= 2
RETURN d_name, genre_count
;""")
for record in result:
   f.write(("%s, %d\n" %(record['d_name'], record['genre_count'])))


f.write("\n### Q8 ###\n")
result = transaction.run("""
MATCH (d:Director) -[:DIRECTED]-> (:Movie) <-[:ACTS_IN]- (a:Actor)
WITH d.name AS d_name, a.name AS a_name, count(*) AS frequency
RETURN distinct d_name, a_name, frequency
ORDER BY frequency DESC LIMIT 5
;""")
for record in result:
   f.write(("%s, %s, %d\n" %(record['d_name'], record['a_name'], record['frequency'])))

f.close()
transaction.close()
session.close()



	