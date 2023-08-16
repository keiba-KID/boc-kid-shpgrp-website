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

##### 有力な生産家出力
sub orank{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>有力な生産家</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<center><br><font color=red size=5><B>有力な生産家</B></font><P>

<table border="1" width="400">

<tr><td bgcolor=green><center>順位</td><td bgcolor=green><center>勝数</td><td bgcolor=green><center>名前</td><td bgcolor=green><center>ランク</td></tr>

_HTML1_

open(OK,"$orfile");
	seek(OK,0,0);  @orank = <OK>;  close(OK);

for ($i=0; $i<10; $i++){
	($sakusya[$i], $win[$i], ) = split(/<>/,$orank[$i]);
	
        if($win[$i] > 99){$iro[$i] = "#FFFF00";}
        elsif($win[$i] > 39){$iro[$i] = "#00FFFF";}
        elsif($win[$i] > 19){$iro[$i] = "#00FF00";}
        else{$iro[$i] = "000000";}
        if($win[$i] > 55){$ookisa[$i] = "4";}
        else{$ookisa[$i] = "3";}

          if($win[$i] > 999){$syou[$i] = "世界馬生産界の頂点";}
          elsif($win[$i] > 699){$syou[$i] = "日本馬界の神";}
          elsif($win[$i] > 499){$syou[$i] = "日本馬界の王";}
          elsif($win[$i] > 299){$syou[$i] = "日本馬界の救世主";}
          elsif($win[$i] > 199){$syou[$i] = "馬生産界のトップ";}
          elsif($win[$i] > 99){$syou[$i] = "馬生産家業";}
          elsif($win[$i] > 74){$syou[$i] = "馬生産人";}
          elsif($win[$i] == 77){$syou[$i] = "(ﾟдﾟ)ｳﾏｰ";}
          elsif($win[$i] > 49){$syou[$i] = "相馬眼（・∀・）ｲｲ!";}
          elsif($win[$i] > 24){$syou[$i] = "（・∀・）ｲｲ!馬生産家";}
          elsif($win[$i] > 14){$syou[$i] = "もっと馬を生産しる";}
          elsif($win[$i] > 9){$syou[$i] = "馬好き";}
          elsif($win[$i] > 4){$syou[$i] = "馬人";}
          else{$syou[$i] = "一般人";}
            
          $f = $i + 1; 
	print "<tr><td><center>$f位</td><td><center><B><font size=$ookisa[$i]>$win[$i]勝</font></B></td><td><center>$sakusya[$i]</td><td><center>$syou[$i]</td></tr>";
	}
        print "</table></center><P><center><select>";

        if($#orank >= 50){$hyouzi = 50;}else{$hyouzi = $#orank+1;}
        for ($i=10; $i<$hyouzi; $i++){
	($sakusya[$i], $win[$i], ) = split(/<>/,$orank[$i]);
        $f = $i + 1;
        print "<option>[$f] $win[$i]勝 $sakusya[$i]\n";
	}
	print "</select>";

print <<"_HTML2_";
<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" name="orank" value="有力な生産家">
<input type="submit" name="kisyu" value="騎手ランキング">
<input type="submit" name="syurank" value="種牡･繁殖ランキング">
</td></tr></table>
</form>
_HTML2_
&chosaku;
}#end orank


##### 種牡馬・繁殖牝馬ランキング
sub syurank{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>種牡馬・繁殖牝馬ランキング</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<center><br><font color=red size=5><B>種牡馬・繁殖牝馬ランキング</B></font><P>

<table border="2" width="300"><tr><td>

<table border="1" width="260">
<tr><td bgcolor=green><center>勝数</td><td bgcolor=green><center>種牡馬</td></tr>

_HTML1_

open(SK,"$syurankfile");
	seek(SK,0,0);  @syurank = <SK>;  close(SK);

for ($i=0; $i<10; $i++){
	($sakusya[$i], $win[$i]) = split(/<>/,$syurank[$i]);
	($name[$i], $toku[$i]) = split(/<mm>/,$sakusya[$i]);
        if($win[$i] > 999){$iro[$i] = "gold";}
        elsif($win[$i] > 699){$iro[$i] = "#00FFFF";}
        elsif($win[$i] > 499){$iro[$i] = "#00FF00";}
        else{$iro[$i] = "000000";}
        
	print "<tr><td><center><B><font color=$iro[$i] size=3>$win[$i]勝</font></B></td><td><center>$name[$i]</td></tr>";
	}

        print "</table></center><P><center><select>";

        if($#syurank >= 30){$hyouzi = 30;}else{$hyouzi = $#syurank+1;}
        for ($i=10; $i<$hyouzi; $i++){
	($sakusya[$i], $win[$i],) = split(/<>/,$syurank[$i]);
        ($name[$i], $toku[$i]) = split(/<mm>/,$sakusya[$i]);
        $f = $i + 1;
        print "<option>[$f] $win[$i]勝 $name[$i]\n";
	}
	print "</select><P>";

print <<"_HTML1_";

</td><td><table border="1" width="260">

<tr><td bgcolor=green><center>勝数</td><td bgcolor=green><center>繁殖牝馬</td></tr>

_HTML1_

open(SM,"$mesrankfile");
	seek(SM,0,0);  @mesrank = <SM>;  close(SM);

for ($i=0; $i<10; $i++){
	($sak[$i], $winm[$i], ) = split(/<>/,$mesrank[$i]);
	($names[$i], $toku[$i]) = split(/<mm>/,$sak[$i]);
        if($winm[$i] > 999){$irom[$i] = "gold";}
        elsif($winm[$i] > 699){$irom[$i] = "#00FFFF";}
        elsif($winm[$i] > 499){$irom[$i] = "#00FF00";}
        else{$irom[$i] = "000000";}
        
	print "<tr><td><center><B><font color=$irom[$i] size=3>$winm[$i]勝</font></B></td><td><center>$names[$i]</td></tr>";
	}

        print "</table></center><P><center><select>";

        if($#mesrank >= 30){$hyouzi = 30;}else{$hyouzi = $#mesrank+1;}
        for ($i=10; $i<$hyouzi; $i++){
	($sak[$i], $winm[$i], ) = split(/<>/,$mesrank[$i]);
        ($names[$i], $toku[$i]) = split(/<mm>/,$sak[$i]);
        $f = $i + 1;
        print "<option>[$f] $winm[$i]勝 $names[$i]\n";
	}
	print "</select><P></td></tr></table>";

print <<"_HTML2_";
<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" name="orank" value="有力な生産家">
<input type="submit" name="kisyu" value="騎手ランキング">
<input type="submit" name="syurank" value="種牡･繁殖ランキング">
</td></tr></table>
</form>
_HTML2_
&chosaku;
}#end suyrank


##### レコード
sub rtime{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>レコード</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<center><br><font color=red size=5><B>レコード</B></font><P>
<table border="0" width="600"><tr>
_HTML1_

open(RR,"$recordsfile");
	seek(RR,0,0);  @rr = <RR>;  close(RR);

        for($i=0; $i<10; $i++){
	($rkaisai[$i], $rname0[$i], $rtime0[$i], $rname1[$i], $rtime1[$i], $rname2[$i], $rtime2[$i], $rname3[$i], $rtime3[$i], $rname4[$i], $rtime4[$i]) = split(/<>/,$rr[$i]);

        ($hunt0[$i], $byout0[$i], $nant0[$i]) = split(/<t>/,$rtime0[$i]);
        $hjuy0[$i] = "$hunt0[$i]′$byout0[$i]″$nant0[$i]";
        ($hunt1[$i], $byout1[$i], $nant1[$i]) = split(/<t>/,$rtime1[$i]);
        $hjuy1[$i] = "$hunt1[$i]′$byout1[$i]″$nant1[$i]";
        ($hunt2[$i], $byout2[$i], $nant2[$i]) = split(/<t>/,$rtime2[$i]);
        $hjuy2[$i] = "$hunt2[$i]′$byout2[$i]″$nant2[$i]";
        ($hunt3[$i], $byout3[$i], $nant3[$i]) = split(/<t>/,$rtime3[$i]);
        $hjuy3[$i] = "$hunt3[$i]′$byout3[$i]″$nant3[$i]";
        ($hunt4[$i], $byout4[$i], $nant4[$i]) = split(/<t>/,$rtime4[$i]);
        $hjuy4[$i] = "$hunt4[$i]′$byout4[$i]″$nant4[$i]";

	print "<td><table border=1 width=300><tr><td bgcolor=green width=70><center><font color=yellow><B>$rkaisai[$i]</B></font></td><td bgcolor=green width=150><center>馬名</td><td bgcolor=green width=80><center>タイム</td></tr><tr><td><center>1600</td><td><center><B>$rname1[$i]</font></B></td><td><center>$hjuy1[$i]</td></tr><tr><td><center>1800</td><td><center><B>$rname2[$i]</font></B></td><td><center>$hjuy2[$i]</td></tr><tr><td><center>2000</td><td><center><B>$rname0[$i]</font></B></td><td><center>$hjuy0[$i]</td></tr><tr><td><center>2200</td><td><center><B>$rname3[$i]</font></B></td><td><center>$hjuy3[$i]</td></tr><tr><td><center>2400</td><td><center><B>$rname4[$i]</font></B></td><td><center>$hjuy4[$i]</td></tr></table><br><br></td>";

            if($i % 2 ne "0"){
             print "</tr><tr>";
            }
        }

&chosaku;
}#end rtime


###### 歴代優勝馬

sub past{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>歴代優勝馬</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<center><br><font color=red size=5><B>歴代優勝馬</B></font><P>

<table border="1" width="700">

<tr>
<td bgcolor=green width=35><center>代</td>
<td bgcolor=green width=60><center>馬</td>
<td bgcolor=green width=165><center>馬/1600m</td>
<td bgcolor=green width=110><center>主戦/1800m</td>
<td bgcolor=green width=110><center>成績/2000m</td>
<td bgcolor=green width=110><center>連勝/2200m</td>
<td bgcolor=green width=110><center>馬主/2400m</td>
</tr>

_HTML1_

        open(PT,"$pastfile");
	seek(PT,0,0);  @pt = <PT>;  close(PT);

        open(FG,"$gaifightfile");                # レースの記録
	seek(FG,0,0);  @fg = <FG>;  close(FG);
        $ig=0;
for ($i=0; $i<$#pt+1; $i++){
	($no[$i], $name[$i], $sakusya[$i], $homepage[$i], $lif[$i], $pow[$i], $def[$i], $spe[$i], $date[$i], $ip[$i], $icon[$i], $win[$i], $syu[$i], $total[$i], $tyoushi[$i], $ashi[$i], $osu[$i], $mesu[$i], $sei[$i], $ketou[$i], $baku[$i], $pass[$i], $gazou[$i], $rennsyou[$i], $maxren[$i], $records[$i], $records16[$i], $records18[$i], $records22[$i], $records24[$i], $st[$i], $titi[$i], $tiha[$i], $tititi[$i], $titiha[$i], $tihati[$i], $tihaha[$i], $hati[$i], $haha[$i], $hatiti[$i], $hatiha[$i], $hahati[$i], $hahaha[$i], $dmy, $formkon[$i], $dmy, $dmy, $dmy, $dmy, $dmy, $dmy) = split(/<>/,$pt[$i]);
        ($dmy, $nameg[$ig], $dmy) = split(/<>/,$fg[$ig]);
        ($osuu, $dmy) = split(/<mm>/,$osu[$i]);
        ($mesuu, $dmy) = split(/<mm>/,$mesu[$i]);
        $gano = 701 + $ig;
        if($i < 5 && ($name[$i] eq $nameg[$ig])){$name[$i]="<a href=\"$cgifile?no=$gano\">$name[$i]</a>";$ig++;}
        $ii = $#pt-$i+1;
        $lose[$i] = $total[$i] - $win[$i];
        $icon_pri[$i] = "<img src=\"$imgurl/$icon[$i]\">";
        if($homepage[$i]){$sakusya[$i] = "<a href=$homepage[$i] target=_blank>$sakusya[$i]</a>";}
        ($hunt, $byout, $nant) = split(/<t>/,$records[$i]);
        if($hunt eq ""){$hjuy20[$i] = "未出走";}
        else{$hjuy20[$i] = "$hunt′$byout″$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records16[$i]);
        if($hunt eq ""){$hjuy16[$i] = "未出走";}
        else{$hjuy16[$i] = "$hunt′$byout″$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records18[$i]);
        if($hunt eq ""){$hjuy18[$i] = "未出走";}
        else{$hjuy18[$i] = "$hunt′$byout″$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records22[$i]);
        if($hunt eq ""){$hjuy22[$i] = "未出走";}
        else{$hjuy22[$i] = "$hunt′$byout″$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records24[$i]);
        if($hunt eq ""){$hjuy24[$i] = "未出走";}
        else{$hjuy24[$i] = "$hunt′$byout″$nant";}

        if($no[$i] eq "-2"){$ii = "<font color=gold><b>$ii代</b></font>";}
        else{$ii = "$ii代";}
	print "
<tr>
<td rowspan=2><center>$ii</td>
<td  rowspan=2><center>$icon_pri[$i]</td>
<td><font size=1>$osuu</font><br><center><b>$name[$i]($sei[$i])</b><br><font size=1></center>$mesuu</font></td>
<td><center>$syu[$i]</td>
<td><center>$win[$i]勝$lose[$i]敗</td>
<td><center>$maxren[$i]</td>
<td><center>$sakusya[$i]</td></tr><tr>
<td><center>$hjuy16[$i]</td>
<td><center>$hjuy18[$i]</td>
<td><center>$hjuy20[$i]</td>
<td><center>$hjuy22[$i]</td>
<td><center>$hjuy24[$i]</td>
</tr>";
	}
        print "</table></center>";

&chosaku;

}#end past


##### 騎手一覧
sub kisyu{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>騎手一覧</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<!--広告バナー挿入位置、ページ上部-->
<center><font color="$tcolor" size="5"><B>騎手一覧</B></font><P>
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>

<table border="1" width="800">

<tr>
<td bgcolor=green width=50><center>順位</td>
<td bgcolor=green width=70><center>名前</td>
<td bgcolor=green><center>特徴</td>
<td bgcolor=green width=70><center>勝ち</td>
<td bgcolor=green width=70><center>負け</td>
<td bgcolor=green width=60><center>勝率</td>
<td bgcolor=green width=115><center>特性</td>
</tr>

_HTML1_

        open(KI,"$kisyufile");
	seek(KI,0,0);  @itiran = <KI>;  close(KI);
        @sort = sort { (split(/<>/,$a))[3] <=> (split(/<>/,$b))[3] } @itiran;
        @sortdata = sort { (split(/<>/,$b))[2] <=> (split(/<>/,$a))[2] } @sort;
        $gg=0;
        foreach $line (@sortdata) {
   ($name, $comm, $win, $lose, $omona, $omona2, $omona3, $dmy, $dmy, $dmy) = split(/<>/,$line);
        $gg++;
        if( ($win+$lose) eq "0"){$ritu = "未騎乗";}else{
        $ritu = sprintf("%03d", ( $win/ ($win+$lose) ) * 1000);}
        $total=$win+$lose;
        if($omona3 ne ""){
	print "<tr><td><center>$gg位</td><td><center><b>$name</b></td><td>$comm</td><td><center>$win</td><td><center>$lose</td><td><center>.$ritu</td><td><center>$omona<br>$omona2<br>$omona3</td></tr>\n";
        }else{
        print "<tr><td><center>$gg位</td><td><center><b>$name</b></td><td>$comm</td><td><center>$win</td><td><center>$lose</td><td><center>.$ritu</td><td><center>$omona<br>$omona2</td></tr>\n";}
        }

print <<"_HTML2_";
</table><div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" name="orank" value="有力な生産家">
<input type="submit" name="kisyu" value="騎手ランキング">
<input type="submit" name="syurank" value="種牡･繁殖ランキング">
</td></tr></table>
</form>
_HTML2_
&chosaku;

}#end kisyu
