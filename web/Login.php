<?php

require_once "DBConnection.php";

class Login {

   function Login(){

   }//Login

   function verify($user, $pass){

      $db = new DBConnection();

      $user = $db->get_user($user, $pass);
      $_SESSION['user_id'] = $user[0];

      return count($user);

   }//verify

}//Login

?>
