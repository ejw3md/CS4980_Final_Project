const { exec } = require("child_process");
var command = "python3 triangulation.py";

// read in JSON and parse into individual variables to use as command line arguments to the Python code
var t1 = 2.828
var t2 = 2.236
var t3 = 2.236
var lat1 = 0
var lat2 = 1
var lat3 = 0
var long1 = 0
var long2 = 0
var long3 = 1
var vec1x = 0.5
var vec2x = 0.25
var vec1y = 0.5
var vec2y = 0.75

command += ` ${t1} ${t2} ${t3} ${lat1} ${lat2} ${lat3} ${long1} ${long2} ${long3} ${vec1x} ${vec2x} ${vec1y} ${vec2y}`;

// execute python
// get output data response
exec(command, (error, stdout, stderr) => {
    if (error) {
        console.log(`error: ${error.message}`);
        return;
    } 
    if (stderr) {
        console.log(`stderr: ${stderr}`);
        return;
    }
    else {
        // stdout is formatted: x y
        const coords = stdout.split(' ');// split output into x and y parts
        console.log("X is " + coords[0]);
        console.log("Y is " + coords[1]);
    }
});