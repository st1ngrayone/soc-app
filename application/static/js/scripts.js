$(document).ready(function() {
    setTimeout(function() {
        $(".alert-dismissible").alert('close');
    }, 3000);
});


function sendFollower(followerId, post_id, type)  {
  let data = {
    type: type, post_id: post_id, followerId: followerId
  };

  fetch("/follow", {
    method: "POST",
    body: JSON.stringify(data)
  }).then(res => {
    console.log("Request complete! response:", res);
    window.location.reload();
  });
}
