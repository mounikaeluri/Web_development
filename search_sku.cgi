#!/usr/bin/perl
#   CS645, Spring 2016
#   Project 1
#   Eluri, Mounika 

use DBI;
use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);


if(valid_user()) {
    send_to_main();   
    }
else {
    send_to_login_page();
    }

sub send_to_main{

my $host = "opatija.sdsu.edu";
my $port = "3306";
my $database = "jadrn034";
my $username = "jadrn034";
my $password = "suitcase";
my $database_source = "dbi:mysql:$database:$host:$port";
my $response = "";

my $dbh = DBI->connect($database_source, $username, $password)
or die 'Cannot connect to db';

my $q = new CGI;
my $keyword = $q->param("search");

my $query = "select sku, vendor.name as vendor, category.name as category ,mfdid,retail from products,vendor, category  where sku like '%$keyword%' and vendor.id=products.vendorid and category.id=products.catid";

            
my $sth = $dbh->prepare($query);
$sth->execute();

while(my @row=$sth->fetchrow_array()) {    
    $response .= $row[0]."|".$row[1]."|".$row[2]."|".$row[3]."|".$row[4]."||";
    }
if($response) {
    $response = substr $response, 0, (length($response) - 2); 
    }    
unless($response) {
    $response = "";
    }    

$sth->finish();
$dbh->disconnect();
    
print "Content-type: text/html\n\n";
print $response;
}


sub valid_user {
$q = new CGI;
my $cookiesid=$q->cookie("jadrn034_SID"); 
my $session = new CGI::Session(undef, $cookiesid, {Directory=>'/tmp'});
my $sid = $session->id();
$OK = 0;  #not authorized
if($sid==$cookiesid)
{
    $OK = 1; #authorized
}
return $OK;
}


sub send_to_login_page {
  print <<END;
Content-type:  text/html

<html>
<head>
    <meta http-equiv="refresh" 
        content="0; url=http://jadran.sdsu.edu/~jadrn034/proj1/index.html" />
</head><body></body>
</html>

END

} 
