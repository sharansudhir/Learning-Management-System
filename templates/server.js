$(document).ready(function () {
  $("#chat").keyup(function (event) {
    if (event.keyCode === 13) {
      $("#enter_chat").click();
    }
  });
});
var lastMessageTimeStamp = Date.now();

function sendData() {
  var chat_term = $("#chat").val();

  x = Date.now();
  lastMessageTimeStamp = x;
  // console.log(x);
  // console.log(chat_term);
  var s = {
    sender_id: "sharan",
    message: chat_term,
    timestamp: x,
  };

  const url =
    "https://us-central1-serverless-project-284322.cloudfunctions.net/pub-sub-publisher/";
  const requestOptions = {
    cache: "no-cache",
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(s),
  };

  fetch(url, requestOptions)
    .then((response) => {
      return response.json();
    })
    .then((data) => console.log(data));
}

document.addEventListener("DOMContentLoaded", function (e) {
  setInterval(recv, 2500);
});

function recv() {
  //   console.log("Sharan Sudhir");
  const url =
    "https://us-central1-serverless-project-284322.cloudfunctions.net/get_chat_data/";
  const requestOptions = {
    cache: "no-cache",
    method: "GET",
    headers: { "Content-Type": "application/json" },
  };

  fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data == "") {
        console.log("Empty");
      } else {
        var obj = JSON.parse(data);
        len = obj.length;

        message = obj;
        // console.log(message);

        for (var i = 0; i < len; i++) {
          console.log(message[i]);
          var lastMessage;
          console.log(lastMessageTimeStamp);
          flag = false;
          if (lastMessageTimeStamp < message[i].timestamp) {
            console.log(message[i]);
            insertChat(
              "you",
              message[i].message,
              undefined,
              message[i].sender_id
            );
            lastMessage = message[i].timestamp;
            flag = true;
          }
        }
        if (flag) {
          lastMessageTimeStamp = lastMessage;
        }
      }
    }); //output to web browser console
}

function formatAMPM(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? "PM" : "AM";
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? "0" + minutes : minutes;
  var strTime = hours + ":" + minutes + " " + ampm;
  return strTime;
}

//-- No use time. It is a javaScript effect.
function insertChat(who, text, time, name) {
  if (time === undefined) {
    time = 0;
  }
  var control = "";
  var date = formatAMPM(new Date());

  if (who == "me") {
    control =
      '<li style="width:100%">' +
      '<div class="msj macro">' +
      '<div class="text text-l">' +
      "<p>" +
      name +
      "</p>" +
      "<p>" +
      text +
      "</p>" +
      "<p><small>" +
      date +
      "</small></p>" +
      "</div>" +
      "</div>" +
      "</li>";
  } else {
    control =
      '<li style="width:100%;">' +
      '<div class="msj-rta macro">' +
      '<div class="text text-r">' +
      "<p>" +
      name +
      "</p>" +
      "<p>" +
      text +
      "</p>" +
      "<p><small>" +
      date +
      "</small></p>" +
      "</div>" +
      "</li>";
  }
  setTimeout(function () {
    $("ul").append(control).scrollTop($("ul").prop("scrollHeight"));
  }, time);
}

function resetChat() {
  $("ul").empty();
}

$(".mytext").on("keydown", function (e) {
  if (e.which == 13) {
    var text = $(this).val();
    if (text !== "") {
      insertChat("me", text);
      $(this).val("");
    }
  }
});

$("body > div > div > div:nth-child(2) > span").click(function () {
  $(".mytext").trigger({ type: "keydown", which: 13, keyCode: 13 });
});

//-- Clear Chat
resetChat();

//-- Print Messages

// insertChat("me", "What would you like to talk about today?", 3500);
// insertChat("you", "Tell me a joke",7000);
// insertChat("me", "Spaceman: Computer! Computer! Do we bring battery?!", 9500);
// insertChat("you", "LOL", 12000);

//-- NOTE: No use time on insertChat.

$(document).ready(function () {
  $("#enter_chat").click(function () {
    var chat_term = $("#chat").val();
    insertChat("me", chat_term, 0, "sharan");
    // insertChat("you", "Hi, Pablo", 1500);
  });
});
