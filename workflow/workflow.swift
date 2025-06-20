import python;
import string;
import unix;
import io;
import sys;


app (file out) obtain_data (int from_yr, int to_yr, string cacheloc, string outloc) {

   "/lustre/orion/proj-shared/" the_path @stdout=out
}

string items[];
items = split(outsane,":");

foreach i in [1:]{
    file std_out <"out"+i+".txt"> = run_adv_diff(items[1]+i);
}

