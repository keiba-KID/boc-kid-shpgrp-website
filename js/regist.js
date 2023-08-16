"use strict";
/**
 * ユーザー登録画面
 */
function confirm(){
  // 入力項目を取得
  var user_name = $("input#user_name").val();
  var user_email = $("input#user_email").val();
  var user_passwd = $("input#user_passwd").val();
  var regist_info = {
    user_name     : user_name,
    login_type    : 'email',
    login_cd      : user_email,
    login_passwd  : user_passwd,
    user_type     : 'user',
    user_rank     : 1
  };
  // 入力項目を一旦localStorageに退避
  setLocalItem('regist_info', regist_info);

  // 認証番号発行APIをコール
  var service_result = boc_send_user_regist_confirm({
    login_type  : 'email',
    login_cd    : user_email,
    user_name   : user_name
  });
  if (service_result.err_code == BOC_INVALID_LOGIN_CD){
    bootbox.alert("既に入力されたメールアドレスは使用されています。");
    return;
  }
  else if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("認証番号の取得に失敗しました。");
    return;
  }
  // 認証番号をlocalStorageに保存
  setLocalItem('confirm_number', service_result.confirm_number);
  bootbox.alert({
    title : '認証番号送信完了',
    closeButton: false,
    message : '入力されたメールアドレスに認証番号を送信しました。',
    callback: function (){
      // 認証画面に遷移
      location.href = "/confirm.html";
    }
  });
}