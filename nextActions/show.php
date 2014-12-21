<html>
<head>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
<script> 
function addAction(){        
        $.get(("naweb.pl?text="+document.myform.actiontext.value));
	setTimeout(callback, 500);
	return false;
}
function callback(){
	location.reload();
	return false;
}
</script>
</head>
<body><table border=1 padding=0>

<?php
$f = fopen("nextActions.csv", "r");
while (($line = fgetcsv($f)) !== false) {
        echo "<tr>";
        foreach ($line as $cell) {
                echo "<td>" . htmlspecialchars($cell) . "</td>";
        }
        echo "</tr>\n";
}
fclose($f);
?>
</table><form   name="myform" ><input type="text" name="actiontext" >
 <button type="button" onclick="addAction();">Add</button> 


</form></body></html>
