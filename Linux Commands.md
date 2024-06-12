#### Command for fixing wrong USB loading times (Ubuntu):
```bash
echo vm.dirty_bytes=15000000 | sudo tee -a /etc/sysctl.conf
```

#### Add support for RAR files into the standard "archive manager":
```bash
sudo apt-get install rar
```
