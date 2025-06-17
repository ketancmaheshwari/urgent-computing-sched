#!/bin/bash

# To run: ./step1-obtaindata.sh $startyear $endyear $granularity $cacheloc $outloc
#

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

mkdir -p $OUTLOC
#
sacct --format="UID, GID, JobIDRaw, Group, Account, JobName, TimelimitRaw, Submit, Start, End, State, ExitCode, ReservationId, Reservation, Priority, Eligible, Constraints, SystemCPU, CPUTimeRAW, ElapsedRaw, Layout, NTasks, QOSREQ, QOS, Restarts, WorkDir, ConsumedEnergyRaw, FailedNode, AveDiskRead, AveDiskWrite, MaxDiskRead, MaxDiskWrite, Partition, Reason, Suspended, AllocNodes, AveRSS, MaxRSS, DerivedExitCode, AveVMSize, MaxVMSize, ReqMem, ReqNodes, NNodes, Planned, PlannedCPURAW, NCPUS, UserCPU, ReqCPUS, TotalCPU, TRESUsageInTot, TRESUsageOutTot, ReqTRES, AllocTRES, TRESUsageInMax, TRESUsageOutMax, Flags, Comment, SystemComment, AdminComment" -a -P -S"$SYEAR"-01-01 -E"$EYEAR"-01-02 > "$OUTLOC/$SYEAR-$EYEAR-$GRAN.txt"
#
