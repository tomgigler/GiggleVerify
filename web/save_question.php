<?php

require_once "DBConnection.php";

session_start();

if(!isset($_SESSION['USER'])){ exit; }

$db = new DBConnection();
$db->add_new_question($_POST['guild_id'], $_POST['question_num'], $_POST['question'], $_POST['question_type']);
