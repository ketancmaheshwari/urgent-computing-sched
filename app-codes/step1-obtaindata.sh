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
  parallel --delay 1 "$querystring -S{1}-{2}-01 -E{1}-{2}-02 > $OUTLOC/{1}-{2}.txt" ::: $yrs ::: {01..12}
fi

if [ $GRAN = "year" ]
then
  echo "year granularity"
  parallel --delay 1 "$querystring -S{1}-01-01 -E{1}-01-02 > $OUTLOC/{1}.txt" ::: $yrs 
fi

echo -n $OUTLOC

