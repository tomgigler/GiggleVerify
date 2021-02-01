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

print "    <label>Server:&nbsp;</label>\n";
print "      <select label='Guild:' id='guild_select'>\n";
foreach($guilds as $guild){
  print "        <option value='".$guild[0]."'>".$guild[1]."</option>\n";
}
print "      </select>\n";

$questions = $db->get_questions($guilds[0][0]);
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
  print "  </tr>\n";
}
print "</table>\n";

?>

</center>
</body>
</html>

<script>
$("#question_table").innerHTML = ""
</script>
