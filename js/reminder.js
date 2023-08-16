"use strict";
/**
 * リマインダー画面
 */

/**
 * リマインダー処理を行う
 */
function reminder(){
  /* 入力パラメータを取得 */
  var user_email = $("input#user_email").val();
  /* リマインダー処理 */
  var service_result = boc_reminder(user_email);
  if (service_result.err_code == BOC_INVALID_LOGIN_CD){
    bootbox.alert("ご入力頂いたメールアドレスでのご登録はありません。");
    return;
  }
  else if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("パスワードの送信に失敗しました。");
    return;
  }
  /* メッセージ表示 */
  bootbox.alert({
    title : 'パスワード送信',
    closeButton: false,
    message : '入力されたメールアドレスにパスワードを送信しました。',
    callback: function (){
      // 認証画面に遷移
      location.href = "/login.html";
    }
  });
}