
const vrllogger = {
  uuid: null,
  ipaddr: null,
  url: null,
  code: null,
 
  init: function() {
    this.id = "secim2023site";
    this.url = "https://vrllab.sabanciuniv.edu/api/collect/";
    this.uuid = Date.now().toString(36) + Math.random().toString(36).substring(2);
    // https://stackoverflow.com/questions/391979/how-to-get-clients-ip-address-using-javascript
    $.getJSON('https://json.geoiplookup.io/?callback=?',function(json){
      this.ipaddr = json;
    }.bind(this));
  },

  event: function(eventCode, message) {
    let logdata = {
      "app-id":this.id, 
      "data":{"event_type": eventCode, "message": message},
      "meta":{
        "id": this.uuid,
        "url": window.location.href,
        "ip": this.ipaddr,
        "ts": Math.floor(Date.now() / 1000)
      }
    }

    $.ajax({
            url: this.url,
            type: "POST",
            crossDomain: true,
            data: JSON.stringify(logdata),
            contentType: "application/json; charset=utf-8"
        });

    //var message = JSON.stringify(logdata);
    //console.log(logdata);
  }
};

// Start logger immediately
vrllogger.init();

