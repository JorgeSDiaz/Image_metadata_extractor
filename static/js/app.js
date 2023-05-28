const app = (() => {
  // private
  const apiFlask = api;
  const data_uploaded = [];

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
      $(document).ready(function() {
        $("#driveButton").on("click", function() {
          window.open("https://drive.google.com/drive/folders/1exVAksxzJS4knfayDY176WEUYva9pBqS?usp=sharing", "_blank");
        });
      });
      // upload();
    });
  };

  const chargeTable = () => {
    apiFlask.charge().then((response) => {
      console.log(response)
      response.map((e) => {addRow(e)});
    }).catch((error) => console.log(error));
  }

  const addRow = (data) => {
    if (!(data_uploaded.includes(data.name))) {
      let newRow = $("<tr></tr>");
    
      let nameCell = $("<td></td>").text(data.name);
      let dateCell = $("<td></td>").text(data.date);
      let hourCell = $("<td></td>").text(data.hour);
      let miniatureCell = $("<td></td>");
      let locationCell = $("<td></td>").text(data.location);
      let mapsCell = $("<td></td>");
    
      let img = $("<img>").attr("src", data.url).addClass("img-fluid");
      miniatureCell.append(img);
    
      let button = $("<button></button>").text("OPEN").css({"width": "200px", "height": "50px"});
      if (data.button.startsWith('https')) {
        button.addClass("btn btn-success").on("click", function() {
          window.open(data.button, "_blank");
        });
      } else {
        button.addClass("btn btn-danger").prop("disabled", true);
      }
      mapsCell.append(button);
    
      newRow.append(nameCell, dateCell, hourCell, miniatureCell, locationCell, mapsCell);
    
      $(".table tbody").append(newRow);
      data_uploaded.push(data.name);
    }
    
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
