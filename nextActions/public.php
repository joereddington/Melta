<html>
<head>
<script src="handsontable/dist/handsontable.full.js"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
<link rel="stylesheet" media="screen" href="public.css">
<link rel="stylesheet" media="screen" href="bootstrap.min.css">

</head>
<body >
  <div class="container">
<div class="col-sm-8 col-offset-1">
<h1>Personal Transparency</h1>


<p>My life is better the more open I am with information.</p>

<p>I'm big on information. Knowing more about myself, my habits, and the affects of my actions helps me make better choices.</p>

<p>Equally, sharing more of myself, my thoughts and plans, wins and losses, leads to other people making better choices about me: would this be of interest? Is now a good time? Is this a good person for that keynote?</p>

<h2>Stress Charts</h2>
<p>I keep my todo list online. For everybody: the bigger a todo list gets and the older the tasks are, the more stressed people get. I have some code that charts the size of the list so that I, and everybody else, can get a good look at my stress levels.</p>

<p>The chart below updates every half an hour to give the current size of my Todo list.</p>

<p>Since lots of jobs come in both from various automatic calendar reminders, project reviews, and me  there is a correlation between the chart and my stress levels. So if you’re looking to rope me into some activity, it may be best to consult the chart.</p>

<p>Tasks that have been in the inbox for more than a week are the red line, more than three days the purple, and more than 24 hours the green (the blue is the 'current' state and includes all the tasks triggered by calendar actions and emails to reply to).  Quite often my motivation for a given day is 'Do all of the purple jobs' or 'stop the green line going over ten'.  It's a nice way of making that horrible thing we call work into a game.</p>

<IMG SRC="http://joereddington.com/stress/priority.png">

<h2>Task lists</h2>
A few years after I made the charts public I made the lists themselves public. This is a live feed of my todo list.  For display purposes I've coloured in the tasks using the same indicators as above. 
<table border=0 id="nextActions" border=1 padding=0>
<tr><td>Context</td><td>Minutes</td><td>Task</td><td>Date Added</td></tr>
<?php
date_default_timezone_set("Europe/London");
$b = new DateTime;
$row = 0;
$handle = fopen("/PATH/TO/nextActions.csv", "r");
while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
   for ($c=0; $c <= $row; $c++)
{
$pri=7-$data[0];
$task=$data[3];
if (in_array("0",$data)){
$task="------------------------------";
}
$email = "/[^@\s]*@[^@\s]*\.[^@\s]*/";
$num = "/([0-9][0-9][0-9]* )+[0-9]*/";
$url = "/[a-zA-Z]*[:\/\/]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i";
$private = "/\[[^]]*\]/";
$replacement = "[removed]";
$task=preg_replace($email, $replacement, $task);
$task=preg_replace($url, $replacement, $task);
$task=preg_replace($num, $replacement, $task);
$task=preg_replace($private, $replacement, $task);

$running_total+=$data[2];
$value=$data[5];
$hope = date_create_from_format(" Y-m-d (D) - H:i:s",$value);
$days_old=$hope->diff($b)->days;
$bgcolor="#98AEFA";
if ($days_old>=1){
$bgcolor="#A1FA98";
}
if ($days_old>=3){
$bgcolor="#FA98DC";
}
if ($days_old>=7){
$bgcolor="red";
}
    print("<TR bgcolor= \"".$bgcolor."\">");
    print("<TD>".$data[1]." </td>");
    print("<TD>".$data[2]." </td>");
    print("<TD>".$task." </td>");
    print("<TD>".$data[5]." </td>");
    print("</TR>"); 
}

}
fclose($handle);

?>

</table>
</div>
</div>
</body></html>
