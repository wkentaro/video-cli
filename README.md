<div align="center">
  <h1>video-cli</h1>
  <h3>Command line tools for quick video editing.</h3>
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

### `video_retime`: **Video Retiming (Speed Up/Down)**

```bash
$ video_retime data/2018-11-02_14-44-14.mp4 --retime 2
$ video_retime data/2018-11-02_14-44-14.mp4 --retime 2 --inplace
```
