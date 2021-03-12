var mysql = require('mysql');
var pool = mysql.createPool({
  connectionLimit : 10,
  host            : 'uyendb.c2zznuxfh9vu.us-east-2.rds.amazonaws.com',
  port            : '3306',
  user            : 'admin',
  password        : 'reptarpham1',
  name            : 'uyendb',
});

module.exports.pool = pool;