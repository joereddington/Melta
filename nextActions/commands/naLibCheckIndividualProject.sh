echo ", $1"
if grep --quiet ", $1-" $JURGEN/Jurgen/nextActions/nextActions.csv; then
  echo updated NOT needed
else
  $JURGEN/Jurgen/nextActions/commands/na "Update Projects, $1" 2 t 3
fi
