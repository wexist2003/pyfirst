SELECT d.name AS course
FROM grades g
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN disciplines d ON d.id = g.discipline_id
LEFT JOIN teachers t ON t.id = d.teacher_id
WHERE s.id = 15 AND t.id = 4
GROUP BY d.name
ORDER BY d.name DESC 