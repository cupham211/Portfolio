module.exports = function(){
    var express = require('express');
    var router = express.Router();

    function getTable(res, mysql, formInputs, areaID, complete){
        let grab;
        if (areaID == -1) {
            grab = `SELECT PlantStores.*, PlantAreas.name FROM PlantStores
            INNER JOIN PlantAreas ON PlantAreas.areaID = PlantStores.area
            WHERE PlantStores.area != 5;`;
        } else {
            grab = `SELECT PlantStores.*, PlantAreas.name FROM PlantStores
            INNER JOIN PlantAreas ON PlantAreas.areaID = PlantStores.area
            WHERE PlantStores.area = ?;`;
        }
        mysql.pool.query(grab, areaID, function(err, rows, fields){
            if(err){
                res.write(JSON.stringify(err));
                res.end();
            }
            formInputs.stores = rows;
            complete();
        });
    }

    router.delete('/:areaID/:storeID', function(req, res) {
        var mysql = req.app.get('mysql');
        var del = `DELETE FROM PlantStores WHERE storeID = ?;`
        var values = [req.params.storeID];
        sql = mysql.pool.query(del, values, function(err, rows, fields){
            if(err){
                res.write(JSON.stringify(err));
                res.end();
            } else {
                var callbackCount = 0;
                var formInputs = {};
                getTable(res, mysql, formInputs, req.params.areaID, complete);
                function complete(){
                    callbackCount++;
                    if(callbackCount >= 1){
                        res.json(formInputs);
                    }
                }
            }
        });
    })

    router.put('/:areaID', function(req, res) {
        var mysql = req.app.get('mysql');
        var edit = `UPDATE PlantStores SET area = ?, storeName = ?, website = ?, address = ?, restockDay = ?
        WHERE storeID = ?;`;
        var values = [req.body.area, req.body.store, req.body.website, req.body.address, req.body.restock_day, req.body.storeID];
        sql = mysql.pool.query(edit, values, function(err, rows, fields){
            if(err){
                res.write(JSON.stringify(err));
                res.end();
            } else {
                var callbackCount = 0;
                var formInputs = {};
                getTable(res, mysql, formInputs, req.params.areaID, complete);
                function complete(){
                    callbackCount++;
                    if(callbackCount >= 1){
                        res.json(formInputs);
                    }
                }
            }
        });
    })

    router.post('/:areaID', function(req, res) {
        var mysql = req.app.get('mysql');
        var add = `INSERT INTO PlantStores (area, storeName, website, address, restockDay)
        VALUES (?, ?, ?, ?, ?);`;
        var values = [req.body.area, req.body.store, req.body.website, req.body.address, req.body.restock_day];
        sql = mysql.pool.query(add, values, function(err, rows, fields){
            if(err){
                res.write(JSON.stringify(err));
                res.end();
            } else {
                var callbackCount = 0;
                var formInputs = {};
                getTable(res, mysql, formInputs, req.params.areaID, complete);
                function complete(){
                    callbackCount++;
                    if(callbackCount >= 1){
                        res.json(formInputs);
                    }
                }
            }
        });
    })

    router.get('/:areaID', function(req, res){
        var callbackCount = 0;
        var formInputs = {};
        var mysql = req.app.get('mysql');
        getTable(res, mysql, formInputs, req.params.areaID, complete)
        function complete(){
            callbackCount++;
            if(callbackCount >= 1){
                res.json(formInputs);
            }

        }
    });

    return router;

}();