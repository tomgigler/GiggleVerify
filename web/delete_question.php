<?php

require_once "DBConnection.php";

session_start();

if(!isset($_SESSION['USER'])){ exit; }

$db = new DBConnection();
$db->delete_question($_POST['guild_id'], $_POST['question_num']);
