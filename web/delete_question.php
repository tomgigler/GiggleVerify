<?php

require_once "DBConnection.php";

session_start();

if(!isset($_SESSION['USER'])){ exit; }

$db = new DBConnection();
$db->delete_question($_POST['guild_id'], $_POST['question_num']);

$next_question_num = $_POST['question_num'] + 1;

while($db->decrement_question_num($_POST['guild_id'], $next_question_num)){
  $next_question_num += 1;
}
