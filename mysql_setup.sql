-- MySQL Setup Script for TenantPro
-- Run this before starting the project with MySQL

CREATE DATABASE IF NOT EXISTS tenants_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'tenants_user'@'localhost' 
    IDENTIFIED BY 'SecurePassword123!';

GRANT ALL PRIVILEGES ON tenants_db.* 
    TO 'tenants_user'@'localhost';

FLUSH PRIVILEGES;

-- Verify
SHOW DATABASES LIKE 'tenants_db';
SELECT User, Host FROM mysql.user WHERE User = 'tenants_user';
