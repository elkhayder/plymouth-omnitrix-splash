# Simple Omnitrix Plymouth Splash Screen


## Setup

### Ubuntu

```bash
cd plymouth-omnitrix-splash
```

```bash
sudo cp -r . /usr/share/plymouth/themes/
sudo update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth /usr/share/plymouth/themes/omnitrix-splash/omnitrix-splash.plymouth 200
sudo update-alternatives --config default.plymouth
sudo update-initramfs -u
```