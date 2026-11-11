# Simple Omnitrix Plymouth Splash Screen

The splash uses a 50-frame, 3-second loop for the rotating spinner arc and pulsing
green glow shown in `preview.html`. The source artwork and rendered frames are kept
in `images/`.

## Regenerating the animation

After changing `images/omnitrix.svg`, render the PNG frames with Inkscape:

```bash
python3 scripts/render-frames.py
```

The script writes `images/omnitrix-frame-0.png` through
`images/omnitrix-frame-49.png`. Plymouth advances one frame every three refresh
cycles; at Plymouth's 50 Hz refresh rate this gives a 3-second loop.

## Setup

### Ubuntu

```bash
git clone https://github.com/elkhayder/plymouth-omnitrix-splash.git
cd plymouth-omnitrix-splash
```

Render the frames before installing the theme:

```bash
python3 scripts/render-frames.py
```

```bash
sudo cp -r . /usr/share/plymouth/themes/
sudo update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth /usr/share/plymouth/themes/omnitrix-splash/omnitrix-splash.plymouth 200
sudo update-alternatives --config default.plymouth
sudo update-initramfs -u
```