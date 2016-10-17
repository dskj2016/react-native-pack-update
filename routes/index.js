var express = require('express');
var path = require('path');
var process = require('child_process');

var router = express.Router();
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', {
    title: '控制台服务',
    res: '' 
  });
});

//重svn更新代码
router.get('/updatecode', function(req, res, next) {
  var handleFile = path.join(__dirname, '../handle.py');
  console.log('handleFile====', handleFile);
  res.socket.timeout(10 * 60 * 1000); //设置超时
  process.execFile(handleFile, ['DashengChefu', '--svnupdate'], null,
    function (error,stdout,stderr) {
      console.log(stdout);
    if (error !== null) {
      console.log('exec error: ' + error);
    }

    res.render('index', {
      title: '控制台服务', 
      res: stdout 
    });
  });
});

//打包bundlejs
router.get('/bundlejs', function(req, res, next) {
  var handleFile = path.join(__dirname, '../handle.py');
  console.log('handleFile====', handleFile);
  res.socket.timeout(10 * 60 * 1000); //设置超时
  process.execFile(handleFile, ['DashengChefu', '--onlybundlejs'], null,
    function (error,stdout,stderr) {
    var callRes = stdout;
    if (error !== null) {
      callRes = stderr;
      console.log('exec error: ' + error);
    }

    res.render('index', {
      title: '控制台服务', 
      res: callRes 
    });
  });
});


module.exports = router;
