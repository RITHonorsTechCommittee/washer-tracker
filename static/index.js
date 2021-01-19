// from https://stackoverflow.com/a/5574446
String.prototype.toProperCase = function () {
  return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

setInterval(function() {
  fetch('/washers')
      .then(res => res.json())
      .then(data => {
          for (const [id, state] of Object.entries(data)) {
              const washerElem = document.getElementById('machine' + id);
              if (washerElem) {
                  // set color
                  washerElem.classList.remove('available', 'unavailable');
                  washerElem.classList.add(state === 'EMPTY' ? 'available' : 'unavailable');

                  // set text
                  const textElems = washerElem.getElementsByTagName('p');
                  if (textElems.length > 0) {
                    textElems[0].textContent = state.toProperCase();
                  }
              }
          }
      })
      .catch((err) => {
        console.log(err);
          alert('Something went wrong, please try again later');
      });
}, 10 * 1000);  // 10 seconds (TODO: change to 1 minute after testing)