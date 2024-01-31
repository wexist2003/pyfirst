SELECT d.name, gr.name, ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN disciplines d ON d.id = g.discipline_id
LEFT JOIN [groups] gr ON gr.id = s.group_id
WHERE d.id = 3
GROUP BY gr.name
ORDER BY average_grade DESC