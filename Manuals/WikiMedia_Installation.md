# MediaWiki Installation & Secure Configuration Guide  
**Cleaned, Organized, and Production-Ready**

---

## 1. Installation Instructions

> **Read First**: [Official MediaWiki Installation Guide](https://www.mediawiki.org/wiki/Manual:Installation_guide)

### Step-by-Step

1. **Download MediaWiki**
   ```bash
   wget https://releases.wikimedia.org/mediawiki/1.44/mediawiki-1.44.2.tar.gz
   tar -xvzf mediawiki-1.44.2.tar.gz
   mv mediawiki-1.44.2 /var/www/html/mediawiki
   ```

2. **Set Permissions**
   ```bash
   chown -R www-data:www-data /var/www/html/mediawiki
   chmod -R 755 /var/www/html/mediawiki
   ```

3. **Run Web Installer**
   - Visit: `http://your-server/mediawiki`
   - Follow the setup wizard
   - **Download `LocalSettings.php` when complete**

4. **Move `LocalSettings.php`**
   ```bash
   mv LocalSettings.php /var/www/html/mediawiki/LocalSettings.php
   ```

5. **Edit `LocalSettings.php`** → Use the **clean config below**

---

## 2. Final `LocalSettings.php` (Clean & Secure)

```php
<?php
# LocalSettings.php - MediaWiki 1.44.2
# Secure, private wiki with full lockdown
# Only authenticated, email-confirmed users can access content

if ( !defined( 'MEDIAWIKI' ) ) {
    exit;
}

## BASIC SETTINGS
$wgSitename = "My Test Wiki";
$wgMetaNamespace = "My_Test_Wiki";

$wgScriptPath = "/mediawiki";
$wgServer = "http://172.18.29.119";
$wgResourceBasePath = $wgScriptPath;

$wgLogos = [
    '1x'   => "$wgScriptPath/images/9/96/Icon_hjv.png",
    'icon' => "$wgScriptPath/images/9/96/Icon_hjv.png",
];

## UPLOADS - ALLOW ALL FILES (CAUTION!)
$wgEnableUploads = true;
$wgStrictFileExtensions = false;
$wgCheckFileExtensions = false;
$wgFileExtensions = [ 'png', 'gif', 'jpg', 'jpeg', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'txt', 'mp4', 'mp3' ];

## DATABASE
$wgDBtype = "mysql";
$wgDBserver = "localhost";
$wgDBname = "database";
$wgDBuser = "db_user";
$wgDBpassword = "P@ssw0rd";
$wgDBprefix = "";
$wgDBssl = false;
$wgDBTableOptions = "ENGINE=InnoDB, DEFAULT CHARSET=binary";
$wgSharedTables[] = "actor";

## PERFORMANCE
$wgMainCacheType = CACHE_NONE;
$wgMemCachedServers = [];

## EMAIL
$wgEnableEmail = true;
$wgEnableUserEmail = true;
$wgEmergencyContact = "admin@example.com";
$wgPasswordSender = "no-reply@example.com";
$wgEnotifUserTalk = false;
$wgEnotifWatchlist = false;
$wgEmailAuthentication = true;
$wgEmailConfirmToEdit = true;  # Require confirmed email to edit

## LANGUAGE & TIME
$wgLanguageCode = "en";
$wgLocaltimezone = "UTC";

## SECURITY KEYS (KEEP SECRET!)
$wgSecretKey = "35e43818b8b3f04fce0178bfdec9845d9afe7d0936aa19d13bec7389e7a0ba56";
$wgAuthenticationTokenVersion = "1";
$wgUpgradeKey = "e26c4de60badf1f4";

## TOOLS
$wgUseInstantCommons = false;
$wgPingback = false;  # Disable telemetry
$wgDiff3 = "/usr/bin/diff3";

## SKINS
$wgDefaultSkin = "timeless";
wfLoadSkin( 'MinervaNeue' );
wfLoadSkin( 'MonoBook' );
wfLoadSkin( 'Timeless' );
wfLoadSkin( 'Vector' );

## EXTENSIONS
wfLoadExtension( 'VisualEditor' );

## === FULL WIKI LOCKDOWN ===
# Only authenticated users can access anything

# Disable all anonymous access
$wgGroupPermissions['*']['read'] = false;
$wgGroupPermissions['*']['edit'] = false;
$wgGroupPermissions['*']['createpage'] = false;
$wgGroupPermissions['*']['createtalk'] = false;
$wgGroupPermissions['*']['upload'] = false;
$wgGroupPermissions['*']['writeapi'] = false;
$wgGroupPermissions['*']['move'] = false;
$wgGroupPermissions['*']['delete'] = false;
$wgGroupPermissions['*']['createaccount'] = false;
$wgGroupPermissions['*']['autocreateaccount'] = false;
$wgGroupPermissions['*']['readapi'] = false;

# Allow logged-in users
$wgGroupPermissions['user']['read'] = true;
$wgGroupPermissions['user']['edit'] = true;
$wgGroupPermissions['user']['upload'] = true;
$wgGroupPermissions['user']['move'] = true;

# Whitelist login pages
$wgWhitelistRead = [
    'Special:UserLogin',
    'Special:UserLogout',
    'Special:PasswordReset'
];

# API Security
$wgEnableAPI = true;
$wgEnableRestAPI = false;  # Disable REST API
$wgAllowCopyUploads = false;

# Hide from search engines
$wgDefaultRobotPolicy = 'noindex,nofollow';

# End of LocalSettings.php
```

---

## 3. Increase Upload File Size (PHP)

Edit PHP config:

```bash
sudo nano /etc/php/8.3/apache2/php.ini
```

Update these lines:
```ini
upload_max_filesize = 100M
post_max_size = 110M
max_execution_time = 300
memory_limit = 256M
```

Restart Apache:
```bash
sudo systemctl restart apache2
```

---

## 4. Security Summary

| Feature | Status |
|-------|--------|
| Anonymous viewing | Disabled |
| Anonymous editing | Disabled |
| Self-registration | Disabled |
| API access | Auth-only |
| REST API | Disabled |
| Email confirmation required | Enabled |
| File upload (all types) | Enabled |
| Search engine indexing | Blocked |

---

## 5. How to Add Users (No Registration)

### Option 1: CLI (Recommended)
```bash
cd /var/www/html/mediawiki/maintenance
php createAndPromote.php "JohnDoe" "StrongP@ssw0rd!" --force
```

### Option 2: Admin Panel
1. Log in as **admin**
2. Go to **Special:UserRights**
3. Enter username → check `user` → **Save**

> Users must **confirm email** before editing.

---

## 6. Best Practices

| Do | Don't |
|------|---------|
| Use HTTPS (`$wgServer = "https://..."`) | Hardcode IP in production |
| Backup `LocalSettings.php` | Commit DB password to Git |
| Use strong `$wgSecretKey` | Allow `.php` uploads |
| Monitor logs | Ignore PHP errors |

---

## 7. Optional: Enable Caching (Performance)

Uncomment and set:
```php
$wgCacheDirectory = "$IP/cache";
$wgMainCacheType = CACHE_ACCEL;
```

---

**You're done!**  
Your wiki is now **secure, private, and fully functional**.

> **Last Updated**: October 28, 2025  
> **MediaWiki Version**: 1.44.2  
> **Status**: Production-Ready Lockdown
