#!/usr/bin/perl -w

use Cwd;
$dir = cwd;

if ($#ARGV != 3) {
    print "\t USAGE: ./steering_gen.pl \$energy \$efrcthn \$wmax \$rmax\n";
    print "\t  e.g.: ./steering_gen.pl 1e6 1e-15 1 0\n\n";
    print "\t Energy is in GeV.\n\n";
    print "\t See Corsika docs for definitions of\n";
    print "\t thinning parameters efrcthn, wmax, and rmax.\n\n";
    print "\t For effectively no thinning, choose 1e-15 1 0.\n";
    exit;
}

# Get the current time and format it as YYYYMMDD-HHMMSS.
# Save the resulting string in $formatted_time
my @time = localtime;
$time[5]+=1900;
$time[4]++;
my $formatted_time = sprintf "%04d%02d%02d-%02d%02d%02d",@time[5,4,3,2,1,0];


open(template_file,"<steering.template") or die $!;
my @lines = <template_file>;
close(template_file);

$seed1 = int(100000+rand(899999));
$seed2 = int(100000+rand(899999));
$seed3 = int(100000+rand(899999));

open(steering_file,"+>steering_$formatted_time.txt") or die $!;
foreach $line (@lines){
    $line =~ s/__PATH__/\/scratch\/showerLib\/beth\/$formatted_time/;
    $line =~ s/__SEED1__/$seed1/;
    $line =~ s/__SEED2__/$seed2/;
    $line =~ s/__SEED3__/$seed3/;
    $line =~ s/__ENERGY__/$ARGV[0]/g;
    $line =~ s/__EFRCTHN__/$ARGV[1]/;
    $line =~ s/__WMAX__/$ARGV[2]/;
    $line =~ s/__RMAX__/$ARGV[3]/;
    print steering_file $line;
}
close(steering_file);

print "Steering file created as steering_$formatted_time.txt.\n\n";
print "Suggested usage of steering file:\n";
print "  \$ mkdir -p /scratch/showerLib/beth/$formatted_time\n";
print "  \$ cd /usr/local/corsika/corsika-6990/run/\n";
print "  \$ ./corsika6990Linux_QGSII_fluka < $dir/steering_$formatted_time.txt";
print       " > /scratch/showerLib/beth/steering_$formatted_time.out\n\n";
