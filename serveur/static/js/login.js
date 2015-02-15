function tryLogin () {
  var jsondata = {
      email: $("#opz-email").val(),
      password: $("#opz-password").val(),
  };
  if ($("#opz-remember").prop('checked'))
    jsondata.remember = "1";
	$.ajax({
      type: "POST",
      url: "/api/v1/login",
      data: JSON.stringify(jsondata),
      contentType: "application/json",
      success: function(data, status, xhr) {
        if (data != "0")
          window.location.href = "/" + getLang(document.location.href) + "/dashboard?account_id=" + data;
        else
          alert('login successful, connect with the link in the welcome email');
      },
      error: function(xhr, status, error) {
        alert('Cant connect. Sign up, use the forget your password functionality or contact us if you have any problem.');
      }
	});
}


function forgotPassword() {
  $.ajax({
      type: "GET",
      url: "/api/v1/forgot_password?email=" + $("#opz-email").val(),
      success: function(data, status, xhr) {
          alert('Email succesfully sent');
      },
      error: function(xhr, status, error) {
        alert('Could not send the password to the specified email. Account may not exist.');
      }
  });  
}