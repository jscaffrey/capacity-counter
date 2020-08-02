$(document).ready(function(){
  $("#increment").click(function(){
      console.log("clicked!");

      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4){
          document.getElementById('occupancy').innerHTML = xhr.responseText;
        }
      };
      xhr.open('GET', 'increment');
    xhr.send();
  });

  $("#decrement").click(function(){
      console.log("clicked!");

      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4){
          document.getElementById('occupancy').innerHTML = xhr.responseText;
        }
      };
      xhr.open('GET', 'decrement');
    xhr.send();
  });

});
