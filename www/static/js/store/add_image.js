// Generated by CoffeeScript 1.12.7
(function() {
  var Hs, canvasDataURL, convertBase64UrlToBlob, root;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.Hs || (root.Hs = {});

  Hs = root.Hs;

  canvasDataURL = function(path, obj, quality, callback) {
    var img;
    if (quality == null) {
      quality = 0.7;
    }
    img = new Image();
    img.src = path;
    return img.onload = function() {
      var anh, anw, base64, canvas, ctx, h, scale, that, w;
      that = this;
      w = that.width;
      h = that.height;
      scale = w / h;
      w = obj.width || w;
      h = obj.height || (w / scale);
      canvas = document.createElement('canvas');
      ctx = canvas.getContext('2d');
      w = parseInt(w * quality);
      h = parseInt(h * quality);
      anw = document.createAttribute("width");
      anw.nodeValue = w;
      anh = document.createAttribute("height");
      anh.nodeValue = h;
      canvas.setAttributeNode(anw);
      canvas.setAttributeNode(anh);
      ctx.drawImage(that, 0, 0, w, h);
      if (obj.quality && obj.quality <= 1 && obj.quality > 0) {
        quality = obj.quality;
      }
      base64 = canvas.toDataURL('image/png', 0.7);
      return callback(base64);
    };
  };

  convertBase64UrlToBlob = function(urlData) {
    var arr, bstr, mime, n, u8arr;
    arr = urlData.split(',');
    mime = arr[0].match(/:(.*?);/)[1];
    bstr = atob(arr[1]);
    n = bstr.length;
    u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {
      type: mime
    });
  };

  $(function() {
    var CDN_PREFIX, current_dom_img, file_lists, handleFileSelect;
    CDN_PREFIX = "http://qcdn.winni.app";
    CDN_PREFIX = "http://office-cdn.xialiwei.com";
    file_lists = [];
    current_dom_img = null;
    if (window.File && window.FileList && window.FileReader && window.Blob && window.Worker) {
      handleFileSelect = function(evt) {
        var _room_id, content_type, endingByte, file_index, files, img_add, ref, startingByte, uploadFile;
        img_add = (ref = $(this).attr("id") === "msh_hollow_img_add_upload") != null ? ref : {
          "true": false
        };
        _room_id = BLOCK_ID;
        content_type = "HQWEBIMG//";
        evt.stopPropagation();
        evt.preventDefault();
        files = null;
        if (evt.target.files) {
          files = evt.target.files;
        } else {
          files = evt.dataTransfer.files;
        }
        file_lists.push(files);
        file_index = 0;
        startingByte = 0;
        endingByte = 0;
        console.log("image coffee");
        console.log(BLOCK_ID);
        uploadFile = function(file) {
          var loading_flag, reader, tempfile, type, updateProgress, uploadNextFile, xhrProvider;
          if (file === void 0) {
            return;
          }
          if (file.type === void 0) {
            return;
          }
          type = file.type ? file.type : 'n/a';
          console.log(type);
          if (!(type === "image/jpeg" || type === "image/jpg" || type === "image/webp" || type === "image/png" || type === "image/gif" || type === "image/bmp")) {
            file_index += 1;
            alert("文件格式不支持");
            return;
          }
          reader = new FileReader();
          tempfile = null;
          startingByte = 0;
          console.log("正在上传第一张图片");
          loading_flag = uuid2(6, null);
          current_dom_img.after("<div id=\"loading_" + loading_flag + "\" class=\"loading_flag\" contenteditable=\"false\"></div>");
          $("#loading_" + loading_flag).animate({
            "width": "25%"
          }, 1000);
          xhrProvider = function() {
            var xhr;
            xhr = jQuery.ajaxSettings.xhr();
            if (xhr.upload) {
              xhr.upload.addEventListener('progress', updateProgress, false);
            }
            return xhr;
          };
          updateProgress = function(evt) {
            return console.log("Uploading file " + (file_index + 1) + " of " + files.length + " at " + ((startingByte + (endingByte - startingByte) * evt.loaded / evt.total) / file.size * 100) + "%");
          };
          uploadNextFile = function() {
            var obj;
            console.log("正在要上传下一张图片");
            file_index += 1;
            if (file_index < files.length) {
              uploadFile(files[file_index]);
              console.log("===");
              console.log(file_index);
              return console.log("===|||");
            } else {
              file_lists.shift();
              if (file_lists.length > 1) {
                file_index = 0;
                files = file_lists[0];
                uploadFile(files[file_index]);
                console.log("===+++");
                console.log(file_index);
                return console.log("===|||");
              } else {
                console.log("===>>>");
                obj = document.getElementById('msh_hollow_img_add_upload');
                return obj.outerHTML = obj.outerHTML;
              }
            }
          };
          reader.onload = function(evt) {
            var bin, content, re, re_this, w, worker;
            content = evt.target.result.slice(evt.target.result.indexOf("base64,") + 7);
            bin = atob(content);
            re_this = this;
            re = re_this.result;
            w = {
              quality: 0.3
            };
            worker = new Worker("/static/js/md5.js");
            worker.onmessage = function(event) {
              var Qiniu_UploadUrl, Qiniu_UploadUrl_https, md5, worker_aim_url;
              md5 = event.data;
              Qiniu_UploadUrl_https = "https://up-z1.qiniup.com";
              if (window.location.protocol === "https:") {
                Qiniu_UploadUrl = Qiniu_UploadUrl_https;
              } else {
                Qiniu_UploadUrl = "http://up-z1.qiniup.com";
              }
              worker_aim_url = "/api/image/check";
              return $.post(worker_aim_url, {
                "block_id": _room_id,
                "md5": md5
              }, function(data) {
                var Qiniu_upload, obj, ref1, result_url, size, size_scale, upload_token;
                if (files.length === 1) {
                  console.log("正在上传1张图片");
                  if (data["exists"]) {
                    result_url = CDN_PREFIX + "/" + BLOCK_ID + "_" + md5 + "?imageView2/2/w/300";
                    $(".comment_submit_add_imgs").removeClass("hide");
                    $(".comment_submit_add_imgs").find(".comment_submit_add_img_more").before("<div class=\"comment_submit_add_img_one\">\n    <img class=\"comment_submit_add_img_one_img\" src=\"" + result_url + "\">\n    <div class=\"del_one\"></div>\n</div>");
                    $("#loading_" + loading_flag).animate({
                      "width": "100%"
                    }, 500, function() {
                      return $("#loading_" + loading_flag).remove();
                    });
                    obj = document.getElementById('msh_hollow_img_add_upload');
                    obj.outerHTML = obj.outerHTML;
                    return;
                  }
                } else {
                  if (file_index + 1 === files.length) {
                    console.log("正在上传最后一张图片");
                    if (data["exists"]) {
                      result_url = CDN_PREFIX + "/" + BLOCK_ID + "_" + md5 + "?imageView2/2/w/300";
                      $(".comment_submit_add_imgs").removeClass("hide");
                      $(".comment_submit_add_imgs").find(".comment_submit_add_img_more").before("<div class=\"comment_submit_add_img_one\">\n    <img class=\"comment_submit_add_img_one_img\" src=\"" + result_url + "\">\n    <div class=\"del_one\"></div>\n</div>");
                      $("#loading_" + loading_flag).animate({
                        "width": "100%"
                      }, 500, function() {
                        return $("#loading_" + loading_flag).remove();
                      });
                      obj = document.getElementById('msh_hollow_img_add_upload');
                      obj.outerHTML = obj.outerHTML;
                      return;
                    }
                  } else {
                    console.log("正在上传" + (file_index + 1) + "/" + files.length + "张图片");
                    if (data["exists"]) {
                      result_url = CDN_PREFIX + "/" + BLOCK_ID + "_" + md5 + "?imageView2/2/w/300";
                      $(".comment_submit_add_imgs").removeClass("hide");
                      $(".comment_submit_add_imgs").find(".comment_submit_add_img_more").before("<div class=\"comment_submit_add_img_one\">\n    <img class=\"comment_submit_add_img_one_img\" src=\"" + result_url + "\">\n    <div class=\"del_one\"></div>\n</div>");
                      $("#loading_" + loading_flag).animate({
                        "width": "100%"
                      }, 500, function() {
                        return $("#loading_" + loading_flag).remove();
                      });
                      return uploadNextFile();
                    }
                  }
                }
                upload_token = data["token"];
                Qiniu_upload = function(f, token, key) {
                  var formData, startDate, xhr;
                  xhr = new XMLHttpRequest();
                  xhr.open('POST', Qiniu_UploadUrl, true);
                  formData = new FormData();
                  if (key !== null && key !== void 0) {
                    formData.append('key', key);
                  }
                  formData.append('token', token);
                  formData.append('file', f);
                  xhr.upload.addEventListener("progress", function(evt) {
                    var formatSpeed, nowDate, percentComplete, taking, uploadSpeed, x, y;
                    if (evt.lengthComputable) {
                      nowDate = new Date().getTime();
                      taking = nowDate - startDate;
                      x = evt.loaded / 1024;
                      y = taking / 1000;
                      uploadSpeed = x / y;
                      if (uploadSpeed > 1024) {
                        formatSpeed = (uploadSpeed / 1024).toFixed(2) + "Mb\/s";
                      } else {
                        formatSpeed = uploadSpeed.toFixed(2) + "Kb\/s";
                      }
                      percentComplete = Math.round(evt.loaded * 100 / evt.total);
                      console.log(percentComplete, ",", formatSpeed);
                      return $("#loading_" + loading_flag).css({
                        "width": (25 + percentComplete * 0.75) + "%"
                      });
                    }
                  }, false);
                  xhr.onreadystatechange = function(response) {
                    var blkRet;
                    if (xhr.readyState === 4 && xhr.status === 200 && xhr.responseText !== "") {
                      blkRet = JSON.parse(xhr.responseText);
                      return $.post("/api/image/add", {
                        "aim_id": _room_id,
                        "md5": md5
                      }, function() {
                        result_url = CDN_PREFIX + "/" + BLOCK_ID + "_" + md5 + "?imageView2/2/w/300";
                        $(".comment_submit_add_imgs").removeClass("hide");
                        $(".comment_submit_add_imgs").find(".comment_submit_add_img_more").before("<div class=\"comment_submit_add_img_one\">\n    <img class=\"comment_submit_add_img_one_img\" src=\"" + result_url + "\">\n    <div class=\"del_one\"></div>\n</div>");
                        $("#loading_" + loading_flag).animate({
                          "width": "100%"
                        }, 500, function() {
                          return $("#loading_" + loading_flag).remove();
                        });
                        return uploadNextFile();
                      });
                    }
                  };
                  startDate = new Date().getTime();
                  return xhr.send(formData);
                };
                size = file.size / 1024;
                console.log(size);
                if (size > 1025 && ((ref1 = file.type) !== "image/gif")) {
                  if (size > 20480) {
                    size_scale = (4 * 1024 / size).toFixed(3);
                  } else {
                    size_scale = (2 / (size / 1024)).toFixed(1);
                  }
                  console.log(size_scale);
                  return canvasDataURL(re, w, size_scale, function(base64Codes) {
                    var bl;
                    bl = convertBase64UrlToBlob(base64Codes);
                    file = bl;
                    console.log("===");
                    return Qiniu_upload(file, upload_token, _room_id + "_" + md5);
                  });
                } else {
                  return Qiniu_upload(file, upload_token, _room_id + "_" + md5);
                }
              });
            };
            return worker.postMessage(bin);
          };
          return reader.readAsDataURL(file);
        };
        if (file_lists.length >= 1) {
          return uploadFile(files[file_index]);
        }
      };
      $("body").on("change", "#msh_hollow_img_add_upload", handleFileSelect);
      return $("body").on("click", ".comment_submit_add_img_more_img,.comment_submit_add_img", function(evt) {
        var dom_img, obj;
        obj = document.getElementById('msh_hollow_img_add_upload');
        obj.outerHTML = obj.outerHTML;
        dom_img = $(this);
        current_dom_img = dom_img;
        console.log("click to add img");
        return $("#msh_hollow_img_add_upload").click();
      });
    }
  });

}).call(this);
