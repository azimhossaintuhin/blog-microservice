-- mysql-init/init.sql
CREATE USER IF NOT EXISTS 'mysql'@'%' IDENTIFIED BY 'mysql';
GRANT ALL PRIVILEGES ON *.* TO 'mysql'@'%';
FLUSH PRIVILEGES;
