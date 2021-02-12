<div align="center">
  <h1>video-cli</h1>
  <h3>Command line tools for quick video editing.</h3>
  <a href="https://pypi.python.org/pypi/video-cli"><img src="https://img.shields.io/pypi/v/video-cli.svg"></a>
  <a href="https://pypi.org/project/video-cli"><img src="https://img.shields.io/pypi/pyversions/video-cli.svg"></a>
  <a href="https://github.com/wkentaro/video-cli/actions"><img src="https://github.com/wkentaro/video-cli/workflows/ci/badge.svg"></a>
</div>


Video-cli is made aiming at editing video with a one-line
command on a terminal. You can do more detailed video editing using
other Python tools (e.g., [MoviePy](https://github.com/Zulko/moviepy))
and GUI video editors (e.g., [iMovie](https://www.apple.com/imovie/)),
which is not the goal of this tool.


## Installation

```bash
pip install video-cli
```


## Commands

### `video-retime`: **Video Retiming (Speed Up/Down)**

```bash
video-retime data/2018-11-02_14-44-14.mp4 --retime 2
video-retime data/2018-11-02_14-44-14.mp4 --retime 2 --inplace
```

### `video-togif`: **Create a GIF**

```bash
video-togif data/2018-11-02_14-44-14.mp4 --fps 2 --duration 5
video-togif data/2018-11-02_14-44-14.mp4 --fps 2 --duration 5 --resize 0.5
```

### `video-trim`: **Video Triming**

```bash
video-trim data/2018-11-02_14-44-14.mp4 --start 3 --duration 5
```

### `video-tile`: **Video Tiling**

```bash
video-tile data/2018-11-02_14-44-14.mp4 data/2018-11-02_14-44-14.mp4 --shape 1x2 -o tile.mp4
```

### `video-toimg`: **Convert a Video to Images**

```bash
video-toimg data/2018-11-02_14-44-14.mp4 --rate 10 --start 3 --duration 10
```

### `video-tovideo`: **Convert to Video**

```bash
video-tovideo data/2018-11-02_14-44-14.mp4
```

### `video-resize`: **Video Resizing**

```bash
video-resize data/2018-11-02_14-44-14.mp4 --scale 0.5
```

### `video-fromimg`: **Create a Video from Images**

```bash
video-toimg data/2018-11-02_14-44-14.mp4
video-fromimg "data/2018-11-02_14-44-14/*.jpg" --fps 30
```

### `video-crop`: **Crop a region of a Video**

```bash
video-crop data/2018-11-02_14-44-14.mp4
```
