"use strict";
/**
 * マイページ編集画面
 */

 var login_info;

/**
 * DOMContentLoadedイベントハンドラ
 */
window.addEventListener('DOMContentLoaded', function(){
	init();
});

/**
 * 初期化処理
 */
function init(){
  /* ユーザー情報を取得する */
  var service_result = boc_get_user_info({
    user_cd : getLoginUserCD()
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("ユーザー情報の取得に失敗しました。");
    return;
  }
  /* データを反映 */
  $("input#user_name").val(service_result.user_info.user_name);
  $("input#user_email").val(service_result.user_info.login_cd);
  $("input#user_passwd").val(service_result.user_info.login_passwd);
}

/////////////////////////////////////
// イベントハンドラ
//

/**
 * ユーザー情報を更新する。
 */
function onClickedUpdateLoginUser(){
  var user_name = $("input#user_name").val();
  var user_email = $("input#user_email").val();
  var user_passwd = $("input#user_passwd").val();

  // ユーザー情報を更新
  var update_info = {
    user_cd       : getLoginUserCD(),
    user_name     : user_name,
    login_cd      : user_email,
    login_passwd  : user_passwd
  };
  var service_result = boc_regist_user(update_info);
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("ユーザー情報の更新に失敗しました。");
    return;
  }
  // 更新メッセージを表示
  bootbox.alert("ユーザー情報を更新しました。",function(){
    location.href = "/mypage.html";
  });

}
