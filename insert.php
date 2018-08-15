<?php
$dbhost = 'localhost';
$dbuser = 'root';
$dbpass = 'manuvava';
$conn = mysql_connect($dbhost, $dbuser, $dbpass);
if(! $conn )
{
  die('Could not connect: ' . mysql_error());
}

$name = mysqli_real_escape_string($link, $_REQUEST['config_name']);
$tempe = mysqli_real_escape_string($link, $_REQUEST['temp']);
$light = mysqli_real_escape_string($link, $_REQUEST['light']);

$sql = "UPDATE Configs SET Name='$name',Temperature='$tempe', Light='$light' WHERE cID=1";

mysql_select_db('PP');
$retval = mysql_query( $sql, $conn );

if(! $retval )
{
  die('Could not update data: ' . mysql_error());
}
else{
	echo "Configuration successfully updated!";
}

mysql_close($conn);
?>