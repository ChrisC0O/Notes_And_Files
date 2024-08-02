# detectron2 Instalation on ubuntu:

#### Install Python 3.8.0
```bash
# Run this command to make sure _lzma get made when installing Python
sudo apt-get install liblzma-dev
```

Then:
```bash
sudo apt-get install libssl-dev openssl
wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz
tar xzvf Python-3.8.0.tgz
cd Python-3.8.0
./configure
make
sudo make install
```

#### Install PyTorch:
Make a virtuel enviroment and install Torch.
Follow the guide on [pytorch.org](https://pytorch.org/)

#### Install detectron2:
Follow the guide on [readthedocs](https://detectron2.readthedocs.io/en/latest/tutorials/install.html)

#### Get Started!
[Tutorial](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5)
