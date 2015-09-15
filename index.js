//environment
var express = require('express')
var app = express()
var stylus = require('stylus')
var http = require('http')
var path = require('path')
var bodyParser = require('body-parser')
var jade = require('jade')
var globule = require('globule')
var util = require('util')
var child = require('child_process')
var regulator = require('./lib/regulator')

//Database connection
var sqlite3 = require('sqlite3').verbose()
var db = new sqlite3.Database('/Users/carynjohansen/Documents/NYUClasses/Purugganan_Lab/TFInteraction_db/michael.db')

app.set('port', (process.env.PORT || 5000))
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'jade')

//app.use(express.logger('dev'))
app.use(express.static(__dirname + '/static'))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))

app.use(regulator)
/// catch 404 and forward to error handler
//app.use(function(request, response, next) {
//	var err = new Error('Not Found')
//	err.status = 404
//	next(err)
//})


//app.get('/', function (request, response) {
//    response.render('query')
//})

//app.post('/query', function (request, response, next) {
//	regulator.showRegulator
//}) //close app.post

var template = 'Node app is running at localhost: {port~number}'
var txt = template.replace('{port~number}', app.get('port'))

app.listen(app.get('port'), function() {
    console.log(txt)
})


