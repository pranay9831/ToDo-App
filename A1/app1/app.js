const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const app = express();
const path = require('path');
const fs = require('fs');

const PORT =  5000;

app.use(bodyParser.urlencoded({ extended: false}));
app.use(bodyParser.json());

app.get("/", (req,res) => {
    res.status(200);
    res.send("Container 1")
})
 
app.post("/checksum", function(request, response){
    const fileName = request.body.file;

    response.setHeader('Content-Type', 'application/json');

    fs.readFile(`./files/${fileName}`, "utf-8", (error, data) => {
       
        if (!fs.existsSync(`./files/${fileName}`)){
            response.json({file : fileName, error : "File not found."})
         }

        else if (fileName == undefined || fileName == ""){
                response.json({file : null, error : "Invalid JSON input."})
            }
        
        else {
             
            axios({
                method: "post",
                url: 'http://app2:6000',            
                data: {file : fileName},
                headers: {
                    "Content-type": "application/json"
                }
            })
            .then(function (res) {
                response.status(200).send(res.data)

            }).catch((error) => {
                if (error.response){
                    console.log(error.response.data);
                    console.log(error.response.status);
                } else if (error.request){
                    console.log(error.request);
                } else {
                    console.log("Error", error.message);
                }
            })
        }
    })
})

app.listen(PORT, (error) => {
    if(!error){
        console.log("server is going on "+PORT)
    }
    else{
        console.log("Error occured")
    }
})