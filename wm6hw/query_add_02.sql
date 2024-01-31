SELECT s.fullname AS studet, g.grade AS average_grade
FROM grades g
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN disciplines d ON d.id = g.discipline_id
LEFT JOIN teachers t ON t.id = d.teacher_id
LEFT JOIN groups gr  ON gr.id = s.group_id
WHERE gr.id = 1 AND d.id = 4 AND g.date_of = (SELECT max(g.date_of) FROM grades g WHERE gr.id = s.group_id AND d.id = g.discipline_id)