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

  function get_guilds($user_id){
    $this->connect();
    $sql = "SELECT guild_id, name FROM user_guilds, guilds WHERE user_id = ? AND user_guilds.guild_id = guilds.id";
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

  function add_new_question($guild_id, $question_num, $question, $question_type){
    $this->connect();
    $sql = "INSERT INTO questions values (?,?,?,?) ON DUPLICATE KEY UPDATE question = ?, question_type = ?";
    $stmt = $this->connection->prepare($sql);
    $stmt->bind_param('iisisi', $guild_id, $question_num, $question, $question_type, $question, $question_type);
    $stmt->execute();
    $this->close();
  }

  function delete_question($guild_id, $question_num){
    $this->connect();
    $sql = "DELETE FROM questions WHERE guild_id = ? AND question_num = ?";
    $stmt = $this->connection->prepare($sql);
    $stmt->bind_param('ii', $guild_id, $question_num);
    $stmt->execute();
    $this->close();
  }

  function decrement_question_num($guild_id, $question_num){
    $new_question_num = $question_num - 1;
    $this->connect();
    $sql = "UPDATE questions SET question_num = ? WHERE guild_id = ? AND question_num = ?";
    $stmt = $this->connection->prepare($sql);
    $stmt->bind_param('iii', $new_question_num, $guild_id, $question_num);
    $stmt->execute();
    $ret = $this->connection->affected_rows;
    $this->close();
    return $ret;
  }
}
