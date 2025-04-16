-- Database Schema for UIS-Connect
-- Drop existing tables if they exist
DROP TABLE IF EXISTS Friendships;
DROP TABLE IF EXISTS Likes;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Post_Courses;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS User_Courses;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Users;

-- Users table for storing user information
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,  -- Hashed for security
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    bio TEXT,
    major VARCHAR(100),
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Courses table (to support course-related features)
CREATE TABLE Courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL
);

-- User_Courses table (many-to-many relationship between users and courses)
CREATE TABLE User_Courses (
    user_id INTEGER,
    course_id INTEGER,
    semester VARCHAR(20) NOT NULL,
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

-- Posts table for storing user posts
CREATE TABLE Posts (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Post_Courses table (many-to-many relationship for tagging posts with courses)
CREATE TABLE Post_Courses (
    post_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (post_id, course_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

-- Comments table for storing comments on posts
CREATE TABLE Comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Likes table for tracking post likes
CREATE TABLE Likes (
    user_id INTEGER,
    post_id INTEGER,
    like_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE
);

-- Friendships table (symmetric relationship)
CREATE TABLE Friendships (
    user_id1 INTEGER,
    user_id2 INTEGER,
    status VARCHAR(20) NOT NULL,  -- 'pending', 'accepted', 'rejected'
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id1, user_id2),
    FOREIGN KEY (user_id1) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id2) REFERENCES Users(user_id) ON DELETE CASCADE,
    CHECK (user_id1 < user_id2)  -- Ensures unique representation of friendship pairs
);

-- Indexes for performance optimization
CREATE INDEX idx_posts_user_id ON Posts(user_id);
CREATE INDEX idx_comments_post_id ON Comments(post_id);
CREATE INDEX idx_comments_user_id ON Comments(user_id);
CREATE INDEX idx_likes_post_id ON Likes(post_id);
CREATE INDEX idx_user_courses_user_id ON User_Courses(user_id);
CREATE INDEX idx_user_courses_course_id ON User_Courses(course_id);
CREATE INDEX idx_post_courses_post_id ON Post_Courses(post_id);