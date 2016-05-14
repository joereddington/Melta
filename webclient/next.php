<!DOCTYPE html http://stackoverflow.com/a/9826008/170243>
<html >
    <head>
        <title>Hello World</title>
        <style>

        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            width: 100%;
        }

        body {
            display: table;
        }

        .my-block {
            text-align: center;
            display: table-cell;
            vertical-align: middle;
		  font-size:180px;
        }
        </style>
    </head>
    <body>
    <div class="my-block">
<?php 
$csv = array_map('str_getcsv', file('/home/joereddington/Jurgen/nextActions/nextActions.csv'));
echo $csv[0][3];
?>
    </div>
    </body>
</html>
