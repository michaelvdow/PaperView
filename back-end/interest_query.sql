USE googleScholar;
SELECT AuthorId, Name, MAX(Interest) FROM Author NATURAL JOIN InterestedIn
WHERE Interest LIKE '%python%'
GROUP BY AuthorId
