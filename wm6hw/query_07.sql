SELECT s.fullname AS student, date_of AS date, grade
FROM grades g
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN disciplines d ON d.id = g.discipline_id
LEFT JOIN [groups] gr ON gr.id = s.group_id
WHERE d.id = 3 AND gr.id = 2
ORDER BY s.fullname