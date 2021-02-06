<?php

include "login_check.php";

require_once "DBConnection.php";

$db = new DBConnection();
$db->add_new_question($_POST['guild_id'], $_POST['question_num'], $_POST['question'], $_POST['question_type']);
