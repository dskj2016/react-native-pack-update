/*
* @Author: keminggu
* @Date:   2016-09-26 11:41:33
* @Last Modified by:   keminggu
* @Last Modified time: 2016-10-17 16:34:25
*/

var express = require('express');
var router = express.Router();

//获取最新版本号
router.get('/', function(req, res, next) {
  res.json({
    "version": "1.0.24",
    "minAppVersion": "1.0",
    "url": {
      "url": "http://10.8.70.221:3000/package/HotUpdateDemo/ios/1.0/bundle/1.0.3/index.ios.bundle.dskj",
      "isRelative": false
    }
  });
});

module.exports = router;