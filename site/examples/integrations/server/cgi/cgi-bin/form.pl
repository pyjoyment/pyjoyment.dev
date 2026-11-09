#!/usr/bin/env perl
# A script of Perl of CGI.pm days, which reads the body of a form from its standard input
use strict;
use warnings;

read STDIN, my $body, $ENV{CONTENT_LENGTH} // 0;
my %form = map { s/\+/ /gr =~ s/%([0-9A-Fa-f]{2})/chr hex $1/ger } map { split /=/, $_, 2 } split /&/, $body;

print "Content-Type: text/plain\r\n\r\n";
print "$ENV{REQUEST_METHOD} $ENV{SCRIPT_NAME}: Hello $form{name}!\n";
