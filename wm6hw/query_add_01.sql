SELECT ROUND(AVG(g.grade),2) AS average_grade
FROM grades g
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN disciplines d ON d.id = g.discipline_id
LEFT JOIN teachers t ON t.id = d.teacher_id
WHERE s.id = 15 AND t.id = 4