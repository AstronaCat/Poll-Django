# working Branch


## MySQL DB 설정

```sql
CREATE DATABASE polldb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'polluser'@'%' IDENTIFIED BY '11poll22';
GRANT ALL PRIVILEGES ON polldb.* TO 'polluser'@'%';
FLUSH PRIVILEGES;
```