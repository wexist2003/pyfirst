SELECT s.fullname AS student
FROM students s
LEFT JOIN [groups] gr ON gr.id = s.group_id
WHERE gr.id = 2
ORDER BY s.fullname