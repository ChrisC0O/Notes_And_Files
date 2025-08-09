## Prerequisites

Before starting, ensure you have:

- **Administrative access** (sudo) on both the source and destination Ubuntu machines.
- **SSH access** to both machines for secure file transfer and remote commands.
- **WordPress site details**:
  - Location of the WordPress files (e.g., `/var/www/html/wordpress`).
  - Database name, username, and password (found in `wp-config.php`).
- **Backup tools** installed on both machines:
  - `zip` for compressing files (`sudo apt install zip unzip`).
  - `rsync` for file transfer (`sudo apt install rsync`).
  - `mysqldump` for database backup (part of MySQL/MariaDB).
- **Same or compatible versions** of PHP, MySQL/MariaDB, and Apache/Nginx on both machines.
- A **domain name** or temporary access to test the migrated site.

---

## Step 1: Back Up the WordPress Site on the Source Machine

### 1.1 Back Up WordPress Files
The WordPress files include the core files, themes, plugins, and uploads. These are typically located in the web server’s document root (e.g., `/var/www/html/wordpress`).

1. **Log in to the source machine** via SSH:
   ```bash
   ssh user@source-server-ip
   ```

2. **Navigate to the WordPress directory**:
   ```bash
   cd /var/www/html/wordpress
   ```

3. **Compress the WordPress files** into a `.zip` archive:
   ```bash
   zip -r wordpress_backup.zip .
   ```

4. **Move the backup to a safe location** (e.g., your home directory):
   ```bash
   mv wordpress_backup.zip ~/wordpress_backup.zip
   ```

### 1.2 Back Up the WordPress Database
The database contains all your site’s content (posts, pages, comments, settings, etc.).

1. **Locate the database details** in `wp-config.php`:
   ```bash
   nano /var/www/html/wordpress/wp-config.php
   ```
   Look for:
   ```php
   define('DB_NAME', 'your_database_name');
   define('DB_USER', 'your_database_user');
   define('DB_PASSWORD', 'your_database_password');
   define('DB_HOST', 'localhost');
   ```

2. **Export the database** using `mysqldump`:
   ```bash
   mysqldump -u your_database_user -p your_database_name > wordpress_db_backup.sql
   ```
   Enter the database password when prompted. This creates a `wordpress_db_backup.sql` file in your current directory.

3. **Move the database backup** to a safe location:
   ```bash
   mv wordpress_db_backup.sql ~/wordpress_db_backup.sql
   ```

---

## Step 2: Transfer Files and Database to the Destination Machine

### 2.1 Set Up SSH Access
Ensure you can SSH from the source to the destination machine. If not already set up, generate an SSH key on the source machine and copy it to the destination:

1. On the source machine:
   ```bash
   ssh-keygen -t rsa
   ssh-copy-id user@destination-server-ip
   ```

2. Test SSH access:
   ```bash
   ssh user@destination-server-ip
   ```

### 2.2 Transfer WordPress Files
Use `rsync` or `scp` to transfer the compressed WordPress files securely.

- **Using `rsync`** (recommended for large sites or resuming interrupted transfers):
   ```bash
   rsync -avz ~/wordpress_backup.zip user@destination-server-ip:~/wordpress_backup.zip
   ```

- **Using `scp`** (simpler for smaller sites):
   ```bash
   scp ~/wordpress_backup.zip user@destination-server-ip:~/wordpress_backup.zip
   ```

### 2.3 Transfer the Database Backup
Similarly, transfer the database backup:
```bash
rsync -avz ~/wordpress_db_backup.sql user@destination-server-ip:~/wordpress_db_backup.sql
```

---

## Step 3: Set Up the Destination Machine

### 3.1 Install Required Software
Ensure the destination machine has the necessary software installed:
```bash
sudo apt update
sudo apt install apache2 mysql-server php php-mysql libapache2-mod-php unzip
```
For Nginx, replace `apache2` and `libapache2-mod-php` with `nginx` and `php-fpm`.

### 3.2 Set Up the Web Server
1. **Create the WordPress directory**:
   ```bash
   sudo mkdir -p /var/www/html/wordpress
   sudo chown -R www-data:www-data /var/www/html/wordpress
   ```

2. **Unzip the WordPress files**:
   ```bash
   cd /var/www/html/wordpress
   sudo unzip ~/wordpress_backup.zip
   ```

3. **Set correct permissions**:
   ```bash
   sudo chown -R www-data:www-data /var/www/html/wordpress
   sudo chmod -R 755 /var/www/html/wordpress
   ```

4. **Configure the web server**:
   - **For Apache**:
     Create or edit the virtual host configuration:
     ```bash
     sudo nano /etc/apache2/sites-available/wordpress.conf
     ```
     Add:
     ```apache
     <VirtualHost *:80>
         ServerName your-domain.com
         DocumentRoot /var/www/html/wordpress
         <Directory /var/www/html/wordpress>
             AllowOverride All
         </Directory>
         ErrorLog ${APACHE_LOG_DIR}/wordpress_error.log
         CustomLog ${APACHE_LOG_DIR}/wordpress_access.log combined
     </VirtualHost>
     ```
     Enable the site and rewrite module:
     ```bash
     sudo a2ensite wordpress.conf
     sudo a2enmod rewrite
     sudo systemctl restart apache2
     ```

   - **For Nginx**:
     Create or edit the configuration:
     ```bash
     sudo nano /etc/nginx/sites-available/wordpress
     ```
     Add:
     ```nginx
     server {
         listen 80;
         server_name your-domain.com;
         root /var/www/html/wordpress;
         index index.php;
         location / {
             try_files $uri $uri/ /index.php?$args;
         }
         location ~ \.php$ {
             include snippets/fastcgi-php.conf;
             fastcgi_pass unix:/run/php/php7.4-fpm.sock; # Adjust PHP version as needed
             fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
             include fastcgi_params;
         }
     }
     ```
     Link and restart:
     ```bash
     sudo ln -s /etc/nginx/sites-available/wordpress /etc/nginx/sites-enabled/
     sudo nginx -t
     sudo systemctl restart nginx
     ```

### 3.3 Set Up the Database
1. **Log in to MySQL/MariaDB**:
   ```bash
   sudo mysql -u root -p
   ```

2. **Create a new database**:
   ```sql
   CREATE DATABASE new_wordpress_db;
   ```

3. **Create a database user** and grant permissions:
   ```sql
   CREATE USER 'new_wp_user'@'localhost' IDENTIFIED BY 'new_secure_password';
   GRANT ALL PRIVILEGES ON new_wordpress_db.* TO 'new_wp_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

4. **Import the database backup**:
   ```bash
   mysql -u new_wp_user -p new_wordpress_db < ~/wordpress_db_backup.sql
   ```
   Enter the password (`new_secure_password`) when prompted.

### 3.4 Update `wp-config.php`
Update the database connection details in the WordPress configuration file:
```bash
sudo nano /var/www/html/wordpress/wp-config.php
```
Modify the following lines to match the new database details:
```php
define('DB_NAME', 'new_wordpress_db');
define('DB_USER', 'new_wp_user');
define('DB_PASSWORD', 'new_secure_password');
define('DB_HOST', 'localhost');
```

---

## Step 4: Update Site URLs (if necessary)
If the domain name or URL structure is changing (e.g., from `old-domain.com` to `new-domain.com` or a different path), update the site URLs in the database.

1. **Log in to MySQL**:
   ```bash
   mysql -u new_wp_user -p new_wordpress_db
   ```

2. **Update the `wp_options` table**:
   ```sql
   UPDATE wp_options SET option_value = 'http://new-domain.com' WHERE option_name = 'siteurl';
   UPDATE wp_options SET option_value = 'http://new-domain.com' WHERE option_name = 'home';
   ```

3. **Update URLs in posts and metadata** (to fix internal links and media):
   Use a tool like `wp-cli` or a plugin like **Better Search Replace** after the site is running, or run the following SQL:
   ```sql
   UPDATE wp_posts SET post_content = REPLACE(post_content, 'http://old-domain.com', 'http://new-domain.com');
   UPDATE wp_postmeta SET meta_value = REPLACE(meta_value, 'http://old-domain.com', 'http://new-domain.com');
   ```

4. **Exit MySQL**:
   ```sql
   EXIT;
   ```

Alternatively, install `wp-cli` for easier URL updates:
```bash
sudo curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
sudo chmod +x wp-cli.phar
sudo mv wp-cli.phar /usr/local/bin/wp
cd /var/www/html/wordpress
wp search-replace 'http://old-domain.com' 'http://new-domain.com' --all-tables
```

---

## Step 5: Test the Migrated Site
1. **Update DNS or hosts file**:
   - If using a domain, update the DNS records to point to the destination server’s IP address.
   - For testing, edit the local `/etc/hosts` file on your computer:
     ```bash
     sudo nano /etc/hosts
     ```
     Add:
     ```
     destination-server-ip your-domain.com
     ```

2. **Access the site** in a browser:
   - Visit `http://your-domain.com` or the server’s IP address.
   - Check the front end and log in to the WordPress admin dashboard (`/wp-admin`).

3. **Verify functionality**:
   - Check pages, posts, images, and links.
   - Test forms, comments, and plugins.
   - Ensure permalinks work (refresh permalinks in **Settings > Permalinks** if needed).

---

## Step 6: Finalize and Clean Up
1. **Set up SSL (optional but recommended)**:
   - Install Certbot for Let’s Encrypt:
     ```bash
     sudo apt install certbot python3-certbot-apache
     sudo certbot --apache
     ```
     Or for Nginx:
     ```bash
     sudo apt install certbot python3-certbot-nginx
     sudo certbot --nginx
     ```

2. **Update .htaccess or Nginx rules** (if needed):
   - Ensure the `.htaccess` file (Apache) or Nginx configuration supports WordPress permalinks.

3. **Clean up backups**:
   - Remove temporary backup files from both machines:
     ```bash
     rm ~/wordpress_backup.zip ~/wordpress_db_backup.sql
     ```

4. **Monitor the site**:
   - Check error logs (`/var/log/apache2/error.log` or `/var/log/nginx/error.log`).
   - Set up a backup schedule on the new server.

---

## Troubleshooting Common Issues
- **Database connection errors**: Verify `wp-config.php` credentials and ensure MySQL is running (`sudo systemctl status mysql`).
- **404 errors**: Check permalink settings or `.htaccess`/Nginx rewrite rules.
- **Mixed content warnings**: Ensure all URLs in the database use `https` if SSL is enabled.
- **Missing images**: Verify the `wp-content/uploads` folder was transferred correctly and permissions are set.
- **White screen of death**: Enable debugging in `wp-config.php`:
  ```php
  define('WP_DEBUG', true);
  define('WP_DEBUG_LOG', true);
  define('WP_DEBUG_DISPLAY', false);
  ```
  Check `/wp-content/debug.log` for errors.

---

## Additional Tips
- **Use a migration plugin** (e.g., Duplicator or All-in-One WP Migration) for simpler migrations, but manual migration ensures full control.
- **Test on a staging environment** before updating DNS for production.
- **Back up regularly** on the new server using tools like UpdraftPlus or cron jobs for automated backups.
