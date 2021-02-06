<?php

include "login_check.php";

require_once "DBConnection.php";

$db = new DBConnection();
$db->set_current_guild($_POST['guild_id'], $_SESSION['user_id']);
