import string;
import unix;
import io;
import sys;
import files;

// Command line arguments:
date_spec = argp(1);
date1 = argp(2);
date2 = argp(3);
cache = argp(4);
outloc = argp(5);

raw_data<"out1.txt"> = obtain_data(date1, date2, date_spec, cache, outloc);

app (file out) obtain_data (int from_yr, int to_yr, string gran, string cacheloc, string outloc) {

   "../app-codes/step1-obtaindata.sh" from_yr to_yr gran cacheloc outloc @stdout=out
}

app (file out) curate_data (file txtfile) {

   "../app-codes/step2-curatedata.sh" txtfile @stdout=out
}

app (file out) job_waittimes (file input) {

  "../app-codes/step4b-jobwaittimes.py" "--infile" input "--outfile" out
}

app (file out) auxdataprep1 (file input) {
      
  "../app-codes/prep-data4nodevselapsed.sh" input @stdout=out
}

app (file out) auxdataprep2 (file input) {
      
  "../app-codes/prep-data4backfillanalysis.sh" input @stdout=out
}

app (file out) job_nodevselapsed (file input) {

  "../app-codes/step4a-nodesvselapsed.py" "--infile" input "--outfile" out
}


app (file out) user_jobstates (file input) {

  "../app-codes/step4c-userjobstates.py" "--infile" input "--outfile" out
}

app (file out) jobtimediffandstates (file input) {

  "../app-codes/step4d-timediff-state-backfill.py" "--infile" input "--outfile" out
}

app (file out) html2png (file input) {

  "../app-codes/HTML2PNG.sh" input out
}

app (file out) llmanalysis (file input) {

  "../app-codes/step5-llm-analysis.py" "--infile" input "--outfile" out
}

app (file out) llmcompare (file input1, file input2) {

  "../app-codes/step5-llm-analysis.py" "--infile" input1 "--infile2" input2 "--outfile" out
}







//file raw_data<"out1.txt"> = obtain_data(2021, 2024, "month", "none", "/lustre/orion/proj-shared/stf053/frontierjobs/urgent-computing-sched/swift-data");

string dataloc = read(raw_data);
file txtfiles[] = glob(dataloc+"/*.txt");

foreach f, i in txtfiles {
 file orig_csv<"out2_"+i+".csv"> = curate_data(f);
 file jobwaitplot<"jobwaitplot_"+i+".html"> = job_waittimes(orig_csv);
 file userjobstatesplot<"userjobstates_"+i+".html"> = user_jobstates(orig_csv);
 file nodevselapsedcsv<"tmpoutfile_"+i+".csv"> = auxdataprep1(orig_csv);
 file timediffcsv<"tmpoutfile2_"+i+".csv"> = auxdataprep2(orig_csv);
 file plotfile2<"elapsedvsnodes_"+i+".html"> = job_nodevselapsed(nodevselapsedcsv);
 file plotfile3<"timediff4backfilledjobsandstates_"+i+".html"> = jobtimediffandstates(timediffcsv);
 file pngfile2<"elapsedvsnode"+i+".png"> = html2png(plotfile2);
 file pngfile3<"timediff"+i+".png"> = html2png(plotfile3);

 file llmout<"llmout_"+i+".md"> = llmanalysis(pngfile2);
 file llmcompout<"llmcompout_"+i+".md"> = llmcompare(pngfile2,pngfile3);
}

