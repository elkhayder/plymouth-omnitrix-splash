# Simple Omnitrix Plymouth Splash Screen


## Setup

### Ubuntu

```bash
git clone https://github.com/elkhayder/plymouth-omnitrix-splash.git
cd plymouth-omnitrix-splash
```

```bash
sudo cp -r . /usr/share/plymouth/themes/
sudo update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth /usr/share/plymouth/themes/omnitrix-splash/omnitrix-splash.plymouth 200
sudo update-alternatives --config default.plymouth
sudo update-initramfs -u
```