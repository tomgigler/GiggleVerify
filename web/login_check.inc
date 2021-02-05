<?php
   include "settings.inc";

   session_start();

   if (!isset($_SESSION['username']))
   {
      header("Location: index.php");
   }
?> 
