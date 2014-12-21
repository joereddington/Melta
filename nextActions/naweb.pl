#!/usr/bin/perl
use strict;
    use warnings;
use CGI qw(:standard -debug);
my $text = param('text');
die if $text =~ /\x00/;
print "Content-type: text/html\n\n";
$text =~ s/^-+//;
system('/home/joereddington/joereddington.com/Jurgen/nextActions/commands/na', $text);
