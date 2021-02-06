<?php

session_start();
include "settings.php";

// The url you wish to send the POST request to
$url = "https://discord.com/api/v6/oauth2/token";
$REDIRECT_URI = "https://" . $_SERVER['HTTP_HOST'] . rtrim(dirname($_SERVER['PHP_SELF']), '/\\') . "/get_token.php";
print $REDIRECT_URI;

//The data you want to send via POST
$fields = [ 'client_id' => $CLIENT_ID, 'client_secret' => $CLIENT_SECRET, 'grant_type' => 'authorization_code',
	'code' => $_GET['code'], 'redirect_uri' => $REDIRECT_URI, 'scope' => 'identify'];

//url-ify the data for the POST
$fields_string = http_build_query($fields);

//open connection
$ch = curl_init();

//set the url, number of POST vars, POST data
curl_setopt($ch,CURLOPT_URL, $url);
curl_setopt($ch,CURLOPT_POST, true);
curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);

//So that curl_exec returns the contents of the cURL; rather than echoing it
curl_setopt($ch,CURLOPT_RETURNTRANSFER, true); 

//execute post
$result = curl_exec($ch);
$json = json_decode($result, true);

$_SESSION['access_token'] =  $json['access_token'];
$_SESSION['refresh_token'] = $json['refresh_token'];

$opts = array(
    'http'=>array(
    'method'=>"GET",
    'header'=>"Authorization: Bearer ".$_SESSION['access_token']."\r\n" .
    "Content-type: application/json\r\n"
    )
);

$context = stream_context_create($opts);

$fp = fopen('https://discord.com/api/users/@me', 'r', false, $context);
$user_json = fgets($fp);
$user_json = json_decode($user_json, true);

$_SESSION['user_id'] = $user_json['id'];
$_SESSION['username'] = $user_json['username'];
$_SESSION['avatar'] = $user_json['avatar'];

fclose($fp);

header("Location: index.php");
exit();

?>
