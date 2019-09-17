const mysql = require('mysql');
var databaseOptions = require('./config.js');
console.log(databaseOptions);
class Database{
    constructor(config){
        this.connection = mysql.createConnection(config);
        this.connection.connect();
    }
    query(sql, args){

        return new Promise((resolve, reject)=>{
            this.connection.query(sql, args, (err,rows)=>{
                if(err){
                    return reject(err);
                }
                resolve( rows );
            })
        });

    }

    close(){
        return new Promise((resolve, reject)=>{
            this.connection.end(err=>{
                if(err) return reject(err);
                resolve();
            })
        })
    }

}

database = new Database(databaseOptions.databaseOptions);
database.query("select * from products").then(rows=>{
    console.log(rows);
})
database.close();
