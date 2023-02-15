const express = require('express');
const bodyParser = require('body-parser');
const crypto = require('crypto');
const app = express();
const path = require('path');
const fs = require('fs');



app.use(bodyParser.urlencoded({ extended: false}));
app.use(bodyParser.json());

app.post("/", (req, res) => {
    const fileName = req.body.file;
    const filePath = `./files/${fileName}`
    
    function checksumCalculator(string, algo, encoding){
        return crypto
        .createHash(algo || 'md5')
        .update(string, 'utf-8')
        .digest(encoding || 'hex');
    }

    fs.readFile(filePath, 'utf-8', (err, data) => {
        if (err){
            console.log("some thing is not good")
        }
        else
        {
            var checksum = checksumCalculator(data);
            console.log(checksum);
            res.json({
                "file": fileName,
                "checksum": checksum
            })};
    })

})

app.listen(6000, (error) => {
    if(!error){
        console.log("Server is going on  " + 6000)
    }
    else{
        console.log("Error occured")
    }
})

