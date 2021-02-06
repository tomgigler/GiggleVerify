<?php

session_start();
if(!isset($_SESSION['user_id'])) { http_response_code(500); exit(); }

if(!isset($_POST['guild_id'])) exit();

require_once "DBConnection.php";

$db = new DBConnection();
$db->add_new_question($_POST['guild_id'], $_POST['question_num'], $_POST['question'], $_POST['question_type']);
