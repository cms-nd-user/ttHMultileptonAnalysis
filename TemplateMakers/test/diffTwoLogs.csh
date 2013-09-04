#!/bin/tcsh -f


if ($#argv < 2) then
    echo "Usage: diffTwoLogs.csh nd.log cern.log"
    exit (3)
endif


set logOne = $1
set logTwo = $2

echo "Overlap"
diff -y $logOne $logTwo | egrep -v -c '(<|>|\|)'

echo "$logOne has, $logTwo does not have"
diff --suppress-common-lines -y $logOne $logTwo | egrep '(<|\|)' | awk '{print $1, $2, $3}' > & ! inOne_outTwo.log
wc -l inOne_outTwo.log

echo "$logOne does not have, $logTwo has"
diff --suppress-common-lines -y $logOne $logTwo | egrep '(>|\|)' |  awk '{if (NF == 4) {print $2, $3, $4} else {print $5,$6,$7}}' > & ! outOne_inTwo.log
wc -l outOne_inTwo.log


