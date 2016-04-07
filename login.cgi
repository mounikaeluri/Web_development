#!/usr/bin/perl
#   CS645, Spring 2016
#   Project 1
#  ELURI,MOUNIKA


# I used the post/redirect/get design pattern to prevent duplicate form submissions 
# after the user logs out, goes back and tries to resubmit a form.

# 1. The user submits the login form to the server.
# 2. The server validates the user credentials.
# 3. Upon successful validation, the server returns a redirection command instead of a web page.
# 4. Now if the user logs out and goes back, he/she is at the redirected page.
# 5. If the user refreshes the page, it will perform a HTTP GET to fetch the web page rather than the initial
#    HTTP POST that submits the login form. This prevents submission of the login form on refresh.


use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;

##---------------------------- MAIN ---------------------------------------

my $q;
if(authenticate_user()) {
    send_to_main();
       
    }
else {
    send_to_login_error();
    }    
###########################################################################

###########################################################################
sub authenticate_user {
    $q = new CGI;
    my $user = $q->param("username");
    my $password = $q->param("password");    
    open DATA, "</home/jadrn034/public_html/proj1/passwords.dat" 
        or die "Cannot open file.";
    @file_lines = <DATA>;
    close DATA;

    $OK = 0; #not authorized

    foreach $line (@file_lines) {
        chomp $line;
        ($stored_user, $stored_pass) = split /=/, $line;    
        if($stored_user eq $user && Crypt::SaltedHash->validate($stored_pass, $password)) {
            $OK = 1;
            last;
            }
        }
    return $OK;
    }
###########################################################################

###########################################################################
sub send_to_login_error {
    print <<END;
Content-type:  text/html

<html>
<head>
    <meta http-equiv="refresh" 
        content="0; url=http://jadran.sdsu.edu/~jadrn034/proj1/error.html" />
</head><body></body>
</html>

END
    }  
    
###########################################################################
      
###########################################################################
sub send_to_main {
# args are DRIVER, CGI OBJECT, SESSION LOCATION
# default for undef is FILE, NEW SESSION, /TMP 
# for login.html, don't look for any existing session.
# Always start a new one.  Send a cookie to the browser.
# Default expiration is when the browser is closed.
# WATCH YOUR COOKIE NAMES! USE JADRNXXX_SID  
    my $session = new CGI::Session(undef, undef, {Directory=>'/tmp'});
    $session->expires('+1d');
    my $cookie = $q->cookie(jadrn034_SID => $session->id);
    print $q->header( -cookie=>$cookie ); #send cookie with session ID to browser    
    print $q->redirect('http://jadran.sdsu.edu/~jadrn034/proj1/home.html');
    #print <<END;
#<html>
#<head>
 #   <META http-equiv="refresh" content="0;URL=http://jadran.sdsu.edu/~jadrn034/proj1/home.html">
#/head>
#body>
#Redirecting to home page...
#<br />
#</body>
#</html>

END
}
###########################################################################    
