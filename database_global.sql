-- ==================================================
-- GLOBAL DATABASE SETUP
-- ==================================================
CREATE DATABASE main_system;
USE main_system;

-- ----------------------------
-- GLOBAL AUTHENTICATION TABLE
-- ----------------------------
CREATE TABLE tenant_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    tenant_schema VARCHAR(255) NOT NULL,  -- The schema where the user's data is stored
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);