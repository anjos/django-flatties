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

//breaks a string using newlines as a marker
function break_string(s, max_length) {
  var retval = new Array();
  s.split('\n').forEach(function(item) {
        var current = 0;
        if (item.length == 0) { //preserves empty lines
          retval.push(item);
          return;
        }
        while (current < item.length) { //no empty lines get here
          retval.push(item.substr(current, max_length));
          current = current + max_length;
        }
        });
  return retval;
}

//A check function for setInterval() has to be global and use globals
var interval = "";
var original = null;
var translated = null;
var trans_destination_field = null;
function check() {
  var nulls = false;
  for (k in translated) { 
    if (k == null) { nulls = true; }
  }
  if ((original.length == translated.length) && (!nulls) && (interval != "")) {
    clearInterval(interval);
    //at this point, we just have to set the output
    if (trans_destination_field) {
      trans_destination_field.val(translated.join("\n"));
    }
  }
}

//This function is supposed to be called when the user clicks the translation
//button at the textarea icon for "google translation".
function translate_text(id) {
  var hint = id.split("-");
  var src_lang = get_google_language($("#id_language").val());
  if (!src_lang) {
    alert("Please select first a language for the base menu item!");
    return;
  }
  var source = $("#id_" + hint[2]).val(); //get the source nav item value
  var dest_lang = get_google_language($("#id_"+hint[0]+"-"+hint[1]+"-language").val());
  if (!dest_lang) {
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
  // => so, this gets very complicated...
  // => we have to split the input and collect the outputs from google 
  // => now comes something interesting: the call to google's translate() is
  // assynchronous. that means you cannot expect to collect the results in the
  // right order just by waiting. you have to introduced an ordered collection
  // of the translations. and that is why we keep the translation in an array,
  // "translated", which is a reflection of the original untranslated text.
  // => to add a "salt", because the translation is assynchronous, it follows
  // that we have to do the requests and keep testing if all the strings have 
  // come back. This is done with the "setInterval()" function call by the end 
  // of this method.
  // => please note that this weird function has a very peculiar way of
  // working: its scope and the scope of tested variables (internally) should
  // be global or these variables are not found.
  // => if everything goes ok and all positions in the output array are filled,
  // the textarea is refreshed (that are is pointed by
  // "trans_destination_field").
  original = break_string(source, 500); //global
  translated = new Array(); //global

  original.forEach(function(item, index) {
      //if the item is empty that means a newline should be inserted
      //and that is it for this entry.
      if (item.length == 0) { 
        translated[index] = item; 
      }
      else {
        //otherwise, we have to consult with google
        var content = new Object();
        content.text = item;
        content.type = type;
        content.index = index;
        google.language.translate(content, src_lang, dest_lang, function(result) {
          if (!result.error) {
            translated[content.index] = fix_translation(result.translation);
          }
          else {
            alert("Google Translate returned error (" + result.error.code + "):\n" + result.error.message);
            translated[context.index] = original[context.index]; 
          }
        });//lambda for translate()
      } //else clause
    });//lambda for source.forEach() 

  //now we just have to wait until all positions have been filled
  trans_destination_field = $("#id_" + id);
  interval = setInterval('check()', 100);
}
