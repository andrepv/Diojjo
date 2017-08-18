 $("#signup_form").validate({
	rules:
	{
		username: {
			required: true,
			minlength: 5
		},
		email: {
			required: true
		},
		password1: {
			required: true,
		},
	},

	messages:
	{
		username:{
			required: "This field is required",
			minlength: "This value length is invalid",
		},
		email:{
			required: "This field is required",
		},
		password1:{
			required: "This field is required",
		},
	}
});
$('#login_form').validate({
	rules:
	{
		username: {
			required: true,
		},
		password: {
			required: true,
		},
	},
		messages:
	{
		username:{
			required: "This field is required",
		},
		password:{
			required: "This field is required",
		},
	}
});
$('#edit_form').validate({
	rules:
	{
		username: {
			required: true,
		},
	}
});

$("#id_username").change(function () {
	var form = $(this).closest("form");
	$.ajax({
		url: form.attr("data-validate-username"),
		data: form.serialize(),
		dataType: 'json',
		success: function (data) {
		if (data.is_taken) {
			$("#name_check_ok").hide();
			$("#name_check_error").show();
		}else{
			$("#name_check_error").hide();
			$("#name_check_ok").show();
			}
		}
	});
});