$(document).ready(function(){
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  var id = urlParams.get('id');
  if ( id == null ) {
    id = 1;
  }

  $("#increment").click(function(){

      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4){
          document.getElementById('occupancy').innerHTML = xhr.responseText;
        }
      };
      xhr.open('GET', 'increment?id=' + id );
    xhr.send();
  });

  $("#decrement").click(function(){

      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4){
          document.getElementById('occupancy').innerHTML = xhr.responseText;
        }
      };
      xhr.open('GET', 'decrement?id=' + id );
    xhr.send();
  });

});
