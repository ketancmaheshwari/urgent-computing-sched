import string;
import unix;
import io;
import sys;
import files;


app (file out) obtain_data (int from_yr, int to_yr, string gran, string cacheloc, string outloc) {

   /* "/lustre/orion/proj-shared/" the_path @stdout=out */
   "/home/km0/urgent-computing-sched/app-codes/step1-obtaindata.sh" from_yr to_yr gran cacheloc outloc @stdout=out
}

app (file out) curate_data (string dataloc) {

   /* "/lustre/orion/proj-shared/" the_path @stdout=out */
   "/home/km0/urgent-computing-sched/app-codes/step2-curatedata.sh" dataloc @stdout=out
}

file outfile1<"out1.txt"> = obtain_data(2024, 2024, "year", "/home/km0/urgent-computing-sched/data/workdata/txtdata", "/home/km0/urgent-computing-sched/data/workdata/txtdata");

string arg2=read(outfile1);
file outfile2<"out2.txt"> = curate_data(arg2);

