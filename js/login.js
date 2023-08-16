"use strict";
/**
 * ログイン画面
 */

/**
 * ログイン処理を行う
 */
function login(){
  var user_email = $("input#user-email").val();
  var user_passwd = $("input#user-passwd").val();

  /* 入力チェックを行う */
  if (!user_email){
    bootbox.alert("IDまたはメールアドレスが未入力です。");
    return;
  }
  if (!user_passwd){
    bootbox.alert("パスワードが未入力です。");
    return;
  }
  /* ログイン処理を行う */
  var req_param = {
    login_id      : user_email,
    login_passwd  : user_passwd
  };
  var service_result = boc_login(req_param);
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("IDまたはパスワードが異なります。");
    return;
  }
  /* ログイン成功ならuser_cdをlocalStorageに保存 */
  setLoginUserCD(service_result.user_info.user_cd);
  location.href = "index.html";
}