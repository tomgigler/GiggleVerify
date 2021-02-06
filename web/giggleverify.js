var editing = false;
var current_question = "";
var current_question_num = null;
var current_question_type = null;

function guild_select_change(){
  data = new FormData();
  data.append('guild_id', $('#guild_select').val());

  myRequest = new Request("update_current_guild.php");

  fetch(myRequest ,{
    method: 'POST',
    body: data,
  })
  .then(function(response) {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  });

  location.reload();
}

function edit_question(question_num){
  if(editing){ return; }
  editing = true;
  $('.action-cell').attr('class', 'disable-cell');
  $('#add_question_button').toggle(false);
  $('#edit_save_button').toggle(true);
  $('#edit_cancel_button').toggle(true);
  current_question = $('#question_'+question_num).text();
  current_question_type = $('#question_'+question_num+'_type').text();
  current_question_num = question_num;
  $('#question_'+question_num).html('<input id="new_question" style="display:table-cell; width:100%" value="'+current_question+'" maxlength="200">')
  $('#question_'+question_num+'_type').html('<select id="question_type" style="display:table-cell; width:100%">');
  $('#question_type').append($('<option value=3>Text</option>'));
  $('#question_type').append($('<option value=2>Yes/No</option>'));
  $('#question_type').append($('<option value=1>Number</option>'));
  if(current_question_type == "Number"){ $('#question_type').val(1); }
  if(current_question_type == "Yes/No"){ $('#question_type').val(2); }
  $('#new_question').focus();
  $('#new_question').on('keypress', function(e){
    if(e.which == 13){
      save_edit_question();
    }
  });
}

function cancel_edit_question(){
  $('#add_question_button').toggle(true);
  $('#edit_save_button').toggle(false);
  $('#edit_cancel_button').toggle(false);
  $('.disable-cell').attr('class', 'action-cell');
  $('#question_'+current_question_num).text(current_question);
  $('#question_'+current_question_num+'_type').text(current_question_type);
  editing = false;
}

function save_edit_question(){
  if($('#new_question').val() == ""){
    alert("Question cannot be blank!");
    return;
  }
  data = new FormData();
  data.append('guild_id', guild_id);
  data.append('question_num', current_question_num);
  data.append('question', $('#new_question').val());
  data.append('question_type', $('#question_type').find(":selected").val());

  myRequest = new Request("save_question.php");

  fetch(myRequest ,{
    method: 'POST',
    body: data,
  })
  .then(function(response) {
    if (!response.ok) {
      location.href='index.php'
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  });

  current_question = $('#new_question').val();
  current_question_type = $('#question_type').find(":selected").text();
  cancel_edit_question();
}

function delete_question(question_num){
  // $(this).closest('tr').find('textarea').val("some text");
  if(editing){ return; }
  if(!confirm('Delete question ' + question_num + '?')){ return; }
  data = new FormData();
  data.append('guild_id', guild_id);
  data.append('question_num', question_num);

  myRequest = new Request("delete_question.php");

  fetch(myRequest ,{
    method: 'POST',
    body: data,
  })
  .then(function(response) {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    location.href='home.php'
  });
}

function add_question(){
  $('#add_question_button').toggle(false);
  $('#add_save_button').toggle(true);
  $('#add_cancel_button').toggle(true);
  $('#question_table').append($('<tr id="tmp_row">').append($('<td>').html("<center>"+next_question_num+"</center>")));
  $('#tmp_row').append($('<td>').append($('<input id="new_question" style="display:table-cell; width:100%" maxlength="200">')));
  $('#tmp_row').append($('<td>').append($('<select id="question_type" style="display:table-cell; width:100%">')));
  $('#question_type').append($('<option value=3>Text</option>'));
  $('#question_type').append($('<option value=2>Yes/No</option>'));
  $('#question_type').append($('<option value=1>Number</option>'));
  $('.action-cell').attr('class', 'disable-cell');
  $('#new_question').focus();
  $('#new_question').on('keypress', function(e){
    if(e.which == 13){
      save_add_question();
    }
  });
  editing = true;
}

function cancel_add_question(){
  $('#add_question_button').toggle(true);
  $('#add_save_button').toggle(false);
  $('#add_cancel_button').toggle(false);
  $('#tmp_row').remove();
  $('.disable-cell').attr('class', 'action-cell');
  editing = false;
}

function save_add_question(){
  if($('#new_question').val() == ""){
    alert("Question cannot be blank!");
    return;
  }
  data = new FormData();
  data.append('guild_id', guild_id);
  data.append('question_num', next_question_num);
  data.append('question', $('#new_question').val());
  data.append('question_type', $('#question_type').find(":selected").val());

  myRequest = new Request("save_question.php");

  fetch(myRequest ,{
    method: 'POST',
    body: data,
  })
  .then(function(response) {
    if (!response.ok) {
      location.href='index.php'
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  });

  $('#add_question_button').toggle(true);
  $('#add_question_button').focus();
  $('#add_save_button').toggle(false);
  $('#add_cancel_button').toggle(false);
  $('#question_table').find('tbody').append($('<tr id="new_row">').append($('<td>').html("<center>"+next_question_num+"</center>")));
  $('#new_row').append($('<td>').text($('#new_question').val()));
  $('#new_row').append($('<td>').text($('#question_type').find(":selected").text()));
  $('#new_row').append($('<td class="action-cell" onclick="delete_question('+next_question_num+')">❌</td>'))
  $('#new_row').append($('<td class="action-cell" onclick="edit_question('+next_question_num+')">✏️</td>'))
  $('#new_row').removeAttr('id');
  $('#tmp_row').remove();
  next_question_num += 1;
  $('.disable-cell').attr('class', 'action-cell');
  editing = false;
}
