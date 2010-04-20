google.load("jquery", "1.3");
google.load("language", "1");

//Returns a language code that Google understands
function get_google_language(val) {
  var v = val.split("-");
  if (v.length == 1) {
    v = v[0].toLowerCase();
  }
  else {
    v = v[0].toLowerCase() + '-' + v[1].toUpperCase();
  }
  //special case covered
  if (v == "pt-BR") {
    return google.language.Languages.PORTUGUESE;
  }
  return v;
}

//Fixes a few things Google does automatically
function fix_translation(v) {
  v = unescape(v);
  v = v.replace(/&#39;/g,'\'');
  v = v.replace(/&quot;/g,'"');
  v = v.replace(/%\s+(\([^\)]+\))\s*s/g,' %$1s ');
  return v;
}

//Calls Google Translate to get a suggestion for the item
function translate(id) {
  var hint = id.split("-");
  var s_lang = get_google_language($("#id_language").val());
  if (!s_lang) {
    alert("Please select first a language for the base menu item!");
    return;
  }
  var source = $("#id_" + hint[2]).val(); //get the source nav item value
  var lang = get_google_language($("#id_"+hint[0]+"-"+hint[1]+"-language").val());
  if (!lang) {
    alert("Please select first a language for this item translation!");
    return;
  }
  google.language.translate(source, s_lang, lang, function(result) {
      if (!result.error) {
        $("#id_" + id).val(fix_translation(result.translation));
      }
      else {
        alert("Google Translate returned error (" + result.error.code + "):\n" + result.error.message);
      }
      });
}

//breaks a string respecting html tags
function break_string(s, max_length) {
  var retval = new Array();
  var current = 0;
  while (current < s.length) {
    var slice = s.substring(current, current + max_length);
    current += max_length;
    retval.push(slice);
  }
  return retval;
}

function translate_code(id) {
  var hint = id.split("-");
  var s_lang = get_google_language($("#id_language").val());
  if (!s_lang) {
    alert("Please select first a language for the base menu item!");
    return;
  }
  var source = $("#id_" + hint[2]).val(); //get the source nav item value
  var lang = get_google_language($("#id_"+hint[0]+"-"+hint[1]+"-language").val());
  if (!lang) {
    alert("Please select first a language for this item translation!");
    return;
  }
  var type = $("#id_markup").val();
  switch (type) {
  case "R":
    type = "html";
    break;
  default:
    type = "text";
  }
  
  //google poses a limitation on the number of characters per request
  $("#id_" + id).val(""); //reset field contents
  break_string(source, 1000).forEach(function(item) {
      var content = new Object();
      content.text = item; 
      content.type = type;
      google.language.translate(content, s_lang, lang, function(result) {
        if (!result.error) {
          $("#id_" + id).val($("#id_" + id).val() + fix_translation(result.translation));
        }
        else {
          alert("Google Translate returned error (" + result.error.code + "):\n" + result.error.message);
        }
      })//lambda for translate()
    });//lambda for source.forEach() 

}
