USE googleScholar;
SELECT AuthorId, Name, MAX(Interest) AS Interest
FROM Author NATURAL JOIN InterestedIn
WHERE Interest LIKE '%python%'
GROUP BY AuthorId
ORDER BY Name
