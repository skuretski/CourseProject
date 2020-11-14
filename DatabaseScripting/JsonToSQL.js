const data = require('./db.json');
const mysql = require('mysql');
const dotenv = require('dotenv');
dotenv.config();

const connection = mysql.createConnection({
	host: process.env.DB_URL,
	user: "admin",
	password: process.env.DB_PW,
	database: "memes",
	charset: "utf8mb4"
});

connection.connect();

for(let d of data){
	connection.query(`INSERT INTO memes
		(id, title, link, author, ups, downs) 
		VALUES ("${d.id}", "${d.title}", "${d.media}", "${!d.author}", ${d.ups}, ${d.downs})
		ON DUPLICATE KEY UPDATE id="${d.id}"
	`)
}

connection.end();