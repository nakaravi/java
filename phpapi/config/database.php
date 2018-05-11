<?php
class Database{
 
    // specify your own database credentials
    private $host = "localhost";
    private $db_name = "api";//"tourismeveryonecom1.ipagemysql.com";"66.96.147.96";
    private $username = "root";
    private $password = "";
    public $conn;
 
    // get the database connection
    public function getConnection(){
 
        $this->conn = null;
 
        try{
            $this->conn = new PDO("mysql:host=" . $this->host . ";dbname=" . $this->db_name, $this->username, $this->password);
            $this->conn->exec("set names utf8");
        }catch(PDOException $exception){
            echo "Connection error: " . $exception->getMessage();
        }
 
        return $this->conn;
    }
}
?>
 <?php 
/*$link = mysql_connect('tourismeveryonecom1.ipagemysql.com', 'tourism', '*password*'); 
if (!$link) { 
    die('Could not connect: ' . mysql_error()); 
} 
echo 'Connected successfully'; 
mysql_select_db(tourism); */
?> 
