<?php
include "login_check.php";
include "header.php";
include "settings.php";
require_once "DBConnection.php";

print "<center>\n";

if(isset($_SESSION['message']))
{
  print $_SESSION['message'];
  unset($_SESSION['message']);
} else {
  print "<br><br>\n";
}

$db = new DBConnection();
$guilds = $db->get_guilds($_SESSION['user_id']);

if(! $guild = $db->get_current_guild($_SESSION['user_id'])){
  $guild = $guilds[0][0];
}

$guild_found = false;
print "  <div id='server_list_div'>\n";
print "    <label>Server:&nbsp;</label>\n";
print "      <select label='Guild:' id='guild_select' onchange='guild_select_change()'>\n";
foreach($guilds as $g){
  print "        <option value='".$g[0]."'";
  if($guild == $g[0]) { print " selected"; $guild_found = true; }
  print ">".$g[1]."</option>\n";
}
print "      </select>\n";

$questions = $db->get_questions($guild);
$question_types = ["None", "Number", "Yes/No", "Text"];

print "<h2>Questions</h2>\n";

print "<table id='question_table'>\n";
print "  <tr>\n";
print "    <th>#</th>\n";
print "    <th>Question</th>\n";
print "    <th>Type</th>\n";
print "  </tr>\n";
foreach($questions as $question){
  print "  <tr>\n";
  print "    <td><center>".$question[0]."</center></td>\n";
  print "    <td id='question_".$question[0]."'>".$question[1]."</td>\n";
  print "    <td id='question_".$question[0]."_type'>".$question_types[$question[2]]."</td>\n";
  print "    <td class='action-cell' onclick='delete_question(".$question[0].")'>❌</td>\n";
  print "    <td class='action-cell' onclick='edit_question(".$question[0].")'>✏️</td>\n";
  print "  </tr>\n";
}
print "</table>\n";

print "</div>\n";
if(!$guild_found){
  print "<br><br><br>\n";
  print "<div class='footer'>\n";
  print "<center>\n";
  print "Hi ".$_SESSION['username']."!<br><br>\n";
  print "It looks like you don't have access to anything here<br><br>\n";
  print "If you've already invited the ".$CLIENT_NAME." bot to your server, DM the bot to request access\n";
  print "</center>\n";
  print "</div>\n";
}
print "<br>\n";
print "<br>\n";

print "<button id='add_question_button' onclick=\"add_question()\" >Add Question</button>\n";
print "<button id='add_save_button' onclick=\"save_add_question()\" >Save</button>\n";
print "<button id='add_cancel_button' onclick=\"cancel_add_question()\" >Cancel</button>\n";
print "<button id='edit_save_button' onclick=\"save_edit_question()\" >Save</button>\n";
print "<button id='edit_cancel_button' onclick=\"cancel_edit_question()\" >Cancel</button>\n";
print "<button onclick=\"location.href='logout.php'\" >Logout</button>\n";

include "footer.php";

?>

</center>
</body>
</html>

<script>
<?php
  if(!$guild_found){
    print "$('#server_list_div').toggle(false)\n";
    print "$('#add_question_button').toggle(false)\n";
  }
  print "var next_question_num=".count($questions)."+1\n";
  print "var guild_id='".$guild."'\n";
?>
$('#add_save_button').toggle(false)
$('#add_cancel_button').toggle(false)
$('#edit_save_button').toggle(false)
$('#edit_cancel_button').toggle(false)
</script>
