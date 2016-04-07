#!/usr/bin/perl 

#   file upload script.  
#   Remember that you MUST use enctype="mulitpart/form-data"
#   in the web page that invokes this script, and the destination 
#   directory for the uploaded file must have permissions set to 777.  
#   Do NOT set 777 permission on any other directory in your account!
#   
#   CS645, Spring 2016
#   Project 1
#  ELURI,MOUNIKA

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
$CGI::POST_MAX = 1024 * 3000; # Limit file size to 3MB
my $upload_dir = '/home/jadrn034/public_html/proj1/file_upload/_tk_images';
my $safe_filename_chars = "a-zA-Z0-9_.-";
####################################################################

my $q = new CGI;
my $filename = $q->param("productimage");
if($filename==undef)
{
   rename($upload_dir."/".lc($q->param("originalsku")).".jpg",$upload_dir."/".lc($q->param("sku")).".jpg");
}
else
{
unless($filename) {
    die "There was a problem uploading the image; ";        
    }
    
my ($name, $path, $extension) = fileparse($filename, '/..*/');

$filename = $q->param("originalsku").".jpg";
$filename =~ s/ //; #remove any spaces
if($filename !~ /^([$safe_filename_chars]+)$/) {
    die "Sorry, invalid character in the filename.";
    }   

$filename = untaint($filename);
$filename = lc($filename);
unlink($upload_dir."/".$filename);

$filename=$q->param("sku").".jpg";
$filename =~ s/ //; #remove any spaces
if($filename !~ /^([$safe_filename_chars]+)$/) {
    die "Sorry, invalid character in the filename.";
    }   

$filename = untaint($filename);
$filename = lc($filename);


# get a handle on the uploaded image     
my $filehandle = $q->upload("productimage"); 

unless($filehandle) { die "Invalid handle"; }

# save the file
open UPLOADFILE, ">$upload_dir/$filename" or die
    "Error, cannot save the file.";
binmode UPLOADFILE;
while(<$filehandle>) {
    print UPLOADFILE $_;
    }
close UPLOADFILE;
}

updateProduct();

}

# this is needed because mod_perl runs with -T (taint mode), and thus the
# filename is insecure and disallowed unless untainted. Return values
# from a regular expression match are untainted.
sub untaint {
    if($filename =~ m/^(\w+)$/) { die "Tainted filename!"; }
    return $1;
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


sub updateProduct{

my $q = new CGI;
my $sku= $q->param("sku");
my $skuToDelete=$q->param("originalsku");
my $vendorid= $q->param("vendor");
my $categoryid= $q->param("category");
my $mfdid= $q->param("manufactureid");
my $desc= $q->param("description");
my $features= $q->param("productfeatures");
my $cost= $q->param("cost");
my $retail= $q->param("retail");

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

my $deletestatement="DELETE from products where sku='$skuToDelete';";
my $deletesth = $dbh->prepare($deletestatement);
$deletesth->execute();


########################################################
### insert a new product
#my $statement = "INSERT INTO products values(".
#"'$sku',$vendorid,$categoryid,'$mfdid','$desc',".
#"'$features',$cost,'$retail');";

my $statement =$dbh->prepare("INSERT INTO products values(?,?,?,?,?,?,?,?)");
$statement->execute($sku,$vendorid,$categoryid,$mfdid,$desc,$features,$cost,$retail);


#$how_many = $dbh->do($statement);
#print " $how_many rows affected\n<br />";


print "Content-type:  text/html\n\n";
print "<html>";
print "<head>\n";
print "<link type=\"text/css\" rel=\"stylesheet\" href=\"/~jadrn034/proj1/newproduct.css\" />\n";
#print "<script type=\"text/javascript\" src=\"/~jadrn034/proj1/newproduct.js\"></script>\n";
print "</head>\n";
#print "\nThe statement is\n$statement\n<br />";    




########################################################
### search for the product and display the data

$statement = "SELECT sku, vendor.name, category.name, mfdid, description, features,cost,retail ".
    " FROM vendor, category, products WHERE sku='$sku' and vendor.id=products.vendorid and ".
    " category.id=products.catid;";


my $sth = $dbh->prepare($statement);
$sth->execute();

print "<h2>The record was updated successfully!</h2>";
print "<a href=\"/~jadrn034/proj1/home.html\">HOME</a>\n";
print"<table>\n";
print "<tr>\n";
print"<th>SKU</th> <th>Vendor</th> <th>Category</th> <th>Manufacturer's ID</th> <th>Description</th> <th>Features</th> <th>Cost</th> <th>Retail</th>";
print "</tr>\n";
print "<tr>\n";
while(my @rows = $sth->fetchrow_array()) {
    foreach $item (@rows) {
     print "<td>$item</td>";
        }
    print "</tr>\n";
    }
print "</table>\n";
my $imagename=lc($sku);
print "<img src=\"/~jadrn034/proj1/file_upload/_tk_images/$imagename.jpg\" />";
$sth->finish();
$dbh->disconnect();
}
