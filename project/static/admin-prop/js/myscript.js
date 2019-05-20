// Confirmation Delete Data

var elems = document.getElementsByClassName('confirmation_delete');

var confirmIt = function (e) {
  if (!confirm('Are you sure delete this?')) e.preventDefault();
};
for (var i = 0; i < elems.length; i++) {
  elems[i].addEventListener('click', confirmIt, false);
}

// Money Input
function moneyformat(){
    let x = document.getElementById("moneyinput");
    x.value = x.value.toSTring().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,")
}
