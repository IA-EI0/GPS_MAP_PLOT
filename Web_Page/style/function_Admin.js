// Setup Function
window.onload = function(){
  // Status(RP1)
  fetch('./json/GPS_RP1.json',{cache: "no-store"})
  .then(function (data) {
    return data.json();
  })
  .then(function (jsonG1) {
    var time1 = jsonG1["Time"];
    document.getElementById("red_gps").innerHTML = time1;
  });
   // Status(RP2)
  fetch('./json/GPS_RP2.json',{cache: "no-store"})
  .then(function (data) {
    return data.json();
  })
  .then(function (jsonG2) {
    var time2 = jsonG2["Time"];
    document.getElementById("blue_gps").innerHTML = time2;
  });
   // Status(RP3)
  fetch('./json/GPS_RP3.json',{cache: "no-store"})
  .then(function (data) {
    return data.json();
  })
  .then(function (jsonG3) {
    var time3 = jsonG3["Time"];
    document.getElementById("yellow_gps").innerHTML = time3;
  });
  // UpdateTime
  // Admin
  fetch('./json/Map_Admin.json',{cache: "no-store"})
  .then(function (data) {
    return data.json();
  })
  .then(function (jsonMA) {
    var time_a = jsonMA["LastUpdateTime"];
    let lua = document.getElementById('LastUpdate_A');
    if (lua !== null) {
      document.getElementById("LastUpdate_A").innerHTML = time_a;
    }
  });
  // Player
    fetch('./json/Map_Player.json',{cache: "no-store"})
  .then(function (data) {
    return data.json();
  })
  .then(function (jsonMP) {
    var time_p = jsonMP["LastUpdateTime"];
    let lup = document.getElementById('LastUpdate_P');
    if (lup !== null) {
      document.getElementById("LastUpdate_P").innerHTML = time_p;
    }
  });
}
