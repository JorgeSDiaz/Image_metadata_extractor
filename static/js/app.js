const app = (() => {
  // private
  const apiFlask = api;

  const upload = () => {
    $(".upload").submit(function (event) {
      event.preventDefault();
      var form = this;
      apiFlask
        .upload(form, new FormData(form))
        .then((response) => {
          getRow();
          event.preventDefault();
        })
        .catch((error) => {
          console.log(error);
        });
    });
  }

  const init = () => {
    $(document).ready(function () {
      chargeTable();
      upload();
    });
  };

  const chargeTable = () => {
    apiFlask.charge().then((response) => {
      console.log(response)
      response.map((e) => {addRow(e)});
    }).catch((error) => console.log(error));
  }

  const addRow = (data) => {
    console.log(data);
    let tableBody = document.querySelector(".table tbody");

    var newRow = document.createElement('tr');

    var nameCell = document.createElement('td');
    var dateCell = document.createElement('td');
    var hourCell = document.createElement('td');
    var miniatureCell = document.createElement('td');
    var locationCell = document.createElement('td');
    var mapsCell = document.createElement('td');

    nameCell.textContent = data.name;
    dateCell.textContent = data.date;
    hourCell.textContent = data.hour;
    locationCell.textContent = data.location;

    var img = document.createElement('img');
    img.src = data.url;
    img.classList.add('img-fluid');
    miniatureCell.appendChild(img);

    var button = document.createElement('button');
    console.log(data.button != "")
    if (data.button != "") {
      button.classList.add('btn', 'btn-success');
      button.addEventListener('click', () => {
        window.open(data.button, '_blank');
      })
    } else {
      button.classList.add('btn', 'btn-danger');
      button.setAttribute('disabled', 'disabled');
    }
    button.textContent = "OPEN";
    button.style.width = '200px';
    button.style.height = '50px';
    mapsCell.appendChild(button);

    newRow.appendChild(nameCell);
    newRow.appendChild(dateCell);
    newRow.appendChild(hourCell);
    newRow.appendChild(miniatureCell);
    newRow.appendChild(locationCell);
    newRow.appendChild(mapsCell);

    tableBody.appendChild(newRow);
  };

  const getRow = () => {
    let data = apiFlask
      .getImage()
      .then((response) => addRow(response))
      .catch((error) => {
        alert(error);
      });
  };

  // public
  return {
    getRow: getRow,
    init: init,
  };
})();
