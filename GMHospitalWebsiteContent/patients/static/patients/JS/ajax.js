$(document).ready(function(){

   $('#submit').click(function(){

        $.ajax({
              type: "POST",
              url: "/patients/postToDB",
              dataType: "json",
              data: {"aadharNo": $("#aadharNo").val(),
                     "name": $("#name").val(),
                     "surname": $("#surname").val(),
                     "gender": $("#optradio").val(),
                     "age": $("#age").val(),
                     "address": $("#address").val(),
                     "mobile": $("#mobile").val(),
              },
              success: function(output){

              }
        });
   });

   $('#forgetPwd').click(function(){
        $('#forgetPasswd').modal('show');
   });

   $('#resetPwd').click(function(){
        $('#resetPasswd').modal('show');
   });

   $('#resetPasswd').on('hidden.bs.modal', function (e) {
      $(this)
        .find("input,email,select")
           .val('')
           .end()
        .find("input,password,select")
           .val('')
           .end();
   });

   $('#setPassword').click(function(){
        $.ajax({
            type: "POST",
            url: "/patients/resetPassword",
            dataType: "json",
            data: {"email": $("#setEmail").val(),
                   "oldPassword": $("#curPassword").val(),
                   "newPassword": $("#newPassword").val(),
                   "type": $("#type").val(),
            },
            success: function(output){
                document.getElementById("serverReply").innerHTML = output["message"];
                $('#serverMsg').modal('show');
            }
        });
   });

   $('#callResetPassword').click(function(){

        $.ajax({
            type: "POST",
            url: "/patients/forgetPassword",
            dataType: "json",
            data: {"email": $("#resetEmail").val(),
                   "type": $("#type").val(),
            },
            success: function(output){
                document.getElementById("serverReply").innerHTML = output["message"];
                $('#serverMsg').modal('show');
            }
        });
   });

   $('#generate').click(function(){

       $.ajax({
           type: "POST",
           url: "/patients/generateOp",
           dataType: "json",
           data: {"type": $("#type").val(),
               "identifier": $("#identifier").val(),
               "problems": $("#problems").val(),
           },
           success: function(output){
               document.getElementById("message").innerHTML = output["message"]+" and patient token is "+output["patientToken"];
               $('#myModal').modal('show');
           }
       });
   });

  $("#unapprovedUsers").click(function(){

      $.ajax({
          type: "POST",
          url: "/patients/getUnapprovedUsers",
          dataType: "json",
          success: function(output){
              var i=0;
              var count = output["count"];
              var table = document.getElementById("approveTable");
              for(i=1;i<=count;i++){
                  var row = table.insertRow(i);
                  var cell1 = row.insertCell(0);
                  var cell2 = row.insertCell(1);
                  var cell3 = row.insertCell(2);
                  var checkbox = '<input type="checkbox" id="checkBox'+i+'" value="no">';
                  cell1.innerHTML = checkbox;
                  cell2.innerHTML = '<p id="email'+i+'">'+output["email"+i]+'</p>';
                  cell3.innerHTML = output["name"+i];
              }
              $('#pendingApproval').modal('show');
          }
      });
  });

  $("#approveUsers").click(function(){

      var table = document.getElementById("approveTable");
      while(table.rows.length > 1) {
          var rowCount = table.rows.length-1;
          //var id = "checkBox"+rowCount;
          var eid = "email"+rowCount;
          //var bool = document.getElementById(id).checked;
          //window.alert($("#eid").val());
          var TextInsideLi = document.getElementsByTagName(eid).innerHTML;
          window.alert(TextInsideLi);
          table.deleteRow(rowCount-1);
//          if(bool){
//              window.alert($('#eid').val());
//          }
      }

//      $.ajax({
//          type: "POST",
//          url: "/patients/getUnapprovedUsers",
//          dataType: "json",
//          success: function(output){
//              var i=0;
//              var count = output["count"];
//              var table = document.getElementById("approveTable");
//              for(i=1;i<=count;i++){
//                  var row = table.insertRow(i);
//                  var cell1 = row.insertCell(0);
//                  var cell2 = row.insertCell(1);
//                  var cell3 = row.insertCell(2);
//                  var checkbox = '<input type="checkbox" id="checkBox'+i+'" value="no">';
//                  cell1.innerHTML = checkbox;
//                  cell2.innerHTML = '<p id="email'+i+'">'+output["email"+i]+'</p>';
//                  cell3.innerHTML = output["name"+i];
//              }
//              $('#pendingApproval').modal('show');
//          }
//      });
  });

 $('#deleteTable').click(function(){
      var table = document.getElementById("approveTable");
      while(table.rows.length > 1) {
          var rowCount = table.rows.length;
          table.deleteRow(rowCount-1);
      }
      $('#pendingApproval').modal('toggle');
 });

   $('#save').click(function(){

       $.ajax({
           type: "POST",
           url: "/patients/createUser",
           dataType: "json",
           data: {"loginAlias": $("#userName").val(),
               "password": $("#passwd").val(),
               "email": $("#email").val(),
           },

           success: function(output){
            document.getElementById("message").innerHTML = output["message"];
            $('#myModal').modal('show');
           }
       });
   });

   function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
   }
   var csrftoken = getCookie('csrftoken');

   function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
   }
   $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
     });
});