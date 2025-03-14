-- ==================================================
-- Multi-Tenant Employee Task & Time Tracking System
-- ==================================================

-- ----------------------------
-- 1. SCHEMA SETUP (Multi-Tenant)
-- ----------------------------
CREATE SCHEMA company_placeholder;
USE company_placeholder;

-- ----------------------------
-- 2. USERS & AUTHENTICATION
-- ----------------------------
CREATE TABLE users (
    id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    email         VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name    VARCHAR(100) NOT NULL,
    last_name     VARCHAR(100) NOT NULL,
    department_id BIGINT DEFAULT NULL,
    team_id       BIGINT DEFAULT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL
);

-- User profiles for additional information
CREATE TABLE user_profiles (
    user_id     BIGINT PRIMARY KEY,
    position    VARCHAR(100),
    skills      TEXT,
    bio         TEXT,
    profile_pic VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ----------------------------
-- 3. ROLES & PERMISSIONS
-- ----------------------------
CREATE TABLE roles (
    id   BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE permissions (
    id   BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE user_roles (
    user_id BIGINT,
    role_id BIGINT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

CREATE TABLE role_permissions (
    role_id       BIGINT,
    permission_id BIGINT,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);

-- ----------------------------
-- 4. ORGANIZATION STRUCTURE
-- ----------------------------
CREATE TABLE companies (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(255) UNIQUE NOT NULL,
    industry    VARCHAR(100),
    country     VARCHAR(100),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE departments (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    company_id BIGINT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE teams (
    id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    department_id BIGINT,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
);

-- Company settings (timezone, working hours)
CREATE TABLE company_settings (
    company_id         BIGINT PRIMARY KEY,
    timezone           VARCHAR(50) NOT NULL DEFAULT 'UTC',
    work_hours_per_day INT DEFAULT 8,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- ----------------------------
-- 5. PROJECTS & TASK MANAGEMENT
-- ----------------------------
CREATE TABLE projects (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(255) NOT NULL,
    description  TEXT,
    start_date   DATE NOT NULL,
    end_date     DATE,
    status       ENUM('Not Started', 'In Progress', 'Completed', 'On Hold') DEFAULT 'Not Started',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id   BIGINT NOT NULL,
    name         VARCHAR(255) NOT NULL,
    description  TEXT,
    priority     ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    status       ENUM('To Do', 'In Progress', 'Done') DEFAULT 'To Do',
    due_date     DATE,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Task assignments to users
CREATE TABLE task_assignments (
    task_id BIGINT,
    user_id BIGINT,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (task_id, user_id),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Task comments by users
CREATE TABLE comments (
    id        BIGINT AUTO_INCREMENT PRIMARY KEY,
    task_id   BIGINT NOT NULL,
    user_id   BIGINT NOT NULL,
    content   TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- File attachments for tasks
CREATE TABLE file_attachments (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    task_id    BIGINT NOT NULL,
    file_path  VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- ----------------------------
-- 6. TIME TRACKING & ATTENDANCE
-- ----------------------------
CREATE TABLE time_logs (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id    BIGINT NOT NULL,
    task_id    BIGINT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time   TIMESTAMP DEFAULT NULL,
    duration   INT, -- Duration in minutes
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

CREATE TABLE attendance (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id    BIGINT NOT NULL,
    check_in   TIMESTAMP NOT NULL,
    check_out  TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Leave requests (vacation, sick leave, etc.)
CREATE TABLE leave_requests (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id    BIGINT NOT NULL,
    leave_type ENUM('Vacation', 'Sick Leave', 'Personal', 'Other') NOT NULL,
    start_date DATE NOT NULL,
    end_date   DATE NOT NULL,
    status     ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ----------------------------
-- 7. NOTIFICATIONS & ACTIVITY LOGS
-- ----------------------------
CREATE TABLE notifications (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id    BIGINT NOT NULL,
    message    TEXT NOT NULL,
    read_status BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE activity_logs (
    id        BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id   BIGINT NOT NULL,
    action    TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ----------------------------
-- 8. BILLING & PAYROLL (OPTIONAL)
-- ----------------------------
CREATE TABLE invoices (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    company_id BIGINT NOT NULL,
    amount     DECIMAL(10,2) NOT NULL,
    issued_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status     ENUM('Pending', 'Paid') DEFAULT 'Pending',
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- ==================================================
-- END OF SCHEMA
-- ==================================================