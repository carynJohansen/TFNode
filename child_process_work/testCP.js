var child = require('child_process')

var python = child.spawn('python',['../database/vcf_get.py', 6512743, 6518792, 'Chr3'])
//var python = child.spawn('python', ['testCP.py'])
var chunk = ''
//console.log(__dirname )
//console.log(python)

python.stdout.on('data', function (data) {
	chunk += data
	json = JSON.stringify(chunk)
	console.log(typeof json == 'string')
	json = json.replace(/\s/g, '')
	console.log(json)
	response = JSON.parse(json)
	console.log(typeof response == 'string')
	
})

python.stderr.on('data', function (data) {
	console.log('stderr: ' + data)
})
//python.stdin.write(JSON.strigify(data))