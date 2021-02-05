<?php 

class DBConnection {
  var $connection;
   
  function DBConnection(){
  } //DBConnection

  function connect(){
    include "settings.inc";
    $this->connection = new mysqli("localhost", $db_user, $db_pass, $db_name);
    $this->connection->set_charset("utf8mb4");
    return $this->connection;
  } //connect

  function close(){
    $this->connection->close();
  } //close

  function get_user($user, $pass){
    $this->connect();
    $sql = "SELECT id FROM users WHERE name = ? AND password = PASSWORD(?)";
    $stmt = $this->connection->prepare($sql);
    $stmt->bind_param('ss', $user, $pass);
    $stmt->execute();
    $ret = $stmt->get_result()->fetch_all()[0];
    $this->close();
    return $ret;
  }

  function get_guilds($user_id){
    $this->connect();
    $sql = "SELECT guild_id, guild_name FROM user_guilds WHERE user_id = ?";
    $stmt = $this->connection->prepare($sql);
    $stmt->bind_param('i', $user_id);
    $stmt->execute();
    $ret = $stmt->get_result()->fetch_all();
    $this->close();
    return $ret;
  }

  function get_questions($guild_id){
    $this->connect();
    $sql = "SELECT question_num, question, question_type FROM questions WHERE guild_id = ?";
    $stmt = $this->connection->prepare($sql);
    $stmt->bind_param('i', $guild_id);
    $stmt->execute();
    $ret = $stmt->get_result()->fetch_all();
    $this->close();
    return $ret;
  }
}
