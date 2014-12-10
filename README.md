BandBrosBot
=========================

3DS『大合奏!バンドブラザーズP』の新曲情報を呟くbotです

http://twitter.com/bandbrosp

http://bandbros-p.nintendo.co.jp/release/newRelease/

設定方法
================

```sh
$ export CONSUMER_KEY=aaaaaaaaaa
$ export CONSUMER_SECRET=bbbbbbb
$ export ACCESS_TOKEN_KEY=ccccccc
$ export ACCESS_TOKEN_SECRET=dddddddd
$ pip install -r requirements.txt
$ ./bin/notify_new_release
```

HerokuへDeployする
===================

```sh
$ heroku login
$ heroku create
$ heroku addons:add scheduler:standard
$ heroku config:add CONSUMER_KEY=aaaaaaaaaa      
$ heroku config:add CONSUMER_SECRET=bbbbbbb
$ heroku config:add ACCESS_TOKEN_KEY=ccccccc     
$ heroku config:add ACCESS_TOKEN_SECRET=dddddddd 
$ git push heroku master
```
