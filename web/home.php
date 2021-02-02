<?php
include "login_check.inc";
include "header.inc";
include "settings.inc";
require_once "DBConnection.php";

print "<center>\n";
print "<button onclick=\"location.href='change_password.php'\" >Change Password</button>\n";
print "<button onclick=\"location.href='logout.php'\" >Logout</button>\n";
print "<br><br>\n";

if(isset($_SESSION['message']))
{
  print $_SESSION['message'];
  unset($_SESSION['message']);
} else {
  print "<br><br>\n";
}

$db = new DBConnection();
$guilds = $db->get_guilds($_SESSION['user_id']);

$guild = $guilds[0][0];

if(isset($_GET['guild'])){
  foreach($guilds as $g){
    if($g[0] == $_GET['guild']){ $guild = $g[0]; }
  }
}

print "    <label>Server:&nbsp;</label>\n";
print "      <select label='Guild:' id='guild_select' onchange=\"location.href='home.php?guild='+$('#guild_select').val()\">\n";
foreach($guilds as $g){
  print "        <option value='".$g[0]."'";
  if($guild == $g[0]) { print " selected"; }
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
  print "    <td>".$question[0]."</td>\n";
  print "    <td>".$question[1]."</td>\n";
  print "    <td>".$question_types[$question[2]]."</td>\n";
  print "    <td class='delete-cell' onclick='del_question(".$question[0].")'>❌</td>\n";
  print "    <td class='delete-cell' onclick='edit_question(".$question[0].")'>✏️</td>\n";
  print "  </tr>\n";
}
print "</table>\n";

print "<br>\n";
print "<br>\n";

print "<button id='add_question_button' onclick=\"add_question()\" >Add Question</button>\n";
print "<button id='save_button' onclick=\"save_add_question()\" >Save</button>\n";
print "<button id='cancel_button' onclick=\"cancel_add_question()\" >Cancel</button>\n";

?>

</center>
</body>
</html>

<script>
<?php print "var next_question_num=".count($questions)."+1\n"; ?>
<?php print "var guild_id='".$guild."'\n"; ?>
$('#save_button').toggle(false)
$('#cancel_button').toggle(false)
</script>
