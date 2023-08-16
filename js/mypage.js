"use strict";
/**
 * マイページ画面
 */

// 表示対象となるユーザーCD
var tgt_user_cd = null;

/**
 * DOMContentLoadedイベントハンドラ
 */
window.addEventListener('DOMContentLoaded', function(){
	init();
});

/**
 * マイページ初期化処理
 */
function init(){
  // ユーザー成績一覧を取得する。
  var user_cd = getLoginUserCD();
  var service_result;
  service_result = boc_get_user_info_list({
    ope_user_cd : getLoginUserCD(),
    user_cd     : user_cd
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("成績データの取得に失敗しました。");
    return;
  }
  // 最初のユーザーデータを設定
  updateLoginScoreView(service_result.user_list[0]);

  // ユーザーの保有ポイントを取得
  var avaival_pt = 0;
  service_result = boc_get_total_avaival_point({
    user_cd : user_cd
  });
  if (service_result.err_code == BOC_NO_ERROR){
    avaival_pt = service_result.avaival_pt;
  }
  $("span#avaival_pt").html(avaival_pt);
}


/**
 * 成績管理に成績を反映する。
 * @param {in} cursor_index : 表示するユーザーリストのIndex
 */
function updateLoginScoreView(user_score){
  /* データを反映 */
  // タイトル画像
  $("img#title_img").attr("src", "img/" + user_score.rabking_img);
  // ユーザー名
  $("input#user_name").val(user_score.user_name);
  if (!tgt_user_cd){
    // メールアドレス
    $("input#user_email").val(user_score.login_cd);
  }
  // タイトル称号
  $("span#title_name").html(user_score.ranking_rank);
  // 投票回数
  $("span#vote_count").html(user_score.vote_history.length);
  // テーブルヘッダ◎
  $("span#h_mk1").html(user_score.vote_overview.year_ranking.mark1_hit + "/" + user_score.vote_history.length);
  // テーブルヘッダ〇
  $("span#h_mk2").html(user_score.vote_overview.year_ranking.mark2_hit + "/" + user_score.vote_history.length);
  // テーブルヘッダ▲
  $("span#h_mk3").html(user_score.vote_overview.year_ranking.mark3_hit + "/" + user_score.vote_history.length);
  // テーブルヘッダ☆
  $("span#h_mk4").html(user_score.vote_overview.year_ranking.mark4_hit + "/" + user_score.vote_history.length);
  // テーブルヘッダ穴
  $("span#h_mk5").html(user_score.vote_overview.year_ranking.mark5_hit + "/" + user_score.vote_history.length);
  // テーブルヘッダ消
  $("span#h_mk6").html(user_score.vote_overview.year_ranking.mark6_hit + "/" + user_score.vote_history.length);
  // 履歴詳細
  $("tbody#vote_history").empty();
  var tpl_history = getTemplate("/tpl_score_history_item.html");
  for(let i=0; i<user_score.vote_history.length; i++){
    var vote_info = user_score.vote_history[i];
    var add_item = tpl_history.replace(/{race_name}/g,  vote_info.race_name);
    add_item = add_item.replace(/{mk1_unum}/g,  (vote_info.mark1 && vote_info.mark1 > 0 ? vote_info.mark1 + ":" + vote_info.mark1_name : '') );
    add_item = add_item.replace(/{mk1_class}/g,  (vote_info.mark1_pt>0 ? 'hit-cell' : 'lost-cell') );
    add_item = add_item.replace(/{mk1_mark}/g,  (vote_info.mark1_pt>0 ? '当' : '×') );
    add_item = add_item.replace(/{mk2_unum}/g,  (vote_info.mark2 && vote_info.mark2 > 0 ? vote_info.mark2 + ":" + vote_info.mark2_name : '')  );
    add_item = add_item.replace(/{mk2_class}/g,  (vote_info.mark2_pt>0 ? 'hit-cell' : 'lost-cell') );
    add_item = add_item.replace(/{mk2_mark}/g,  (vote_info.mark2_pt>0 ? '当' : '×') );
    add_item = add_item.replace(/{mk3_unum}/g,  (vote_info.mark3 && vote_info.mark3 > 0 ? vote_info.mark3 + ":" + vote_info.mark3_name : '')  );
    add_item = add_item.replace(/{mk3_class}/g,  (vote_info.mark3_pt>0 ? 'hit-cell' : 'lost-cell') );
    add_item = add_item.replace(/{mk3_mark}/g,  (vote_info.mark3_pt>0 ? '当' : '×') );
    add_item = add_item.replace(/{mk4_unum}/g,  (vote_info.mark4 && vote_info.mark4 > 0 ? vote_info.mark4 + ":" + vote_info.mark4_name : '')  );
    add_item = add_item.replace(/{mk4_class}/g,  (vote_info.mark4_pt>0 ? 'hit-cell' : 'lost-cell') );
    add_item = add_item.replace(/{mk4_mark}/g,  (vote_info.mark4_pt>0 ? '当' : '×') );
    add_item = add_item.replace(/{mk5_unum}/g,  (vote_info.mark5 && vote_info.mark5 > 0 ? vote_info.mark5 + ":" + vote_info.mark5_name : '')  );
    add_item = add_item.replace(/{mk5_class}/g,  (vote_info.mark5_pt>0 ? 'hit-cell' : 'lost-cell') );
    add_item = add_item.replace(/{mk5_mark}/g,  (vote_info.mark5_pt>0 ? '当' : '×') );
    add_item = add_item.replace(/{mk6_unum}/g,  (vote_info.mark6 && vote_info.mark6 > 0 ? vote_info.mark6 + ":" + vote_info.mark6_name : '')  );
    add_item = add_item.replace(/{mk6_class}/g,  (vote_info.mark6_pt>0 ? 'hit-cell' : 'lost-cell') );
    add_item = add_item.replace(/{mk6_mark}/g,  (vote_info.mark6_pt>0 ? '当' : '×') );
    $(add_item).appendTo("tbody#vote_history");
  }
  // 履歴概要
  // pt
  $("div#pt_month").html((user_score.vote_overview.month_ranking ? user_score.vote_overview.month_ranking.pt : 0)+"pt");
  $("div#pt_year").html((user_score.vote_overview.year_ranking ? user_score.vote_overview.year_ranking.pt : 0)+"pt");
  $("div#pt_first_half").html((user_score.vote_overview.first_half_ranking ? user_score.vote_overview.first_half_ranking.pt : 0)+"pt");
  $("div#pt_last_half").html((user_score.vote_overview.last_half_ranking ? user_score.vote_overview.last_half_ranking.pt : 0)+"pt");
  // ◎
  $("div#mk1_month").html((user_score.vote_overview.month_ranking ? user_score.vote_overview.month_ranking.mark1_rate : 0)+"%");
  if (user_score.vote_overview.month_ranking && user_score.vote_overview.month_ranking.mark1_rate >= 60){
    $("div#mk1_month").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk1_month").css("background-color", "rgba(255,242,0,0)");
  }
  $("div#mk1_year").html((user_score.vote_overview.year_ranking ? user_score.vote_overview.year_ranking.mark1_rate : 0)+"%");
  if (user_score.vote_overview.year_ranking && user_score.vote_overview.year_ranking.mark1_rate >= 60){
    $("div#mk1_year").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk1_year").css("background-color", "rgba(255,242,0,0)");
  }
  $("div#mk1_first_half").html((user_score.vote_overview.first_half_ranking ? user_score.vote_overview.first_half_ranking.mark1_rate : 0)+"%");
  if (user_score.vote_overview.first_half_ranking && user_score.vote_overview.first_half_ranking.mark1_rate >= 60){
    $("div#mk1_first_half").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk1_first_half").css("background-color", "rgba(255,242,0,0)");
  }
  $("div#mk1_last_half").html((user_score.vote_overview.last_half_ranking ? user_score.vote_overview.last_half_ranking.mark1_rate : 0)+"%");
  if (user_score.vote_overview.last_half_ranking && user_score.vote_overview.last_half_ranking.mark1_rate >= 60){
    $("div#mk1_last_half").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk1_last_half").css("background-color", "rgba(255,242,0,0)");
  }
  // 〇
  $("div#mk2_month").html((user_score.vote_overview.month_ranking ? user_score.vote_overview.month_ranking.mark2_rate : 0)+"%");
  $("div#mk2_year").html((user_score.vote_overview.year_ranking ? user_score.vote_overview.year_ranking.mark2_rate : 0)+"%");
  $("div#mk2_first_half").html((user_score.vote_overview.first_half_ranking ? user_score.vote_overview.first_half_ranking.mark2_rate : 0)+"%");
  $("div#mk2_last_half").html((user_score.vote_overview.last_half_ranking ? user_score.vote_overview.last_half_ranking.mark2_rate : 0)+"%");
  // ▲
  $("div#mk3_month").html((user_score.vote_overview.month_ranking ? user_score.vote_overview.month_ranking.mark3_rate : 0)+"%");
  $("div#mk3_year").html((user_score.vote_overview.year_ranking ? user_score.vote_overview.year_ranking.mark3_rate : 0)+"%");
  $("div#mk3_first_half").html((user_score.vote_overview.first_half_ranking ? user_score.vote_overview.first_half_ranking.mark3_rate : 0)+"%");
  $("div#mk3_last_half").html((user_score.vote_overview.last_half_ranking ? user_score.vote_overview.last_half_ranking.mark3_rate : 0)+"%");
  // ☆
  $("div#mk4_month").html((user_score.vote_overview.month_ranking ? user_score.vote_overview.month_ranking.mark4_rate : 0)+"%");
  $("div#mk4_year").html((user_score.vote_overview.year_ranking ? user_score.vote_overview.year_ranking.mark4_rate : 0)+"%");
  $("div#mk4_first_half").html((user_score.vote_overview.first_half_ranking ? user_score.vote_overview.first_half_ranking.mark4_rate :0)+"%");
  $("div#mk4_last_half").html((user_score.vote_overview.last_half_ranking ? user_score.vote_overview.last_half_ranking.mark4_rate : 0)+"%");
  // 穴
  $("div#mk5_month").html((user_score.vote_overview.month_ranking ? user_score.vote_overview.month_ranking.mark5_rate : 0)+"%");
  if (user_score.vote_overview.month_ranking && user_score.vote_overview.month_ranking.mark5_rate >= 30){
    $("div#mk5_month").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk5_month").css("background-color", "rgba(255,242,0,0)");
  }
  $("div#mk5_year").html((user_score.vote_overview.year_ranking ? user_score.vote_overview.year_ranking.mark5_rate : 0)+"%");
  if (user_score.vote_overview.year_ranking && user_score.vote_overview.year_ranking.mark5_rate >= 30){
    $("div#mk5_year").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk5_year").css("background-color", "rgba(255,242,0,0)");
  }
  $("div#mk5_first_half").html((user_score.vote_overview.first_half_ranking ? user_score.vote_overview.first_half_ranking.mark5_rate : 0)+"%");
  if (user_score.vote_overview.first_half_ranking && user_score.vote_overview.first_half_ranking.mark5_rate >= 30){
    $("div#mk5_first_half").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk5_first_half").css("background-color", "rgba(255,242,0,0)");
  }
  $("div#mk5_last_half").html((user_score.vote_overview.last_half_ranking ? user_score.vote_overview.last_half_ranking.mark5_rate : 0)+"%");
  if (user_score.vote_overview.last_half_ranking && user_score.vote_overview.last_half_ranking.mark5_rate >= 30){
    $("div#mk5_last_half").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk5_last_half").css("background-color", "rgba(255,242,0,0)");
  }
  // 消
  $("div#mk6_month").html((user_score.vote_overview.month_ranking ? user_score.vote_overview.month_ranking.mark6_rate : 0)+"%");
  if (user_score.vote_overview.month_ranking && user_score.vote_overview.month_ranking.mark6_rate >= 80){
    $("div#mk6_month").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk6_month").css("background-color", "rgba(255,242,0,0)");
  }
  $("div#mk6_year").html((user_score.vote_overview.year_ranking ? user_score.vote_overview.year_ranking.mark6_rate : 0)+"%");
  if (user_score.vote_overview.year_ranking && user_score.vote_overview.year_ranking.mark6_rate >= 80){
    $("div#mk6_year").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk6_year").css("background-color", "rgba(255,242,0,0)");
  }
  $("div#mk6_first_half").html((user_score.vote_overview.first_half_ranking ? user_score.vote_overview.first_half_ranking.mark6_rate : 0)+"%");
  if (user_score.vote_overview.first_half_ranking && user_score.vote_overview.first_half_ranking.mark6_rate >= 80){
    $("div#mk6_first_half").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk6_first_half").css("background-color", "rgba(255,242,0,0)");
  }
  $("div#mk6_last_half").html((user_score.vote_overview.last_half_ranking ? user_score.vote_overview.last_half_ranking.mark6_rate : 0)+"%");
  if (user_score.vote_overview.last_half_ranking && user_score.vote_overview.last_half_ranking.mark6_rate >= 80){
    $("div#mk6_last_half").css("background-color", "rgb(255,242,0)");
  }
  else{
    $("div#mk6_last_half").css("background-color", "rgba(255,242,0,0)");
  }
  // 単勝回収率
  $("div#p1_month").html((user_score.vote_overview.month_ranking ? user_score.vote_overview.month_ranking.pay1_rate : 0)+"%");
  $("div#p1_year").html((user_score.vote_overview.year_ranking ? user_score.vote_overview.year_ranking.pay1_rate : 0)+"%");
  $("div#p1_first_half").html((user_score.vote_overview.first_half_ranking ? user_score.vote_overview.first_half_ranking.pay1_rate : 0)+"%");
  $("div#p1_last_half").html((user_score.vote_overview.last_half_ranking ? user_score.vote_overview.last_half_ranking.pay1_rate : 0)+"%");
  // 複勝回収率
  $("div#p2_month").html((user_score.vote_overview.month_ranking ? user_score.vote_overview.month_ranking.pay2_rate : 0)+"%");
  $("div#p2_year").html((user_score.vote_overview.year_ranking ? user_score.vote_overview.year_ranking.pay2_rate : 0)+"%");
  $("div#p2_first_half").html((user_score.vote_overview.first_half_ranking ? user_score.vote_overview.first_half_ranking.pay2_rate : 0)+"%");
  $("div#p2_last_half").html((user_score.vote_overview.last_half_ranking ? user_score.vote_overview.last_half_ranking.pay2_rate : 0)+"%");

}


///////////////////////////////////////////////
// イベントハンドラ
//

/**
 * マイページ編集ボタンクリックイベント
 */
function onClickedMyPageEdit(){
  window.location.href = "/myedit.html";
}