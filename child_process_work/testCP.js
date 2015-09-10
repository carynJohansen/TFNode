var child = require('child_process')

//var python = child.spawn('python',['database/vcf_get.py', 6512743, 6518792, 'Chr3'])
var python = child.spawn('python', ['./testCP.py'])
var chunk = ''

console.log(python)

python.stdout.on('data', function(data) {
	//chunk += data
	//console.log(typeof data == 'string')
	//response = JSON.parse(data)
	//console.log(response)
	
})
python.stdin.write(JSON.strigify(data))