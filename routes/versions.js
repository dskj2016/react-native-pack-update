/*
* @Author: keminggu
* @Date:   2016-09-26 11:41:33
* @Last Modified by:   keminggu
* @Last Modified time: 2016-09-28 11:18:03
*/

var express = require('express');
var router = express.Router();

//获取最新版本号
router.get('/', function(req, res, next) {
  res.json({
    "version": "1.11.45",
    "minAppVersion": "1.0",
    "url": {
      "url": "http://10.8.71.186:3000/package/HotUpdateDemo/android/2.0/bundle/1.0.10/index.android.bundle.dskj?raw=1",
      "isRelative": false
    }
  });
});

module.exports = router;