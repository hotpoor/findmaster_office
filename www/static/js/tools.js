// Generated by CoffeeScript 1.12.7
(function() {
  var Hs, root;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.Hs || (root.Hs = {});

  Hs = root.Hs;

  root.uuid2s = [];

  $(function() {
    return root.uuid2 = function(len, radix) {
      var chars, i, j, k, r, ref, ref1, uuid;
      chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');
      uuid = [];
      i = null;
      radix = radix || chars.length;
      if (len) {
        for (i = j = 0, ref = len; 0 <= ref ? j <= ref : j >= ref; i = 0 <= ref ? ++j : --j) {
          uuid[i] = chars[0 | Math.random() * radix];
        }
      } else {
        r = null;
        uuid[8] = uuid[13] = uuid[18] = uuid[23] = '-';
        uuid[14] = '4';
        for (i = k = 0; k <= 36; i = ++k) {
          if (!uuid[i]) {
            r = 0 | Math.random() * 16;
            uuid[i] = chars[(ref1 = i === 19) != null ? ref1 : (r & 0x3) | {
              0x8: r
            }];
          }
        }
      }
      return uuid.join('');
    };
  });

}).call(this);