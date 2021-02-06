<?php
   session_start();

   if (isset($_SESSION['user_id']))
   {
      $message = "    <font color='green'><b>You have been successfully logged out.</b></font>\n";
   }

   session_destroy();

   header("Location: index.php");
   exit();

?>


