-- Sample data for UIS-Connect
-- This will populate the database with test data to demonstrate the app's functionality

-- Sample Users
-- Note: In a real application, passwords would be properly hashed
-- These are placeholder hashes for testing only
INSERT INTO Users (username, email, password_hash, first_name, last_name, bio, major, join_date, last_login)
VALUES 
    ('john_doe', 'john.doe@uis.edu', 'pbkdf2:sha256:150000$aB1cD2eF$e8c9b2d0a1f6e3d5c7b9a0f3e5d2c1b8a7f6', 'John', 'Doe', 'Computer Science student interested in AI', 'Computer Science', '2024-09-01 10:00:00', '2025-04-10 14:30:00'),
    ('jane_smith', 'jane.smith@uis.edu', 'pbkdf2:sha256:150000$gH3iJ4kL$b7a9c2e1d3f5g7h9i0j2k4l6m8n0p2q4', 'Jane', 'Smith', 'Biology major with a focus on marine biology', 'Biology', '2024-08-15 09:30:00', '2025-04-12 16:45:00'),
    ('mike_johnson', 'mike.johnson@uis.edu', 'pbkdf2:sha256:150000$mN5oP6qR$r3s5t7u9v2w4x6y8z0a2b4c6d8e0f2g4', 'Mike', 'Johnson', 'Math enthusiast and tutor', 'Mathematics', '2024-09-03 14:15:00', '2025-04-13 10:20:00'),
    ('sarah_williams', 'sarah.williams@uis.edu', 'pbkdf2:sha256:150000$sT7uV8wX$h5i7j9k1l3m5n7o9p1q3r5s7t9u1v3w5', 'Sarah', 'Williams', 'Psychology student researching human behavior', 'Psychology', '2024-08-20 11:45:00', '2025-04-11 13:10:00'),
    ('david_brown', 'david.brown@uis.edu', 'pbkdf2:sha256:150000$yZ9aB0cD$x6y8z0a2b4c6d8e0f2g4h6i8j0k2l4m6', 'David', 'Brown', 'Business administration major with focus on marketing', 'Business', '2024-09-05 08:30:00', '2025-04-14 09:15:00'),
    ('emily_jones', 'emily.jones@uis.edu', 'pbkdf2:sha256:150000$eF1gH2iJ$n7o9p1q3r5s7t9u1v3w5x7y9z1a3b5c7', 'Emily', 'Jones', 'English literature lover and aspiring writer', 'English', '2024-08-25 13:20:00', '2025-04-10 11:30:00'),
    ('ryan_miller', 'ryan.miller@uis.edu', 'pbkdf2:sha256:150000$kL3mN4oP$d8e0f2g4h6i8j0k2l4m6n8o0p2q4r6s8', 'Ryan', 'Miller', 'Physics major interested in theoretical physics', 'Physics', '2024-09-10 15:40:00', '2025-04-12 14:25:00'),
    ('olivia_davis', 'olivia.davis@uis.edu', 'pbkdf2:sha256:150000$qR5sT6uV$t9u1v3w5x7y9z1a3b5c7d9e1f3g5h7i9', 'Olivia', 'Davis', 'Chemistry student with a passion for organic chemistry', 'Chemistry', '2024-08-30 10:10:00', '2025-04-13 16:50:00'),
    ('jacob_wilson', 'jacob.wilson@uis.edu', 'pbkdf2:sha256:150000$wX7yZ8aB$j0k2l4m6n8o0p2q4r6s8t0u2v4w6x8y0', 'Jacob', 'Wilson', 'Political science major interested in international relations', 'Political Science', '2024-09-12 12:35:00', '2025-04-11 15:15:00'),
    ('emma_taylor', 'emma.taylor@uis.edu', 'pbkdf2:sha256:150000$cD9eF0gH$z1a3b5c7d9e1f3g5h7i9j1k3l5m7n9o1', 'Emma', 'Taylor', 'History enthusiast focusing on American history', 'History', '2024-09-02 09:45:00', '2025-04-14 10:40:00');

-- Sample Courses
INSERT INTO Courses (course_code, course_name, department)
VALUES 
    ('CSC367', 'Database Systems', 'Computer Science'),
    ('CSC385', 'Data Structures and Algorithms', 'Computer Science'),
    ('BIO241', 'Cell Biology', 'Biology'),
    ('MAT332', 'Linear Algebra', 'Mathematics'),
    ('PSY301', 'Cognitive Psychology', 'Psychology'),
    ('BUS220', 'Principles of Marketing', 'Business'),
    ('ENG315', 'Creative Writing', 'English'),
    ('PHY301', 'Classical Mechanics', 'Physics'),
    ('CHM241', 'Organic Chemistry', 'Chemistry'),
    ('POS352', 'International Relations', 'Political Science'),
    ('HIS202', 'American History', 'History'),
    ('CSC310', 'Web Programming', 'Computer Science');

-- Sample User_Courses
INSERT INTO User_Courses (user_id, course_id, semester)
VALUES 
    (1, 1, 'Spring 2025'),
    (1, 2, 'Spring 2025'),
    (1, 12, 'Fall 2024'),
    (2, 3, 'Spring 2025'),
    (3, 4, 'Spring 2025'),
    (4, 5, 'Spring 2025'),
    (5, 6, 'Spring 2025'),
    (6, 7, 'Spring 2025'),
    (7, 8, 'Spring 2025'),
    (8, 9, 'Spring 2025'),
    (9, 10, 'Spring 2025'),
    (10, 11, 'Spring 2025'),
    (2, 5, 'Spring 2025'),
    (3, 1, 'Spring 2025'),
    (4, 7, 'Spring 2025');

-- Sample Posts
INSERT INTO Posts (user_id, content, post_date, is_public)
VALUES 
    (1, 'Just finished my database project. SQLite is amazing for small applications!', '2025-04-01 14:20:00', 1),
    (2, 'Looking for study partners for the Cell Biology midterm next week.', '2025-04-02 10:15:00', 1),
    (3, 'Anyone have good resources for understanding eigenvalues and eigenvectors?', '2025-04-03 16:30:00', 1),
    (4, 'Fascinating lecture today on memory formation and retrieval.', '2025-04-04 13:45:00', 1),
    (5, 'Check out this interesting article on digital marketing strategies.', '2025-04-05 09:20:00', 1),
    (6, 'Would anyone be interested in joining a creative writing workshop this weekend?', '2025-04-06 15:10:00', 1),
    (7, 'Just solved the most challenging mechanics problem. Physics is beautiful!', '2025-04-07 11:25:00', 1),
    (8, 'Organic chemistry lab report due tomorrow. Anyone want to review each other''s work?', '2025-04-08 17:40:00', 1),
    (9, 'Great discussion in class today about global governance structures.', '2025-04-09 12:50:00', 1),
    (10, 'Working on a presentation about the Civil Rights Movement. Looking for primary sources.', '2025-04-10 14:15:00', 1),
    (1, 'Looking for project partners for the Web Programming final project.', '2025-04-11 09:30:00', 1),
    (2, 'Does anyone have the textbook for Cognitive Psychology? The bookstore is out.', '2025-04-12 16:20:00', 1);

-- Sample Post_Courses
INSERT INTO Post_Courses (post_id, course_id)
VALUES 
    (1, 1),  -- Database post linked to Database Systems course
    (2, 3),  -- Cell Biology post linked to Cell Biology course
    (3, 4),  -- Linear Algebra post linked to Linear Algebra course
    (4, 5),  -- Psychology post linked to Cognitive Psychology
    (5, 6),  -- Marketing post linked to Principles of Marketing
    (6, 7),  -- Writing post linked to Creative Writing
    (7, 8),  -- Physics post linked to Classical Mechanics
    (8, 9),  -- Chemistry post linked to Organic Chemistry
    (9, 10), -- Political Science post linked to International Relations
    (10, 11), -- History post linked to American History
    (11, 12), -- Web programming post linked to Web Programming
    (12, 5);  -- Psychology textbook post linked to Cognitive Psychology

-- Sample Comments
INSERT INTO Comments (post_id, user_id, content, comment_date)
VALUES 
    (1, 3, 'What features did you implement in your project?', '2025-04-01 15:30:00'),
    (1, 5, 'I''m also working with SQLite for my business analytics project. Any tips?', '2025-04-01 16:45:00'),
    (2, 4, 'I can study with you. How about meeting at the library on Monday?', '2025-04-02 11:20:00'),
    (3, 1, 'Check out the Math tutoring center, they have great resources for Linear Algebra.', '2025-04-03 17:15:00'),
    (4, 2, 'I found that topic fascinating too! Did you read the paper Professor Williams recommended?', '2025-04-04 14:30:00'),
    (5, 9, 'Thanks for sharing! This will be helpful for my marketing project.', '2025-04-05 10:40:00'),
    (6, 10, 'I''d be interested! What time are you planning to meet?', '2025-04-06 16:05:00'),
    (7, 3, 'Physics problems can be so satisfying when you finally crack them.', '2025-04-07 12:10:00'),
    (8, 1, 'I can help review. I took organic chem last semester.', '2025-04-08 18:20:00'),
    (9, 5, 'International relations is becoming increasingly important in the business world too.', '2025-04-09 13:45:00'),
    (10, 6, 'The university archive has some great primary sources on civil rights.', '2025-04-10 15:10:00'),
    (11, 7, 'I''m looking for a team too! Want to partner up?', '2025-04-11 10:25:00');

-- Sample Likes
INSERT INTO Likes (user_id, post_id, like_date)
VALUES 
    (3, 1, '2025-04-01 15:25:00'),
    (5, 1, '2025-04-01 16:40:00'),
    (7, 1, '2025-04-01 18:15:00'),
    (4, 2, '2025-04-02 11:15:00'),
    (6, 2, '2025-04-02 13:30:00'),
    (1, 3, '2025-04-03 17:10:00'),
    (5, 3, '2025-04-03 19:25:00'),
    (2, 4, '2025-04-04 14:25:00'),
    (8, 4, '2025-04-04 16:50:00'),
    (9, 5, '2025-04-05 10:35:00'),
    (10, 6, '2025-04-06 16:00:00'),
    (3, 7, '2025-04-07 12:05:00'),
    (1, 8, '2025-04-08 18:15:00'),
    (5, 9, '2025-04-09 13:40:00'),
    (6, 10, '2025-04-10 15:05:00'),
    (7, 11, '2025-04-11 10:20:00'),
    (2, 12, '2025-04-12 17:30:00');

-- Sample Friendships
INSERT INTO Friendships (user_id1, user_id2, status, action_date)
VALUES 
    (1, 2, 'accepted', '2025-03-10 09:30:00'),
    (1, 3, 'accepted', '2025-03-12 14:45:00'),
    (1, 5, 'accepted', '2025-03-15 11:20:00'),
    (2, 4, 'accepted', '2025-03-11 16:30:00'),
    (2, 6, 'accepted', '2025-03-14 10:15:00'),
    (3, 7, 'accepted', '2025-03-16 13:50:00'),
    (4, 8, 'accepted', '2025-03-18 15:25:00'),
    (5, 9, 'accepted', '2025-03-20 12:40:00'),
    (6, 10, 'accepted', '2025-03-22 09:15:00'),
    (1, 7, 'pending', '2025-04-01 14:30:00'),
    (2, 8, 'pending', '2025-04-02 16:45:00'),
    (3, 9, 'pending', '2025-04-03 11:10:00'),
    (4, 10, 'pending', '2025-04-04 09:55:00'),
    (5, 6, 'pending', '2025-04-05 13:20:00');