
// Redirect to the specified URL after a certain number of seconds
function redirect(url, time) {
  setTimeout(function() {
    window.location.href = url;
  }, time * 1000);
}

// Redirect to the specified URL after 6 seconds
redirect('http://127.0.0.1:8000/', 5);
