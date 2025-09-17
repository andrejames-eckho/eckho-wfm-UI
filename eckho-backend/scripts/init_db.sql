-- Create the database user
CREATE USER eckho_user WITH PASSWORD 'eckho_password';

-- Create the database
CREATE DATABASE eckho_wfm OWNER eckho_user;

-- Grant all privileges to the user on the database
GRANT ALL PRIVILEGES ON DATABASE eckho_wfm TO eckho_user;
