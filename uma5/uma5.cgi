#!/usr/bin/perl

#----------------------------------------------------------------------
#	 だぼっちバトルロイヤル ver 1.17 (Free)
#	 製作者	: Alpha-kou.
#	 E-MAIL	: dabo@dabo.design.co.jp
#	 URL	: http://D-BR.net/
#
#        改造者	: ゴードン
#        E-MAIL	: zaza99jp@yahoo.co.jp
#	 URL	: http://godon.bbzone.net/
#
# 使用前にまず利用規定を読んでください
#	http://D-BR.net/kitei.html
#       http://godon.bbzone.net/kitei.html
# [このスクリプトを使用して起きたいかなる損害にも責任は負いません。]
#----------------------------------------------------------------------

$| = 1;
require './jcode.pl';

########## ローカル変数指定
sub kankyou{

# クッキーを取得
        &get_cookie;

# メンテ
        $mente = 0;     # メンテの時は1に
        $mentecom = 'メンテしてます。';  #メンテ時のコメント

# 基本設定

	$cgifile = './uma5.cgi';	# このファイル名
	$logfile = './chara.dat';	# 馬登録ファイル
        $time2file = './time2.dat';	# リーグ時間記録ファイル
	$fightfile = './fightlog.dat';	# 前の試合の記録ファイル
        $commentfile = './comment.dat';	# コメントファイル
        $cntfile = './count.dat';       # カウンタファイル
        $orfile = './orank.dat';	# オーナーランキングファイル
        $tanefile = './tane.dat';	# 種牡馬ファイル
        $tamefile = './tame.dat';	# 繁殖牝馬ファイル
        $syurankfile = './syurank.dat';	# 種牡馬ランキングファイル
        $mesrankfile = './mesrank.dat';	# 繁殖牝馬ランキングファイル
        $winfile = './win.dat';         # チャンピオンファイル
        $lockfile = './lock.dat';         # ロックファイル
        $pastfile = './past.dat';         # 歴代優勝馬ファイル
        $recordsfile = './record.dat';    # レコードファイル
        $backupfile = './backup.dat';    # バックアップファイル
        $gaisenfile = './gaisen.dat';    # 凱旋門賞馬ファイル
        $gaifightfile = './gaifight.dat';    # 凱旋門賞結果ファイル
        $kisyufile = './kisyu.dat';    # 騎手ファイル

	$method = 'POST';	# GET or POSTを指定
	$max_chara = '100';	# 登録馬の最大数
	$max_fight = '3';	# 戦いの記録の最大数
        $max_jyoui = '7';	# ＴＯＰに表示する上位馬の頭数
        $jyouiga = '0';         # ＴＯＰに表示する上位馬に何頭目までアイコンを表示するか

	$title = '激突競馬リーグ';	# ＴＯＰページに表示されるタイトル
	$title2 = '激突競馬リーグ';	# ブラウザに表示されるタイトル
	$acomment = '';		        # タイトル下のコメント（タグ可能）
	$url = '';                      # ホームページのＵＲＬ

	$nameleng = '9';	# 名前の長さを全角何文字までにするか。（馬）
        $nameleng2 = '5';      # 名前の長さを全角何文字までにするか。（人）

# ページ全体（変数の名前はbodyタグそのままです。）

	$bgcolor = 'ffffff';    # default:ffffff     # 背景色
	$text = '000000';       # default:000000
	$link = '0000CD';       # default:0000CD
	$vlink = '6699FF';      # default:6699FF
	$alink = '303030';      # default:303030
        $iroformwaku = 'green'; # フォームボタン周りの色
	$background = '';       # 背景画像
        $backgaisenmon = '';    # 凱旋門時の背景画像
        $ncolor = 'green';      # ニュース時のコメントの色
        $news = 'ニュース';     # ニュース時のタイトル
        $counter = '0';         # カウンターを設置するか（0:しない、1:する）

	$tcolor = '#FF4500';	# タイトルの色
	$tsize = '6';		# タイトルサイズ
        $bbs_name  = '';	# 掲示板の名前
	$bbs_url  = '';         # 掲示板のＵＲＬ

# ゲームバランス諸設定
        $ktime     = '5';    # 日数の変わる時間(0～23)
        $racemax   = '50';   # １シーズン何レースか
        $racemax2  = $racemax - 1;
        $playday   =  '7';   # １シーズン何日か（日）
        $kankaku   =  '3';   # レース間隔（分）
        $max_com   = '10';   # コメントの最大数
        $max_zi    = '35';   # コメントの最大字数
        $taneosu   = '35';   # 牡は何勝以上で種牡馬になるか。
        $tanemesu  = '30';   # 牝は何勝以上で繁殖牝馬になるか。
        $osuintai  = '25';   # 種牡馬は何歳で種牡馬を引退するか。
        $mesuintai = '15';   # 繁殖牝馬は何歳で繁殖牝馬を引退するか。
        $shyoka    = '2';    # リーグ何日目から世代評価を表示するか。
        $iconuse   = '0';    # アイコンを使用するか（0:しない、1:する）
        $imgurl    = '';     # 各自ファルダの絶対パス（最後の / は必要ありません。）

# アイコンリスト
        @icon1 = ('one','two');#アイコンのファイル名(.gifは書かなくて良いです。)

        @icon2 = ('１号','２号');#アイコン名

# ニックス(上が種牡馬、下が繁殖牝馬の血統の時ニックス)、例)エルバジェとグレイソヴリン
# 種牡馬・繁殖牝馬の区別をなくすには上と下を反対にしたものも書く必要があります。
#(スピード)

        @spo = ('エルバジェ','エルバジェ','グレイソヴリン','ボワルセル','ダンテ','ダンテ','ノーザンダンサー','プリンスリーギフト','ノーザンダンサー','テディ','ネイティヴダンサー','ノーザンダンサー','ボールドルーラー','ハイペリオン','マンノウォー','ファイントップ','ニジンスキー','ノーザンダンサー');
        @spm = ('グレイソヴリン','ボワルセル','エルバジェ','エルバジェ','ノーザンダンサー','プリンスリーギフト','ダンテ','ダンテ','テディ','ノーザンダンサー','ノーザンダンサー','ネイティヴダンサー','ハイペリオン','ボールドルーラー','ファイントップ','マンノウォー','ノーザンダンサー','ニジンスキー');

#(瞬発力)

        @syo = ('パーソロン','ボワルセル','ネヴァーベンド','パーソロン','ニジンスキー','ニジンスキー','ニジンスキー','レッドゴッド','レイズアネイティヴ','ネヴァーベンド','ノーザンダンサー','ノーザンダンサー','ノーザンダンサー','ノーザンダンサー','レッドゴッド','リボー','ハイペリオン','ヘイルトゥリーズン');
        @sym = ('ボワルセル','パーソロン','パーソロン','ネヴァーベンド','ネヴァーベンド','レイズアネイティヴ','レッドゴッド','ニジンスキー','ニジンスキー','ニジンスキー','レッドゴッド','リボー','ハイペリオン','ヘイルトゥリーズン','ノーザンダンサー','ノーザンダンサー','ノーザンダンサー','ノーザンダンサー');

$body = "<body bgcolor=\"$bgcolor\" text=\"$text\" alink=\"$alink\" link=\"$link\" vlink=\"$vlink\" background=\"$background\">";

}#end kankyou

srand( time() ^ ( $$ + ( $$ << 15)) );

&kankyou;
&decode;
&readlog;

# 対戦処理
         if($form{'race'} && $lines[1]){require './uma_race.cgi';&syori;&fight;exit;}
# 登録処理
	 if($form{'record'}) {require './uma_umu.cgi';&record;&rec;exit;}
         if($form{'no'}){require './uma_race.cgi';&fight;exit;}
         if($form{'rule'}){&rule;exit;}
         if($form{'rec'}){require './uma_umu.cgi';&seisan;&rec;exit;}
         if($form{'log'}){&log;exit;}
         if($form{'comment'}){&comsyori;}
         if($form{'orank'}){require './uma_rank.cgi';&orank;exit;}
         if($form{'syurank'}){require './uma_rank.cgi';&syurank;exit;}
         if($form{'mode'} eq 'chara' || $form{'chara'}){&chara;exit;}
         if($form{'mode'} eq 'hinba' || $form{'hinba'}){&hinba;exit;}
         if($form{'login'}){&login;exit;}
         if($form{'itiran'}){&itiran;exit;}
         if($form{'mode'} eq 'icon'){&icon;exit;}
         if($form{'mode'} eq 'ketou'){require './uma_umu.cgi';&ketou;exit;}
         if($form{'mode'} eq 'mketou'){require './uma_umu.cgi';&mketou;exit;}
         if($form{'past'}){require './uma_rank.cgi';&past;exit;}
         if($form{'rtime'}){require './uma_rank.cgi';&rtime;exit;}
         if($form{'nameda'}){require './uma_umu.cgi';&umaname;&rec;exit;}
     if($form{'kisyu'} || $form{'mode'} eq 'kisyu'){require './uma_rank.cgi';&kisyu;exit;}
         
&html;
exit;

##### デコード＆ローカル変数へ受け渡し
sub decode{

#入力された値をデコード
	if ($ENV{'REQUEST_METHOD'} eq "GET") {
		$buffer = $ENV{'QUERY_STRING'};
	} elsif ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	}
@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {
	($key, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	&jcode'convert(*value, "sjis");
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;
        $value =~ s/ //g;
        $value =~ s/　//g;
	$form{$key} = $value;
	}

}#end decode

##### ログ読み込み
sub readlog{
	open(DB,"$logfile");
	seek(DB,0,0);  @lines = <DB>;  close(DB);
	
	($lno, $lname, $lsakusya, $lhomepage, $llif, $lpow, $ldef, $lspe, $ldate, $lip, $licon, $lwin, $lsyu, $ltotal, $ltyoushi, $lashi, $losu, $lmesu, $lsei, $lketou, $lbaku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,$lines[0]);

	open(TM,"$timefile");
	seek(TM,0,0);  @times = <TM>;  close(TM);

# 時間の取得

        $times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

###### リーグ日数の更新
        if($ktime >= 24 || $ktime < 0){$ktime=5;}
        open(ST,"$time2file");
	seek(ST,0,0);  @st = <ST>;  close(ST);
        $hour = int(sprintf("%02d",$hour));
        $day = sprintf("%02d",$mday);
        $playdays = $playday + 1;
        ($hiniti, $hi, $zikan, $rigu, $sedai) = split(/<>/, @st[0]);
      if((($hi < $day || $hi - $day > 20) && $hour >= $ktime) || (abs($hi - $day) >= 2 && abs($hi - $day) <= 20)){
        $hiniti++;
        &backup;
      if($hiniti == $playdays){&koushin;$hiniti=1;$rigu++;$sedai=0;}    # リーグ更新処理
        $zikann = "$hiniti<>$day<>$hour<>$rigu<>$sedai<>";
        open(ST,">$time2file") ;
		eval 'flock(ST,2);';
		seek(ST,0,0);	print ST $zikann;
		eval 'flock(ST,8);';
	close(ST);
      }

}#end 

sub backup{      # １日１回バックアップする

        open(LL,"$logfile");
	seek(LL,0,0);  @ll = <LL>;  close(LL);

        open(BK,"$backupfile");
	seek(BK,0,0);  @bk = <BK>;  close(BK);

        if($#ll >= $#bk){
        open(BK,">$backupfile") ;
        eval 'flock(BK,2);';
	seek(BK,0,0);	print BK @ll;
	eval 'flock(BK,8);';
        close(BK);
        }
}#end backup

##### コメント記入処理
sub comsyori{

         # リモートホスト取得
	$host = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};

	if(length($form{'comtext'}) < 1 || length($form{'comtext'}) > $max_zi * 2){&error("字数は$max_zi字までです。");}

        $year += 1900;
	$month = sprintf("%02d",$mon +1);
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
	$ljikan = "$month/$mday $hour:$min";

	open(CF,"+<$commentfile") || &error("指定されたファイルが開けません。");
	eval 'flock(CF,2);';

	@comments = <CF>;

        foreach $line (@comments) {
        &jcode'convert(*line,'sjis');
        local($comm, $host, $name, $time, $kekka) = split(/<>/,$line);
        if($comm eq $form{'comtext'}){&error("すでに同じ書き込みがあります。");}
        if($time eq $ljikan){&error("もう少し時間をあけて書きこんで下さい。");}
        }

        $comkati = $form{'comkati'};
        $commake = $form{'commake'};
        $comsa = $form{'comsa'};
        $comuma = $form{'comuma'};
        if($comkati eq $comuma){
        $kekka = "$comkati ○-$comsa-● $commake";
        }elsif($commake eq $comuma){
        $kekka = "$commake ●-$comsa-○ $comkati";
        }
        if($comkati eq ""){$kekka = "";}
        if($form{'comname'} eq "外人"){
        $kakiko = "$form{'comtext'}<>$host<>凱旋門賞結果<>$ljikan<>$kekka<>\n";
        }else{
	$kakiko = "$form{'comtext'}<>$host<>$form{'comname'}<>$ljikan<>$kekka<>\n";
        }
	unshift(@comments, $kakiko);
	splice(@comments, $max_com);

        truncate (CF, 0); 
	seek(CF,0,0);	print CF @comments;
	close(CF);
	eval 'flock(CF,8);';

}#end comsyori

#####著作権表示

sub chosaku{
&secretcopyright;

print <<"_HTML2_";

<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="5"><tr><td bgcolor="$iroformwaku">
<center><input type="submit" value="トップページ">
<input type="submit" name="rec" value="新規登録">
<input type="submit" name="orank" value="各種ランキング">
<input type="submit" name="itiran" value="競走馬一覧">
<input type="submit" name="past" value="歴代優勝馬">
<input type="submit" name="rtime" value="レコード">
<input type="submit" name="rule" value="ｹﾞーﾑ説明">
<input type="button" value="ﾎｰﾑﾍﾟｰｼﾞ" onClick="top.location.href='$url'">
</td></tr></table>
</form>

_HTML2_

print <<"_CHOSAKU_";

<hr size="1">
<div align="right"><a href="http://godon.bbzone.net/" target=_blank>激突競馬リーグver1.01β(Free)</a>
<br>

<a href="http://D-BR.net/" target=_blank>オリジナル版/だぼっちバトルロイヤルver1.17(Free)</a></div>
<!--広告バナー挿入位置、ページ下部-->
</html>
_CHOSAKU_

}#end chosaku

##### 出力
sub html{

        if($mente eq "1"){&error("只今設定変更中です。<br><br>$mentecom");}

if ($title){$acomment = "<BR><BR>$acomment";}

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis">
$body

<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
</head>

<center><font color="$tcolor" size=6><B>$title</B></font>$acomment<P>
<a href=$bbs_url target=_blank>$bbs_name</a>
_HTML1_

        open(ST,"$time2file");
	seek(ST,0,0);  @st = <ST>;  close(ST);
        @st = split(/<>/,@st[0]);

        if($st[0] == 1){$hizuke = "初日";}
     elsif($st[0] == $playday){$hizuke = "最終日";}
                     else{$hizuke = "$st[0]日目";}

        if($st[4] >= 500){$reveru = "[世代評価：至高の最強世代]";}
     elsif($st[4] >= 300){$reveru = "[世代評価：最強世代]";}
     elsif($st[4] >= 100){$reveru = "[世代評価：一頭抜けている]";}
     elsif($st[4] >= 2){$reveru = "[世代評価：中堅世代]";}
                     else{$reveru = "[世代評価：貧弱世代]";}
print "<P>（第$st[3]回）<font size=5><b>$hizuke</b></font>（$playday日間$racemaxレース）";

if($counter){
           &counter;
           }
        if($st[0] >= $shyoka){
        print "$reveru";}
print "（$ktime時更新）";
	open(FG,"$fightfile");                # レースの記録
	seek(FG,0,0);  @fg = <FG>;  close(FG);
       
        print "<DIV align=center><TABLE width=700 cellpadding=0 cellspacing=10><TBODY><tr><td valign=top><table border=2 width=220><td valign=top bgcolor=green><center>レースの記録</center></td>\n";
	for ($i=0 ; $i<$max_fight ; $i++){
	$fgno = $i +1;
	
	if($fg[$i]){
	($time , $name , $name2 , $fight) = split(/<>/,$fg[$i]);
	print "<tr><td><center><a href=\"$cgifile?no=$fgno\">$time</a><br>$nameＶＳ$name2</center></td>\n";
	}
	}
        print "</table></center>";

        print "<DIV align=center><td><table border=2 width=500><tr><td width=30 bgcolor=green><center>順位</td><td width=170 bgcolor=green><center>馬名</td><td width=150 bgcolor=green><center>馬主名</td><td width=75 bgcolor=green><center>勝</td><td width=75 bgcolor=green><center>敗</td></tr>";

        open(XD,"$logfile");
	seek(XD,0,0);  @nowue = <XD>;  close(XD);    # 現在の上位

        for ($i=0 ; $i<$max_jyoui ; $i++){
	($nowno[$i], $nowname[$i], $nowsakusya[$i], $nowhomepage[$i], $nowlif[$i], $nowpow[$i], $nowdef[$i], $nowspe[$i], $nowdate[$i], $nowip[$i], $nowicon[$i], $nowwin[$i], $nowsyu[$i], $nowtotal[$i], $nowtyoushi[$i], $nowashi[$i], $nowosu[$i], $nowmesu[$i], $nowsei[$i], $nowketou[$i], $nowbaku[$i], $nowpass[$i], $gazou[$i], $rennsyou[$i], $maxren[$i], $records[$i], $records16[$i], $records18[$i], $records22[$i], $records24[$i], $nowst[$i], $titi[$i], $tiha[$i], $tititi[$i], $titiha[$i], $tihati[$i], $tihaha[$i], $hati[$i], $haha[$i], $hatiti[$i], $hatiha[$i], $hahati[$i], $hahaha[$i], $checkketou1[$i], $checkketou2[$i], $checkketou3[$i], $tokusyu[$i], $formkon[$i], $dmy, $dmy, $dmy) = split (/<>/, $nowue[$i]);
        $nowlose[$i] = $nowtotal[$i] - $nowwin[$i];

        if($nowhomepage[$i]){$nowsakusya[$i] = "<a href=\"$nowhomepage[$i]\" target=_blank>$nowsakusya[$i]</a>";}
        }
        for ($i=0 ; $i<$max_jyoui ; $i++){
        $jj = $i+1;
        if($i<$jyouiga && $iconuse eq "1"){$ga[$i] = "<img src = $imgurl/$gazou[$i]>";}
        print "<tr><td><center>$jj位</td><td>$ga[$i]<center>$nowname[$i]</td><td><center>$nowsakusya[$i]</td><td><B><center>$nowwin[$i]</B>勝</td><td><center>$nowlose[$i]敗</td></tr>";
        }

        print "</table><tr><td>";

        print <<"_HTML1_";
<DIV align=center>
<table border=2 width=200><tr><td>
<form action="$cgifile" method="$method">
<center><input type="text" name="loginname" value="$c_name" size="16">：名前<br>
<input type="password" name="loginpass" value="$c_pass" size="10">：パスワード<BR><br>
<input type="submit" name="login" value="ログイン"></center></td></tr></table></td>

_HTML1_

        open(WI,"$winfile");
	seek(WI,0,0);  @nowwin = <WI>;  close(WI);    # チャンピオンを調べる

        ($nowno, $nowname, $nowsakusya, $nowhomepage, $nowlif, $nowpow, $nowdef, $nowspe, $nowdate, $nowip, $nowicon, $nowwin, $nowsyu, $nowtotal, $nowtyoushi, $nowashi, $nowosu, $nowmesu, $nowsei, $nowketou, $nowbaku, $nowpass, $nowgazou, $nowrennsyou, $nowmaxren, $records, $records16, $records18, $records22, $records24, $nowst, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/, @nowwin[0]);
        $nowlose = $nowtotal - $nowwin;
        if($nowrennsyou < 0){$nowrennsyou = 0;}
        if($nowhomepage){$nowsakusya = "<a href=\"$nowhomepage\" target=_blank>$nowsakusya</a>";}
        if($nowrennsyou eq ""){$nowrennsyou = 0;}
        if(@nowwin[0] eq ""){
        print "<DIV align=center><td><br><center><table border=2 width=400 cellspacing=0 cellpadding=5><tr align=center><td><font color=\"DD9966\"><B><br>現在登録者待ち<br><br></B></td></tr></table><br>";
        }else{
        if($iconuse){$use="<img src=$imgurl/$nowgazou>";}else{$use = "";}
        print "<DIV align=center><td><br><center><table border=2 width=400 cellspacing=0 cellpadding=5><tr align=center><td><font color=\"DD9966\"><B>現在のチャンピオン　　　<font color=gold>$nowrennsyou</B>連勝中</font><br></font>$use $nowname 【 馬主 : $nowsakusya 】 $nowwin勝 $nowlose敗<br></td></tr></table><br>";
        }
print <<"_HTML2_";
</table>
</TBODY> 
</table>
</DIV>

<center>
_HTML2_

open(CF,"$commentfile") || &error('指定されたファイルが開けません。');
	seek(CF,0,0);  @comments = <CF>;  close(CF);

	print "<br><table border=2 width=\"760\" cellpadding=5 cellspacing=0>\n";
	print "<tr align=\"center\"><td bgcolor=green>コメント（字数は$max_zi字までです。）</td></tr>\n";
	print "<tr><td>\n";
        
	$i = 0;
	foreach $comments (@comments){
		($com, $host, $name, $time, $kekka) = split (/<>/, $comments);
        
	if($name eq "$news" && $kekka eq ""){print "<font color=$ncolor>■$name 『 $com 』 ($time)</font>\n";}
     elsif($name eq "$news" && $kekka ne ""){print "<font color=$ncolor>■$name 『 $com 』 【 $kekka 】($time)</font>\n";}
     elsif($kekka eq ""){   print "■$name 『 $com 』  ($time)\n";}
        else{   print "■$name 『 $com 』 【 $kekka 】 ($time)\n";}

		if($i ne $#comments){ print "<hr width=\"100%\" size=1>\n"; }
		$i++;
	}
	print "</table><br></table></center>\n";

&chosaku;

}#end html

##### ログイン画面
sub login{

         $loginname = $form{'loginname'};
         $loginpass = $form{'loginpass'};
         $logpass = "0";

         if($loginname eq "" || $loginpass eq ""){&error('入力されてません。');}

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis">
$body

<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
</head>

_HTML1_

       open(LO,"$logfile");
       seek(LO,0,0);  @login = <LO>;  close(LO);

        foreach $login (@login) {
	($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $osu, $mesu, $sei, $ketoui, $baku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,$login);

   if($loginname eq $sakusya && $loginpass eq $pass){

        $check = "$login";
        @check = split(/<>/,$check);
        @iro="";

   for ($k=16; $k<43; $k++){
         if($k == 42 || $k == 38){($check, $ketou, $tokusyu) = split(/<mm>/,$check[$k]);}
         else{($check, $tokusyu) = split(/<mm>/,$check[$k]);}
         if($tokusyu ne ""){$check[$k]="$check<img src=\"$imgurl/$tokusyu.gif\">";}else{
         $check[$k]="$check";}
    if($k == 17){$k = 30;}
    }

    for ($k=31; $k<43; $k++){
         ($check, $tokusyu) = split(/<mm>/,$check[$k]);
      for ($kk=31; $kk<43; $kk++){
         ($check2, $tokusyu2) = split(/<mm>/,$check[$kk]);
         if($check eq $check2 && $k ne $kk){push(@iro, $k);}
       else{
         if($tokusyu ne ""){$check[$k]="$check<img src=\"$imgurl/$tokusyu.gif\">";}else{
         $check[$k]="$check";}}
      }
   }
       foreach $line (@iro) {
        ($check, $tokusyu) = split(/<mm>/,$check[$line]);
         if($tokusyu ne ""){$check[$line]="<font color=red>$check</font><img src=\"$imgurl/$tokusyu.gif\">";}else{
         $check[$line]="<font color=red>$check</font>";}
       }

           if($win > 34 && $sei eq "牡"){$kongo = "種牡馬";}
        elsif($win > 29 && $sei eq "牝"){$kongo = "繁殖牝馬";}
        elsif($icon eq "uma10.gif" || $icon eq "uma9.gif"){$kongo = "誘導馬";}
        elsif($win > 19){$kongo = "乗馬";}
        elsif($win > 9){$kongo = "雑用";}
         else{$kongo = "肉";}
        
        if($icon eq "uma1.gif"){$iconn="鹿毛";}
        elsif($icon eq "uma2.gif"){$iconn="黒鹿毛";}
        elsif($icon eq "uma3.gif"){$iconn="栃栗毛";}
        elsif($icon eq "uma4.gif"){$iconn="栗毛";}
        elsif($icon eq "uma5.gif"){$iconn="尾花栗毛";}
        elsif($icon eq "uma6.gif"){$iconn="青鹿毛";}
        elsif($icon eq "uma7.gif"){$iconn="青毛";}
        elsif($icon eq "uma8.gif"){$iconn="芦毛(濃)";}
        elsif($icon eq "uma9.gif"){$iconn="芦毛(薄)";}
        else{$iconn="白毛";}

        $icon_pri = "<img src=\"$imgurl/$icon\" alt=\"$iconn\">";
        
        if   ($tyoushi < 2){ $cond = "1.gif"; }
	elsif($tyoushi < 4){ $cond = "2.gif"; }
	elsif($tyoushi < 7){ $cond = "3.gif"; }
	elsif($tyoushi < 9){ $cond = "4.gif"; }
	elsif($tyoushi < 11){$cond = "5.gif"; }

        $pows = ($pow-20)*20;
        $defs = ($def-20)*20;
        $spes = ($spe-20)*20;
        $sts = ($st-20)*20;
        $kon = ($formkon)*20;

        $lose = $total - $win;
        ($hunt, $byout, $nant) = split(/<t>/,$records);
        if($hunt eq ""){$hjuy20 = "未出走";}
        else{$hjuy20 = "$hunt′$byout″$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records16);
        if($hunt eq ""){$hjuy16 = "未出走";}
        else{$hjuy16 = "$hunt′$byout″$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records18);
        if($hunt eq ""){$hjuy18 = "未出走";}
        else{$hjuy18 = "$hunt′$byout″$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records22);
        if($hunt eq ""){$hjuy22 = "未出走";}
        else{$hjuy22 = "$hunt′$byout″$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records24);
        if($hunt eq ""){$hjuy24 = "未出走";}
        else{$hjuy24 = "$hunt′$byout″$nant";}

        $sup = int(800+ (40 * $st));   # 最長
        $inf = int($sup - (13 * $spe));   # 最短

print <<"_HTML_";

<center>
<table border="2" width=640 cellpadding="0">
<tr><td width=170><br><center>馬名：<b>$name</b>($sei)<br><br>
$icon_pri<br><br>
<img src=\"$imgurl/$cond\"><br><br>
馬主：<b>$sakusya</b><br>
</td><td rowspan=2>

<table border=1 cellspacing=0 cellpadding=4>
<tr>
<td rowspan=4 bgcolor=#1E90FF width=150>$check[16]

<p><a href=\"$cgifile?mode=chara\" target=\~_blank\">種牡馬一覧</font></a>
<br><a href=\"$cgifile?mode=ketou\" target=\~_blank\">種牡馬血統詳細</font></a>

</td>
<td rowspan=2 bgcolor=#1E90FF width=150>$check[31]</td>
<td bgcolor=#1E90FF width=150>$check[33]</td></tr><tr>
<td bgcolor=#FF69B4>$check[34]</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>$check[32]</td>
<td bgcolor=#1E90FF>$check[35]</td></tr><tr>
<td bgcolor=#FF69B4>$check[36]</td>
</tr><tr>
<td rowspan=4 bgcolor=#FF69B4>$check[17]
<P><a href=\"$cgifile?mode=hinba\" target=\~_blank\">繁殖牝馬一覧</font></a>
<br><a href=\"$cgifile?mode=mketou\" target=\~_blank\">繁殖牝馬血統詳細</font></a>

</td>
<td rowspan=2 bgcolor=#1E90FF>$check[37]</td>
<td bgcolor=#1E90FF>$check[39]</td></tr><tr>
<td bgcolor=#FF69B4>$check[40]</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>$check[38]</td>
<td bgcolor=#1E90FF>$check[41]</td></tr><tr>
<td bgcolor=#FF69B4>$check[42]</td>
</tr>
</table>

</td></tr>
<tr><td><center>$total回出走：$win勝$lose敗

</td></tr></table>

<table border=1 width=630 background=$imgurl/memori.gif><tr><td>
<table border=0  width=630 cellspacing=3 align=center><tr></center>
<td bgcolor=#00008B width=$pows></td><td>スピード</td></tr></table>
<table border=0 width=630 cellspacing=3 align=center><tr></center>
<td bgcolor=#000080 width=$defs></td><td>瞬発力</td></tr></table>
<table border=0 width=630 cellspacing=3 align=center><tr></center>
<td bgcolor=#00008B width=$spes></td><td>気性</td></tr></table>
<table border=0 width=630 cellspacing=3 align=center><tr></center>
<td bgcolor=#000080 width=$sts></td><td>スタミナ</td></tr></table>
<table border=0 width=630 cellspacing=3 align=center><tr></center>
<td bgcolor=#000080 width=$kon></td><td>勝負根性</td></tr></table>
</td></tr></table><center>

<table border=1 width=640 cellpadding=0>
<tr>
<td bgcolor=green width=120><center>適性距離</td>
<td bgcolor=green><center>1600m</td>
<td bgcolor=green><center>1800m</td>
<td bgcolor=green><center>2000m</td>
<td bgcolor=green><center>2200m</td>
<td bgcolor=green><center>2400m</td>
</tr><tr>
<td><center>$inf～$sup</td>
<td><center>$hjuy16</td>
<td><center>$hjuy18</td>
<td><center>$hjuy20</td>
<td><center>$hjuy22</td>
<td><center>$hjuy24</td>
</tr>
</table>
<P>

_HTML_

   $logpass = "1";last;}
       }# end foreach
       
       if(!$logpass){$wawa=1;&error('パスワードか名前が違います。');}

       ($gmonth, $gday, $ghour, $gmin) = split(/<g>/,$date);   # 最終レース時間

	$times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

	$tmonth = sprintf("%02d",$mon +1);     # 現在の時間
	$tday = sprintf("%02d",$mday);
	$thour = sprintf("%02d",$hour);
	$tmin = sprintf("%02d",$min);

print "<form action=$cgifile method=$method>";

      if($gmonth == $tmonth && $gday == $tday && $ghour == $thour && abs($gmin - $tmin) < $kankaku){
$mate = $kankaku - abs($gmin - $tmin);

print "<br>あと$mate分待っててね。<br><br>";

       }elsif($no eq "-1"){
print <<"_HTML_";

<P>上記の馬は引退しました。<P>
<input type="hidden" name="logint" value="$loginname">
<input type="hidden" name="tourou" value="5">
<input type="submit" name="rec" value="今シーズン用の競争馬の登録"><P>
_HTML_

       }elsif($no eq "-2"){

       open(KK,"$kisyufile");
       seek(KK,0,0);  @kk = <KK>;  close(KK);
       @kisyu="";
       for ($i=0; $i<$#kk+1; $i++){
       ($name[$i], $comm[$i], $win[$i], $lose[$i], $omona[$i], $omona2[$i], $dmy) = split(/<>/,$kk[$i]);
       $kisyu[$i]=$name[$i];
       }

       @sakusen = ('大逃','逃げ','先行','差し','追込');
print"<P>優勝馬として凱旋門賞に挑戦することが決まりました。<P>\n";
print"<select name=syu>\n";
foreach (@kisyu) {
		if ($_ eq "$syu") { print "<option value=\"$_\" selected>$_\n"; }
		else { print "<option value=\"$_\">$_\n"; }
	}
print"</select><a href=\"$cgifile?mode=kisyu\" target=\"_blank\">騎手一覧</a>\n";
print"<select name=sakusen>\n";
foreach (@sakusen) {
		if ($_ eq "$ashi") { print "<option value=\"$_\" selected>$_\n"; }
		else { print "<option value=\"$_\">$_\n"; }
	}
print"</select>\n";
print"<input type=hidden name=logint value=$loginname>\n";
print"<input type=hidden name=gaisen value=7>\n";
print"<input type=submit name=race value=凱旋門賞に挑戦><br><br>\n";


       }elsif($name eq "名無し"){

print <<"_HTML_";

<P>$seiの仔が生まれました。名前をつけて下さい。（$nameleng文字以下）<P>
<input type="text" name="umaname" size=25>
<input type="hidden" name="comsaku" value="$loginname">
<input type="submit" name="nameda" value="名前決定"><br><br>
_HTML_

       }elsif($total < $racemax){

       open(KK,"$kisyufile");
       seek(KK,0,0);  @kk = <KK>;  close(KK);
       @kisyu="";
       for ($i=0; $i<$#kk+1; $i++){
       ($name[$i], $comm[$i], $win[$i], $lose[$i], $omona[$i], $omona2[$i], $dmy) = split(/<>/,$kk[$i]);
       $kisyu[$i]=$name[$i];
       }

       @sakusen = ('大逃','逃げ','先行','差し','追込');
print"<select name=syu>\n";
foreach (@kisyu) {
		if ($_ eq "$syu") { print "<option value=\"$_\" selected>$_\n"; }
		else { print "<option value=\"$_\">$_\n"; }
	}
print"</select><a href=\"$cgifile?mode=kisyu\" target=\"_blank\">騎手一覧</a>\n";
print"<select name=sakusen>\n";
foreach (@sakusen) {
		if ($_ eq "$ashi") { print "<option value=\"$_\" selected>$_\n"; }
		else { print "<option value=\"$_\">$_\n"; }
	}
print"</select>\n";
print"<input type=hidden name=logint value=$loginname>\n";
print"<input type=submit name=race value=レース開始><P>\n";

       }else{

print "<br>シーズン終了($kongo)<br>";

      }
print <<"_HTML2_";

<center>コメント
<input type="text" name="comtext" size=75>
<input type="hidden" name="comname" value="$loginname">
<input type="submit" name="comment" value="書き込む">
<input type="submit" value="トップページ"></form>

_HTML2_

&chosaku;

}#end login

##### 競走馬一覧
sub itiran{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<!--広告バナー挿入位置、ページ上部-->
<center><font color="$tcolor" size="5"><B>競走馬一覧</B></font><P>
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>

<table border="1" width="790">

<tr>
<td bgcolor=green width=50><center>順位</td>
<td bgcolor=green width=180><center>馬名（性別）</td>
<td bgcolor=green width=50><center>ﾚｰｽ</td>
<td bgcolor=green width=50><center>勝ち</td>
<td bgcolor=green width=50><center>負け</td>
<td bgcolor=green width=50><center>連勝</td>
<td bgcolor=green width=60><center>勝率</td>
<td bgcolor=green width=70><center>主戦</td>
<td bgcolor=green width=70><center>脚質</td>
<td bgcolor=green width=70><center>毛色</td>
<td bgcolor=green width=110><center>馬主</td>
</tr>

_HTML1_

        open(LL,"$logfile");
	seek(LL,0,0);  @itiran = <LL>;  close(LL);
if($#itiran > 20){
$gg = 19;
}else{$gg = $#itiran;}
$ggg=$gg+1;
       for ($g=0; $g<$ggg; $g++){
       ($no[$g], $name[$g], $sakusya[$g], $homepage[$g], $lif[$g], $pow[$g], $def[$g], $spe[$g], $date[$g], $ip[$g], $icon[$g], $win[$g], $syu[$g], $total[$g], $tyoushi[$g], $ashi[$g], $osu[$g], $mesu[$g], $sei[$g], $ketou[$g], $baku[$g], $pass[$g], $gazou[$g], $rennsyou[$g], $maxren[$g], $records[$g], $records16[$g], $records18[$g], $records22[$g], $records24[$g], $st[$g], $titi[$g], $tiha[$g], $tititi[$g], $titiha[$g], $tihati[$g], $tihaha[$g], $hati[$g], $haha[$g], $hatiti[$g], $hatiha[$g], $hahati[$g], $hahaha[$g], $checkketou1[$g], $checkketou2[$g], $checkketou3[$g], $dmy, $formkon[$g], $dmy, $dmy, $dmy) = split(/<>/,$itiran[$g]);

        if($homepage[$g]){$sakusya[$g] = "<a href=\"$homepage[$g]\" target=_blank>$sakusya[$g]</a>";}
        @keiroo = ('','鹿毛','黒鹿毛','栃栗毛','栗毛','尾花栗毛','青鹿毛','青毛','芦毛(濃)','芦毛(薄)','白毛');
        for ($y=1; $y<11; $y++){
        if($icon[$g] eq "uma$y.gif"){$icon[$g] = $y;}
        }
        $keiro[$g] =  "$keiroo[$icon[$g]]";
        if($total[$g] == $racemax){$gcolor[$g]=green}
        $lose[$g] = $total[$g] - $win[$g];
        if($total[$g] eq "0"){$ritu[$g] = "未出走";}else{
        $ritu[$g] = sprintf("%03d", ($win[$g]/$total[$g]) * 1000);}
        $gg = $g+1;

	print "<tr><td><center>$gg位</td><td><center><b>$name[$g]($sei[$g])</b></td><td><center><font color=$gcolor[$g]>$total[$g]</font></td><td><center>$win[$g]</td><td><center>$lose[$g]</td><td><center>$maxren[$g]</td><td><center>.$ritu[$g]</td><td><center>$syu[$g]</td><td><center>$ashi[$g]</td><td><center>$keiro[$g]</td><td><center>$sakusya[$g]</td></tr>\n";
                }

        print "</table><P><center>";

    if($#itiran > 20){
        print "<select>";
        for ($g=20; $g<$#itiran+1; $g++){
	($no[$g], $name[$g], $sakusya[$g], $homepage[$g], $lif[$g], $pow[$g], $def[$g], $spe[$g], $date[$g], $ip[$g], $icon[$g], $win[$g], $syu[$g], $total[$g], $tyoushi[$g], $ashi[$g], $osu[$g], $mesu[$g], $sei[$g], $ketou[$g], $baku[$g], $pass[$g], $gazou[$g], $rennsyou[$g], $maxren[$g], $records[$g], $records16[$g], $records18[$g], $records22[$g], $records24[$g], $st[$g], $titi[$g], $tiha[$g], $tititi[$g], $titiha[$g], $tihati[$g], $tihaha[$g], $hati[$g], $haha[$g], $hatiti[$g], $hatiha[$g], $hahati[$g], $hahaha[$g], $checkketou1[$g], $checkketou2[$g], $checkketou3[$g], $dmy, $formkon[$g], $dmy, $dmy, $dmy) = split(/<>/,$itiran[$g]);
        $gg = $g + 1;
        $lose[$g] = $total[$g] - $win[$g];
        print "<option>[$gg] $total[$g]レース $win[$g]勝 $lose[$g]敗 $name[$g] （$sakusya[$g]）\n";
     }
	print "</select></table>";
        }
&chosaku;

}#end itiran


##### アイコン一覧
sub icon{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<!--広告バナー挿入位置、ページ上部-->
<center><font color="red" size="5"><b>アイコン一覧</b></font><P>

_HTML1_

print "<table width=400 border=1><tr>";
          $iconsuu=0;
      for ($i=0; $i<$#icon1+1; $i++){
          $iconsuu++;
          if($iconsuu eq "4"){$iconsuu=0;
      print "<td><br><center><img src=$imgurl/$icon1[$i].gif><br><center>$icon2[$i]</font></td></tr><tr>";
          }else{
      print "<td><br><center><img src=$imgurl/$icon1[$i].gif><br><center>$icon2[$i]</font></td>";
          }
      }

print "</table></TBODY></TABLE></DIV>";

&chosaku;

}#end icon

##### 種牡馬一覧
sub chara{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<!--広告バナー挿入位置、ページ上部-->
<center><font color="$tcolor" size="5"><B>種牡馬一覧</B></font><P>
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>

<form action="$cgifile" method="$method">
<input type="hidden" name="chara" value=1>
<input type="submit" name="toshi"  value="年齢">
　　<input type="submit" name="syu"  value="名前">
　　<input type="submit" name="ketou"  value="血統">
　　<input type="submit" name="uma"  value="毛色">
　　<input type="submit" name="sp"  value="ｽﾋﾟｰﾄﾞ">
　　<input type="submit" name="syun"  value="瞬発力">
　　<input type="submit" name="ki"  value="気性">
　　<input type="submit" name="kon"  value="勝負根性">
　　<input type="submit" name="teki"  value="距離適性">
　　<input type="submit" name="baku"  value="爆発力">
</form>

<table border="1" width="720"><tr>
<td bgcolor=green><center>年齢</td>
<td bgcolor=green width=140><center>名前</td>
<td bgcolor=green width=140><center>血統</td>
<td bgcolor=green><center>毛色</td>
<td bgcolor=green><center>ｽﾋﾟｰﾄﾞ</td>
<td bgcolor=green><center>瞬発力</td>
<td bgcolor=green><center>気性</td>
<td bgcolor=green><center>勝負根性</td>
<td bgcolor=green><center>距離適性</td>
<td bgcolor=green><center>爆発力</td></tr>
_HTML1_

        open(TK,"$tanefile");
        seek(TK,0,0);  @tk = <TK>;  close(TK);
        if($form{'toshi'}){$snumber = 8;}
     elsif($form{'syu'}){$snumber = 0;}
     elsif($form{'ketou'}){$snumber = 1;}
     elsif($form{'kon'}){$snumber = 2;}
     elsif($form{'uma'}){$snumber = 6;}
     elsif($form{'sp'}){$snumber = 3;}
     elsif($form{'syun'}){$snumber = 4;}
     elsif($form{'ki'}){$snumber = 5;}
     elsif($form{'teki'}){$snumber = 9;} 
     elsif($form{'baku'}){$snumber = 7;}
      else{$snumber = 0;}

        if($snumber == 0 || $snumber == 1 || $snumber == 6 || $snumber == 7){
   @sortdata = sort { (split(/<>/,$a))[$snumber] cmp (split(/<>/,$b))[$snumber] } @tk;}
        else{
   @sortdata = sort { (split(/<>/,$b))[$snumber] <=> (split(/<>/,$a))[$snumber] } @tk;}

        foreach $line (@sortdata) {
	($tanename, $kettou, $formkon, $supi, $syun, $kisei, $keiro, $baku, $toshi, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha) = split(/<>/,$line);

        ($tane, $tokusyu) = split(/<mm>/,$tanename);

        if($keiro eq "uma1.gif"){$iconn="鹿毛";}
        elsif($keiro eq "uma2.gif"){$iconn="黒鹿毛";}
        elsif($keiro eq "uma3.gif"){$iconn="栃栗毛";}
        elsif($keiro eq "uma4.gif"){$iconn="栗毛";}
        elsif($keiro eq "uma5.gif"){$iconn="尾花栗毛";}
        elsif($keiro eq "uma6.gif"){$iconn="青鹿毛";}
        elsif($keiro eq "uma7.gif"){$iconn="青毛";}
        elsif($keiro eq "uma8.gif"){$iconn="芦毛(濃)";}
        elsif($keiro eq "uma9.gif"){$iconn="芦毛(薄)";}
        else{$iconn="白毛";}

        $icon_pri = "<img src=\"$imgurl/$keiro\" align=\"absmiddle\" alt=\"$iconn\">";

        &nouhan;

print "<tr><td><center>$toshi歳</td><td><center><B>$tane</B></td><td><center>$kettou系</td><td><center>$icon_pri</td><td><center>$s</td><td><center>$ss</td><td><center>$sss</td><td><center>$sssss</td><td><center>$ssss</td><td><center>$baku</td></tr>";
      }

print "</table>";

&chosaku;

}#end chara


##### 繁殖牝馬一覧
sub hinba{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<!--広告バナー挿入位置、ページ上部-->
<center><font color="$tcolor" size="5"><B>繁殖牝馬一覧</B></font><P>
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>

<form action="$cgifile" method="$method">
<input type="hidden" name="hinba" value=1>
<input type="submit" name="toshi"  value="年齢">
　　<input type="submit" name="syu"  value="名前">
　　<input type="submit" name="ketou"  value="血統">
　　<input type="submit" name="uma"  value="毛色">
　　<input type="submit" name="sp"  value="ｽﾋﾟｰﾄﾞ">
　　<input type="submit" name="syun"  value="瞬発力">
　　<input type="submit" name="ki"  value="気性">
　　<input type="submit" name="kon"  value="勝負根性">
　　<input type="submit" name="teki"  value="距離適性">
</form>

<table border="1" width="680"><tr>
<td bgcolor=green><center>年齢</td>
<td bgcolor=green width=150><center>名前</td>
<td bgcolor=green width=150><center>血統</td>
<td bgcolor=green><center>毛色</td>
<td bgcolor=green><center>ｽﾋﾟｰﾄﾞ</td>
<td bgcolor=green><center>瞬発力</td>
<td bgcolor=green><center>気性</td>
<td bgcolor=green><center>勝負根性</td>
<td bgcolor=green><center>距離適性</td>
</tr>
_HTML1_

        open(TK,"$tamefile");
        seek(TK,0,0);  @mk = <TK>;  close(TK);
        if($form{'toshi'}){$mnumber = 8;}   #
     elsif($form{'syu'}){$mnumber = 0;}
     elsif($form{'ketou'}){$mnumber = 1;}
     elsif($form{'kon'}){$mnumber = 2;}
     elsif($form{'uma'}){$mnumber = 6;}
     elsif($form{'sp'}){$mnumber = 3;}      #
     elsif($form{'syun'}){$mnumber = 4;}    #
     elsif($form{'ki'}){$mnumber = 5;}      #
     elsif($form{'teki'}){$mnumber = 9;}    #
     elsif($form{'baku'}){$mnumber = 7;}
      else{$mnumber = 0;}

        if($mnumber == 0 || $mnumber == 1 || $mnumber == 6 || $mnumber == 7){
   @sortdata = sort { (split(/<>/,$a))[$mnumber] cmp (split(/<>/,$b))[$mnumber] } @mk;}
        else{
   @sortdata = sort { (split(/<>/,$b))[$mnumber] <=> (split(/<>/,$a))[$mnumber] } @mk;}

        foreach $line (@sortdata) {
	($tanename, $kettou, $formkon, $supi, $syun, $kisei, $keiro, $baku, $toshi, $st, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha) = split(/<>/,$line);
         ($tane, $tokusyu) = split(/<mm>/,$tanename);
        ($checkname2, $checkketou2) = split(/<mm>/,$haha);
        $hinhaha    = $checkketou2; # 母母
        ($checkname3, $checkketou3) = split(/<mm>/,$hahaha);
        $hinhahaha  = $checkketou3; # 母母母

                if($keiro eq "uma1.gif"){$iconn="鹿毛";}
        elsif($keiro eq "uma2.gif"){$iconn="黒鹿毛";}
        elsif($keiro eq "uma3.gif"){$iconn="栃栗毛";}
        elsif($keiro eq "uma4.gif"){$iconn="栗毛";}
        elsif($keiro eq "uma5.gif"){$iconn="尾花栗毛";}
        elsif($keiro eq "uma6.gif"){$iconn="青鹿毛";}
        elsif($keiro eq "uma7.gif"){$iconn="青毛";}
        elsif($keiro eq "uma8.gif"){$iconn="芦毛(濃)";}
        elsif($keiro eq "uma9.gif"){$iconn="芦毛(薄)";}
        else{$iconn="白毛";}

        $icon_pri = "<img src=\"$imgurl/$keiro\" align=\"absmiddle\" alt=\"$iconn\">";

        &nouhan;

print "<tr><td><center>$toshi歳</td><td><center><B>$tane</B></td><td><center><B>$kettou系</B><br><font size=1>$hinhaha系<br>$hinhahaha系</font></td><td><center>$icon_pri</td><td><center>$s</td><td><center>$ss</td><td><center>$sss</td><td><center>$sssss</td><td><center>$ssss</td></tr>";
      }
print "</table>";

&chosaku;

}#end hinba

#######  カウンタ処理

sub counter{
	local($cnt,$host);

# カウントファイルを読みこみ
	open(IN,"$cntfile") || &error("Open Error : $cntfile");
	eval "flock(IN, 1);";
        $data = <IN>;
	close(IN);

# リモートホスト取得
	$hostt = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};

# 別ＩＰ時のみカウントアップ
        ($cnt, $host) = split(/<>/, $data);
        if($host ne $hostt){
        $cnt++;
	open(OUT,"+< $cntfile") || &error("Write Error : $cntfile");
	eval "flock(OUT, 2);";
	truncate(OUT, 0);
	seek(OUT, 0, 0);
	print OUT "$cnt\<>$hostt";
	close(OUT);
	}

# カウンタ表示
	if($counter){
		print "<p>$cnt人の観戦者\n";
	}
}#end counter

#######  クッキーの発行

sub set_cookie{
	$ENV{'TZ'} = "GMT"; # 国際標準時を取得
	local($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg)=localtime(time+60*24*60*60);
	$yearg += 1900;
	if ($secg  < 10)  { $secg  = "0$secg";  }
	if ($ming  < 10)  { $ming  = "0$ming";  }
	if ($hourg < 10)  { $hourg = "0$hourg"; }
	if ($mdayg < 10)  { $mdayg = "0$mdayg"; }
	$month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mong];
	$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')[$wdayg];
	$ENV{'TZ'} = "Japan";
	$date_gmt = "$youbi, $mdayg\-$month\-$yearg $hourg:$ming:$secg GMT";

       $cookies="name\<>$formname\,hp\<>$formhp\,pass\<>$formpass";
	print "Set-Cookie: UMA=$cookies; expires=$date_gmt\n";
}#end set_cookie

#######  クッキーを取得

sub get_cookie{ 
    @pairs = split(/\;/, $ENV{'HTTP_COOKIE'});
    foreach $pair (@pairs) {
      local($name, $value) = split(/\=/, $pair);
      $name =~ s/ //g;
      $DUMMY{$name} = $value;
    }
    @pairs = split(/\,/, $DUMMY{'UMA'});
    foreach $pair (@pairs) {
      local($name, $value) = split(/\<>/, $pair);
      $COOKIE{$name} = $value;
    }

        $c_name = $COOKIE{'name'};
        $c_hp = $COOKIE{'hp'};
        $c_pass = $COOKIE{'pass'};
        
	if($form{'name'}){$c_name = $form{'name'};}
	if($form{'hp'}){$c_hp = $form{'hp'};}
        if($form{'pass'}){$c_pass = $form{'pass'};}
        
}#end get_cookie


##### リーグ更新処理
sub koushin{

        open(LL,"$logfile");                        # 優勝馬
	seek(LL,0,0);  @yuusyou = <LL>;  close(LL);

       ($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $osu, $mesu, $sei, $ketou, $baku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,@yuusyou[0]);

        $endname = "$name";
        $endman = "$sakusya";
        $endmake = $total - $win;
        $endwin = $win;

        open(ST,"$time2file");
	seek(ST,0,0);  @st = <ST>;  close(ST);
        ($hiniti, $hi, $zikan, $rigu) = split(/<>/, @st[0]);
        $endrigu = $rigu;

        open(PST,"$pastfile");
	seek(PST,0,0);  @pst = <PST>;  close(PST);
        
        $pasts = "@yuusyou[0]";
@pst = reverse(@pst);
        push(@pst,$pasts);
@pst = reverse(@pst);
        open(PST,">$pastfile") ;             # 歴代優勝馬に記録
        eval 'flock(PST,2);';
	seek(PST,0,0);	print PST @pst;
	eval 'flock(PST,8);';
        close(PST);

        $shiki = 7;&shinkiro;                # ニュースに記録

###### 種牡馬の年齢を+1
        @umao = "";
        open(RO,"$tanefile");
	seek(RO,0,0);  @syubo = <RO>;  close(RO);

        foreach $lines (@syubo) {      # 年齢を+1にする。
	($name, $ketou, $formkon, $pow, $def, $spe, $icon, $baku, $toshi, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha) = split(/<>/,$lines);
        if($toshi < $osuintai){         # 引退
           $toshi++;
    $syubouma = "$name<>$ketou<>$formkon<>$pow<>$def<>$spe<>$icon<>$baku<>$toshi<>$st<>$titi<>$tiha<>$tititi<>$titiha<>$tihati<>$tihaha<>\n";
        push(@umao,$syubouma);
        }} # if とforeach
        open(RO,">$tanefile") ;
		eval 'flock(RO,2);';
		seek(RO,0,0);	print RO @umao;
		eval 'flock(RO,8);';
	close(RO);

###### 繁殖牝馬の年齢を+1
        @umam = "";
        open(RM,"$tamefile");
	seek(RM,0,0);  @hansyo = <RM>;  close(RM);

        foreach $lines (@hansyo) {      # 年齢を+1にする。
	($name, $ketou, $formkon, $pow, $def, $spe, $icon, $baku, $toshi, $st, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha) = split(/<>/,$lines);
        if($toshi < $mesuintai){         # 引退
           $toshi++;
    $hansyouma = "$name<>$ketou<>$formkon<>$pow<>$def<>$spe<>$icon<>$baku<>$toshi<>$st<>$hati<>$haha<>$hatiti<>$hatiha<>$hahati<>$hahaha<>\n";

        push(@umam,$hansyouma);
        }}
        open(RM,">$tamefile") ;
		eval 'flock(RM,2);';
		seek(RM,0,0);	print RM @umam;
		eval 'flock(RM,8);';
	close(RM);

        open(RO,"$tanefile");
	seek(RO,0,0);  @umao = <RO>;  close(RO);

        @liness = "";
        open(LK,"$logfile");
	seek(LK,0,0);  @lines = <LK>;  close(LK);

              foreach $lines (@lines) {      # 出走数・勝ち数を０にする。
	($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $osu, $mesu, $sei, $ketou, $baku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,$lines);
        $reiketu = 1;
        if($sei eq "牡" && $total > 0){
        $reiketu = 0;
        foreach $line (@umao) {
	($names, $keto, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy) = split(/<>/,$line);
        if($ketou eq $keto){$reiketu = 1;last;}
        }}
###### 種牡馬・繁殖牝馬に書き込み
        if(($win >= $taneosu && $sei eq "牡") || ($win >= $tanemesu && $sei eq "牝") || $reiketu eq "0"){

        if($pow >= 40){$pows=$pow;
           while($pows >= 37){
           $pows--;}}
        elsif($pow >= 39){$pows=$pow;
           while($pows >= 36){
           $pows--;}}
        elsif($pow >= 37){$pows=$pow;
           while($pows >= 35){
           $pows--;}}
        elsif($pow >= 35){$pows = 35;}
         else{$pows = $pow;}
        if($def >= 40){$defs=$def;
           while($defs >= 37){
           $defs--;}}
        elsif($def >= 39){$defs=$def;
           while($defs >= 36){
           $defs--;}}
        elsif($def >= 37){$defs=$def;
           while($defs >= 35){
           $defs--;}}
        elsif($def >= 35){$defs = 35;}
         else{$defs = $def;}
        if($spe >= 40){$spes=$spe;
           while($spes >= 37){
           $spes--;}}
        elsif($spe >= 39){$spes=$spe;
           while($spes >= 36){
           $spes--;}}
        elsif($spe >= 37){$spes=$spe;
           while($spes >= 35){
           $spes--;}}
        elsif($spe >= 35){$spes = 35;}
         else{$spes = $spe;}
        if($formkon >= 20){$formkon = 20;}
        if($sei eq "牡"){
        $katiuma = "$name<mm>$tokusyu<>$ketou<>$formkon<>$pows<>$defs<>$spes<>$icon<>$baku<>6<>$st<>$osu<>$mesu<>$titi<>$tiha<>$hati<>$haha<>\n";}else{
        ($checkname2, $tokusyu2) = split(/<mm>/,$mesu);
        ($checkname3, $tokusyu3) = split(/<mm>/,$haha);
        $katiuma = "$name<mm>$tokusyu<>$ketou<>$formkon<>$pows<>$defs<>$spes<>$icon<>$baku<>6<>$st<>$osu<>$checkname2<mm>$checkketou1<mm>$tokusyu2<>$titi<>$tiha<>$hati<>$checkname3<mm>$checkketou2<mm>$tokusyu3<>\n";}

if($sei eq "牡"){
        open(RO,"$tanefile");
	seek(RO,0,0);  @umao = <RO>;  close(RO);

        push(@umao,$katiuma);
        open(RO,">$tanefile") ;
		eval 'flock(RO,2);';
		seek(RO,0,0);	print RO @umao;
		eval 'flock(RO,8);';
	close(RO);

}elsif($sei eq "牝"){
        open(RM,"$tamefile");
	seek(RM,0,0);  @umam = <RM>;  close(RM);

        push(@umam,$katiuma);
        open(RM,">$tamefile") ;
		eval 'flock(RM,2);';
		seek(RM,0,0);	print RM @umam;
		eval 'flock(RM,8);';
	close(RM);
}
}

             if($total > 0){
                 if($endname eq $name){
             $liness = "-2<>$name<>$sakusya<>$homepage<>$lif<>$pow<>$def<>$spe<>$date<>$ip<>$icon<>0<>$syu<>0<>5<>$ashi<>$osu<>$mesu<>$sei<>$ketou<>$baku<>$pass<>$gazou<>0<>0<><><><><><>$st<>$titi<>$tiha<>$tititi<>$titiha<>$tihati<>$tihaha<>$hati<>$haha<>$hatiti<>$hatiha<>$hahati<>$hahaha<>$checkketou1<>$checkketou2<>$checkketou3<>$tokusyu<>$formkon<>$dmy<>$dmy<>$dmy<>\n";
                 }else{
             $liness = "-1<>$name<>$sakusya<>$homepage<>$lif<>$pow<>$def<>$spe<>$date<>$ip<>$icon<>0<>$syu<>0<>5<>$ashi<>$osu<>$mesu<>$sei<>$ketou<>$baku<>$pass<>$gazou<>0<>0<><><><><><>$st<>$titi<>$tiha<>$tititi<>$titiha<>$tihati<>$tihaha<>$hati<>$haha<>$hatiti<>$hatiha<>$hahati<>$hahaha<>$checkketou1<>$checkketou2<>$checkketou3<>$tokusyu<>$formkon<>$dmy<>$dmy<>$dmy<>\n";}

             push(@liness,$liness)
             }
             }

        open(LK,">$logfile") ;             # 競走馬一覧に記録
        eval 'flock(LK,2);';
	seek(LK,0,0);	print LK @liness;
	eval 'flock(LK,8);';
        close(LK);

        @kuufile = "";              # チャンピオンを消す
	open(TT,">$winfile") ;
		eval 'flock(TT,2);';
		seek(TT,0,0);	print TT @kuufile;
		eval 'flock(TT,8);';
	close(TT);

        open(LI,">$fightfile") ;             # レースの記録を消す
		eval 'flock(LI,2);';
		seek(LI,0,0);	print LI @kuufile;
		eval 'flock(LI,8);';
	close(LI);

        open(BK,">$backupfile") ;
               eval 'flock(BK,2);';           # バックアップファイルを消す
	       seek(BK,0,0);	print BK @kuufile;
	       eval 'flock(BK,8);';
        close(BK);

}#end koushin

##### ルール説明
sub rule{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<center><font color="$tcolor" size="5"><B>あそびかた</B></font>

<hr size="1">
<table border="1" width="660" cellpadding="5"><tr><td><BR>
　・　このゲームは馬を登録して遊ばせるゲームだよ。<BR><BR>
　・　１シーズンは<b>$playday</b>日間<b>$racemax</b>レースだよ。<BR><BR>
　・　１人登録できるのは１頭までだよ。<BR><BR>
　・　日時は$ktime時に変わるよ。<BR><BR>
　・　レースとレースの間隔は<b>$kankaku</b>分必要だよ。<BR><BR>
　・　種牡馬と繁殖牝馬を選んでね。<BR><BR>
　・　勝数のランキングがあるよ。<BR><BR>
　・　勝数の生産家ランキングがあるよ。<BR><BR>
　・　勝数の種牡馬・繁殖牝馬ランキングがあるよ。<BR><BR>
　・　調子は勝った馬も負けた馬も変化するよ。<br><br>
【爆発力】・・・持っている\能\力をどれだけ仔に伝えるかと言うものだよ。<br>
　｜<br>
　├Ａ：安定して高い\能\力を伝える。<br>
　├Ｂ：結\構\安定して高い\能\力を伝える。<br>
　├Ｃ：あんまり安定してないが稀に・・・（謎。<br>
　└Ｄ：不安定気味。<br><br>
　・　レースの距離は1600m～2400mだよ。<BR><BR>
【距離適性】・・・気性が良いほど適性範囲は広いよ。<BR>
　｜<br>
　├短　距離：1600m～2000m<br>
　├短中距離：1700m～2100m<br>
　├中　距離：1800m～2200m<br>
　├中長距離：1900m～2300m<br>
　└長　距離：2000m～2400m<br><br>
【騎手特性】・・・騎手の特徴だよ。<br>
　｜<br>
　├新馬：１・２戦目の馬の\能\力アップ<br>
　├海外：海外（凱旋門賞で\能\力アップ）<br>
　├牝馬：牝馬の\能\力アップ<br>
　├穴馬：思い切った騎乗で人気薄の馬の\能\力アップ<br>
　├豪腕：ゴール前で逃げ・先行馬の\能\力アップ<br>
　├長手綱：2200m以上で\能\力アップ<br>
　├風車鞭：ゴール前で差し・追込み馬の\能\力アップ<br>
　├折り合い：気難しい馬をなだめる<br>
　├ローカル：小倉・中京・福島・新潟・函館・札幌で\能\力アップ<br>
　└好スタート：好スタートをしやすい<br><br>
<table border=1 cellspacing=0 cellpadding=4>
<tr>
<td rowspan=4 bgcolor=#1E90FF width=150>父(Ａ系)</td>
<td rowspan=2 bgcolor=#1E90FF width=150>父父</td>
<td bgcolor=#1E90FF width=150>父父父</td></tr><tr>
<td bgcolor=#FF69B4>父父母</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>父母</td>
<td bgcolor=#1E90FF>父母父</td></tr><tr>
<td bgcolor=#FF69B4>父母母</td>
</tr><tr>
<td rowspan=4 bgcolor=#FF69B4 width=150>母(Ｂ系)</td>
<td rowspan=2 bgcolor=#1E90FF>母父</td>
<td bgcolor=#1E90FF>母父父</td></tr><tr>
<td bgcolor=#FF69B4>母父母</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>母母(Ｃ系)</td>
<td bgcolor=#1E90FF>母母父</td></tr><tr>
<td bgcolor=#FF69B4>母母母(Ｄ系)</td>
</tr>
</table><br><br>
【配合理論】・・・強い競走馬を生産するための理論だよ。<br>
　｜<br>
　├相性：ある特定の血統同士からは強い馬が産まれやすいと言うものだよ。<br>
　｜　｜<br>
　｜　├トリプルニックス（Ａ系－Ｂ系、Ａ系－Ｃ系、Ａ系－Ｄ系）<br>
　｜　｜　　　├スピードニックス：スピード＋＋＋<br>
　｜　｜　　　└瞬発力ニックス：瞬発力＋＋＋<br>
　｜　｜<br>
　｜　├ダブルニックス（Ａ系－Ｂ系、Ａ系－Ｃ系）<br>
　｜　｜　　　├スピードニックス：スピード＋＋<br>
　｜　｜　　　└瞬発力ニックス：瞬発力＋＋<br>
　｜　｜<br>
　｜　└ニックス（Ａ系－Ｂ系）<br>
　｜　　　　　├スピードニックス：スピード＋<br>
　｜　　　　　└瞬発力ニックス：瞬発力＋<br>
　｜<br>
　├サヨナラ配合：種牡馬と繁殖牝馬の年齢が共に○○の配合。スピード＋＋<br>
　├原爆配合：種牡馬と繁殖牝馬の爆発力が共に○同士の配合。スピード＋＋＋、瞬発力＋＋<br>
　├芦毛伝説配合：種牡馬と繁殖牝馬の毛色が共に○毛同士の配合。スピード＋、瞬発力＋<br>
　├栗配合：種牡馬と繁殖牝馬の毛色が共に○毛同士の配合。スピード＋、気性＋<br>
　├同系配合：同じ血統同士の配合。スピード－－<br>
　├インブリード：種牡馬、繁殖牝馬の血統に共通の祖先の馬がいる配合。<br>
　｜　　├(１×２)(１×３)(２×２)(２×３)：禁止<br>
　｜　　└(３×３)：気性－、大因子（<img src=\"$imgurl/sp2.gif\"><img src=\"$imgurl/syu2.gif\"><img src=\"$imgurl/ki2.gif\"><img src=\"$imgurl/st2.gif\"><img src=\"$imgurl/kon2.gif\">）を持っていたら因子＋＋、小因子（<img src=\"$imgurl/sp1.gif\"><img src=\"$imgurl/syu1.gif\"><img src=\"$imgurl/ki1.gif\"><img src=\"$imgurl/st1.gif\"><img src=\"$imgurl/kon1.gif\">）を持っていたら因子＋<br>
　｜　　　　├因子の特性は左から（スピード、瞬発力、気性、スタミナ、勝負根性）<br>
　｜　　　　└さらに３０％の確率でスピード＋、瞬発力＋、７０％の確率でスピード－、瞬発力－<br>
　└アウトブリード：種牡馬、繁殖牝馬の血統に共通の祖先の馬がいない配合。気性＋＋<br><br>
【配合例】　フサイチコンコルド（日本ダービー）<br><br>
・父カーリアンは世界各地で名馬（凱旋門賞馬：マリエンバート等）を輩出した名種牡馬。→高い能\力、爆発力Ａ<br>
・母バレークイーンの仔にはボーンキング・グレースアドマイヤなど重賞で活躍する馬がいる。→高い能\力<br>
・ノーザンダンサーのインブリード(３×３)→スピード＋、瞬発力＋、勝負根性＋、気性－<br>
・ニジンスキー系とノーザンダンサー系はスピードニックス→スピード＋<br>
<table border=1 cellspacing=0 cellpadding=4>
<tr>
<td rowspan=4 bgcolor=#1E90FF width=150>カーリアン<br>(ニジンスキー系)</td>
<td rowspan=2 bgcolor=#1E90FF width=150>Nijinsky<img src=\"$imgurl/sp1.gif\"></td>
<td bgcolor=#1E90FF width=150><font color=red>ノーザンダンサー</font><img src=\"$imgurl/kon1.gif\"></td></tr><tr>
<td bgcolor=#FF69B4>Flaming Page</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>Foreseer</td>
<td bgcolor=#1E90FF>Round Table</td></tr><tr>
<td bgcolor=#FF69B4>Regal Gleam</td>
</tr><tr>
<td rowspan=4 bgcolor=#FF69B4 width=150>バレークイーン<br>(ノーザンダンサー系)</td>
<td rowspan=2 bgcolor=#1E90FF>Sadler's Wells</td>
<td bgcolor=#1E90FF><font color=red>ノーザンダンサー</font><img src=\"$imgurl/kon1.gif\"></td></tr><tr>
<td bgcolor=#FF69B4>Fairy Bridge</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>Sun Princess</td>
<td bgcolor=#1E90FF>イングリッシュプリンス</td></tr><tr>
<td bgcolor=#FF69B4>Sunny Valley</td>
</tr>
</table><br><br>
　・　牡馬は引退後<b>$taneosu</b>勝以上で種牡馬になるよ。<BR><BR>
　・　例外として血統が途絶えた場合その年の最も成績の良かった牡馬は種牡馬になるよ。<BR><BR>
　・　牝馬は引退後<b>$tanemesu</b>勝以上で繁殖牝馬になるよ。<BR><BR>
　・　種牡馬は<b>$osuintai</b>歳で種牡馬を引退するよ。<BR><BR>
　・　繁殖牝馬は<b>$mesuintai</b>歳で繁殖牝馬を引退するよ。<BR><BR>
　・　シーズン優勝馬は次のシーズンの始めに凱旋門賞に挑戦できるよ。<BR><BR>
　・　凱旋門賞に勝つと歴代優勝馬の○代の色が変わるよ。<br><br>
</td></tr></table>

_HTML_
&chosaku;
}

##### 能力
sub nouhan{

        if   ($supi >= 37){$s = "☆";}
        elsif($supi >= 35){$s = "◎";}
        elsif($supi >= 30){$s = "○";}
        elsif($supi > 26){$s = "△";}
        else            {$s = "×";}

        if   ($syun >= 37){$ss = "☆";}
        elsif($syun >= 35){$ss = "◎";}
        elsif($syun >= 30){$ss = "○";}
        elsif($syun > 26){$ss = "△";}
        else            {$ss = "×";}

        if   ($kisei >= 37){$sss = "☆";}
        elsif($kisei >= 35){$sss = "◎";}
        elsif($kisei >= 30){$sss = "○";}
        elsif($kisei > 26){$sss = "△";}
        else            {$sss = "×";}

        if   ($st > 38){$ssss = "長距離";}
        elsif($st > 36){$ssss = "中長距離";}
        elsif($st > 34){$ssss = "中距離";}
        elsif($st > 32){$ssss = "短中距離";}
        else            {$ssss = "短距離";}

        if   ($formkon >= 20){$sssss = "☆";}
        elsif($formkon >= 17){$sssss = "◎";}
        elsif($formkon >= 15){$sssss = "○";}
        elsif($formkon >= 13){$sssss = "△";}
        else            {$sssss = "×";}

}# end nouhan

#####ニュースに記録
sub shinkiro{

# 時間の取得
	
	$times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);
        $year += 1900;
	$month = sprintf("%02d",$mon +1);
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
	$ljikan = "$month/$mday $hour:$min";

        open(CO,"$commentfile");
	seek(CO,0,0);  @nyusu = <CO>;  close(CO);

      $kekka = "";
      $flag=0;
      if($shiki == 1){

             $shinnbunn = "$winp[0]氏が$winp[1]勝の快挙を達成！";}

      elsif($shiki == 2){
             ($nameosu, $tokusyu) = split(/<mm>/,$winz[0]);
             $shinnbunn = "$nameosuの産駒が$winz[1]勝の快挙を達成！";}

      elsif($shiki == 3){
             ($namemesu, $tokusyu) = split(/<mm>/,$winzm[0]);
             $shinnbunn = "$namemesuの仔が$winzm[1]勝の快挙を達成！";}

      elsif($shiki == 4){

             $shinnbunn = "白毛のサラブレットが誕生。名前は$formumanameと命名された。";}

      elsif($shiki == 5){

           $shinnbunn = "尾花栗毛のサラブレットが誕生。名前は$formumanameと命名された。";}
      
      elsif($shiki == 6){

             $shinnbunn = "$lname[$k]が９馬身差で圧勝！";
             $kekka = "$lname[$k] ○-９馬身-● $lname[$kk]";}
      elsif($shiki == 7){

        $shinnbunn = "第$endrigu回は$endname【$endman】が$endwin勝$endmake敗で優勝！";}

      elsif($shiki == 8){

       $shinnbunn = "$lname[$j]の連勝が$rennsyou[$j]でストップ。止めたのは$lname[$i]！";}

	$kakiko = "$shinnbunn<>127.0.0.1<>$news<>$ljikan<>$kekka<>\n";

        foreach $line (@nyusu) {
        ($comm, $host, $name, $time, $kekka) = split(/<>/,$line);
        if($comm eq $shinnbunn){$flag=1;last;}
        }

    if($flag ne "1"){
	unshift(@nyusu, $kakiko);
	splice(@nyusu, $max_com);
    }

        open(CO,">$commentfile") ;
               eval 'flock(CO,2);';
	       seek(CO,0,0);	print CO @nyusu;
	       eval 'flock(CO,8);';
        close(CO);
}

##### エラーの時の処理
sub error{
if($wawa ne "1"){
print "Content-type: text/html\n\n";#コンテントタイプ出力
}
       $err_msg = @_[0];
         
print <<"_ERROR_";

<html><head><title>ERROR</title></head>
$body
<br><br><br><center>$err_msg
<BR></body></html>
<center><form action="$cgifile" method="$method">
<input type="submit" value="戻る">
_ERROR_

exit;

}#END error

sub secretcopyright{
$secret = qq|<!--このスクリプトの知的所有権はαkouとゴードンにあります。-->|;
print $secret;
} #END
