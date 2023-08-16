"use strict";
/**
 * HOME画面
 */

/* 各種ランキングデータ */
var current_rank_month = 1;
var pt_month_ranking_list = null;
var pt_year_ranking_list = null;
var pt_first_half_ranking_list = null;
var pt_last_half_ranking_list = null;

var mk1_month_ranking_list = null;
var mk1_year_ranking_list = null;
var mk1_first_half_ranking_list = null;
var mk1_last_half_ranking_list = null;

var p1_month_ranking_list = null;
var p1_year_ranking_list = null;
var p1_first_half_ranking_list = null;
var p1_last_half_ranking_list = null;

var p2_month_ranking_list = null;
var p2_year_ranking_list = null;
var p2_first_half_ranking_list = null;
var p2_last_half_ranking_list = null;

/* ユーザー成績リスト */
var current_cursor_index = 0;
var user_score_list = null;
var user_score_user_cds = null;


 /**
 * DOMContentLoadedイベントハンドラ
 */
window.addEventListener('DOMContentLoaded', function(){
	init();
});

/**
 * HOME画面初期化処理
 */
function init(){
  // デフォルトは管理者タブを非表示
  $(".for_user").css("display", "none");
  $(".for_staff").css("display", "none");
  $(".for_admin").css("display", "none");
  $(".for_superuser").css("display", "none");

  // 自動ログイン処理
  var user_cd = getLoginUserCD();
  if (user_cd){
    var check_result = boc_check_use_function({
      func_name   : BOC_USE_VOTE,
      ope_user_cd : user_cd
    });
    if (check_result.err_code == BOC_NO_ERROR){
      var service_result = boc_get_public_user_info({
        user_cd : user_cd
      });
      if (service_result.err_code == BOC_NO_ERROR){
        $("span#login_user_name").html(service_result.user_info.user_name);
        $(".for_user").css("display", "block");
        $(".for_guest").css("display", "none");
      }
    }
    else{
      /* システムバージョンアップにつき、再度ログインさせる */
      bootbox.alert('システムがバージョンアップされています。再度ログイン願います',function(){
        // ログイン情報を削除
        removeLocalItem('login_info');
        removeLocalItem('login_user_cd');
        location.href = 'login.html';
        return;
      });
    }

    /* superuser権限チェック*/
    var check_result = boc_check_use_function({
      func_name   : BOC_USE_USER_MANAGE,
      ope_user_cd : user_cd
    });
    if (check_result.err_code == BOC_NO_ERROR){
      $(".for_staff").css("display", "block");
      $(".for_admin").css("display", "block");
      $(".for_superuser").css("display", "block");
    }

    /* 管理者権限チェック */
    var check_result = boc_check_use_function({
      func_name   : BOC_USE_SCORE_MANAGE,
      ope_user_cd : user_cd
    });
    if (check_result.err_code == BOC_NO_ERROR){
      $(".for_staff").css("display", "block");
      $(".for_admin").css("display", "block");
    }

    /* スタッフ権限チェック */
    var check_result = boc_check_use_function({
      func_name   : BOC_USE_RACE_MANAGE,
      ope_user_cd : user_cd
    });
    if (check_result.err_code == BOC_NO_ERROR){
      $(".for_staff").css("display", "block");
    }
  }

  // Homeタブを初期化
  initHomeTab();
  // ランキングタブ初期化
  initRankingTab();

  var check_result = boc_check_use_function({
    func_name   : BOC_USE_VOTE,
    ope_user_cd : user_cd
  });
  if (check_result.err_code == BOC_NO_ERROR){
    // 予選タブ初期化
    initVoteTab();
  }

  var check_result = boc_check_use_function({
    func_name   : BOC_USE_RACE_MANAGE,
    ope_user_cd : user_cd
  });
  if (check_result.err_code == BOC_NO_ERROR){
    // レース管理初期化
    initRaceManager();
  }

  var check_result = boc_check_use_function({
    func_name   : BOC_USE_SCORE_MANAGE,
    ope_user_cd : user_cd
  });
  if (check_result.err_code == BOC_NO_ERROR){
    // 成績管理初期化
    initScoreTab();
  }

  var check_result = boc_check_use_function({
    func_name   : BOC_USE_USER_MANAGE,
    ope_user_cd : user_cd
  });
  if (check_result.err_code == BOC_NO_ERROR){
    // ユーザ管理の初期化
    initUserTab()
  }

}

/**
 * ホームタブを初期化する
 */
function initHomeTab(){
  /* 各種ランキングデータを取得 */
  // ポイント月間
  var service_result = boc_get_ranking_list({
    ranking_type  : BOC_POINT_RANKING,
    sum_type      : BOC_RANKING_MONTH
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  current_rank_month = service_result.month;
  pt_month_ranking_list = service_result.ranking_list;
  // ポイント年間
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_POINT_RANKING,
    sum_type      : BOC_RANKING_YEAR
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  pt_year_ranking_list = service_result.ranking_list;
  // ポイント上半期
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_POINT_RANKING,
    sum_type      : BOC_RANKING_FIRST_HALF
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  pt_first_half_ranking_list = service_result.ranking_list;
  // ポイント下半期
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_POINT_RANKING,
    sum_type      : BOC_RANKING_LAST_HALF
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  pt_last_half_ranking_list = service_result.ranking_list;

  // ◎的中率月間
  var service_result = boc_get_ranking_list({
    ranking_type  : BOC_HONMEI_RANKING,
    sum_type      : BOC_RANKING_MONTH
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  mk1_month_ranking_list = service_result.ranking_list;
  // ◎的中率年間
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_HONMEI_RANKING,
    sum_type      : BOC_RANKING_YEAR
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  mk1_year_ranking_list = service_result.ranking_list;
  // ◎的中率上半期
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_HONMEI_RANKING,
    sum_type      : BOC_RANKING_FIRST_HALF
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  mk1_first_half_ranking_list = service_result.ranking_list;
  // ◎的中率下半期
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_HONMEI_RANKING,
    sum_type      : BOC_RANKING_LAST_HALF
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  mk1_last_half_ranking_list = service_result.ranking_list;

  // 単勝回収率月間
  var service_result = boc_get_ranking_list({
    ranking_type  : BOC_TANSHO_RANKING,
    sum_type      : BOC_RANKING_MONTH
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  p1_month_ranking_list = service_result.ranking_list;
  // 単勝回収率年間
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_TANSHO_RANKING,
    sum_type      : BOC_RANKING_YEAR
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  p1_year_ranking_list = service_result.ranking_list;
  // 単勝回収率上半期
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_TANSHO_RANKING,
    sum_type      : BOC_RANKING_FIRST_HALF
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  p1_first_half_ranking_list = service_result.ranking_list;
  // 単勝回収率下半期
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_TANSHO_RANKING,
    sum_type      : BOC_RANKING_LAST_HALF
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  p1_last_half_ranking_list = service_result.ranking_list;

  // 複勝回収率月間
  var service_result = boc_get_ranking_list({
    ranking_type  : BOC_FUKUSHO_RANKING,
    sum_type      : BOC_RANKING_MONTH
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  p2_month_ranking_list = service_result.ranking_list;
  // 単勝回収率年間
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_FUKUSHO_RANKING,
    sum_type      : BOC_RANKING_YEAR
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  p2_year_ranking_list = service_result.ranking_list;
  // 単勝回収率上半期
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_FUKUSHO_RANKING,
    sum_type      : BOC_RANKING_FIRST_HALF
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  p2_first_half_ranking_list = service_result.ranking_list;
  // 単勝回収率下半期
  service_result = boc_get_ranking_list({
    ranking_type  : BOC_FUKUSHO_RANKING,
    sum_type      : BOC_RANKING_LAST_HALF
  });
  if (service_result.err_code != BOC_NO_ERROR){
  }
  p2_last_half_ranking_list = service_result.ranking_list;

  /* 各種ランキングを更新 */
  /* ポイント月間 */
  $("span#tgt_pt_rank_month").html(current_rank_month);
  if (pt_month_ranking_list.length >= 1){
    $("span#pt_month_rank1_name").html(pt_month_ranking_list[0]['user_name']);
    $("span#pt_month_rank1_count").html(pt_month_ranking_list[0]['v_count']+"回");
    $("span#pt_month_rank1_point").html(pt_month_ranking_list[0]['pt']+"pt");
  }
  if (pt_month_ranking_list.length >= 2){
    $("span#pt_month_rank2_name").html(pt_month_ranking_list[1]['user_name']);
    $("span#pt_month_rank2_count").html(pt_month_ranking_list[1]['v_count']+"回");
    $("span#pt_month_rank2_point").html(pt_month_ranking_list[1]['pt']+"pt");
  }
  if (pt_month_ranking_list.length >= 3){
    $("span#pt_month_rank3_name").html(pt_month_ranking_list[2]['user_name']);
    $("span#pt_month_rank3_count").html(pt_month_ranking_list[2]['v_count']+"回");
    $("span#pt_month_rank3_point").html(pt_month_ranking_list[2]['pt']+"pt");
  }
  /* ポイント年間 */
  if (pt_year_ranking_list.length >= 1){
    $("span#pt_year_rank1_name").html(pt_year_ranking_list[0]['user_name']);
    $("span#pt_year_rank1_count").html(pt_year_ranking_list[0]['v_count']+"回");
    $("span#pt_year_rank1_point").html(pt_year_ranking_list[0]['pt']+"pt");
  }
  if (pt_year_ranking_list.length >= 2){
    $("span#pt_year_rank2_name").html(pt_year_ranking_list[1]['user_name']);
    $("span#pt_year_rank2_count").html(pt_year_ranking_list[1]['v_count']+"回");
    $("span#pt_year_rank2_point").html(pt_year_ranking_list[1]['pt']+"pt");
  }
  if (pt_year_ranking_list.length >= 3){
    $("span#pt_year_rank3_name").html(pt_year_ranking_list[2]['user_name']);
    $("span#pt_year_rank3_count").html(pt_year_ranking_list[2]['v_count']+"回");
    $("span#pt_year_rank3_point").html(pt_year_ranking_list[2]['pt']+"pt");
  }
  /* ポイント半期 */
  var tgt_half = "上";
  var tgt_pt_list = pt_first_half_ranking_list;
  if (current_rank_month>6){
    tgt_half = "下";
    tgt_pt_list = pt_last_half_ranking_list;
  } 
  $("span#pt_half_rank").html(tgt_half);
  if (tgt_pt_list.length >= 1){
    $("span#pt_half_rank1_name").html(tgt_pt_list[0]['user_name']);
    $("span#pt_half_rank1_count").html(tgt_pt_list[0]['v_count']+"回");
    $("span#pt_half_rank1_point").html(tgt_pt_list[0]['pt']+"pt");
  }
  if (tgt_pt_list.length >= 2){
    $("span#pt_half_rank2_name").html(tgt_pt_list[1]['user_name']);
    $("span#pt_half_rank2_count").html(tgt_pt_list[1]['v_count']+"回");
    $("span#pt_half_rank2_point").html(tgt_pt_list[1]['pt']+"pt");
  }
  if (tgt_pt_list.length >= 3){
    $("span#pt_half_rank3_name").html(tgt_pt_list[2]['user_name']);
    $("span#pt_half_rank3_count").html(tgt_pt_list[2]['v_count']+"回");
    $("span#pt_half_rank3_point").html(tgt_pt_list[2]['pt']+"pt");
  }

  /* ◎的中率月間 */
  $("span#tgt_mk1_rank_month").html(current_rank_month);
  if (mk1_month_ranking_list.length >= 1){
    $("span#mk1_month_rank1_name").html(mk1_month_ranking_list[0]['user_name']);
    $("span#mk1_month_rank1_count").html(mk1_month_ranking_list[0]['v_count']+"回");
    $("span#mk1_month_rank1_rate").html(mk1_month_ranking_list[0]['mark1_rate']+"%");
  }
  if (mk1_month_ranking_list.length >= 2){
    $("span#mk1_month_rank2_name").html(mk1_month_ranking_list[1]['user_name']);
    $("span#mk1_month_rank2_count").html(mk1_month_ranking_list[1]['v_count']+"回");
    $("span#mk1_month_rank2_rate").html(mk1_month_ranking_list[1]['mark1_rate']+"%");
  }
  if (mk1_month_ranking_list.length >= 3){
    $("span#mk1_month_rank3_name").html(mk1_month_ranking_list[2]['user_name']);
    $("span#mk1_month_rank3_count").html(mk1_month_ranking_list[2]['v_count']+"回");
    $("span#mk1_month_rank3_rate").html(mk1_month_ranking_list[2]['mark1_rate']+"%");
  }
  /* ◎的中率年間 */
  if (mk1_year_ranking_list.length >= 1){
    $("span#mk1_year_rank1_name").html(mk1_year_ranking_list[0]['user_name']);
    $("span#mk1_year_rank1_count").html(mk1_year_ranking_list[0]['v_count']+"回");
    $("span#mk1_year_rank1_rate").html(mk1_year_ranking_list[0]['mark1_rate']+"%");
  }
  if (mk1_year_ranking_list.length >= 2){
    $("span#mk1_year_rank2_name").html(mk1_year_ranking_list[1]['user_name']);
    $("span#mk1_year_rank2_count").html(mk1_year_ranking_list[1]['v_count']+"回");
    $("span#mk1_year_rank2_rate").html(mk1_year_ranking_list[1]['mark1_rate']+"%");
  }
  if (mk1_year_ranking_list.length >= 3){
    $("span#mk1_year_rank3_name").html(mk1_year_ranking_list[2]['user_name']);
    $("span#mk1_year_rank3_count").html(mk1_year_ranking_list[2]['v_count']+"回");
    $("span#mk1_year_rank3_rate").html(mk1_year_ranking_list[2]['mark1_rate']+"%");
  }
  /* ◎的中率半期 */
  var tgt_half = "上";
  var tgt_pt_list = mk1_first_half_ranking_list;
  if (current_rank_month>6){
    tgt_half = "下";
    tgt_pt_list = mk1_last_half_ranking_list;
  } 
  $("span#mk1_half_rank").html(tgt_half);
  if (tgt_pt_list.length >= 1){
    $("span#mk1_half_rank1_name").html(tgt_pt_list[0]['user_name']);
    $("span#mk1_half_rank1_count").html(tgt_pt_list[0]['v_count']+"回");
    $("span#mk1_half_rank1_rate").html(tgt_pt_list[0]['mark1_rate']+"%");
  }
  if (tgt_pt_list.length >= 2){
    $("span#mk1_half_rank2_name").html(tgt_pt_list[1]['user_name']);
    $("span#mk1_half_rank2_count").html(tgt_pt_list[1]['v_count']+"回");
    $("span#mk1_half_rank2_rate").html(tgt_pt_list[1]['mark1_rate']+"%");
  }
  if (tgt_pt_list.length >= 3){
    $("span#mk1_half_rank3_name").html(tgt_pt_list[2]['user_name']);
    $("span#mk1_half_rank3_count").html(tgt_pt_list[2]['v_count']+"回");
    $("span#mk1_half_rank3_rate").html(tgt_pt_list[2]['mark1_rate']+"%");
  }

  /* 単勝回収率月間 */
  $("span#tgt_p1_rank_month").html(current_rank_month);
  if (p1_month_ranking_list.length >= 1){
    $("span#p1_month_rank1_name").html(p1_month_ranking_list[0]['user_name']);
    $("span#p1_month_rank1_count").html(p1_month_ranking_list[0]['v_count']+"回");
    $("span#p1_month_rank1_rate").html(p1_month_ranking_list[0]['pay1_rate']+"%");
  }
  if (p1_month_ranking_list.length >= 2){
    $("span#p1_month_rank2_name").html(p1_month_ranking_list[1]['user_name']);
    $("span#p1_month_rank2_count").html(p1_month_ranking_list[1]['v_count']+"回");
    $("span#p1_month_rank2_rate").html(p1_month_ranking_list[1]['pay1_rate']+"%");
  }
  if (p1_month_ranking_list.length >= 3){
    $("span#p1_month_rank3_name").html(p1_month_ranking_list[2]['user_name']);
    $("span#p1_month_rank3_count").html(p1_month_ranking_list[2]['v_count']+"回");
    $("span#p1_month_rank3_rate").html(p1_month_ranking_list[2]['pay1_rate']+"%");
  }
  /* 単勝回収率年間 */
  if (p1_year_ranking_list.length >= 1){
    $("span#p1_year_rank1_name").html(p1_year_ranking_list[0]['user_name']);
    $("span#p1_year_rank1_count").html(p1_year_ranking_list[0]['v_count']+"回");
    $("span#p1_year_rank1_rate").html(p1_year_ranking_list[0]['pay1_rate']+"%");
  }
  if (p1_year_ranking_list.length >= 2){
    $("span#p1_year_rank2_name").html(p1_year_ranking_list[1]['user_name']);
    $("span#p1_year_rank2_count").html(p1_year_ranking_list[1]['v_count']+"回");
    $("span#p1_year_rank2_rate").html(p1_year_ranking_list[1]['pay1_rate']+"%");
  }
  if (p1_year_ranking_list.length >= 3){
    $("span#p1_year_rank3_name").html(p1_year_ranking_list[2]['user_name']);
    $("span#p1_year_rank3_count").html(p1_year_ranking_list[2]['v_count']+"回");
    $("span#p1_year_rank3_rate").html(p1_year_ranking_list[2]['pay1_rate']+"%");
  }
  /* 単勝回収率半期 */
  var tgt_half = "上";
  var tgt_pt_list = p1_first_half_ranking_list;
  if (current_rank_month>6){
    tgt_half = "下";
    tgt_pt_list = p1_last_half_ranking_list;
  } 
  $("span#p1_half_rank").html(tgt_half);
  if (tgt_pt_list.length >= 1){
    $("span#p1_half_rank1_name").html(tgt_pt_list[0]['user_name']);
    $("span#p1_half_rank1_count").html(tgt_pt_list[0]['v_count']+"回");
    $("span#p1_half_rank1_rate").html(tgt_pt_list[0]['pay1_rate']+"%");
  }
  if (tgt_pt_list.length >= 2){
    $("span#p1_half_rank2_name").html(tgt_pt_list[1]['user_name']);
    $("span#p1_half_rank2_count").html(tgt_pt_list[1]['v_count']+"回");
    $("span#p1_half_rank2_rate").html(tgt_pt_list[1]['pay1_rate']+"%");
  }
  if (tgt_pt_list.length >= 3){
    $("span#p1_half_rank3_name").html(tgt_pt_list[2]['user_name']);
    $("span#p1_half_rank3_count").html(tgt_pt_list[2]['v_count']+"回");
    $("span#p1_half_rank3_rate").html(tgt_pt_list[2]['pay1_rate']+"%");
  }

  /* 複勝回収率月間 */
  $("span#tgt_p2_rank_month").html(current_rank_month);
  if (p2_month_ranking_list.length >= 1){
    $("span#p2_month_rank1_name").html(p2_month_ranking_list[0]['user_name']);
    $("span#p2_month_rank1_count").html(p2_month_ranking_list[0]['v_count']+"回");
    $("span#p2_month_rank1_rate").html(p2_month_ranking_list[0]['pay2_rate']+"%");
  }
  if (p2_month_ranking_list.length >= 2){
    $("span#p2_month_rank2_name").html(p2_month_ranking_list[1]['user_name']);
    $("span#p2_month_rank2_count").html(p2_month_ranking_list[1]['v_count']+"回");
    $("span#p2_month_rank2_rate").html(p2_month_ranking_list[1]['pay2_rate']+"%");
  }
  if (p2_month_ranking_list.length >= 3){
    $("span#p2_month_rank3_name").html(p2_month_ranking_list[2]['user_name']);
    $("span#p2_month_rank3_count").html(p2_month_ranking_list[2]['v_count']+"回");
    $("span#p2_month_rank3_rate").html(p2_month_ranking_list[2]['pay2_rate']+"%");
  }
  /* 複勝回収率年間 */
  if (p2_year_ranking_list.length >= 1){
    $("span#p2_year_rank1_name").html(p2_year_ranking_list[0]['user_name']);
    $("span#p2_year_rank1_count").html(p2_year_ranking_list[0]['v_count']+"回");
    $("span#p2_year_rank1_rate").html(p2_year_ranking_list[0]['pay2_rate']+"%");
  }
  if (p2_year_ranking_list.length >= 2){
    $("span#p2_year_rank2_name").html(p2_year_ranking_list[1]['user_name']);
    $("span#p2_year_rank2_count").html(p2_year_ranking_list[1]['v_count']+"回");
    $("span#p2_year_rank2_rate").html(p2_year_ranking_list[1]['pay2_rate']+"%");
  }
  if (p2_year_ranking_list.length >= 3){
    $("span#p2_year_rank3_name").html(p2_year_ranking_list[2]['user_name']);
    $("span#p2_year_rank3_count").html(p2_year_ranking_list[2]['v_count']+"回");
    $("span#p2_year_rank3_rate").html(p2_year_ranking_list[2]['pay2_rate']+"%");
  }
  /* 複勝回収率半期 */
  var tgt_half = "上";
  var tgt_pt_list = p2_first_half_ranking_list;
  if (current_rank_month>6){
    tgt_half = "下";
    tgt_pt_list = p2_last_half_ranking_list;
  } 
  $("span#p2_half_rank").html(tgt_half);
  if (tgt_pt_list.length >= 1){
    $("span#p2_half_rank1_name").html(tgt_pt_list[0]['user_name']);
    $("span#p2_half_rank1_count").html(tgt_pt_list[0]['v_count']+"回");
    $("span#p2_half_rank1_rate").html(tgt_pt_list[0]['pay2_rate']+"%");
  }
  if (tgt_pt_list.length >= 2){
    $("span#p2_half_rank2_name").html(tgt_pt_list[1]['user_name']);
    $("span#p2_half_rank2_count").html(tgt_pt_list[1]['v_count']+"回");
    $("span#p2_half_rank2_rate").html(tgt_pt_list[1]['pay2_rate']+"%");
  }
  if (tgt_pt_list.length >= 3){
    $("span#p2_half_rank3_name").html(tgt_pt_list[2]['user_name']);
    $("span#p2_half_rank3_count").html(tgt_pt_list[2]['v_count']+"回");
    $("span#p2_half_rank3_rate").html(tgt_pt_list[2]['pay2_rate']+"%");
  }

}

/**
 * ランキングタブを初期化する
 */
function initRankingTab(){
  /* テーブルデータを設定 */
  var tpl = getTemplate("/tpl_ranking_item.html");
  /* 月間ランキングを反映 */
  $("tbody#month_ranking").empty();
  for(let i=0; i<pt_month_ranking_list.length; i++){
    var rank_info = pt_month_ranking_list[i];
    var rank = i+1;
    var add_record = tpl.replace(/{rank}/g, rank);
    add_record = add_record.replace(/{user_name}/g, rank_info.user_name);
    add_record = add_record.replace(/{vote_count}/g, rank_info.v_count);
    add_record = add_record.replace(/{pt}/g, rank_info.pt);
    add_record = add_record.replace(/{mark1_rate}/g, rank_info.mark1_rate);
    add_record = add_record.replace(/{mark2_rate}/g, rank_info.mark2_rate);
    add_record = add_record.replace(/{mark3_rate}/g, rank_info.mark3_rate);
    add_record = add_record.replace(/{mark4_rate}/g, rank_info.mark4_rate);
    add_record = add_record.replace(/{mark5_rate}/g, rank_info.mark5_rate);
    add_record = add_record.replace(/{mark6_rate}/g, rank_info.mark6_rate);
    add_record = add_record.replace(/{pay1_rate}/g, rank_info.pay1_rate);
    add_record = add_record.replace(/{pay2_rate}/g, rank_info.pay2_rate);
    $(add_record).appendTo("tbody#month_ranking");
  }
  /* 年間ランキングを反映 */
  $("tbody#year_ranking").empty();
  for(let i=0; i<pt_year_ranking_list.length; i++){
    var rank_info = pt_year_ranking_list[i];
    var rank = i+1;
    var add_record = tpl.replace(/{rank}/g, rank);
    add_record = add_record.replace(/{user_name}/g, rank_info.user_name);
    add_record = add_record.replace(/{vote_count}/g, rank_info.v_count);
    add_record = add_record.replace(/{pt}/g, rank_info.pt);
    add_record = add_record.replace(/{mark1_rate}/g, rank_info.mark1_rate);
    add_record = add_record.replace(/{mark2_rate}/g, rank_info.mark2_rate);
    add_record = add_record.replace(/{mark3_rate}/g, rank_info.mark3_rate);
    add_record = add_record.replace(/{mark4_rate}/g, rank_info.mark4_rate);
    add_record = add_record.replace(/{mark5_rate}/g, rank_info.mark5_rate);
    add_record = add_record.replace(/{mark6_rate}/g, rank_info.mark6_rate);
    add_record = add_record.replace(/{pay1_rate}/g, rank_info.pay1_rate);
    add_record = add_record.replace(/{pay2_rate}/g, rank_info.pay2_rate);
    $(add_record).appendTo("tbody#year_ranking");
  }
  /* 上半期ランキングを反映 */
  $("tbody#first_half_ranking").empty();
  for(let i=0; i<pt_first_half_ranking_list.length; i++){
    var rank_info = pt_first_half_ranking_list[i];
    var rank = i+1;
    var add_record = tpl.replace(/{rank}/g, rank);
    add_record = add_record.replace(/{user_name}/g, rank_info.user_name);
    add_record = add_record.replace(/{vote_count}/g, rank_info.v_count);
    add_record = add_record.replace(/{pt}/g, rank_info.pt);
    add_record = add_record.replace(/{mark1_rate}/g, rank_info.mark1_rate);
    add_record = add_record.replace(/{mark2_rate}/g, rank_info.mark2_rate);
    add_record = add_record.replace(/{mark3_rate}/g, rank_info.mark3_rate);
    add_record = add_record.replace(/{mark4_rate}/g, rank_info.mark4_rate);
    add_record = add_record.replace(/{mark5_rate}/g, rank_info.mark5_rate);
    add_record = add_record.replace(/{mark6_rate}/g, rank_info.mark6_rate);
    add_record = add_record.replace(/{pay1_rate}/g, rank_info.pay1_rate);
    add_record = add_record.replace(/{pay2_rate}/g, rank_info.pay2_rate);
    $(add_record).appendTo("tbody#first_half_ranking");
  }
  /* 下半期ランキングを反映 */
  $("tbody#last_half_ranking").empty();
  for(let i=0; i<pt_last_half_ranking_list.length; i++){
    var rank_info = pt_last_half_ranking_list[i];
    var rank = i+1;
    var add_record = tpl.replace(/{rank}/g, rank);
    add_record = add_record.replace(/{user_name}/g, rank_info.user_name);
    add_record = add_record.replace(/{vote_count}/g, rank_info.v_count);
    add_record = add_record.replace(/{pt}/g, rank_info.pt);
    add_record = add_record.replace(/{mark1_rate}/g, rank_info.mark1_rate);
    add_record = add_record.replace(/{mark2_rate}/g, rank_info.mark2_rate);
    add_record = add_record.replace(/{mark3_rate}/g, rank_info.mark3_rate);
    add_record = add_record.replace(/{mark4_rate}/g, rank_info.mark4_rate);
    add_record = add_record.replace(/{mark5_rate}/g, rank_info.mark5_rate);
    add_record = add_record.replace(/{mark6_rate}/g, rank_info.mark6_rate);
    add_record = add_record.replace(/{pay1_rate}/g, rank_info.pay1_rate);
    add_record = add_record.replace(/{pay2_rate}/g, rank_info.pay2_rate);
    $(add_record).appendTo("tbody#last_half_ranking");
  }

  jQuery(function($){ 
    var dt_setting = {
      lengthMenu: [ 5, 10, 50, 100 ],
      order: [ [ 0, "asc" ] ],
      columnDefs: [
        {targets: 0, 'type': 'num', render: $.fn.dataTable.render.number( ',', '.', 0, '','位' )} ,
        {targets: 3, 'type': 'num', render: $.fn.dataTable.render.number( ',', '.', 1, '','pt' )} ,
        {targets: 4, 'type': 'num', render: $.fn.dataTable.render.number( ',', '.', 0, '','%' )} ,
        {targets: 5, 'type': 'num', render: $.fn.dataTable.render.number( ',', '.', 0, '','%' )} ,
        {targets: 6, 'type': 'num', render: $.fn.dataTable.render.number( ',', '.', 0, '','%' )} ,
        {targets: 7, 'type': 'num', render: $.fn.dataTable.render.number( ',', '.', 0, '','%' )} ,
        {targets: 8, 'type': 'num', render: $.fn.dataTable.render.number( ',', '.', 0, '','%' )} ,
        {targets: 9, 'type': 'num', render: $.fn.dataTable.render.number( ',', '.', 0, '','%' )} ,
        {targets: 10, 'type': 'num', render: $.fn.dataTable.render.number( ',', '.', 0, '','%' )} ,
        {targets: 11, 'type': 'num', render: $.fn.dataTable.render.number( ',', '.', 0, '','%' )}
      ],
      language: {
        "sProcessing":   "処理中...",
        "sLengthMenu":   "_MENU_ 件表示",
        "sZeroRecords":  "データはありません。",
        "sInfo":         " _TOTAL_ 件中 _START_ から _END_ まで表示",
        "sInfoEmpty":    " 0 件中 0 から 0 まで表示",
        "sInfoFiltered": "（全 _MAX_ 件より抽出）",
        "sInfoPostFix":  "",
        "sSearch":       "お名前:",
        "sUrl":          "",
        "oPaginate": {
          "sFirst":    "先頭",
          "sPrevious": "前へ",
          "sNext":     "次へ",
          "sLast":     "最終"
        }      
      }
    };
    $("#monthly_ranking").DataTable(dt_setting); 
    $("#yearly_ranking").DataTable(dt_setting); 
    $("#first_half_ranking").DataTable(dt_setting); 
    $("#last_half_ranking").DataTable(dt_setting); 
  });       
}

/**
 * 成績管理を初期化する
 */
function initScoreTab(){
  // 高速化の為、ユーザーCDのみを取得
  var service_result = boc_get_scores_user_cd(null);
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("ユーザー一覧の取得に失敗しました。");
    return;
  }
  user_score_user_cds = service_result.score_user_cds;

  // 最初のユーザーの成績を取得
  var service_result = boc_get_user_info_list({
    ope_user_cd : getLoginUserCD(),
    user_cd     : user_score_user_cds[0].user_cd
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("成績データの取得に失敗しました。");
    return;
  }
  // 最初のユーザーデータを設定
  updateUserScoreView(service_result.user_list[0]);
}

/**
 * ユーザータブを初期化する
 */
function initUserTab(){
  /* ユーザー一覧を取得する */
  var service_result = boc_get_user_list({
    ope_user_cd : getLoginUserCD()
  });
  if (service_result.err_msg != BOC_NO_ERROR){
    bootbox.alert("ユーザー一覧の取得に失敗しました。");
    return;
  }
  // ユーザー一覧を更新
  updateUserListView(service_result.user_list);
}

/**
 * レース登録タブを初期化する
 */
function initRaceManager(){
  $(".radio_check").on("click", function(){
    // 変更後の値を取得
    var isChecked = $(this).prop("checked");
    $('.radio_check').prop('checked', false);  //  全部のチェックを外す
    // 再度値を設定
    $(this).prop("checked", isChecked);
  });

  // レース一覧を取得
  var service_result = boc_get_race_list({
    ope_user_cd : getLoginUserCD()
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("レース一覧の取得に失敗しました。");
    return;
  }
  updateRaceListView(service_result.race_list);

}

/**
 * 予選バトルタブを初期化する。
 */
function initVoteTab(){
  /* 投票可能なリストを取得する */
  var user_cd = getLoginUserCD();
  if (user_cd){
    var service_result = boc_get_vote_race({
      user_cd : user_cd
    });
    if (service_result.err_code != BOC_NO_ERROR){
      bootbox.alert("投票可能なレース一覧の取得に失敗しました。");
      return;
    }
    updateVoteRaceListView(service_result.race_list);
  }
}

/**
 * 成績管理に成績を反映する。
 * @param {in} cursor_index : 表示するユーザーリストのIndex
 */
function updateUserScoreView(user_score){
  /* データを反映 */
  // タイトル画像
  $("img#title_img").attr("src", "img/" + user_score.rabking_img);
  // ユーザー名
  $("span#user_name").html(user_score.user_name);
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

/**
 * 投票可能なレースリストを更新する
 * @param {in} race_list : 投票可能なレースリスト
 */
function updateVoteRaceListView(race_list){
  $("tbody#vote_race_list").empty();
  if (race_list){
    // テンプレートの読込
    var tpl = getTemplate("/tpl_vote_race_item.html");
    for(let race_idx=0; race_idx<race_list.length; race_idx++){
      var race_info = race_list[race_idx];
      var add_record = tpl.replace(/{race_date}/g, race_info.race_date);    
      add_record = add_record.replace(/{race_place}/g, race_info.race_place); 
      var race_disp_num = race_info.race_num + "R";
      if (race_info.race_num==13){
        race_disp_num = "SP";
      }   
      add_record = add_record.replace(/{race_num}/g, race_disp_num);    
      add_record = add_record.replace(/{race_name}/g, race_info.race_name);    
      add_record = add_record.replace(/{race_time}/g, race_info.race_time.substr(11,5));    
      add_record = add_record.replace(/{vote_status}/g, race_info.vote_status);    
      add_record = add_record.replace(/{race_cd}/g, race_info.race_cd);    
      /* ボタン名を設定 */
      var btn_name = "投票";
      if (race_info.vote_status == '済')　btn_name = "修正";
      add_record = add_record.replace(/{btn_name}/g, 　btn_name);
      $(add_record).appendTo("tbody#vote_race_list");   
    }
  }
}

/**
 * ユーザーリストを更新
 * @param {in} user_list : ユーザーリスト
 */
function updateUserListView(user_list){
  $("tbody#tbl_user_list").empty();
  // テンプレートの読込
  var tpl = getTemplate("/tpl_user_list_item.html");
  for(let user_info of user_list){
    // データを反映
    var add_record = tpl.replace(/{user_name}/g, user_info.user_name);    
    add_record = add_record.replace(/{user_type_name}/g, user_info.user_type_name);    
    add_record = add_record.replace(/{user_rank_name}/g, user_info.user_rank_name);    
    add_record = add_record.replace(/{user_cd}/g, user_info.user_cd);
    $(add_record).appendTo("tbody#tbl_user_list");   
  }
  jQuery('#tbl_users').tablesorter();
  $("#tbl_users").trigger("update");

}


/**
 * レース一覧を更新する
 * @param {in} race_list : レースリスト
 */
function updateRaceListView(race_list){
  $("#race_list").empty();
  // テンプレートの読込
  var tpl = getTemplate("/tpl_race_list_item.html");
  for(let i=0; i<race_list.length; i++){
    // データを反映
    var race_info = race_list[i];
    var add_record = tpl.replace(/{race_date}/g, race_info.race_date);    
    add_record = add_record.replace(/{race_place}/g, race_info.race_place);
    var race_disp_num = race_info.race_num + "R";
    if (race_info.race_num==13){
      race_disp_num = "SP";
    }
    add_record = add_record.replace(/{race_num}/g, race_disp_num);    
    add_record = add_record.replace(/{race_name}/g, race_info.race_name);    
    add_record = add_record.replace(/{race_cd}/g, race_info.race_cd);    
    $(add_record).appendTo("tbody#race_list");   
  }
}


/////////////////////////////////////////////
// イベントハンドラ
//

/**
 * 投票画面を表示する
 */
function onClickedShowVote(race_id){
  // レース情報を取得
  var service_result = boc_get_race_info({
    race_cd : race_id
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("レース情報の取得に失敗しました。");
    return;
  }
  var race_info = service_result.race_info;
  // レースCDを設定
  $("input#v_race_cd").val(race_info.race_cd);
  // タイトル部分を設定
  var vote_title = "{race_short_date}&nbsp;{race_place}{race_num}R&nbsp;{race_name}";
  vote_title = vote_title.replace(/{race_short_date}/g, race_info.race_date.substr(5,5));
  vote_title = vote_title.replace(/{race_place}/g, race_info.race_place);
  vote_title = vote_title.replace(/{race_num}/g, race_info.race_num);
  vote_title = vote_title.replace(/{race_name}/g, race_info.race_name);
  $("span#vote_race_title").html(vote_title);
  // 発走時刻を設定
  var vote_time = "{race_time}発走";
  vote_time = vote_time.replace(/{race_time}/g, race_info.race_time.substr(11,5));
  $("span#vote_race_time").html(vote_time);
  // 各マークの候補リストを設定
  $("select[name=v_mark1]").empty();
  $("select[name=v_mark2]").empty();
  $("select[name=v_mark3]").empty();
  $("select[name=v_mark4]").empty();
  $("select[name=v_mark5]").empty();
  $("select[name=v_mark6]").empty();
  /* 最初に空レコードを追加 */
  $("<option value=''>--馬名を選択--</option>").appendTo("select[name=v_mark1]");
  $("<option value=''>--馬名を選択--</option>").appendTo("select[name=v_mark2]");
  $("<option value=''>--馬名を選択--</option>").appendTo("select[name=v_mark3]");
  $("<option value=''>--馬名を選択--</option>").appendTo("select[name=v_mark4]");
  $("<option value=''>--馬名を選択--</option>").appendTo("select[name=v_mark5]");
  $("<option value=''>--馬名を選択--</option>").appendTo("select[name=v_mark6]");

  var tpl_option = "<option value='{uban}'>{uban}:{uname}</option>";
  for(let uidx=0; uidx<race_info.race_horses.length; uidx++){
    var horse_info = race_info.race_horses[uidx];
    var add_record = tpl_option.replace(/{uban}/g, horse_info.horse_num);
    add_record = add_record.replace(/{uname}/g, horse_info.horse_name);
    // 各selectに追加
    $(add_record).appendTo("select[name=v_mark1]");
    $(add_record).appendTo("select[name=v_mark2]");
    $(add_record).appendTo("select[name=v_mark3]");
    $(add_record).appendTo("select[name=v_mark4]");
    $(add_record).appendTo("select[name=v_mark5]");
    $(add_record).appendTo("select[name=v_mark6]");
  }

  // 自身の投票データを取得
  var user_cd = getLoginUserCD();
  var service_result = boc_get_vote({
    user_cd   : user_cd,
    race_cd   : race_info.race_cd
  });
  if (service_result.err_code == BOC_NO_ERROR){
    if (service_result.vote_info){
      /* 投票データが存在する場合はデータを反映 */
      var vote_info = service_result.vote_info;
      if (vote_info.mark1 && vote_info.mark1 != 0) $("select[name=v_mark1]").val(vote_info.mark1);
      if (vote_info.mark2 && vote_info.mark2 != 0) $("select[name=v_mark2]").val(vote_info.mark2);
      if (vote_info.mark3 && vote_info.mark3 != 0) $("select[name=v_mark3]").val(vote_info.mark3);
      if (vote_info.mark4 && vote_info.mark4 != 0) $("select[name=v_mark4]").val(vote_info.mark4);
      if (vote_info.mark5 && vote_info.mark5 != 0) $("select[name=v_mark5]").val(vote_info.mark5);
      if (vote_info.mark6 && vote_info.mark6 != 0) $("select[name=v_mark6]").val(vote_info.mark6);
      // 販売情報も反映
      if (vote_info.is_sale && vote_info.is_sale != 0){
        $("input#is_sale_1").attr('checked', true);
      }
      if (vote_info.sale_pt && vote_info.sale_pt != 0) $("input[name=sale_pt]").val(vote_info.sale_pt);
    }
    /* 販売予想があれば販売予想も表示する */
    if (service_result.sale_vote){
      /* テンプレートを読み込む */
      var tpl_sale = getTemplate('/tpl_sale_vote_item.html');
      var sale_votes = service_result.sale_vote;
      var sale_cnt = sale_votes.length;
      for(let i=0; i<sale_cnt; i++){
        var sale_info = sale_votes[i];
        var add_item = tpl_sale.replace(/{user_name}/g, sale_info['user_name']);
        add_item = add_item.replace(/{vote_id}/g, sale_info['vote_id']);
        add_item = add_item.replace(/{is_baught}/g, sale_info['is_baught']);
        // 既に購入ずみならボタンの文言を変更
        var str_btn = "{sale_pt}ptで購入";
        str_btn = str_btn.replace(/{sale_pt}/g, sale_info['sale_pt']);
        if (sale_info['is_baught']==1){
          str_btn = "予想を見る";
        }
        add_item = add_item.replace(/{str_btn}/g, str_btn);
        // 暫定でランク照合は固定
        add_item = add_item.replace(/{user_ranking}/g, '/img/title_ol.png');

        // 販売予想を追加
        $(add_item).appendTo("#sale_votes");
      }
    }
  }

  // 投票画面を表示
  $("#vote_frame").css("display", "block");
}


 /**
  * レースの新規登録イベントハンドラ
  */
 function onClickedAddRace(){
  /* 入力項目をクリア */
  $("input#race_date").val('');
  $("select[name=race_place]").val('');
  $("select[name=race_num]").val('');
  $("input#race_time").val('');
  $("input#race_name").val('');
  $("select[name=race_month]").val('');
  $("input#race_date:checked").val('');
  $("#is_trial_race").prop('checked', false);
  $(".radio_check").prop('checked', false);
  for(let unum=1; unum<=18; unum++){
    $("input[name=r-umaname"+unum+"]").val('');
  }

  /* 対象のカードのみ表示 */
  $("#update_race").css("display","none");
  $("#update_race_result").css("display","none");
  $("#add_race").css("display","block");
}

/**
 * レース修正のイベントハンドラ
 */
function onClickedRaceUpdate(race_id){
  /* 入力項目をクリア */
  $("input#u_race_cd").val('');
  $("input#u_race_date").val('');
  $("select[name=u_race_place]").val('');
  $("select[name=u_race_num]").val('');
  $("input#u_race_time").val('');
  $("input#u_race_name").val('');
  $("select[name=u_race_month]").val('');
  $("input#u_race_date:checked").val('');
  $("#u_is_trial_race").prop('checked', false);
  $(".radio_check").prop('checked', false);

  /* レース情報を取得 */
  var service_result = boc_get_race_info({
    race_cd : race_id
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("レース情報の取得に失敗しました。");
    return;
  }

  /* レース情報を反映 */
  var race_info = service_result.race_info;
  $("input#u_race_cd").val(race_info.race_cd);
  $("input#u_race_date").val(race_info.race_date);
  $("select[name=u_race_place]").val(race_info.race_place);
  $("select[name=u_race_num]").val(zeroPadding(race_info.race_num,2));
  $("input#u_race_time").val(race_info.race_time.substr(11,5));
  $("input#u_race_name").val(race_info.race_name);
  $("select[name=u_race_month]").val(race_info.race_month);
  if (race_info.race_type == 1 || race_info.race_type == 3 || race_info.race_type == 5){
    $("#u_is_trial_race").prop('checked', true);
  }
  if (race_info.race_type == 3){
    $("#u_is_semi_final").prop('checked', true);
  }
  else if (race_info.race_type == 5){
    $("#u_is_final").prop('checked', true);
  }

  /*出馬表を反映 */
  if (race_info.race_horses && race_info.race_horses.length > 0){
    for(let unum=1; unum<=18; unum++){
      var horse_info = race_info.race_horses[unum-1];
      if (horse_info){
        $("input[name=u_r-umaname"+unum+"]").val(horse_info.horse_name);
      }
      else{
        /* 存在しない場合は馬名クリア */
        $("input[name=u_r-umaname"+unum+"]").val('');
      }
    }
  }


  /* 対象のdivのみ表示 */
  $("#update_race").css("display","block");
  $("#update_race_result").css("display","none");
  $("#add_race").css("display","none");
}

/**
 * レース結果入力クリックイベントハンドラ
 */
function onClickedUpdateRaceResult(race_cd){
  /* 入力項目をクリア */
  $("input#r_result_cd").val('');
  $("input#r_result_type").val('');
  $("span#r_result_date").html('');
  $("span#r_result_place").html('');
  $("span#r_result_num").html('');
  $("span#r_result_name").html('');
  $("select[name=r_rank1_umban]").val('');
  $("input#r_ozz1").val('');
  $("input#r_tansho1").val('');
  $("input#r_fukusho1").val('');
  $("select[name=r_rank2_umban]").val('');
  $("input#r_ozz2").val('');
  $("input#r_tansho2").val('0');
  $("input#r_fukusho2").val('');
  $("select[name=r_rank3_umban]").val('');
  $("input#r_ozz3").val('');
  $("input#r_tansho3").val('0');
  $("input#r_fukusho3").val('');

  /* 出馬表を取得 */
  var service_result = boc_get_race_info({
    race_cd : race_cd
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("レース情報の取得に失敗しました。");
    return;
  }

  /* ヘッダーを設定 */
  var race_info = service_result.race_info;
  $("input#r_result_cd").val(race_info.race_cd);
  $("input#r_result_type").val(race_info.race_type);
  $("span#r_result_date").html(race_info.race_date);
  $("span#r_result_place").html(race_info.race_cd.race_place);
  $("span#r_result_num").html(race_info.race_num);
  $("span#r_result_name").html(race_info.race_name);

  /* selectの中身を更新 */
  var opt_tpl = "<option value='{uban}'>{uban}:{uname}</option>";
  for(let ri=1; ri<=3; ri++){
    var tgt_select = "select[name=r_rank"+ri+"_umban]";
    $(tgt_select).empty();
    /* 先頭レコードを追加 */
    $("<option id='' value=''>--馬名を選択--</option>").appendTo(tgt_select);
    if (race_info.race_horses && race_info.race_horses.length > 0){
      for(let unum=1; unum<=18; unum++){
        var horse_info = race_info.race_horses[unum-1];
        if (horse_info){
          var add_record = opt_tpl.replace(/{uban}/g, horse_info.horse_num);
          add_record = add_record.replace(/{uname}/g, horse_info.horse_name);
          $(add_record).appendTo(tgt_select)
        }
      }
    }
  }

  /* 消し馬のselectの中身を更新 */
  for(let ri=1; ri<=8; ri++){
    var tgt_select = "select[name=d_rank"+ri+"_umban]";
    $(tgt_select).empty();
    /* 先頭レコードを追加 */
    $("<option id='' value=''>--馬名を選択--</option>").appendTo(tgt_select);
    if (race_info.race_horses && race_info.race_horses.length > 0){
      for(let unum=1; unum<=18; unum++){
        var horse_info = race_info.race_horses[unum-1];
        if (horse_info){
          var add_record = opt_tpl.replace(/{uban}/g, horse_info.horse_num);
          add_record = add_record.replace(/{uname}/g, horse_info.horse_name);
          $(add_record).appendTo(tgt_select)
        }
      }
    }
  }

  /* 既存データが存在するかをチェック */
  var service_result = boc_get_race_result({
    race_cd : race_cd
  });
  if (service_result.err_code == BOC_NO_ERROR){
    if (service_result.race_result && service_result.race_result.length>0){
      for(let ri=0; ri<service_result.race_result.length; ri++){
        var rank_info = service_result.race_result[ri];
        if (rank_info.race_rank == 1){
          $("select[name=r_rank1_umban]").val(rank_info.horse_num);
          $("input#r_ozz1").val(rank_info.last_ozz);
          $("input#r_tansho1").val(rank_info.pay1);
          $("input#r_fukusho1").val(rank_info.pay2);
        }
        else if (rank_info.race_rank == 2){
          $("select[name=r_rank2_umban]").val(rank_info.horse_num);
          $("input#r_ozz2").val(rank_info.last_ozz);
          $("input#r_fukusho2").val(rank_info.pay2);
        }
        else if (rank_info.race_rank == 3){
          $("select[name=r_rank3_umban]").val(rank_info.horse_num);
          $("input#r_ozz3").val(rank_info.last_ozz);
          $("input#r_fukusho3").val(rank_info.pay2);
        }
      }
    }
    /* 消し馬のデータも反映 */
    if (service_result.d_horses && service_result.d_horses.length>0){
      for(let ri=0; ri<service_result.d_horses.length; ri++){
        var d_horse_info = service_result.d_horses[ri];
        $("select[name=d_rank"+d_horse_info.d_rank+"_umban]").val(d_horse_info.umaban);
        $("input#d_ozz"+d_horse_info.d_rank).val(d_horse_info.del_point);
      }
    }
  }



  /* 結果入力エリアを表示 */
  $("#update_race").css("display","none");
  $("#add_race").css("display","none");
  $("#update_race_result").css("display","block");
}

/**
 * ユーザ情報編集クリックイベントハンドラ
 * @param {in} user_cd  : ユーザCD 
 */
function onClickedUserEdit(user_cd){
  /* ユーザー情報を取得する */
  var check_result = boc_check_use_function({
    func_name   : BOC_USE_UPDATE_USER_INFO,
    ope_user_cd : getLoginUserCD(),
    param1      : user_cd
  });
  if (check_result.err_code != BOC_NO_ERROR){
    bootbox.alert("権限がありません。");
    return;
  }
  else{
    var service_result = boc_get_user_info({
      user_cd       : user_cd
    });
    if (service_result.err_code != BOC_NO_ERROR){
      bootbox.alert("ユーザー情報の取得に失敗しました。");
      return;
    }
    /* ユーザー情報を反映 */
    var user_info = service_result.user_info;
    var user_name = (user_info.user_name ? user_info.user_name : "");
    var user_email = (user_info.login_cd ? user_info.login_cd : "");
    var user_passwd = (user_info.login_passwd ? user_info.login_passwd : "");
    var user_type = (user_info.user_type ? user_info.user_type : "");
    var user_rank = (user_info.user_rank ? user_info.user_rank : "");
    $("input#user_cd").val(user_info.user_cd);
    $("input#user_name").val(user_name);
    $("input#user_email").val(user_email);
    $("input#user_passwd").val(user_passwd);
    $("select#user_type").val(user_type);
    $("select#user_rank").val(user_rank);
    $("#update_user").css("display","block");
  
  }
}

/**
 * キャンセルボタンクリックイベント
 * 対象となるセレクタを非表示にする
 * @param {in} tgt_tag  : 対象となるセレクタ 
 */
function onClickedCancel(tgt_tag){
  $(tgt_tag).css("display", "none");
  return false;
}

/**
 * ユーザー情報を更新する。
 */
function onClickedUpdateUser(){
  var user_cd = $("input#user_cd").val();
  var user_name = $("input#user_name").val();
  var user_email = $("input#user_email").val();
  var user_passwd = $("input#user_passwd").val();
  var user_type = $("select#user_type").val();
  var user_rank = $("select#user_rank").val();

  // ユーザー情報を更新
  var update_info = {
    mode          : 'superuser',
    user_cd       : user_cd,
    user_name     : user_name,
    login_cd      : user_email,
    login_passwd  : user_passwd,
    user_type     : user_type,
    user_rank     : user_rank,
  };
  var service_result = boc_regist_user(update_info);
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("ユーザー情報の更新に失敗しました。");
    return;
  }
  // ユーザー一覧を更新
  initUserTab();
  // 更新メッセージを表示
  bootbox.alert("ユーザー情報を更新しました。",function(){
    // ユーザー編集エリアを非表示
    onClickedCancel('#update_user');
  });

}

/**
 * レース登録更新クリックイベントハンドラ
 */
function onClickedRegistRace(tgt_tag){
  // 入力値を取得
  /* 開催日 */
  var race_date = $("input#race_date").val();
  var race_place = $("select[name=race_place]").val();
  var race_num = $("select[name=race_num]").val();
  var race_time = $("input#race_time").val();
  var race_name = $("input#race_name").val();
  var race_month = $("select[name=race_month]").val();
  var is_trial_race = $("input#is_trial_race:checked").val();
  var is_semi_final = $("input#is_semi_final:checked").val();
  var is_final = $("input#is_final:checked").val();
  /* 更新なら再度値を取得しなおす */
  if (tgt_tag == 'update_race'){
    race_date = $("input#u_race_date").val();
    race_place = $("select[name=u_race_place]").val();
    race_num = $("select[name=u_race_num]").val();
    race_time = $("input#u_race_time").val();
    race_name = $("input#u_race_name").val();
    race_month = $("select[name=u_race_month]").val();
    is_trial_race = $("input#u_is_trial_race:checked").val();
    is_semi_final = $("input#u_is_semi_final:checked").val();
    is_final = $("input#u_is_final:checked").val();
  }

  /* レース種別を特定 */
  var race_type = 0;
  if (is_final) race_type = 5;
  else if (is_semi_final) race_type = 3;
  else if (is_trial_race) race_type = 1;
  /* レースCDを設定 */
  var race_cd = BOC_KBN_RACE_PLACE[race_place] + race_date.substr(0,4) + race_date.substr(5,2) + race_date.substr(8,2) + race_num;

  var race_info = {
    race_cd     : race_cd,
    race_date   : race_date,
    race_place  : race_place,
    race_num    : race_num,
    race_time   : race_date + " " + race_time + ":00",
    race_name   : race_name,
    race_month  : race_month,
    race_type   : race_type,
  };

  // 出馬表を取得
  var race_horses = [];
  for(let unum=1; unum<=18; unum++){
    var tgt_unum = "input[name=r-umaban"+unum+"]";
    var tgt_uname = "input[name=r-umaname"+unum+"]";
    /* 更新なら再度取得しなおす */
    if (tgt_tag == 'update_race'){
      tgt_unum = "input[name=u_r-umaban"+unum+"]";
      tgt_uname = "input[name=u_r-umaname"+unum+"]";
    }
    var uma_name = $(tgt_uname).val();
    if (uma_name){
      var add_info = {
        horse_num : $(tgt_unum).val(),
        horse_name : $(tgt_uname).val(),
      }
      race_horses.push(add_info);
    }
  }
  race_info['race_horses'] = race_horses;

  // レース情報を登録
  var check_result = boc_check_use_function({
    func_name   : BOC_USE_RACE_REGIST,
    ope_user_cd : getLoginUserCD(),
    param1      : race_cd
  });
  if (check_result.err_code != BOC_NO_ERROR){
    bootbox.alert("権限がありません。");
    return;
  }
  else{
    race_info.self_user_cd = getLoginUserCD();
    var service_result = boc_regist_race(race_info);
    if (service_result.err_code != BOC_NO_ERROR){
      bootbox.alert("レース情報の登録に失敗しました。");
      return;
    }
  
    // レース一覧を更新
    var service_result = boc_get_race_list({
      ope_user_cd : getLoginUserCD()
    });
    if (service_result.err_code != BOC_NO_ERROR){
      bootbox.alert("レース情報リストの取得に失敗しました。");
      return;
    }
    updateRaceListView(service_result.race_list);
  
  
    bootbox.alert("レース情報を登録しました。",function(){
      onClickedCancel("#"+tgt_tag);
    });
  
  }
}

/**
 * レース削除ボタンクリックイベントハンドラ
 */
function onClickedDeleteRace(tgt_tag){
  var delete_race_cd = $("input#u_race_cd").val();
  if (!delete_race_cd){
    bootbox.alert("レースCDが未設定です。");
    return;
  }

  bootbox.confirm({
    title: "削除しますか？",
    message: "レース情報を削除しますか？",
    closeButton: false,
    buttons: {
      confirm: {
        label: '削除'
      },
      cancel: {
        label: 'キャンセル'
      }
    },
    callback: function (result) {
        if (result){
          var service_result = boc_delete_race({
            self_user_cd  : getLoginUserCD(),
            race_cd : delete_race_cd
          });
          if (service_result.err_code != BOC_NO_ERROR){
            bootbox.alert("レース情報の削除に失敗しました。");
            return;
          }

          // レース一覧を更新
          var service_result = boc_get_race_list({
            ope_user_cd : getLoginUserCD()
          });
          if (service_result.err_code != BOC_NO_ERROR){
            bootbox.alert("レース情報リストの取得に失敗しました。");
            return;
          }
          updateRaceListView(service_result.race_list);

          bootbox.alert("レース情報を削除しました。",function(){
            onClickedCancel("#"+tgt_tag);
          });
        }
    }
});  
  
}

/**
 * 投票ボタンクリックイベントハンドラ
 */
function onClickedVote(){
  // 権限チェック
  var check_result = boc_check_use_function({
    func_name : BOC_USE_VOTE,
    ope_user_cd : getLoginUserCD()
  });
  if (check_result.err_code != BOC_NO_ERROR){
    bootbox.alert("権限がありません。");
    return;
  }
  // レースCDを取得
  var race_cd = $("input#v_race_cd").val();
  // 現在のログインしているユーザーCDを取得
  var user_cd = getLoginUserCD();
  /* 予想販売有無 */
  var is_sale = $("input[name=is_sale]:checked").val();
  var sale_pt = 0;
  if (is_sale==1){
    sale_pt = $("input[name=sale_pt]").val();
  }
  /* 投票データを設定 */
  var vote_info = {
    user_cd : user_cd,
    race_cd : race_cd,
    mark1   : ($("select[name=v_mark1]").val() ? $("select[name=v_mark1]").val() : 0),
    mark2   : ($("select[name=v_mark2]").val() ? $("select[name=v_mark2]").val() : 0),
    mark3   : ($("select[name=v_mark3]").val() ? $("select[name=v_mark3]").val() : 0),
    mark4   : ($("select[name=v_mark4]").val() ? $("select[name=v_mark4]").val() : 0),
    mark5   : ($("select[name=v_mark5]").val() ? $("select[name=v_mark5]").val() : 0),
    mark6   : ($("select[name=v_mark6]").val() ? $("select[name=v_mark6]").val() : 0),
    is_sale : is_sale,
    sale_pt : sale_pt
  };
  // if (vote_info.mark1=="0"){
  //   bootbox.alert("◎は必須です！");
  //   return;
  // }
  // if (vote_info.mark5=="0"){
  //   bootbox.alert("穴は必須です！");
  //   return;
  // }
  // if (vote_info.mark6=="0"){
  //   bootbox.alert("消は必須です！");
  //   return;
  // }
  // 投票を行う
  var service_result = boc_vote(vote_info);
  if (service_result.err_code == BOC_TIMEOUT){
    bootbox.alert("投票は締め切られました。");
    return;
  }
  else if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("投票に失敗しました。");
    return;
  }
  // 投票一覧を更新
  service_result = boc_get_vote_race({
    user_cd : user_cd
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("投票一覧の取得に失敗しました。");
    return;
  }
  updateVoteRaceListView(service_result.race_list);
  bootbox.alert("投票を受け付けました。",function(){
    onClickedCancel("#vote_frame");
  });
  
}

/**
 * レース結果登録ボタンクリックイベントハンドラ
 */
function onClickedRegistResult(){
  /* 入力情報を取得 */
  var race_cd = $("input#r_result_cd").val();
  var race_type = $("input#r_result_type").val();
  var rank1_umaban = $("select[name=r_rank1_umban]").val();
  var rank1_ozz = $("input#r_ozz1").val();
  var rank1_pay1 = $("input#r_tansho1").val();
  var rank1_pay2 = $("input#r_fukusho1").val();
  var rank2_umaban = $("select[name=r_rank2_umban]").val();
  var rank2_pay1 = '0';
  var rank2_pay2 = $("input#r_fukusho2").val();
  var rank2_ozz = $("input#r_ozz2").val();
  var rank3_umaban = $("select[name=r_rank3_umban]").val();
  var rank3_ozz = $("input#r_ozz3").val();
  var rank3_pay1 = '0';
  var rank3_pay2 = $("input#r_fukusho3").val();
  /* 消し馬データ */
  var d_rank1_umban = $("select[name=d_rank1_umban]").val();
  var d_pt1 = $("input#d_ozz1").val();
  var d_rank2_umban = $("select[name=d_rank2_umban]").val();
  var d_pt2 = $("input#d_ozz2").val();
  var d_rank3_umban = $("select[name=d_rank3_umban]").val();
  var d_pt3 = $("input#d_ozz3").val();
  var d_rank4_umban = $("select[name=d_rank4_umban]").val();
  var d_pt4 = $("input#d_ozz4").val();
  var d_rank5_umban = $("select[name=d_rank5_umban]").val();
  var d_pt5 = $("input#d_ozz5").val();
  var d_rank6_umban = $("select[name=d_rank6_umban]").val();
  var d_pt6 = $("input#d_ozz6").val();
  var d_rank7_umban = $("select[name=d_rank7_umban]").val();
  var d_pt7 = $("input#d_ozz7").val();
  var d_rank8_umban = $("select[name=d_rank8_umban]").val();
  var d_pt8 = $("input#d_ozz8").val();

  // 権限チェック
  var check_result = boc_check_use_function({
    func_name   : BOC_USE_RACE_RESULT_REGIST,
    ope_user_cd : getLoginUserCD(),
    param1      : race_cd
  });
  if (check_result.err_code != BOC_NO_ERROR){
    bootbox.alert("権限がありません。");
    return;
  }

  var r_info = {
    self_user_cd  : getLoginUserCD(),
    race_cd       : race_cd,
    race_type     : race_type,
    rank1_umaban  : rank1_umaban,
    rank1_ozz     : rank1_ozz,
    rank1_pay1    : rank1_pay1,
    rank1_pay2    : rank1_pay2,
    rank2_umaban  : rank2_umaban,
    rank2_ozz     : rank2_ozz,
    rank2_pay1    : rank2_pay1,
    rank2_pay2    : rank2_pay2,
    rank3_umaban  : rank3_umaban,
    rank3_ozz     : rank3_ozz,
    rank3_pay1    : rank3_pay1,
    rank3_pay2    : rank3_pay2,
    d_rank1_umban : d_rank1_umban,
    d_pt1         : d_pt1,
    d_rank2_umban : d_rank2_umban,
    d_pt2         : d_pt2,
    d_rank3_umban : d_rank3_umban,
    d_pt3         : d_pt3,
    d_rank4_umban : d_rank4_umban,
    d_pt4         : d_pt4,
    d_rank5_umban : d_rank5_umban,
    d_pt5         : d_pt5,
    d_rank6_umban : d_rank6_umban,
    d_pt6         : d_pt6,
    d_rank7_umban : d_rank7_umban,
    d_pt7         : d_pt7,
    d_rank8_umban : d_rank8_umban,
    d_pt8         : d_pt8
  }
  /* レース結果を登録 */
  var service_result = boc_regist_race_result(r_info);
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("レース結果の登録に失敗しました。");
    return;
  }
  bootbox.alert("レース結果を登録しました。",function(){
    onClickedCancel("#update_race_result");
  });
}


/**
 * ランキング種別変更イベントハンドラ
 */
function onChangedRankingType(){
  $("div#monthly_ranking_bord").css("display", "none");
  $("div#yearly_ranking_bord").css("display", "none");
  $("div#first_half_ranking_bord").css("display", "none");
  $("div#last_hakf_ranking_bord").css("display", "none");
  var ranking_type = $("select[name=ranking_select]").val();
  if (ranking_type=='month'){
    $("div#monthly_ranking_bord").css("display", "block");
  }
  else if (ranking_type=='year'){
    $("div#yearly_ranking_bord").css("display", "block");
  }
  else if (ranking_type=='first_half'){
    $("div#first_half_ranking_bord").css("display", "block");
  }
  else if (ranking_type=='last_half'){
    $("div#last_hakf_ranking_bord").css("display", "block");
  }

}

/**
 * ひとつ前にユーザー成績を表示
 */
function onClickedUserScoreUp(){
  current_cursor_index--;
  if (current_cursor_index<0) current_cursor_index =0;
  var tgt_user_cd = user_score_user_cds[current_cursor_index].user_cd;
  var service_result = boc_get_user_info_list({
    ope_user_cd : getLoginUserCD(),
    user_cd   : tgt_user_cd
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("成績データの取得に失敗しました。");
    return;
  }
  updateUserScoreView(service_result.user_list[0]);
}

/**
 * 次のユーザー成績を表示
 */
function onClickedUserScoreDown(){
  current_cursor_index++;
  if (current_cursor_index>=user_score_user_cds.length) current_cursor_index = user_score_user_cds.length - 1;
  var tgt_user_cd = user_score_user_cds[current_cursor_index].user_cd;
  var service_result = boc_get_user_info_list({
    ope_user_cd : getLoginUserCD(),
    user_cd   : tgt_user_cd
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("成績データの取得に失敗しました。");
    return;
  }
  updateUserScoreView(service_result.user_list[0]);
}

/**
 * ユーザー削除クリックイベントハンドラ
 */
function onClickedDeleteUser(user_cd){
  bootbox.confirm({
    title: "削除しますか？",
    message: "ユーザー情報を削除しますか？",
    closeButton: false,
    buttons: {
      confirm: {
        label: '削除'
      },
      cancel: {
        label: 'キャンセル'
      }
    },
    callback: function (result) {
      if (result){
        // 権限チェック
        var check_result = boc_check_use_function({
          func_name : BOC_USE_USER_MANAGE,
          ope_user_cd : getLoginUserCD()
        });
        if (check_result.err_code != BOC_NO_ERROR){
          bootbox.alert("権限がありません。");
          return;
        }
        var service_result = boc_delete_user({
          self_user_cd  : getLoginUserCD(),
          user_cd : user_cd
        });
        if (service_result.err_code != BOC_NO_ERROR){
          bootbox.alert("ユーザー情報の削除に失敗しました。");
          return;
        }

        // レース一覧を更新
        var service_result = boc_get_user_list({
          ope_user_cd : getLoginUserCD()
        });
        if (service_result.err_code != BOC_NO_ERROR){
          bootbox.alert("ユーザー情報リストの取得に失敗しました。");
          return;
        }
        updateUserListView(service_result.user_list);

        bootbox.alert("ユーザー情報を削除しました。");
      }
    }
  });
}

/**
 * ユーザー検索ボタンクリックイベント
 */
function onClickedFilterUserList(){
  var user_name = $("input#s-name").val();
  var filter_param = {};
  if (user_name){
    filter_param['user_name'] = user_name;
  }
  var service_result = boc_get_user_list({
    ope_user_cd : getLoginUserCD(),
    user_name   : user_name
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("ユーザーの検索に失敗しました。");
    return;
  }
  // ユーザーリストを更新
  updateUserListView(service_result.user_list);
}

/* 予想購入ボタンクリックイベントハンドラ */
function showVote(vote_id, is_baught){
  /* 予想未購入なら予想を購入 */
  if (is_baught==0){
    var service_result = boc_buy_vote({
      user_cd : getLoginUserCD(),
      vote_id : vote_id
    });
    if (service_result.err_code==BOC_NOT_ENOUGH_POINT){
      bootbox.alert("ポイントが不足しています。");
      return;
    }
    else if (service_result.err_code != BOC_NO_ERROR){
      bootbox.alert("予想の購入に失敗しました。");
      return;
    }
    // 販売予想一覧を更新
    // 自身の投票データを取得
    var user_cd = getLoginUserCD();
    var service_result = boc_get_vote({
      user_cd   : getLoginUserCD(),
      race_cd   : service_result.buy_race_cd 
    });
    if (service_result.err_code == BOC_NO_ERROR){
      $("#sale_votes").empty();
      /* 販売予想があれば販売予想も表示する */
      if (service_result.sale_vote){
        /* テンプレートを読み込む */
        var tpl_sale = getTemplate('/tpl_sale_vote_item.html');
        var sale_votes = service_result.sale_vote;
        var sale_cnt = sale_votes.length;
        for(let i=0; i<sale_cnt; i++){
          var sale_info = sale_votes[i];
          var add_item = tpl_sale.replace(/{user_name}/g, sale_info['user_name']);
          add_item = add_item.replace(/{vote_id}/g, sale_info['vote_id']);
          add_item = add_item.replace(/{is_baught}/g, sale_info['is_baught']);
          // 既に購入ずみならボタンの文言を変更
          var str_btn = "{sale_pt}ptで購入";
          str_btn = str_btn.replace(/{sale_pt}/g, sale_info['sale_pt']);
          if (sale_info['is_baught']==1){
            str_btn = "予想を見る";
          }
          add_item = add_item.replace(/{str_btn}/g, str_btn);
          // 暫定でランク照合は固定
          add_item = add_item.replace(/{user_ranking}/g, '/img/title_ol.png');

          // 販売予想を追加
          $(add_item).appendTo("#sale_votes");
        }
      }
    }



  }
  /* 購入した予想を取得 */
  var service_result = boc_get_buy_vote({
    user_cd : getLoginUserCD(),
    vote_id : vote_id
  });
  if (service_result.err_code != BOC_NO_ERROR){
    bootbox.alert("予想の取得に失敗しました。");
    return;
  }
  /* 予想をポップアップで表示 */
  var content = getTemplate("/tpl_buy_vote_info.html");
  content = content.replace(/{mark_1}/g, service_result.vote_info['mark1']);
  content = content.replace(/{mark1_name}/g, service_result.vote_info['mark1_name']);
  content = content.replace(/{mark_2}/g, service_result.vote_info['mark2']);
  content = content.replace(/{mark2_name}/g, service_result.vote_info['mark2_name']);
  content = content.replace(/{mark_3}/g, service_result.vote_info['mark3']);
  content = content.replace(/{mark3_name}/g, service_result.vote_info['mark3_name']);
  content = content.replace(/{mark_4}/g, service_result.vote_info['mark4']);
  content = content.replace(/{mark4_name}/g, service_result.vote_info['mark4_name']);
  content = content.replace(/{mark_5}/g, service_result.vote_info['mark5']);
  content = content.replace(/{mark5_name}/g, service_result.vote_info['mark5_name']);
  content = content.replace(/{mark_6}/g, service_result.vote_info['mark6']);
  content = content.replace(/{mark6_name}/g, service_result.vote_info['mark6_name']);
  bootbox.alert({
    message : content,
    backdrop: true,
    locale: 'jp'
  });

}
