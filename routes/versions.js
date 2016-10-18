/*
* @Author: keminggu
* @Date:   2016-09-26 11:41:33
* @Last Modified by:   keminggu
* @Last Modified time: 2016-10-18 15:33:47
*/

var express = require('express');
var router = express.Router();
var path = require('path');

//获取最新版本号
//projectName: 项目名称
//platform: 平台名称 ios|android
router.get('/:projectName/:platform', function(req, res, next) {
  var projectName = req.params.projectName;
  var platform = req.params.platform;
  if (!projectName ||  !platform) {
    console.log('projectName or platform is null');
  };
  res.sendFile(path.join(__dirname, '../public/package/' + projectName + '/' + platform + '/version.json'));
});

module.exports = router;