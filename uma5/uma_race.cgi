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
require './uma5.cgi';&kankyou;

##### 対戦処理
sub syori{

# ロック開始

        $times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

	open(GL,"+<$lockfile");
	eval 'flock(GL,2);';

	@gamelock = <GL>;

	($gamecheck, $gametime) = split(/<>/, $gamelock[0]);
	if($gamecheck == 0 || $times > $gametime + 60 * 2){
		$gamelock = "1<>$times<>\n";
	}else{
		&error("現在レース中です。もうちょっと待っててね。");
	}

	truncate (GL, 0);
	seek(GL,0,0);	print GL $gamelock;
	close(GL);
	eval 'flock(GL,8);';

    if($form{'gaisen'} ne "7"){
        $formlogint= $form{'logint'};

        open(WI,"$winfile");
	seek(WI,0,0);  @nowwin = <WI>;  close(WI);    # チャンピオンを調べる

        ($nowno, $nowname, $nowsakusya, $nowhomepage, $nowlif, $nowpow, $nowdef, $nowspe, $nowdate, $nowip, $nowicon, $nowwin, $nowsyu, $nowtotal, $nowtyoushi, $nowashi, $nowosu, $nowmesu, $nowsei, $nowketou, $nowbaku, $nowpass, $nowgazou, $nowrennsyou, $nowmaxren, $nowrecords, $nowrecords16, $nowrecords18, $nowrecords22, $nowrecords24, $nowst, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/, @nowwin[0]);

        if($formlogint eq $nowsakusya){&error("自分の馬と対戦出来ません。");}

        open(FL,"$logfile");
	seek(FL,0,0);  @lines = <FL>;  close(FL);
        
        foreach $check (@lines){      # チャンピオンデータ$nowuma,挑戦者データ$nowumbに。
		@check = split(/<>/,$check);
		if($nowsakusya eq $check[2]){$nowuma = "$check";$check = '';}
             elsif($formlogint eq $check[2]){$nowumb = "$check";$check = '';}
		}
        @c = split(/<>/, $nowuma);     # チャンピオンデータ
        @d = split(/<>/, $nowumb);     # 挑戦者データ
        if($d[13] >= $racemax){&error("シーズン最多レース数を越えてます。");} # 念の為
        if($c[13] == $racemax2 && $d[13] == $racemax2){&error("このレースをすると両方がシーズンを終える事になり現在のチャンピオンがいなくなります。別の人が対戦するのを待ってて下さい。");}

        ($gmonth, $gday, $ghour, $gmin) = split(/<g>/,$d[8]);   # 最終レース時間

	$thour = sprintf("%02d",$hour);
	$tmin = sprintf("%02d",$min);

        if($ghour == $thour && abs($gmin - $tmin) < $kankaku){
        $mate = $kankaku - abs($gmin - $tmin);
        &error("あと$mate分待っててね。"); 
        }


#ログの逆順処理
@lines = reverse(@lines);

        push(@lines,$nowuma);
        push(@lines,$nowumb);

#ログの逆順処理
@lines = reverse(@lines);

        open(FL,">$logfile") ;
		eval 'flock(FL,2);';
		seek(FL,0,0);	print FL @lines;
		eval 'flock(FL,8);';
	close(FL);

        open(FL,"$logfile");
	seek(FL,0,0);  @lines = <FL>;  close(FL);

    }else{ # 凱旋門賞

        open(DB,"$logfile");
	seek(DB,0,0);  @lines = <DB>;  close(DB);
        
        foreach $check (@lines){      # 優勝馬データ$nowuma
		@check = split(/<>/,$check);
		if($check[0]  eq "-2"){$nowuma = "$check";$check = '';last;}
		}
        if($nowuma eq ""){&error("凱旋門賞はもう行われました。");}

        @c = split(/<>/, $nowuma);     # 優勝馬データ

         ($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $osu, $mesu, $sei, $ketou, $baku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,$nowuma);

          $yattaa = "-1<>$name<>$sakusya<>$homepage<>$lif<>$pow<>$def<>$spe<>$date<>$ip<>$icon<>$win<>$syu<>$total<>5<>$ashi<>$osu<>$mesu<>$sei<>$ketou<>$baku<>$pass<>$gazou<>$rennsyou<>$maxren<>$records<>$records16<>$records18<>$records22<>$records24<>$st<>$titi<>$tiha<>$tititi<>$titiha<>$tihati<>$tihaha<>$hati<>$haha<>$hatiti<>$hatiha<>$hahati<>$hahaha<>$checkketou1<>$checkketou2<>$checkketou3<>$tokusyu<>$formkon<>$dmy<>$dmy<>$dmy<>\n";

        push(@lines,$yattaa);
        open(DB,">$logfile") ;
		eval 'flock(DB,2);';
		seek(DB,0,0);	print DB @lines;
	        eval 'flock(DB,8);';
        close(DB);

        open(GA,"$gaisenfile");
	seek(GA,0,0);  @gaisen = <GA>;  close(GA);

        $gaisenaite = int(rand($#gaisen) + 0.5);
        if($gaisenaite > $#gaisen){$gaisenaite = 0;}# 念の為
        $nowumb = @gaisen[$gaisenaite];
        @d = split(/<>/, @gaisen[$gaisenaite]);     # 凱旋門馬データ

        $lines[0] = $nowuma;
        $lines[1] = $nowumb;

    } # end 凱旋門賞

        $a = $lines[0];  # 挑戦馬・優勝馬
	$b = $lines[1];  # ﾁｬﾝﾋﾟｵﾝ・凱旋門馬

	# 対戦者一覧

        $ato = 1;   #レース画面に行く用

	@buckup = ($a,$b);
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

        @kaisaiti = ('sapporo','hakodate','niigata','fukushima','nakayama','tokyou','chukyo','kyoto','hanshin','kokura','ronsyan');
        @kaiti = ('札幌','函館','新潟','福島','中山','東京','中京','京都','阪神','小倉','ロンシャン');
        $ti = int(rand(9)+0.5);
        if($ti > 9){$ti = 9;}  # 念のため
        $kaisai = $kaisaiti[$ti];
        $kaitis = $kaiti[$ti];
        @nowkyori = ('1600','1800','2000','2200','2400');
        $kyorida = int(rand(4)+0.5);
        if($kyorida > 4){$kyorida = 4;}  # 念のため
        $kyori = $nowkyori[$kyorida];    # 距離
        $hankyori = $kyori / 2;          # 距離の半分
        $yonkyori = $kyori - 400;           # 距離-400
    if($form{'gaisen'} eq "7"){ # 凱旋門賞
        $kaisai = $kaisaiti[10];
        $kaitis = $kaiti[10];
        $kyori = $nowkyori[4];}

	$month = sprintf("%02d",$mon + 1);
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
      $log[$m] = "$month月$mday日$hour時$min分のレース<br><center>（$kaitis $kyoriｍ）<>";
	$m++;            #0
	
	@a = split(/<>/,$a);
	@b = split(/<>/,$b);
        $formkisyu = $form{'syu'};
        $formashi = $form{'sakusen'};

##### 騎手
if($kyori >= 2200){    # 長手綱
       if( ($formkisyu eq "角田") || ($formkisyu eq "岡部") || ($formkisyu eq "和田") || ($formkisyu eq "横山典") ){$a[7]++;$a[6]++;}
       if( ($b[12] eq "角田") || ($b[12] eq "岡部") || ($b[12] eq "和田") || ($b[12] eq "横山典") ){$b[7]++;$b[6]++;}
}


if($a[13] < 3){   # 新馬（挑戦馬）
        if( ($formkisyu eq "武豊") || ($formkisyu eq "河内") || ($formkisyu eq "四位") || ($formkisyu eq "蛯名") || ($formkisyu eq "岡部") || ($formkisyu eq "柴田善") || ($formkisyu eq "安藤勝") ){$a[5] += 1;}
}


if($b[13] < 3){ # 新馬（ﾁｬﾝﾋﾟｵﾝ）
       if( ($b[12] eq "武豊") || ($b[12] eq "河内") || ($b[12] eq "四位") || ($b[12] eq "蛯名") || ($b[12] eq "岡部") || ($b[12] eq "柴田善") || ($b[12] eq "安藤勝") ){$b[5]+= 1;}
}


if( ($kaitis eq "小倉") || ($kaitis eq "中京") || ($kaitis eq "福島") || ($kaitis eq "新潟") || ($kaitis eq "函館") || ($kaitis eq "札幌") ){    # ローカル開催
       if( ($formkisyu eq "柴田善") || ($formkisyu eq "藤田") || ($formkisyu eq "坂井") || ($formkisyu eq "田中勝") || ($formkisyu eq "吉田豊") || ($formkisyu eq "佐藤哲") || ($formkisyu eq "渡辺") ){$a[5] += 2;}
       if(($b[12] eq "柴田善") || ($b[12] eq "藤田") || ($b[12] eq "坂井") || ($b[12] eq "田中勝") || ($b[12] eq "吉田豊") || ($b[12] eq "佐藤哲") || ($b[12] eq "渡辺")){$b[5]+= 1;}
}


if($kaitis eq "ロンシャン"){  # 海外（凱旋門賞）
       if( ($formkisyu eq "武豊") || ($formkisyu eq "蛯名") || ($formkisyu eq "ペリエ") || ($formkisyu eq "デザーモ") || ($formkisyu eq "デムーロ") ){$a[7]++;}
}


if($a[18] eq "牝"){   # 牝馬（挑戦馬）
        if( ($formkisyu eq "河内") || ($formkisyu eq "福永") || ($formkisyu eq "松永") || ($formkisyu eq "吉田豊") ){$a[5]++;}
}


if($b[18] eq "牝"){ # 牝馬（ﾁｬﾝﾋﾟｵﾝ）
       if( ($b[12] eq "河内") || ($b[12] eq "福永") || ($b[12] eq "吉田豊") || ($b[12] eq "松永") ){$b[5]++;}
}


if( ($formkisyu eq "武豊") || ($formkisyu eq "河内") ){   # 折り合い（挑戦馬）
        $a[7] += 2;
}


if( ($b[12] eq "武豊") || ($b[12] eq "河内") ){   # 折り合い（ﾁｬﾝﾋﾟｵﾝ）
        $b[7] += 2;
}


if( ($a[5] < 32) || ($a[11] < 5 && $a[13] > 15) || ($a[11] < 15 && $a[13] > 35) ){   # 穴馬（挑戦馬）
        if( ($formkisyu eq "武幸") || ($formkisyu eq "江田照") || ($formkisyu eq "四位") || ($formkisyu eq "渡辺") || ($formkisyu eq "大西") || ($formkisyu eq "後藤") || ($formkisyu eq "坂井") ){$a[5] += 2;}
}


if( ($b[5] < 32) || ($b[11] < 5 && $b[13] > 15) || ($b[11] < 15 && $b[13] > 35) ){   # 穴馬（ﾁｬﾝﾋﾟｵﾝ）
        if( ($b[12] eq "武幸") || ($b[12] eq "江田照") || ($b[12] eq "四位") || ($b[12] eq "渡辺") || ($b[12] eq "大西") || ($b[12] eq "後藤") || ($b[12] eq "坂井") ){$b[5] += 2;}
}

        $a = "$a[0]<>$a[1]<>$a[2]<>$a[3]<>$kyori<>$a[5]<>$a[6]<>$a[7]<>$a[8]<>$a[9]<>$a[10]<>$a[11]<>$formkisyu<>$a[13]<>$a[14]<>$formashi<>$a[16]<>$a[17]<>$a[18]<>$a[19]<>$a[20]<>$a[21]<>$a[22]<>$a[23]<>$a[24]<>$a[25]<>$a[26]<>$a[27]<>$a[28]<>$a[29]<>$a[30]<>$a[31]<>$a[32]<>$a[33]<>$a[34]<>$a[35]<>$a[36]<>$a[37]<>$a[38]<>$a[39]<>$a[40]<>$a[41]<>$a[42]<>$a[43]<>$a[44]<>$a[45]<>$a[46]<>$a[47]<>$a[48]<>$a[49]<>$a[50]<>\n";
        $b = "$b[0]<>$b[1]<>$b[2]<>$b[3]<>$kyori<>$b[5]<>$b[6]<>$b[7]<>$b[8]<>$b[9]<>$b[10]<>$b[11]<>$b[12]<>$b[13]<>$b[14]<>$b[15]<>$b[16]<>$b[17]<>$b[18]<>$b[19]<>$b[20]<>$b[21]<>$b[22]<>$b[23]<>$b[24]<>$b[25]<>$b[26]<>$b[27]<>$b[28]<>$b[29]<>$b[30]<>$b[31]<>$b[32]<>$b[33]<>$b[34]<>$b[35]<>$b[36]<>$b[37]<>$b[38]<>$b[39]<>$b[40]<>$b[41]<>$b[42]<>$b[43]<>$b[44]<>$b[45]<>$b[46]<>$b[47]<>$b[48]<>$b[49]<>$b[50]<>\n";
        @a = split(/<>/,$a);
	@b = split(/<>/,$b);

	$log[$m] = "$a[1]<>$b[1]<>";       #1,2
	$m++;
        
        if   ($a[14] < 2){ $conditiona = "<font color=#4B0082>絶不調</font>"; }
	elsif($a[14] < 4){ $conditiona = "<font color=blue>不調</font>"; }
	elsif($a[14] < 7){ $conditiona = "<font color=#FFD700>普通</font>"; }
	elsif($a[14] < 9){ $conditiona = "<font color=red>好調</font>"; }
	elsif($a[14] < 11){ $conditiona = "<font color=#FF00FF>絶好調</font>"; }

        if($a[10] eq "uma1.gif"){$icon="鹿毛";}
        elsif($a[10] eq "uma2.gif"){$icon="黒鹿毛";}
        elsif($a[10] eq "uma3.gif"){$icon="栃栗毛";}
        elsif($a[10] eq "uma4.gif"){$icon="栗毛";}
        elsif($a[10] eq "uma5.gif"){$icon="尾花栗毛";}
        elsif($a[10] eq "uma6.gif"){$icon="青鹿毛";}
        elsif($a[10] eq "uma7.gif"){$icon="青毛";}
        elsif($a[10] eq "uma8.gif"){$icon="芦毛(濃)";}
        elsif($a[10] eq "uma9.gif"){$icon="芦毛(薄)";}
        else{$icon="白毛";}

        $hai = $a[13] - $a[11];
        if($a[13] eq "0"){$senreki="初出走";}
        else{$makeka=abs($a[23]);$senreki="$makeka連敗中";}
	$log[$m] = "<b>$a[1]</b>（$icon）：$a[12]：$a[15]：<b>$conditiona</b>：$a[11]勝$hai敗（$senreki）<>";   #3
	$m++;

        if   ($b[14] < 2){ $conditionb = "<font color=#4B0082>絶不調</font>"; }
	elsif($b[14] < 4){ $conditionb = "<font color=blue>不調</font>"; }
	elsif($b[14] < 7){ $conditionb = "<font color=#FFD700>普通</font>"; }
	elsif($b[14] < 9){ $conditionb = "<font color=red>好調</font>"; }
	elsif($b[14] < 11){ $conditionb = "<font color=#FF00FF>絶好調</font>"; }

        if($b[10] eq "uma1.gif"){$iconn="鹿毛";}
        elsif($b[10] eq "uma2.gif"){$iconn="黒鹿毛";}
        elsif($b[10] eq "uma3.gif"){$iconn="栃栗毛";}
        elsif($b[10] eq "uma4.gif"){$iconn="栗毛";}
        elsif($b[10] eq "uma5.gif"){$iconn="尾花栗毛";}
        elsif($b[10] eq "uma6.gif"){$iconn="青鹿毛";}
        elsif($b[10] eq "uma7.gif"){$iconn="青毛";}
        elsif($b[10] eq "uma8.gif"){$iconn="芦毛(濃)";}
        elsif($b[10] eq "uma9.gif"){$iconn="芦毛(薄)";}
        else{$iconn="白毛";}

        $haii = $b[13] - $b[11];
        if($b[13] eq "0"){$senreki="初出走";}
     elsif($b[23] < 0){$senreki="0連勝中";}
        else{$senreki="$b[23]連勝中";}
	
	$log[$m] = "<b>$b[1]</b>（$iconn）：$b[12]：$b[15]：<b>$conditionb</b>：$b[11]勝$haii敗（$senreki）<>";   #4
	$m++;

	# 進むを与える処理。

	@fight = ($a,$b);
	$number = 2;
        $goultime = 0;
        $dmgk = 0;
        @dmg = '';
        @dmg2 = '';
        @damegekyori = "";@sup="";@inf="";
	while($number > 1){
		for ($i=0; $i<2; $i++){
		($lno[$i], $lname[$i], $lsakusya[$i], $lhomepage[$i], $llif[$i], $lpow[$i], $ldef[$i], $lspe[$i], $ldate[$i], $lip[$i], $licon[$i], $lwin[$i] , $lsyu[$i] , $ltotal[$i], $ltyoushi[$i], $lashi[$i], $losu[$i], $lmesu[$i], $lsei[$i], $lketou[$i], $lbaku[$i], $pass[$i], $gazou[$i], $rennsyou[$i], $maxren[$i], $records[$i], $records16[$i], $records18[$i], $records22[$i], $records24[$i], $st[$i], $titi[$i], $tiha[$i], $tititi[$i], $titiha[$i], $tihati[$i], $tihaha[$i], $hati[$i], $haha[$i], $hatiti[$i], $hatiha[$i], $hahati[$i], $hahaha[$i], $checkketou1[$i], $checkketou2[$i], $checkketou3[$i], $tokusyu[$i], $formkon[$i], $dmy, $dmy, $dmy) = split(/<>/,$fight[$i]);
        if($i==0){@damege3 = "";}

if($llif[$i] eq $kyori){

##### 距離適性
        
        $sup[$i] = int(800+ (40 * $st[$i]));   # 最長
        $inf[$i] = int($sup[$i] - (13 * $lspe[$i]));   # 最短
        
  if($kyori > $sup[$i]){     # 最長より長い距離の場合
         $damegekyori[$i] = -int(($kyori-$sup[$i]) / 70);
         if($damegekyori[$i] == 0){$damegekyori[$i] = -1;}
  }elsif($kyori < $inf[$i]){     # 最短より短い距離の場合
        $damegekyori[$i] = -int(($inf[$i]-$kyori) / 70);
        if($damegekyori[$i] == 0){$damegekyori[$i] = -1;}
  }
}

        $goultime++;

        if(int(rand(35)) > $lspe[$i]){ # よろけた場合

        @syusei4 = (2.6 , 3.0 , 3.2 , 3.3 , 3.3, 3.2 , 3.6 , 3.3 , 3.2 , 3.0 , 3.3);
	$yy = int(rand(10));
        $damege3[$i] = int($lspe[$i] * $syusei4[$yy]);
        
        }else{

	@syusei1 = (3.0 , 2.3 , 2.2 , 2.2 , 2.3 , 2.4 , 2.5 , 2.6 , 2.6 , 2.6 , 2.2, 2.8 , 2.9 , 2.9 , 3.0 , 2.0 , 3.1 , 3.1);
	$y = int(rand(17));
	@syusei2 = (3.0 , 2.2 , 2.3 , 2.2 , 2.3 , 2.4 , 2.5 , 2.5 , 2.6 , 2.6 , 2.3, 2.8 , 2.9 , 2.9 , 3.0 , 2.1 , 3.1 , 3.1);
	$z = int(rand(17));
        $syusei3 = rand(20)+15;

	$bpow = int($lpow[$i] * $syusei1[$y]);   # スピード
	$bdef = int($ldef[$i] * $syusei2[$z]);   # 瞬発力

##### 騎手
$ki=int(rand(50));
if($ki > 25){
      $damegekisyu = 0;
    if($llif[$i] == $kyori){     # 好スタート
      if( ($lsyu[$i] eq "中館") || ($lsyu[$i] eq "渡辺") || ($lsyu[$i] eq "勝浦") ){
      $damegekisyu += 10;
      }
    }
    if((($lashi[$i] eq "逃げ") || ($lashi[$i] eq "先行")) && ($llif[$i] < 300)){# 豪腕
      if( ($lsyu[$i] eq "角田") || ($lsyu[$i] eq "ペリエ") || ($lsyu[$i] eq "大西") || ($lsyu[$i] eq "中館") || ($lsyu[$i] eq "佐藤哲") || ($lsyu[$i] eq "福永") || ($lsyu[$i] eq "デザーモ") || ($lsyu[$i] eq "安藤勝") || ($lsyu[$i] eq "デムーロ") ){
      $damegekisyu += 10;
      }
    }
    if((($lashi[$i] eq "差し") || ($lashi[$i] eq "追込")) && ($llif[$i] < 300)){# 風車鞭
      if( ($lsyu[$i] eq "後藤") || ($lsyu[$i] eq "ペリエ") || ($lsyu[$i] eq "蛯名") || ($lsyu[$i] eq "横山典") || ($lsyu[$i] eq "藤田") || ($lsyu[$i] eq "田中勝") || ($lsyu[$i] eq "デザーモ") || ($lsyu[$i] eq "デムーロ") ){
      $damegekisyu += 10;
      }
    }
}

##### 勝負根性

      if($i == 0){
         $konjyo = $llif[0];
         if($llif[0] <= 400 && ( abs($llif[0] - $llif[1]) <= 100 ) ){
             $damegekon = $formkon[0];}
      }else{
         if($llif[1] <= 400 && ( abs($konjyo - $llif[1]) <= 100 ) ){
             $damegekon = $formkon[1];}}

##### 脚質の調整
      if($llif[$i] < 800 && $llif[$i] > 300){
        $damege = int($bdef + $syusei3);}
      else{$damege = int($bpow + $syusei3);}

      if($llif[$i] <= $kyori && $llif[$i] > $yonkyori && $lashi[$i] eq "逃げ"){
        $damege += 30;}
   elsif($llif[$i] <= $kyori && $llif[$i] > $yonkyori && $lashi[$i] eq "大逃"){
        $damege += 60;}
   elsif($llif[$i] <= $kyori && $llif[$i] > $yonkyori && $lashi[$i] eq "先行"){
        $damege += 10;}
   elsif($llif[$i] <= $kyori && $llif[$i] > $yonkyori && $lashi[$i] eq "差し"){
        $damege -= 10;}
   elsif($llif[$i] <= $kyori && $llif[$i] > $yonkyori && $lashi[$i] eq "追込"){
        $damege -= 20;}
   elsif($llif[$i] < 500 && $llif[$i] > 0 && $lashi[$i] eq "逃げ"){
        $damege -= 20;}
   elsif($llif[$i] < 550 && $llif[$i] > 0 && $lashi[$i] eq "大逃"){
        $damege -= 40;}
   elsif($llif[$i] < 600 && $llif[$i] > 400 && $lashi[$i] eq "先行"){
        $damege -= 10;}
   elsif($llif[$i] < 600 && $llif[$i] > 100 && $lashi[$i] eq "差し"){
        $damege += 10;}
   elsif($llif[$i] < 800 && $llif[$i] > 600 && $lashi[$i] eq "追込"){
        $damege += 10;}
   elsif($llif[$i] < 400 && $llif[$i] > 0 && $lashi[$i] eq "追込"){
        $damege += 20;}
        if($damege < 50){$damege = 50;}

##### 体調の調整
        if($llif[$i] > $hankyori){$damege2 = 0;}
        elsif($lwin[$i] < 5 && $ltotal[$i] > 15){$damege2 = 10;}
        elsif(($ltotal[$i] - $lwin[$i] < 10) && $ltotal[$i] > 30){$damege2 = 0;}
        else{$damege2 = $ltyoushi[$i];}

##### 各競馬場の特徴

                if($lashi[$i] eq "逃げ"){    # 逃げ
   if( ($llif[$i] > $hankyori) && ($kaitis eq "東京") ){$damegebaba = -5;}
elsif( ($llif[$i] > $hankyori) && ($kaitis eq "小倉") ){$damegebaba = 5;}
            }elsif($lashi[$i] eq "差し"){    # 差し
   if( ($llif[$i] < $hankyori) && ($kaitis eq "中山") ){$damegebaba = 5;}
            }elsif($lashi[$i] eq "追込"){    # 追込
   if( ($llif[$i] < $hankyori) && ($kaitis eq "新潟" || $kaitis eq "東京") ){$damegebaba = 5;}
elsif( ($llif[$i] < $hankyori) && ($kaitis eq "中京") ){$damegebaba = -5;}
           }

$damege3[$i] = $damege+$damege2+$damegebaba+$damegekyori[$i]+$damegekisyu+$damegekon;
	
      }#else
        
        $llif[$i] -= $damege3[$i];

	$fight[$i] = "$lno[$i]<>$lname[$i]<>$lsakusya[$i]<>$lhomepage[$i]<>$llif[$i]<>$lpow[$i]<>$ldef[$i]<>$lspe[$i]<>$ldate[$i]<>$lip[$i]<>$licon[$i]<>$lwin[$i]<>$lsyu[$i]<>$ltotal[$i]<>$ltyoushi[$i]<>$lashi[$i]<>$losu[$i]<>$lmesu[$i]<>$lsei[$i]<>$lketou[$i]<>$lbaku[$i]<>$pass[$i]<>$gazou[$i]<>$rennsyou[$i]<>$maxren[$i]<>$records[$i]<>$records16[$i]<>$records18[$i]<>$records22[$i]<>$records24[$i]<>$st[$i]<>$titi[$i]<>$tiha[$i]<>$tititi[$i]<>$titiha[$i]<>$tihati[$i]<>$tihaha[$i]<>$hati[$i]<>$haha[$i]<>$hatiti[$i]<>$hatiha[$i]<>$hahati[$i]<>$hahaha[$i]<>$checkketou1[$i]<>$checkketou2[$i]<>$checkketou3[$i]<>$tokusyu[$i]<>$formkon[$i]<>$dmy<>$dmy<>$dmy<>\n";
                }# for

        $dmg[$dmgk]="$damege3[0]<>a\n";
        $dmg2[$dmgk]="$damege3[1]<>b\n";
        $dmgk++;

             for ($i=0; $i<2; $i++){
		($kno[$i], $kname[$i], $ksakusya[$i], $khomepage[$i], $klif[$i], $kpow[$i], $kdef[$i], $kspe[$i], $kdate[$i], $kip[$i], $kicon[$i], $kwin[$i], $ksyu[$i], $ktotal[$i], $ktyoushi[$i], $kashi[$i], $kosu[$i], $kmesu[$i], $ksei[$i], $kketou[$i], $kbaku[$i], $pass[$i], $gazou[$i], $rennsyou[$i], $maxren[$i], $records[$i], $records16[$i], $records18[$i], $records22[$i], $records24[$i], $st[$i], $titi[$i], $tiha[$i], $tititi[$i], $titiha[$i], $tihati[$i], $tihaha[$i], $hati[$i], $haha[$i], $hatiti[$i], $hatiha[$i], $hahati[$i], $hahaha[$i], $checkketou1[$i], $checkketou2[$i], $checkketou3[$i], $tokusyu[$i], $formkon[$i], $dmy, $dmy, $dmy) = split(/<>/,$fight[$i]);}

# ゴール処理
    if($klif[0] < 1 && $klif[1] > 0){$k = 0; $kk = 1;}
 elsif($klif[1] < 1 && $klif[0] > 0) {$k = 1; $kk = 0;}
 elsif($klif[1] < 1 && $klif[0] < 1 && $klif[1] < $klif[0]) {$k = 1; $kk = 0;}
 elsif($klif[1] < 1 && $klif[0] < 1 && $klif[0] <= $klif[1]) {$k = 0; $kk = 1;}

    if ($llif[$k] < 1){
                $number--;
                $tyakusa = 0;
                if( abs($llif[$k]) > 100){$tekitou = int(rand(3));}
             elsif( abs($llif[$k]) > 50){$tekitou = int(rand(3))+3;}
                else{$tekitou = int(rand(3))+6;}

          if($kyori eq "2000"){
                $wintime = int($goultime/2) + 42;  # 勝ち馬タイム
      }elsif($kyori eq "1800"){
                $wintime = int($goultime/2) + 30;
      }elsif($kyori eq "1600"){
                $wintime = int($goultime/2) + 19;
      }elsif($kyori eq "2200"){
                $wintime = int($goultime/2) + 54;
      }elsif($kyori eq "2400"){
                $wintime = int($goultime/2) + 64;
      }

           if($wintime > 59){$wintime2 = $wintime - 60;
                $wintimeda = "2′$wintime2″$tekitou";
                $wintimes = "2<t>$wintime2<t>$tekitou";}
           else{$wintimeda = "1′$wintime″$tekitou";
                $wintimes = "1<t>$wintime<t>$tekitou";}

                $rtimef = 0;
                $rkana = 0;
        open(RR,"$recordsfile");
	seek(RR,0,0);  @rr = <RR>;  close(RR);

        foreach $check (@rr){
		@check = split(/<>/,$check);
		if($kaitis eq $check[0]){$rkaisai = "$check";last;}
                }
        ($rti, $ruma, $rtime, $ruma16, $rtime16, $ruma18, $rtime18, $ruma22, $rtime22, $ruma24, $rtime24) = split(/<>/, $rkaisai);
        ($winhun, $winbyou, $winnan) = split(/<t>/,$wintimes);    #   今

        if($kyori eq "1600"){$shirabe = "$rtime16";}
     elsif($kyori eq "1800"){$shirabe = "$rtime18";}
     elsif($kyori eq "2000"){$shirabe = "$rtime";}
     elsif($kyori eq "2200"){$shirabe = "$rtime22";}
     elsif($kyori eq "2400"){$shirabe = "$rtime24";}
        ($winhunt, $winbyout, $winnant) = split(/<t>/,$shirabe);    #レコード

        if($winhun < $winhunt || $winhunt eq ""){
        $rtimef = 1;}
        elsif($winhun == $winhunt && $winbyou < $winbyout){
        $rtimef = 1;}
        elsif($winhun == $winhunt && $winbyou == $winbyout && $winnan < $winnant){
        $rtimef = 1;}

    if($rtimef eq "1"){
            if($kyori eq "1600"){$ruma16 = "$lname[$k]";$rtime16 = "$wintimes";}
         elsif($kyori eq "1800"){$ruma18 = "$lname[$k]";$rtime18 = "$wintimes";}
         elsif($kyori eq "2000"){$ruma = "$lname[$k]";$rtime = "$wintimes";}
         elsif($kyori eq "2200"){$ruma22 = "$lname[$k]";$rtime22 = "$wintimes";}
         elsif($kyori eq "2400"){$ruma24 = "$lname[$k]";$rtime24 = "$wintimes";}

                $rkaisai = "$kaitis<>$ruma<>$rtime<>$ruma16<>$rtime16<>$ruma18<>$rtime18<>$ruma22<>$rtime22<>$ruma24<>$rtime24<>\n";
                $rkana = 1;
                foreach $check (@rr){
		@check = split(/<>/,$check);
		if($kaitis eq $check[0]){$check = "$rkaisai";last;}
                }
                open(RR,">$recordsfile") ;
		eval 'flock(RR,2);';
		seek(RR,0,0);	print RR @rr;
		eval 'flock(RR,8);';
	        close(RR);
     }# if

                $shiki = 0;
        if($llif[$k] < 1 && abs($llif[$k]-$llif[$kk]) > 510){
                $shiki = 6;&shinkiro;
        $sa = "９馬身圧勝！";$tyakusa = 1;$tekitou2 = $tekitou + int(rand(3)) + 3;
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  > 450){
        $sa = "８馬身差";$tyakusa = 0;$tekitou2 = $tekitou + int(rand(2)) + 5;
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  > 390){
        $sa = "７馬身差";$tyakusa = 0;$tekitou2 = $tekitou + int(rand(2)) + 5;
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  > 330){
        $sa = "６馬身差";$tyakusa = 0;$tekitou2 = $tekitou + int(rand(2)) + 5;
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  > 270){
        $sa = "５馬身差";$tyakusa = 0;$tekitou2 = $tekitou + int(rand(2)) + 5;
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  > 210){
        $sa = "４馬身差";$tyakusa = 0;$tekitou2 = $tekitou + int(rand(2)) + 5;
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  > 150){
        $sa = "３馬身差";$tyakusa = 0;$tekitou2 = $tekitou + int(rand(2)) + 4;
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  > 90){
        $sa = "２馬身差";$tyakusa = 0;$tekitou2 = $tekitou + int(rand(2)) + 3;
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  > 40){
        $sa = "１馬身差";$tyakusa = 0;$tekitou2 = $tekitou + int(rand(1)) + 2;
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  > 25){
        $sa = "半馬身差";$tyakusa = 0;$tekitou2 = $tekitou + int(rand(1)) + 2;
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  > 10){
        $sa = "アタマ差";$tyakusa = 0;$tekitou2 = $tekitou + int(rand(1));
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  > 5){
        $sa = "クビ差";$tyakusa = 0;$tekitou2 = $tekitou + int(rand(1));
                } elsif($llif[$k] < 1 && abs($llif[$k]-$llif[$kk])  >= 0){
        $sa = "ハナ差";$tyakusa = 0;$tekitou2 = $tekitou;}
                
                $tekitou3 = 0;
                $flag=0;

                if($tekitou2 > 9){$tekitou3 = $tekitou2 - 10;$tyakusa++;$flag=1;}
                $losetime = $wintime + $tyakusa;   # 負け馬タイム

      if($flag eq "1"){
              if($losetime > 59){$losetime2 = $losetime - 60;
                   $losetimeda = "2′$losetime2″$tekitou3";
                   $losetimes = "2<t>$losetime2<t>$tekitou3";}
              else{$losetimeda = "1′$losetime″$tekitou3";
                   $losetimes = "1<t>$losetime<t>$tekitou3";}
      }else{
              if($losetime > 59){$losetime2 = $losetime - 60;
                   $losetimeda = "2′$losetime2″$tekitou2";
                   $losetimes = "2<t>$losetime2<t>$tekitou2";}
              else{$losetimeda = "1′$losetime″$tekitou2";
                   $losetimes = "1<t>$losetime<t>$tekitou2";}
      }


                if($rkana == 1){$rdesu = "<font color=red>レコード</font>";}
                if($a[1] eq $lname[$k]){$katikisyu="$a[12]";$makekisyu="$b[12]";}
                else{$katikisyu="$b[12]";$makekisyu="$a[12]";}
                if($form{'gaisen'} ne "7"){
                &kisyurank;}

      }# ゴール処理

   }# while

        $tt = int(rand(20) * 0.2);
        if($lname[$k] eq $b[1]){$i=1; $j=0;}
        else{$i=0; $j=1;}

	($lno[$i], $lname[$i], $lsakusya[$i], $lhomepage[$i], $llif[$i], $lpow[$i], $ldef[$i], $lspe[$i], $ldate[$i], $lip[$i], $licon[$i], $lwin[$i], $lsyu[$i], $ltotal[$i], $ltyoushi[$i], $lashi[$i], $losu[$i], $lmesu[$i], $lsei[$i], $lketou[$i], $lbaku[$i], $pass[$i], $gazou[$i], $rennsyou[$i], $maxren[$i], $records[$i], $records16[$i], $records18[$i], $records22[$i], $records24[$i], $st[$i], $titi[$i], $tiha[$i], $tititi[$i], $titiha[$i], $tihati[$i], $tihaha[$i], $hati[$i], $haha[$i], $hatiti[$i], $hatiha[$i], $hahati[$i], $hahaha[$i], $checkketou1[$i], $checkketou2[$i], $checkketou3[$i], $tokusyu[$i], $formkon[$i], $dmy, $dmy, $dmy) = split(/<>/,$lines[$i]);
        $lwin[$i]++;
        $ltotal[$i]++;
        if(rand(50) > 30){$ltyoushi[$i] = $ltyoushi[$i] + $tt;
        }else{
        $ltyoushi[$i] = $ltyoushi[$i] - $tt;}
        if($ltyoushi[$i] < 1){$ltyoushi[$i] = 1;}
        elsif($ltyoushi[$i] > 9){$ltyoushi[$i] = 9;}
        if($maxren[$i] eq ""){$maxren[$i] = $rennsyou[$i];}
   if($rennsyou[$i] eq "" || $rennsyou[$i] < 0){$rennsyou[$i] = 1;}else{$rennsyou[$i]++;}
        if($rennsyou[$i] > $maxren[$i]){$maxren[$i] = $rennsyou[$i];}
        ($winhun, $winbyou, $winnan) = split(/<t>/,$wintimes);

    if($kyori eq "2000"){
        ($winhunt, $winbyout, $winnant) = split(/<t>/,$records[$i]);
        if($records[$i] eq ""){$records[$i] = "$wintimes";}
        elsif( ($winhun < $winhunt) || ($winhun == $winhunt && $winbyou < $winbyout) || ($winhun == $winhunt && $winbyou == $winbyout && $winnan < $winnant) ){
        $records[$i] = "$wintimes";}
    }elsif($kyori eq "1600"){
        ($winhunt, $winbyout, $winnant) = split(/<t>/,$records16[$i]);
        if($records16[$i] eq ""){$records16[$i] = "$wintimes";}
        elsif( ($winhun < $winhunt) || ($winhun == $winhunt && $winbyou < $winbyout) || ($winhun == $winhunt && $winbyou == $winbyout && $winnan < $winnant) ){
        $records16[$i] = "$wintimes";}
    }elsif($kyori eq "1800"){
        ($winhunt, $winbyout, $winnant) = split(/<t>/,$records18[$i]);
        if($records18[$i] eq ""){$records18[$i] = "$wintimes";}
        elsif( ($winhun < $winhunt) || ($winhun == $winhunt && $winbyou < $winbyout) || ($winhun == $winhunt && $winbyou == $winbyout && $winnan < $winnant) ){
        $records18[$i] = "$wintimes";}
    }elsif($kyori eq "2200"){
        ($winhunt, $winbyout, $winnant) = split(/<t>/,$records22[$i]);
        if($records22[$i] eq ""){$records22[$i] = "$wintimes";}
        elsif( ($winhun < $winhunt) || ($winhun == $winhunt && $winbyou < $winbyout) || ($winhun == $winhunt && $winbyou == $winbyout && $winnan < $winnant) ){
        $records22[$i] = "$wintimes";}
    }elsif($kyori eq "2400"){
        ($winhunt, $winbyout, $winnant) = split(/<t>/,$records24[$i]);
        if($records24[$i] eq ""){$records24[$i] = "$wintimes";}
        elsif( ($winhun < $winhunt) || ($winhun == $winhunt && $winbyou < $winbyout) || ($winhun == $winhunt && $winbyou == $winbyout && $winnan < $winnant) ){
        $records24[$i] = "$wintimes";}
    }


# 時間	
	$times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

	$month = sprintf("%02d",$mon +1);    # 最終レース時間
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
	$gjikan = "$month<g>$mday<g>$hour<g>$min";

        if($lsakusya[$i] eq $formlogint){
        $lsyu[$i] = "$formkisyu";
        $lashi[$i] = "$formashi";
        }
	$winner = "$lno[$i]<>$lname[$i]<>$lsakusya[$i]<>$lhomepage[$i]<>$llif[$i]<>$lpow[$i]<>$ldef[$i]<>$lspe[$i]<>$gjikan<>$lip[$i]<>$licon[$i]<>$lwin[$i]<>$lsyu[$i]<>$ltotal[$i]<>$ltyoushi[$i]<>$lashi[$i]<>$losu[$i]<>$lmesu[$i]<>$lsei[$i]<>$lketou[$i]<>$lbaku[$i]<>$pass[$i]<>$gazou[$i]<>$rennsyou[$i]<>$maxren[$i]<>$records[$i]<>$records16[$i]<>$records18[$i]<>$records22[$i]<>$records24[$i]<>$st[$i]<>$titi[$i]<>$tiha[$i]<>$tititi[$i]<>$titiha[$i]<>$tihati[$i]<>$tihaha[$i]<>$hati[$i]<>$haha[$i]<>$hatiti[$i]<>$hatiha[$i]<>$hahati[$i]<>$hahaha[$i]<>$checkketou1[$i]<>$checkketou2[$i]<>$checkketou3[$i]<>$tokusyu[$i]<>$formkon[$i]<>$dmy<>$dmy<>$dmy<>\n";
        $winnero = "$lsakusya[$i]<>$lwin[$i]<>\n";
        $winnersyu = "$losu[$i]<>\n";
        $winnermes = "$lmesu[$i]<>\n";

        if($licon[$i] == uma1.gif){$katikeiro = 1;}
        elsif($licon[$i] == uma2.gif){$katikeiro = 2;}
        elsif($licon[$i] == uma3.gif){$katikeiro = 3;}
        elsif($licon[$i] == uma4.gif){$katikeiro = 4;}
        elsif($licon[$i] == uma5.gif){$katikeiro = 5;}
        elsif($licon[$i] == uma6.gif){$katikeiro = 6;}
        elsif($licon[$i] == uma7.gif){$katikeiro = 7;}
        elsif($licon[$i] == uma8.gif){$katikeiro = 8;}
        elsif($licon[$i] == uma9.gif){$katikeiro = 9;}
        else{$katikeiro = 10;}

        $tty = int(rand(20) * 0.2);

        ($lno[$j], $lname[$j], $lsakusya[$j], $lhomepage[$j], $llif[$j], $lpow[$j], $ldef[$j], $lspe[$j], $ldate[$j], $lip[$j], $licon[$j], $lwin[$j], $lsyu[$j], $ltotal[$j], $ltyoushi[$j], $lashi[$j], $losu[$j], $lmesu[$j], $lsei[$j], $lketou[$j], $lbaku[$j], $pass[$j], $gazou[$j], $rennsyou[$j], $maxren[$j], $records[$j], $records16[$j], $records18[$j], $records22[$j], $records24[$j], $st[$j], $titi[$j], $tiha[$j], $tititi[$j], $titiha[$j], $tihati[$j], $tihaha[$j], $hati[$j], $haha[$j], $hatiti[$j], $hatiha[$j], $hahati[$j], $hahaha[$j], $checkketou1[$j], $checkketou2[$j], $checkketou3[$j], $tokusyu[$j], $formkon[$j], $dmy, $dmy, $dmy) = split(/<>/,$lines[$j]);
        $ltotal[$j]++;
        if(rand(50) > 20){$ltyoushi[$j] = $ltyoushi[$j] + $tty;
        }else{
        $ltyoushi[$j] = $ltyoushi[$j] - $tty;}
        if($ltyoushi[$j] < 1){$ltyoushi[$j] = 1;}
        elsif($ltyoushi[$j] > 9){$ltyoushi[$j] = 9;}
        if($rennsyou[$j] >= 7){$shiki = 8;&shinkiro;}
        if($maxren[$j] eq ""){$maxren[$j] = $rennsyou[$j];}
        elsif($rennsyou[$j] > $maxren[$j]){$maxren[$j] = $rennsyou[$j];}
        if($rennsyou[$j] >= 0){$rennsyou[$j] = -1;
        }else{$rennsyou[$j]--;}
        ($losehun, $losebyou, $losenan) = split(/<t>/,$losetimes);

    if($kyori eq "2000"){
        ($losehunt, $losebyout, $losenant) = split(/<t>/,$records[$j]);
        if($records[$j] eq ""){$records[$j] = "$losetimes";}
        elsif( ($losehun < $losehunt) || ($losehun == $losehunt && $losebyou < $losebyout) || ($losehun == $losehunt && $losebyou == $losebyout && $losenan < $losenant) ){
        $records[$j] = "$losetimes";}
    }elsif($kyori eq "1600"){
        ($losehunt, $losebyout, $losenant) = split(/<t>/,$records16[$j]);
        if($records16[$j] eq ""){$records16[$j] = "$losetimes";}
        elsif( ($losehun < $losehunt) || ($losehun == $losehunt && $losebyou < $losebyout) || ($losehun == $losehunt && $losebyou == $losebyout && $losenan < $losenant) ){
        $records16[$j] = "$losetimes";}
    }elsif($kyori eq "1800"){
        ($losehunt, $losebyout, $losenant) = split(/<t>/,$records18[$j]);
        if($records18[$j] eq ""){$records18[$j] = "$losetimes";}
        elsif( ($losehun < $losehunt) || ($losehun == $losehunt && $losebyou < $losebyout) || ($losehun == $losehunt && $losebyou == $losebyout && $losenan < $losenant) ){
        $records18[$j] = "$losetimes";}
    }elsif($kyori eq "2200"){
        ($losehunt, $losebyout, $losenant) = split(/<t>/,$records22[$j]);
        if($records22[$j] eq ""){$records22[$j] = "$losetimes";}
        elsif( ($losehun < $losehunt) || ($losehun == $losehunt && $losebyou < $losebyout) || ($losehun == $losehunt && $losebyou == $losebyout && $losenan < $losenant) ){
        $records22[$j] = "$losetimes";}
    }elsif($kyori eq "2400"){
        ($losehunt, $losebyout, $losenant) = split(/<t>/,$records24[$j]);
        if($records24[$j] eq ""){$records24[$j] = "$losetimes";}
        elsif( ($losehun < $losehunt) || ($losehun == $losehunt && $losebyou < $losebyout) || ($losehun == $losehunt && $losebyou == $losebyout && $losenan < $losenant) ){
        $records24[$j] = "$losetimes";}
    }

        if($lsakusya[$j] eq $formlogint){
        $lsyu[$j] = "$formkisyu";
        $lashi[$j] = "$formashi";
        }
        $loser = "$lno[$j]<>$lname[$j]<>$lsakusya[$j]<>$lhomepage[$j]<>$llif[$j]<>$lpow[$j]<>$ldef[$j]<>$lspe[$j]<>$gjikan<>$lip[$j]<>$licon[$j]<>$lwin[$j]<>$lsyu[$j]<>$ltotal[$j]<>$ltyoushi[$j]<>$lashi[$j]<>$losu[$j]<>$lmesu[$j]<>$lsei[$j]<>$lketou[$j]<>$lbaku[$j]<>$pass[$j]<>$gazou[$j]<>$rennsyou[$j]<>$maxren[$j]<>$records[$j]<>$records16[$j]<>$records18[$j]<>$records22[$j]<>$records24[$j]<>$st[$j]<>$titi[$j]<>$tiha[$j]<>$tititi[$j]<>$titiha[$j]<>$tihati[$j]<>$tihaha[$j]<>$hati[$j]<>$haha[$j]<>$hatiti[$j]<>$hatiha[$j]<>$hahati[$j]<>$hahaha[$j]<>$checkketou1[$j]<>$checkketou2[$j]<>$checkketou3[$j]<>$tokusyu[$j]<>$formkon[$j]<>$dmy<>$dmy<>$dmy<>\n";

        if($licon[$j] == uma1.gif){$makekeiro = 1;}
        elsif($licon[$j] == uma2.gif){$makekeiro = 2;}
        elsif($licon[$j] == uma3.gif){$makekeiro = 3;}
        elsif($licon[$j] == uma4.gif){$makekeiro = 4;}
        elsif($licon[$j] == uma5.gif){$makekeiro = 5;}
        elsif($licon[$j] == uma6.gif){$makekeiro = 6;}
        elsif($licon[$j] == uma7.gif){$makekeiro = 7;}
        elsif($licon[$j] == uma8.gif){$makekeiro = 8;}
        elsif($licon[$j] == uma9.gif){$makekeiro = 9;}
        else{$makekeiro = 10;}

        @wi = split(/<>/,$winner);
        @lo = split(/<>/,$loser);

        $log[$m] = "<B>$lname[$k]</B><font color=gold>$sa</font>でゴール！現在<B><font color=red>$lwin[$i]勝目！</B></font>タイムは$wintimeda$rdesu<>"; #5
	$m++;

##### javaレース
         
         for($i=0; $i<$#dmg; $i++){
         ($ti, $me) = split(/<>/,$dmg[$i]);
         $tii = int(($ti/10)+0.5);
         $saw = $ti - ($tii * 10);
         $tiii = $tii + $saw;
         $dmg[$i] = "$tii,$tii,$tii,$tii,$tiii,$tii,$tii,$tii,$tii,$tii,";
         }
         ($ti, $me) = split(/<>/,$dmg[$#dmg]);
         $tii = int(($ti/10)+0.5);
         $saw = $ti - ($tii * 10);
         $tiii = $tii + $saw;
         $dmg[$#dmg] = "$tiii,$tii,$tii,$tii,$tii,$tii,$tii,$tii,$tii,$tii";

         $log[$m] = "@dmg<>";     #6
         $m++;

         for($i=0; $i<$#dmg2; $i++){
         ($ti, $me) = split(/<>/,$dmg2[$i]);
         $tii = int(($ti/10)+0.5);
         $saw = $ti - ($tii * 10);
         $tiii = $tii + $saw;
         $dmg2[$i] = "$tii,$tii,$tii,$tii,$tiii,$tii,$tii,$tii,$tii,$tii,";
         }
         ($ti, $me) = split(/<>/,$dmg2[$#dmg2]);
         $tii = int(($ti/10)+0.5);
         $saw = $ti - ($tii * 10);
         $tiii = $tii + $saw;
         $dmg2[$#dmg2] = "$tiii,$tii,$tii,$tii,$tii,$tii,$tii,$tii,$tii,$tii";

         $log[$m] = "@dmg2\n";   #7
         $m++;

if($form{'gaisen'} ne "7"){

##### 対戦記録ファイルの更新

	open(FG,"$fightfile");
	seek(FG,0,0);  @fg = <FG>;  close(FG);

	unshift (@fg , join('' , @log));
	splice( @fg, $max_fight);

	open(FG,">$fightfile") ;
		eval 'flock(FG,2);';
		seek(FG,0,0);	print FG @fg;
		eval 'flock(FG,8);';
	close(FG);

###### チャンピオンを記録
        @nowwinner = split(/<>/,$winner);
        @nowloser = split(/<>/,$loser);
        if($nowwinner[13] < $racemax){$winer[0] = $winner;}
        else{$winer[0] = $loser;}

	open(TT,">$winfile") ;
		eval 'flock(TT,2);';
		seek(TT,0,0);	print TT @winer;
		eval 'flock(TT,8);';
	close(TT);

###### オーナーランキングファイルの更新

	open(OK,"$orfile");
	seek(OK,0,0);  @orank = <OK>;  close(OK);

	@wino = split(/<>/,$winnero);
                foreach $check (@orank){
		@check = split(/<>/,$check);
        if($wino[0] eq $check[0]){$winoooo = $wino[0];$winooo = $check[1]+1;$check = '';$flag=3;last;}      }
        if($flag eq "3"){$winnerp = "$winoooo<>$winooo<>\n";}

                @winp = split(/<>/,$winnerp);
                $shiki = 0;
        if($winp[1] % 100 == 0 && $winp[1] ne "0" && $winp[1] ne ""){$shiki = 1;&shinkiro;}
                $flag=0;
        foreach $check (@orank){
		@check = split(/<>/,$check);
	if($winp[1] > $check[1]){$check = "$winnerp$check";$flag=2;last;}
		elsif($winp[1] eq $check[1]){$check = "$winnerp$check";$flag=2;last;}
		}
	if($flag ne "2"){push(@orank,$winnerp);}
	
	
	open(OK,">$orfile") ;
		eval 'flock(OK,2);';
		seek(OK,0,0);	print OK @orank;
		eval 'flock(OK,8);';
	close(OK);

###### 種牡馬・繁殖牝馬ランキングファイルの更新

	open(SK,"$syurankfile");
	seek(SK,0,0);  @syurank = <SK>;  close(SK);

	@wins = split(/<>/,$winnersyu);
        $flag=0;
                foreach $check (@syurank){
		@check = split(/<>/,$check);
        if($wins[0] eq $check[0]){$winssss = $wins[0];$winsss = $check[1]+1;$check = '';$flag=3;last;}      }
        if($flag eq "3"){$winnerz = "$winssss<>$winsss<>\n";}
        else{$winnerz = "$wins[0]<>1<>\n";}

                @winz = split(/<>/,$winnerz);
                $shiki = 0;
        if($winz[1] % 100 == 0 && $winz[1] ne "0"){$shiki = 2;&shinkiro;}
                $flag=0;
		foreach $check (@syurank){
		@check = split(/<>/,$check);
	if($winz[1] > $check[1]){$check = "$winnerz$check";$flag=2;last;}
		elsif($winz[1] eq $check[1]){$check = "$winnerz$check";$flag=2;last;}
		}
	if($flag ne "2"){push(@syurank,$winnerz);}
	
	open(SK,">$syurankfile") ;
		eval 'flock(SK,2);';
		seek(SK,0,0);	print SK @syurank;
		eval 'flock(SK,8);';
	close(SK);


        open(SM,"$mesrankfile");
	seek(SM,0,0);  @mesrank = <SM>;  close(SM);

	@winm = split(/<>/,$winnermes);
        $flag=0;
                foreach $checkm (@mesrank){
		@checkm = split(/<>/,$checkm);
      if($winm[0] eq $checkm[0]){$winmmmm = $winm[0];$winmmm = $checkm[1]+1;$checkm = '';$flag=3;last;}      }
        if($flag eq "3"){$winnerzm = "$winmmmm<>$winmmm<>\n";}
        else{$winnerzm = "$winm[0]<>1<>\n";}

                @winzm = split(/<>/,$winnerzm);
                $shiki = 0;
        if($winzm[1] % 100 == 0 && $winzm[1] ne "0"){$shiki = 3;&shinkiro;}
                $flag=0;
		foreach $checkm (@mesrank){
		@checkm = split(/<>/,$checkm);
	if($winzm[1] > $checkm[1]){$checkm = "$winnerzm$checkm";$flag=2;last;}
		elsif($winzm[1] eq $checkm[1]){$checkm = "$winnerzm$checkm";$flag=2;last;}
		}
	if($flag ne "2"){push(@mesrank,$winnerzm);}
	
	open(SM,">$mesrankfile") ;
		eval 'flock(SM,2);';
		seek(SM,0,0);	print SM @mesrank;
		eval 'flock(SM,8);';
	close(SM);


###### 現役処理

        @win = split(/<>/,$winner);
        @los = split(/<>/,$loser);

        open(DB,"$logfile");
	seek(DB,0,0);  @line = <DB>;  close(DB);

                foreach $check (@line){             # 勝ち馬を消す
		@check = split(/<>/,$check);
		if($win[1] eq $check[1]){$check = '';last;}
		}
                foreach $check (@line){             # 負け馬を消す
		@check = split(/<>/,$check);
		if($los[1] eq $check[1]){$check = '';last;}
		}

        open(DB,">$logfile") ;
		eval 'flock(DB,2);';
		seek(DB,0,0);	print DB @line;
	eval 'flock(DB,8);';
        close(DB);

        open(DB,"$logfile");
	seek(DB,0,0);  @line = <DB>;  close(DB);

                $flag=0;
        foreach $check (@line){                     # 勝ち馬を記入
		@check = split(/<>/,$check);
		if($win[11] > $check[11]){$check = "$winner$check";$flag=1;last;}
		elsif($win[11] eq $check[11] && $win[13] < $check[13]){$check = "$winner$check";$flag=1;last;}
                elsif($win[11] eq $check[11] && $win[13] == $check[13] && $win[24] > $check[24]){$check = "$winner$check";$flag=1;last;}
		}
		if($flag ne "1"){push(@line,$winner);}

        open(DB,">$logfile") ;
		eval 'flock(DB,2);';
		seek(DB,0,0);	print DB @line;
		eval 'flock(DB,8);';
	close(DB);

        open(DB,"$logfile");
	seek(DB,0,0);  @line = <DB>;  close(DB);

                $flag=0;
        foreach $check (@line){                     # 負け馬を記入
		@check = split(/<>/,$check);
		if($los[11] > $check[11]){$check = "$loser$check";$flag=1;last;}
		elsif($los[11] eq $check[11] && $los[13] < $check[13]){$check = "$loser$check";$flag=1;last;}
                elsif($los[11] eq $check[11] && $los[13] == $check[13] && $los[24] > $check[24]){$check = "$loser$check";$flag=1;last;}
		}
		if($flag ne "1"){push(@line,$loser);}

	open(DB,">$logfile") ;
		eval 'flock(DB,2);';
		seek(DB,0,0);	print DB @line;
		eval 'flock(DB,8);';
	close(DB);

    }else{ # 凱旋門
        @los = split(/<>/,$loser);
        @win = split(/<>/,$winner);
        $ato = 1;   #レース画面に行く用
      if($c[1] eq $win[1]){
       $gai = 1;
      }else{
      $gai = 0;
      }

##### 対戦記録ファイルの更新

	open(FG,"$fightfile");
	seek(FG,0,0);  @fg = <FG>;  close(FG);

	unshift (@fg , join('' , @log));
	splice( @fg, $max_fight);

	open(FG,">$fightfile") ;
		eval 'flock(FG,2);';
		seek(FG,0,0);	print FG @fg;
		eval 'flock(FG,8);';
	close(FG);

        open(GFG,"$gaifightfile");        # 凱旋門専用
	seek(GFG,0,0);  @gfg = <GFG>;  close(GFG);

       unshift (@gfg , join('' , @log));
       splice(@gfg, 5);

	open(GFG,">$gaifightfile") ;
		eval 'flock(GFG,2);';
		seek(GFG,0,0);	print GFG @gfg;
		eval 'flock(GFG,8);';
	close(GFG);

##### 歴代優勝馬に記録
     if($gai eq "1"){

       open(PST,"$pastfile");
       seek(PST,0,0);  @pst = <PST>;  close(PST);

($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $osu, $mesu, $sei, $ketou, $baku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,@pst[0]);

          $yatta = "-2<>$name<>$sakusya<>$homepage<>$lif<>$pow<>$def<>$spe<>$date<>$ip<>$icon<>$win<>$syu<>$total<>5<>$ashi<>$osu<>$mesu<>$sei<>$ketou<>$baku<>$pass<>$gazou<>$rennsyou<>$maxren<>$records<>$records16<>$records18<>$records22<>$records24<>$st<>$titi<>$tiha<>$tititi<>$titiha<>$tihati<>$tihaha<>$hati<>$haha<>$hatiti<>$hatiha<>$hahati<>$hahaha<>$checkketou1<>$checkketou2<>$checkketou3<>$tokusyu<>$formkon<>$dmy<>$dmy<>$dmy<>\n";

      splice(@pst,0,1);

@pst = reverse(@pst);
        push(@pst,$yatta);
@pst = reverse(@pst);
        open(PST,">$pastfile");
        eval 'flock(PST,2);';
	seek(PST,0,0);	print PST @pst;
	eval 'flock(PST,8);';
        close(PST);
       }

   }
# ロック解除

        $times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

	$gamelock = "0<>$times<>\n";

	open(GL,"+<$lockfile");
	eval 'flock(GL,2);';
	truncate (GL, 0);
	seek(GL,0,0);	print GL $gamelock;
	close(GL);
	eval 'flock(GL,8);';
        
}#end syori


sub kisyurank{
###### 騎手ランキングファイルの更新

	open(KK,"$kisyufile");
	seek(KK,0,0);  @kisyurank = <KK>;  close(KK);

        foreach $check (@kisyurank){
	@check = split(/<>/,$check);
        if($katikisyu eq $check[0]){$winkisyu = "$check";last;}
        }

        ($wname, $wcomm, $wwin, $wlose, $womona, $womona2, $womona3, $dmy, $dmy, $dmy) = split(/<>/,$winkisyu);

        if($katikisyu eq $makekisyu)
        {$wwin++;$wlose++;}else{$wwin++;}

        $winkisyu = "$wname<>$wcomm<>$wwin<>$wlose<>$womona<>$womona2<>$womona3<>$dmy<>$dmy<>$dmy<>\n";
        @checkw = split(/<>/,$winkisyu);

	foreach $check (@kisyurank){
	@check = split(/<>/,$check);
	if($checkw[0] eq $check[0]){$check = "$winkisyu";last;}
        }
	
	open(KK,">$kisyufile") ;
		eval 'flock(KK,2);';
		seek(KK,0,0);	print KK @kisyurank;
		eval 'flock(KK,8);';
	close(KK);

  if($katikisyu ne $makekisyu){

        open(KK,"$kisyufile");
	seek(KK,0,0);  @kisyurank = <KK>;  close(KK);

        foreach $check (@kisyurank){
	@check = split(/<>/,$check);
        if($makekisyu eq $check[0]){$losekisyu = "$check";last;}
        }

        ($name, $comm, $win, $lose, $omona, $omona2, $womona3, $dmy, $dmy, $dmy) = split(/<>/,$losekisyu);

        $lose++;

    $losekisyu = "$name<>$comm<>$win<>$lose<>$omona<>$omona2<>$womona3<>$dmy<>$dmy<>$dmy<>\n";
        @checks = split(/<>/,$losekisyu);
        
	foreach $check (@kisyurank){
	@check = split(/<>/,$check);
        if($checks[0] eq $check[0]){$check = "$losekisyu";last;}
        }
        
        open(KK,">$kisyufile") ;
		eval 'flock(KK,2);';
		seek(KK,0,0);	print KK @kisyurank;
		eval 'flock(KK,8);';
	close(KK);
 }

} #end kisyuran

##### 戦いの具体的な記録
sub fight{

	if($ato eq "1"){$no = 1;
        }
        else{
        $no = $form{'no'};
        }
	$no--;

if($no >= 700){

        $ga = $no - 700;
        open(EE,"$gaifightfile");
        seek(EE,0,0);  @ee = <EE>;  close(EE);
        @ew = split(/<>/,$ee[$ga]);
        $er = $ew[0];#$month月$mday日$hour時$min分のレース<br><center>（$kaitis $kyoriｍ）
        $err = $ew[1];  # $a[1]
        $errr = $ew[2];  # $b[1]
    $prof = $ew[3];  #$a[1](icon)：$a[12]：$a[15]：$conditiona：$a[11]勝$hai敗（$senreki）
    $prog = $ew[4];
    $goul = $ew[5];     # $lname[$k]$saでゴール！勝ちタイムは$wintimeda。現在$lwin[$i]勝目
        $saa = $ew[6];
        $ssa = $ew[7];

}else{

        open(EE,"$fightfile");
        seek(EE,0,0);  @ee = <EE>;  close(EE);
        @ew = split(/<>/,$ee[$no]);
        $er = $ew[0];#$month月$mday日$hour時$min分のレース<br><center>（$kaitis $kyoriｍ）
        $err = $ew[1];  # $a[1]
        $errr = $ew[2];  # $b[1]
    $prof = $ew[3];  #$a[1](icon)：$a[12]：$a[15]：$conditiona：$a[11]勝$hai敗（$senreki）
    $prog = $ew[4];
    $goul = $ew[5];     # $lname[$k]$saでゴール！勝ちタイムは$wintimeda。現在$lwin[$i]勝目
        $saa = $ew[6];
        $ssa = $ew[7];

}
        @saa = split(/,/,$saa);
        for ($i=0; $i<$#saa+1; $i++){
        $da += $saa[$i];
        }
        @ssa = split(/,/,$ssa);
        for ($i=0; $i<$#ssa+1; $i++){
        $db += $ssa[$i];
        }

        if($er =~ m/1600/){$kyori="1600";$start="230";}
     elsif($er =~ m/1800/){$kyori="1800";$start="-30";}
     elsif($er =~ m/2000/){$kyori="2000";$start="-230";}
     elsif($er =~ m/2200/){$kyori="2200";$start="-430";}
     elsif($er =~ m/2400/){$kyori="2400";$start="-630";}

        $da = $da - $kyori + 680;
        $db = $db - $kyori + 680;

        if($da > $db){$dd = $da;}else{$dd=$db;}

        if($er =~ m/東京/){$kaisai="tokyo";}
     elsif($er =~ m/京都/){$kaisai="kyoto";}
     elsif($er =~ m/新潟/){$kaisai="niigata";}
     elsif($er =~ m/阪神/){$kaisai="hanshin";}
     elsif($er =~ m/中京/){$kaisai="chukyo";}
     elsif($er =~ m/札幌/){$kaisai="sapporo";}
     elsif($er =~ m/函館/){$kaisai="hakodate";}
     elsif($er =~ m/小倉/){$kaisai="kokura";}
     elsif($er =~ m/福島/){$kaisai="fukushima";}
     elsif($er =~ m/中山/){$kaisai="nakayama";}
                      else{$kaisai="ronsyan";$background = "$backgaisenmon";}

        if($prof =~ m/黒鹿毛/){$icon="uma2.gif";}
     elsif($prof =~ m/青鹿毛/){$icon="uma6.gif";}
     elsif($prof =~ m/鹿毛/){$icon="uma1.gif";}
     elsif($prof =~ m/尾花栗毛/){$icon="uma5.gif";}
     elsif($prof =~ m/栗毛/){$icon="uma4.gif";}
     elsif($prof =~ m/青毛/){$icon="uma7.gif";}
     else{$icon="uma8.gif";}

        if($prog =~ m/黒鹿毛/){$icong="uma2.gif";}
     elsif($prog =~ m/青鹿毛/){$icong="uma6.gif";}
     elsif($prog =~ m/鹿毛/){$icong="uma1.gif";}
     elsif($prog =~ m/尾花栗毛/){$icong="uma5.gif";}
     elsif($prog =~ m/栗毛/){$icong="uma4.gif";}
     elsif($prog =~ m/青毛/){$icong="uma7.gif";}
     else{$icong="uma8.gif";}
    

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_EOF_";

<html><head><title>$title2</title>

<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis">
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>

</head>

<center><P>
$er<br><br>
<table border=1><tr><td><font color=blue><B>■</B></font>$prof</td></tr><tr><td><font color=green><B>■</B></font>$prog</td></tr></table>
<br><center>

<SCRIPT type="text/javascript">

document.write('<center><table border=3 width=1300 height=250><tr><td bgcolor=green>');
document.write('<DIV style=position=relative width=1300 height=250 align=center>');
document.write('<IMG src=$imgurl/uma11.gif id=midoten Name=Hanabi width=55 height=37 style=position:relative;><br>');
document.write('<IMG src=$imgurl/uma11.gif id=midote Name=Hanab width=55 height=37 style=position:relative;><br>');

InitY=$start;
InitX=$start;
kyori=$kyori;
hankyori=($kyori-1200);
var judgeflg;
var cnt;
var damage;
var damag;
var modosu;
var shita;
var Img1 = new Image(); Img1.src="$imgurl/k1.gif";//右から左へ(上)
var Img3 = new Image(); Img3.src="$imgurl/k3.gif";//左から右へ(上)
var Img4 = new Image(); Img4.src="$imgurl/uma11.gif";//動かない馬(スタート前)
var Img5 = new Image(); Img5.src="$imgurl/$kaisai.gif";//ゴール板
var Img6 = new Image(); Img6.src="$imgurl/k2.gif";//右から左へ(下)
var Img7 = new Image(); Img7.src="$imgurl/umuti$icon";//鞭(上)
var Img8 = new Image(); Img8.src="$imgurl/smuti$icong";//鞭(下)
var Img9 = new Image(); Img9.src="$imgurl/k4.gif";//左から右へ(下)
DATAA = new Array($saa);
DATAB = new Array($ssa);

function InitProc(){
   //変数初期化
   cnt=-1;
   damage=0;
   damag=0;
   modosu=0;
   shita=0;
   turn = DATAA.length;

   //画像を戻す
   Hanabi.src=Img4.src;
   Hanabi.width=55;
   Hanabi.height=37;
   Hanab.src=Img4.src;
   Hanab.width=55;
   Hanab.height=37;

   //初期の位置
   InitMidoten();
}

function InitMidoten(){
   midoten.style.posLeft  = InitY;
   midote.style.posLeft  = InitX;
   midoten.style.posTop  = -5;
   midote.style.posTop  = 0;
}
function ShowKazariTrue(){
   InitProc();
   ShowHanabi();
}
function ShowHanabi(){
   timer1 = setTimeout('MoveHanabi()',70);
}
function MoveHanabi(){
  clearTimeout(timer1);
if (cnt == -1){//スタート前

      Hanabi.src=Img4.src;
      Hanab.src=Img4.src;
      timer1=setTimeout('MoveHanabi()',1500);
}
else if ( damage < hankyori && damag < hankyori ){//上

      if (modosu == 0){modosu=1;Hanabi.src=Img3.src;Hanab.src=Img9.src;
      document.getElementById('comm').innerHTML='<b>スタートしました！</b>';}
      midoten.style.posLeft += (DATAA[cnt]);
      midote.style.posLeft += (DATAB[cnt]);
      timer1=setTimeout('MoveHanabi()',100);
}
else if ( cnt < turn ){//下

      if (modosu == 5 && (kyori - damage) < 50){modosu=6;Hanabi.src=Img1.src;}
      if (shita == 3 && (kyori - damag) < 50){shita=4;Hanab.src=Img6.src;}

      if (modosu == 4 && (kyori - damage) < 400){modosu=5;Hanabi.src=Img7.src;}
      if (shita == 2 && (kyori - damag) < 400){shita=3;Hanab.src=Img8.src;}

      if (modosu == 3 && (kyori - damage) < 600){modosu=4;Hanabi.src=Img1.src;}
      if (shita == 1 && (kyori - damag) < 600){shita=2;Hanab.src=Img6.src;}

      if (modosu == 2 && (kyori - damage) < 800){modosu=3;Hanabi.src=Img7.src;}
      if (shita == 0 && (kyori - damag) < 800){shita=1;Hanab.src=Img8.src;}

      if (modosu == 1 && damage > damag){midoten.style.posLeft  = $dd;modosu=2;Hanabi.src=Img1.src;document.getElementById('comm').innerHTML='<b>さぁ最後の直線！</b>';midote.style.posLeft  = $dd + (damage - damag);Hanab.src=Img6.src;Ban.src=Img5.src;Ban.height=45;}

      if (modosu == 1 && damag >= damage){midoten.style.posLeft  = $dd + (damag - damage);modosu=2;Hanabi.src=Img1.src;Ban.src=Img5.src;Ban.height=45;midote.style.posLeft  = $dd;Hanab.src=Img6.src;document.getElementById('comm').innerHTML='<b>さぁ最後の直線！</b>';}

      midoten.style.posTop  = 140;
      midote.style.posTop  = 141;
      midoten.style.posLeft -= (DATAA[cnt]);
      midote.style.posLeft -= (DATAB[cnt]);
      timer1=setTimeout('MoveHanabi()',100);

}else{//ゴール

    document.getElementById('comm').innerHTML='$goul';
      if ( $da >= $db ){
         Hanabi.src=Img6.src;
         Hanab.src=Img6.src;
      }
      else{
         Hanab.src=Img6.src;
         Hanabi.src=Img1.src;
      }
}
   cnt++;
   damage += DATAA[cnt];
   damag += DATAB[cnt];
}
document.write('<IMG src=$imgurl/saku1.gif width=650 height=20><IMG src=$imgurl/saku1.gif width=650 height=20></DIV><BR>');

document.write('</center><img src=$imgurl/saku1.gif id=ita Name=Ban width=1300 height=22><BR><BR><BR><BR><BR><BR></td></tr></table>');

document.write('<BR><div id="comm"></div>');

</SCRIPT>


<BR><BR>
<center>
<INPUT type="button" name="CorrectBtn" value="レース開始" onClick="ShowKazariTrue()">

_EOF_

if($ato eq "1"){$ato = 0;

print <<"_HTML3_";
<form action="$cgifile" method="$method">
<center>コメント
<input type=text name=comtext size=75>

<input type=hidden name=comname value="$d[2]">
<input type=hidden name=comuma value="$d[1]">
<input type=hidden name=comkati value="$win[1]">
<input type=hidden name=commake value="$los[1]">
<input type=hidden name=comsa value="$sa">
<input type=submit name=comment value="書き込む"><br><br>
</form>
_HTML3_
}
&chosaku;
}# end fight