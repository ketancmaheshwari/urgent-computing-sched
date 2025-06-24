#!/bin/bash

# To run: ./step1-obtaindata.sh $startyear $endyear $granularity $cacheloc $outloc
#

querystring="sacct --format=\"UID, GID, JobIDRaw, Group, Account, JobName, TimelimitRaw, Submit, Start, End, State, ExitCode, ReservationId, Reservation, Priority, Eligible, Constraints, SystemCPU, CPUTimeRAW, ElapsedRaw, Layout, NTasks, QOSREQ, QOS, Restarts, WorkDir, ConsumedEnergyRaw, FailedNode, AveDiskRead, AveDiskWrite, MaxDiskRead, MaxDiskWrite, Partition, Reason, Suspended, AllocNodes, AveRSS, MaxRSS, DerivedExitCode, AveVMSize, MaxVMSize, ReqMem, ReqNodes, NNodes, Planned, PlannedCPURAW, NCPUS, UserCPU, ReqCPUS, TotalCPU, TRESUsageInTot, TRESUsageOutTot, ReqTRES, AllocTRES, TRESUsageInMax, TRESUsageOutMax, Flags, Comment, SystemComment, AdminComment\" -a -P " 


if [ "$#" -ne 5 ]
then
	echo "Need 5 args, presented $#, exiting"
	exit 1
fi

SYEAR=$1
shift
EYEAR=$1
shift
GRAN=$1
shift
CACHELOC=$1
shift
OUTLOC=$1

yrs=$(seq $SYEAR $EYEAR)

if [ "$CACHELOC" != "none" ]
then
	OUTLOC=$CACHELOC
        echo -n $OUTLOC
	exit 0
fi

mkdir -p $OUTLOC

if [ $GRAN = "month" ]
then
  echo "monthly granularity"
  #parallel "$querystring -S{1}-{2}-01 -E{1}-{2}-31 > $OUTLOC/{1}-{2}.txt" ::: $yrs ::: {1..12}
  for year in $(seq $SYEAR $EYEAR)
  do
    for month in $(seq 1 12)
    do
	  echo "Running query per month $month-$year"
          # invalid dates will be ignored
	  # $querystring -S"$year"-"$month"-01 -E"$year"-"$month"-31 > "$OUTLOC/$year-$month.txt"
	  sleep 10
    done
  done
fi


if [ $GRAN = "year" ]
then
  echo "year granularity"
  #parallel "$querystring -S{1}-01-01 -E{1}-12-31 > $OUTLOC/{1}.txt" ::: $yrs 
  for year in $(seq $SYEAR $EYEAR)
  do
    echo "Running query per year $year" 
    # $querystring -S"$year"-01-01 -E"$year"-12-31 > "$OUTLOC/$year.txt"
    sleep 10
  done
fi

echo -n $OUTLOC

