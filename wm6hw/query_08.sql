SELECT d.name, ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN disciplines d ON d.id = g.discipline_id
LEFT JOIN [groups] gr ON gr.id = s.group_id
LEFT JOIN teachers t ON t.id = d.teacher_id 
WHERE t.id = 4
GROUP BY d.name
ORDER BY average_grade DESC 