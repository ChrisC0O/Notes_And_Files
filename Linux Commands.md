#### Command for fixing wrong USB loading times (Ubuntu):
```bash
echo vm.dirty_bytes=15000000 | sudo tee -a /etc/sysctl.conf
```

#### Add support for RAR files into the standard "archive manager":
```bash
sudo apt-get install rar
```

#### Install Python:
```bash
sudo apt-get install libssl-dev openssl
wget https://www.python.org/ftp/python/{version}/Python-{version}.tgz
tar xzvf Python-3.5.0.tgz
cd Python-3.5.0
./configure
make
sudo make install

To check if python is installed type python3.5 else:

sudo ln -fs /opt/Python-3.5.0/Python /usr/bin/python3.5
```