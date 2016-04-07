#!/usr/bin/perl 

#   file upload script.  
#   Remember that you MUST use enctype="mulitpart/form-data"
#   in the web page that invokes this script, and the destination 
#   directory for the uploaded file must have permissions set to 777.  
#   Do NOT set 777 permission on any other directory in your account!
#   
#   CS645, Spring 2016
#   Project 1
#   Eluri, Mounika 

use CGI;
use DBI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use File::Basename;


if(valid_user()) {
    send_to_main();   
    }
else {
    send_to_login_page();
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



sub send_to_main {
####################################################################
### constants
my $upload_dir = '/home/jadrn034/public_html/proj1/file_upload/_tk_images';

####################################################################
my $q = new CGI;
my $sku= $q->param("sku");
my $filename=lc($sku).".jpg";
my $response=0;
if(DeleteSKU()){
  unlink($upload_dir."/".$filename);
  $response=1;
}
 print "Content-type: text/html\n\n";
 print $response;
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


sub DeleteSKU{

my $q = new CGI;
my $sku= $q->param("sku");

my $host = "opatija.sdsu.edu";
my $port = "3306";
my $database = "jadrn034";
my $username = "jadrn034";
my $password = "suitcase";
my $database_source = "dbi:mysql:$database:$host:$port";
my $response = "";

########################################################
### connect
my $dbh = DBI->connect($database_source, $username, $password)
or die 'Cannot connect to db';

my $selectstatement="SELECT sku from products where sku='$sku';";
my $selectsth = $dbh->prepare($selectstatement);
$selectsth->execute();
my $count = 0;
while ($selectsth->fetch()) 
{
   $count = 1;
}
$selectsth->finish();

if($count==0){
return 0;
}

my $deletestatement="DELETE from products where sku='$sku';";
my $deletesth = $dbh->prepare($deletestatement);
$deletesth->execute();

$dbh->disconnect();
return 1;

}

