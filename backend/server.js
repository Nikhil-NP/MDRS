const fs = require('fs'); //converting to json

const {exec} = require('child_process'); // to run the route_solver.py code in here itself
const { error } = require('console');
const { stdout, stderr } = require('process');


const numberOfCordinates = 30
const numberOfVehicles = 3
const maxDistancePerVehicle = 20; //5km for now : needs to be more dynamic like distance based for devices
const range = 0.05 //currently 5km range


//a location in pune
const fixed_location = {lat:18.49476,lng:73.890154};

function randomCordinateGenerator(numberOfCordinates){
    let cords = [fixed_location]; //for now only the fixed location in the res

    for (let i = 0; i < numberOfCordinates; i++) {
        //basic fn that will find random location around a specific point
        let lat = fixed_location.lat + Math.random() * range; // 
        let lng = fixed_location.lng + Math.random() * range;
        cords.push({lat,lng});  
    }
    return cords
}

//the json result
let diliveryPoints = randomCordinateGenerator(numberOfCordinates);

//organing it better:not using for now
const final_res = {
    coordinates: diliveryPoints,
    numberOfVehicles: numberOfVehicles,
    maxDistancePerVehicle:maxDistancePerVehicle,
};



fs.writeFileSync('data3.json',JSON.stringify(final_res,null,2));


exec('python route_solver.py',(error,stdout,stderr) =>{
    if(error){//erorr in nodejs
        console.log(`python error: ${error.message}`);
        return;
    }
    if (stderr) {//erro in .py script
        console.log(`python stderr : ${stderr}`);
        return;
    }


    const routeData = JSON.parse(stdout);
    fs.writeFileSync('../frontend/routes6.json',JSON.stringify(routeData,null,2))
    console.log('routes saved in frontend/routes.json');
});