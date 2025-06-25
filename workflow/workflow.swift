import string;
import unix;
import io;
import sys;
import files;


app (file out) obtain_data (int from_yr, int to_yr, string gran, string cacheloc, string outloc) {

   /* "/lustre/orion/proj-shared/" the_path @stdout=out */
   "/home/km0/urgent-computing-sched/app-codes/step1-obtaindata.sh" from_yr to_yr gran cacheloc outloc @stdout=out
}

app (file out) curate_data (file txtfile) {

   /* "/lustre/orion/proj-shared/" the_path @stdout=out */
   "/home/km0/urgent-computing-sched/app-codes/step2-curatedata.sh" txtfile @stdout=out
}

app (file out) job_waittimes (file input) {

  "/home/km0/urgent-computing-sched/app-codes/step4b-jobwaittimes.py" "--infile" input "--outfile" out
}

app (file out) auxdataprep1 (file input) {
      
  "/home/km0/urgent-computing-sched/app-codes/prep-data4nodevselapsed.sh" input @stdout=out
}

app (file out) job_nodevselapsed (file input) {

  "/home/km0/urgent-computing-sched/app-codes/step4a-nodesvselapsed.py" "--infile" input "--outfile" out
}

file outfile1<"out1.txt"> = obtain_data(2024, 2024, "year", "/home/km0/urgent-computing-sched/data/workdata/txtdata", "/home/km0/urgent-computing-sched/data/workdata/txtdata");

string dataloc = read(outfile1);
file txtfiles[] = glob(dataloc+"/*.txt");

foreach f, i in txtfiles {
 file outfile2<"out2_"+i+".csv"> = curate_data(f);
 file plotfile<"jobwaitplot_"+i+".html"> = job_waittimes(outfile2);
 file tmpoutfile<"tmpoutfile_"+i+".csv"> = auxdataprep1(outfile2);
 file plotfile2<"elapsedvsnodes_"+i+".html"> = job_nodevselapsed(tmpoutfile);
}


