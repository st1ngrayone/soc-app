$(document).ready(function() {
    setTimeout(function() {
        $(".alert-dismissible").alert('close');
    }, 3000);
});


function sendFollower(followerId, type)  {
  let data = {
    type: type, followerId: followerId
  };

  fetch("/follow", {
    method: "POST",
    body: JSON.stringify(data)
  }).then(res => {
    console.log("Request complete! response:", res);
  });
}
