#!/usr/bin/perl -w
# Count the number of stimuli in the magno list.

open(IN, "<dmparvo.lst") || die;
my($scroll, $targ, $sat); #sat = scroll after target
my($num_trial);
my(@line);

foreach $line (<IN>) {
	@line = split(/\t/, $line);
	if ($line[0] !~ /^\d/) {
		next;
	} else {
		$num_trials++;
	}
	if ($line[0] == 31) {
		$scroll++;
	} elsif ($line[0] == 101) {
		if ($line[2] =~ /rg/) {
			$sat++;
		} else {
			$targ++;
		}
	}
}

print "Total Trials:\t$num_trials\n";
print "Total Targets:\t$targ\t% Targets:\t";
printf("%.2f\n", $targ/$num_trials * 100);
print "Total Scrolls:\t$scroll\t% Scrolls:\t";
printf("%.2f\n", $scroll/$num_trials * 100);
print "Total SATs:\t$sat\t% SATs\t\t";
printf("%.2f\n", $sat/$num_trials * 100);
<STDIN>;