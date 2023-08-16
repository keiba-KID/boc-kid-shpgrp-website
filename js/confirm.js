"use strict";
/**
 * ユーザー登録認証画面
 */
function regist(){
  // 認証番号チェック
  var save_confirm_num = getLocalItem('confirm_number');
  var chk_confirm_num = $("input#confirm_number").val();
  if (save_confirm_num != chk_confirm_num){
    bootbox.alert("認証番号が違います。");
    return;
  }

  // ユーザー登録APIコール
  var regist_info = getLocalItem('regist_info');
  var service_result = boc_regist_user(regist_info);
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("ユーザーの新規登録に失敗しました。");
    return;
  }

  // login_infoをlocalStoageに保存
  setLoginUserCD(service_result.user_info.user_cd);

  // トップ画面に遷移
  bootbox.alert({
    title : 'ユーザー登録完了',
    closeButton: false,
    message : 'ご登録ありがとうございます。\n引き続きBOCコミュニティをお楽しみください。',
    callback: function (){
      // 認証画面に遷移
      location.href = "/index.html";
    }

  });
}