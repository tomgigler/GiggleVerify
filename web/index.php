<?php

session_start();

include "settings.php";

if (!isset($_SESSION['username']))
{
    include "header.php";

    print "<br><br>\n";

    $auth_url =  "https://discord.com/api/oauth2/authorize?client_id=".$CLIENT_ID."&redirect_uri=https%3A%2F%2F".$_SERVER['HTTP_HOST'].rtrim(dirname($_SERVER['PHP_SELF']), '/\\')."%2Fget_token.php&response_type=code&scope=identify";
    print "   <center><button onclick=location.href='".$auth_url."'>Login</button></center>\n";
    include "footer.php";
}
else
{
    header("Location: home.php");
    exit();
}
?> 
