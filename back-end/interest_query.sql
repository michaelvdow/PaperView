USE googleScholar;
SELECT AuthorId, Name FROM Author NATURAL JOIN InterestedIn
WHERE Interest LIKE '%python%'
GROUP BY AuthorId
