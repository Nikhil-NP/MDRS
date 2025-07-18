const fs = require('fs'); //converting to json

const numberOfCordinates = 30

//a location in banglore
const fixed_location = {lat:12.978792960040103,lng:77.59158937690144};

function randomCordinateGenerator(numberOfCordinates){
    let cords = [fixed_location]; //for now only the fixed location in the res

    for (let i = 0; i < numberOfCordinates; i++) {
        //basic fn that will find random location around a specific point
        let lat = fixed_location.lat + Math.random() * 0.04; // 4km approx
        let lng = fixed_location.lng + Math.random() * 0.04;
        cords.push({lat,lng});  
    }
    return cords
}

//the json result
let res = randomCordinateGenerator(numberOfCordinates);

//organing it better:not using for now
const final_res = {
    fixed_location: fixed_location,
    coordinates: res,

};

//saving to json,the first will always be the 
fs.writeFileSync('data.json',JSON.stringify(res,null,2));