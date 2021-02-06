<?php

require_once "DBConnection.php";

session_start();

if(!isset($_SESSION['user_id'])){ exit; }

$db = new DBConnection();
$db->set_current_guild($_POST['guild_id'], $_SESSION['user_id']);
