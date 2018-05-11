<?php
$con =  @mysqli_connect('localhost','root','','api');

$res = mysqli_query($con, 'call user()');
while($row=mysqli_fetch_array($res)){
	echo $row['id']." | ".$row['name']."\n";
}
mysqli_close($con);
?>
?>
