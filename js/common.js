"use strict";
/**
 * 共通関数
 */

/**
 * JSONかどうかを判定
 * @param {in} arg  : 引数
 * @returns true  : JSONである 
 * @returns false : JSONでない 
 */
function isJson(arg){
  arg = (typeof(arg) == "function") ? arg() : arg;
  if(typeof(arg) != "string"){return false;}
  try{arg = (!JSON) ? eval("(" + arg + ")") : JSON.parse(arg);return true;}catch(e){return false;}
}

/**
 * localStorageに値を保存する。
 * @param {in}  key   :　キー
 * @param {in}  val   :　値
 */
function setLocalItem(key, val){
  var chk_val = val;
  if ($.isPlainObject( chk_val )){
    /* 値が配列ならjsonに変換 */
    chk_val = JSON.stringify(chk_val);
  }
  localStorage.setItem(key, chk_val);
}

/**
 * localStorageに保存されている値を取得
 * @param {in} key  : キー 
 * @returns キーに対応する値
 */
function getLocalItem(key){
  var chk_val = localStorage.getItem(key);
  if (isJson(chk_val)){
    chk_val = JSON.parse(chk_val);
  }
  return chk_val;
}

/**
 * localStorageから指定されたキーを削除する
 * @param {in} key  : 削除するキー 
 */
function removeLocalItem(key){
  localStorage.removeItem(key);
}


/**
 * ログアウト処理を行う
 */
function logout(){
  bootbox.confirm({
    message: "ログアウトしますか？",
    buttons: {
      confirm: {
          label: 'ログアウト',
          className: 'btn-success'
      },
      cancel: {
          label: 'キャンセル',
          className: 'btn-danger'
      }
    },
    callback: function (result) {
      if (result){
        // ログイン情報を削除
        removeLocalItem('login_info');
        removeLocalItem('login_user_cd');
        // index.htmlを再読み込み
        location.href = "index.html";
      }
    }
  });  
}


/**
 * テンプレートを取得する
 * @param {in} file_name : ファイル名
 * @return テンプレートデータ
 */
function getTemplate(file_name)
{
    var result = $.ajax({
      type    : 'GET',
      url     : file_name,
      async   : false
    }).responseText;
    return result;
}

/**
 * 数値を0パディングする
 * @param {in} NUM  : 数値
 * @param {in} LEN  : 桁数
 */
function zeroPadding(NUM, LEN){
	return ( Array(LEN).join('0') + NUM ).slice( -LEN );
}


/**
 * パラメータを取得する
 * 
 * パラメータ名をキーとして連想配列に追加する。
 * @retval result パラメータ名をキーとした連想配列
 */
function getQueryString()
{
	if ( 1 < document.location.search.length )
	{
		// 最初の1文字 (?記号) を除いた文字列を取得する
		var query = document.location.search.substring(1);

		// クエリの区切り記号 (&) で文字列を配列に分割する
		var parameters = query.split('&');

		var result = new Object();
		for( var i = 0; i < parameters.length; i++ )
		{
			// パラメータ名とパラメータ値に分割する
			var element = parameters[i].split('=');
			var paramName = decodeURIComponent( element[0] );
			var paramValue = decodeURIComponent( element[1] );

			// パラメータ名をキーとして連想配列に追加する
			result[paramName] = decodeURIComponent( paramValue );
		}
		return result;
	}
	return null;
}

/**
 * 1つ前に戻る
 */
function goBack(){
  window.history.back(-1);
  return false;
}

/**
 * ログインユーザーCDを取得する
 */
function getLoginUserCD(){
  return getLocalItem('login_user_cd');
}

/**
 * ログインユーザーCDを設定する
 * @param {in} val  : ログインユーザーCD 
 */
function setLoginUserCD(val){
  setLocalItem('login_user_cd', val);
}