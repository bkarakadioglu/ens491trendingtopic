function setCookieIfNotExist(cname){
  let uuid = Date.now().toString(36) + Math.random().toString(36).substring(2);
  if (document.cookie.indexOf(cname + '=') === -1){
    setCookie(cname, uuid);
  }
}

function setCookie(cname, value, expiry) {
  const date = new Date();
  date.setTime(date.getTime() + (expiry * 24 * 60 * 60 * 1000));
  var expires = "expires="+date.toUTCString();
  document.cookie = cname + "=" + value + ";" + expires + ";path=/";
}

function getCookie(cname, dval) {
  let name = cname + "=";
  let spli = document.cookie.split(';');
  for(var j = 0; j < spli.length; j++) {
    let char = spli[j];
    while (char.charAt(0) == ' ') {
      char = char.substring(1);
    }
    if (char.indexOf(name) == 0) {
      return char.substring(name.length, char.length);
    }
  }
  return dval;
}

let langs = ['en', 'tr'];
let lang = getCookie('pagelang','en');

function setLang(l) {
  lang = l;
  setCookie('pagelang', lang, 365);

  console.log('Language set to '+lang);
  for (let i = 0; i < langs.length; i++) {
    if(langs[i] == lang){
      $('[tlang="' + langs[i] + '"]').each(function() {
        $(this).css({'visibility':'visible', 'display':''});
      });
    }else{
      $('[tlang="' + langs[i] + '"]').each(function() {
        $(this).css({'display':'none', 'visibility':''});
      });
    }
  }
  
}

