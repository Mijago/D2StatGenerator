# What is this?
This downloads all your PGCRs (Post Game Carnage Report) from the Bungie.net api and builds some graphs.

# How to Use?
3) Install all required packages
   1) `python -m pip install pandas plotly pathos requests pretty_html_table`
   2) If you want to use mp4 instead of gif, also install `python -m pip python-ffmpeg` and put an `ffmpeg` executable in your PATH variable. Then set the `video_type` in `main.py` to `mp4`
4) Add your api key to `main.py`
5) Edit your user info in `main.py`
6) Run! `python3 main.py`
   1) May take a while. I need 45 seconds for 1000 PGCRs with a download speed of 4.5mb/s.


# Examples
These examples are from the early stage:

![img_4.png](examples/img_4.png)
![img_1.png](examples/img_1.png)
![img_2.png](examples/img_2.png)
![img_3.png](examples/img_3.png)
