echo ", $1"
if grep --quiet ", $1$" /home/joereddington/Jurgen/nextActions/nextActions.csv; then
  echo updated NOT needed
else
  /home/joereddington/Jurgen/nextActions/commands/naFulltdcp "Update Projects, $1" 2 g 3
fi
