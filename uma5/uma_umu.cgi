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

##### 馬登録処理

sub record{
        $uiui = $form{'uiui'};

        open(DB,"$logfile");    #chara.dat
        seek(DB,0,0);  @lines = <DB>;  close(DB);

        if($lines[$max_chara]){&error("これ以上登録できないよ。");}

# 変数を置き換える

	$formname = $form{'name'};
	$formhp = $form{'hp'};
        $formsyu = $form{'syu'};
        $formashi = $form{'ashi'};
        $formpass = $form{'pass'};
        $formgazou = $form{'gazou'};

       open(TK,"$tanefile");     #オス
       seek(TK,0,0);  @tk = <TK>;  close(TK);

       foreach $check (@tk){
		@checks = split(/<>/,$check);
                ($checkosu, $tokusyu) = split(/<mm>/,$checks[0]);
		if($form{'osu'} eq "$checkosu"){@checko = @checks;last;}
	}

       open(TM,"$tamefile");     #メス
       seek(TM,0,0);  @tm = <TM>;  close(TM);

       foreach $checkk (@tm){
		@checksm = split(/<>/,$checkk);
                ($checkmesu, $tokusyu) = split(/<mm>/,$checksm[0]);
		if($form{'mesu'} eq "$checkmesu"){@checkm = @checksm;last;}
       }

        if($checko[0] eq $checko[10] || $checko[0] eq $checko[12] || $checko[0] eq $checko[14] || $checko[0] eq $checkm[10] || $checko[0] eq $checkm[12] || $checko[0] eq $checkm[14]){&error("１×○の配合は出来ません。");}

        ($check11, $ketou11, $tokusyu11) = split(/<mm>/,$checkm[11]);
        ($check15, $ketou15, $tokusyu15) = split(/<mm>/,$checkm[15]);
        $checkm11 = "$check11<mm>$tokusyu11";
        $checkm15 = "$check15<mm>$tokusyu15";

        if($checkm[0] eq $checko[11] || $checkm[0] eq $checko[13] || $checkm[0] eq $checko[15] || $checkm[0] eq $checkm[13] || $checkm[0] eq $checkm11 || $checkm[0] eq $checkm15){&error("１×○の配合は出来ません。");}

        ($checkname, $checkketou2, $tokusyu2) = split(/<mm>/,$checkm[11]); # 母母の血統
        ($checkname2, $checkketou3, $tokusyu3) = split(/<mm>/,$checkm[15]); # 母母母の血統

        @riron = "";
# ニックス（スピード）
        $flag = 0;$flah = 0;$flai = 0;

        for ($k=0; $k<$#spo+1; $k++){ 
        if($spo[$k] eq $checko[1] && $spm[$k] eq $checkm[1]){$flag=1;last;}
        }
        for ($k=0; $k<$#spo+1; $k++){ 
        if($spo[$k] eq $checko[1] && $spm[$k] eq $checkketou2){$flah=1;last;}
        }
        for ($k=0; $k<$#spo+1; $k++){ 
        if($spo[$k] eq $checko[1] && $spm[$k] eq $checkketou3){$flai=1;last;}
        }
        if($flag == 1 && $flah == 1 && $flai == 1){$checko[3] += 3;push(@riron, "トリプルニックス（スピード）<p>");}
     elsif($flag == 1 && $flah == 1){$checko[3] += 2;push(@riron, "ダブルニックス（スピード）<p>");}
     elsif($flag == 1){$checko[3]++;push(@riron, "ニックス（スピード）<p>");}


# ニックス（瞬発力）
        $flag = 0;$flah = 0;$flai = 0;

        for ($k=0; $k<$#syo+1; $k++){ 
        if($syo[$k] eq $checko[1] && $sym[$k] eq $checkm[1]){$flag = 1;last;}
        }
        for ($k=0; $k<$#syo+1; $k++){ 
        if($syo[$k] eq $checko[1] && $sym[$k] eq $checkketou2){$flah=1;last;}
        }
        for ($k=0; $k<$#syo+1; $k++){ 
        if($syo[$k] eq $checko[1] && $sym[$k] eq $checkketou3){$flai=1;last;}
        }
        if($flag == 1 && $flah == 1 && $flai == 1){$checko[4] += 3;push(@riron, "トリプルニックス（瞬発力）<p>");}
     elsif($flag == 1 && $flah == 1){$checko[4] += 2;push(@riron, "ダブルニックス（瞬発力）<p>");}
     elsif($flag == 1){$checko[4]++;push(@riron, "ニックス（瞬発力）<p>");}


# 芦毛伝説配合
    if( ($checko[6] eq "uma8.gif" || $checko[6] eq "uma9.gif") && ($checkm[6] eq "uma8.gif" || $checkm[6] eq "uma9.gif") ){
    $checko[3]++;
    $checko[4]++;
    push(@riron, "芦毛伝説配合<p>");
    }

# 栗配合
    if( ($checko[6] eq "uma3.gif" || $checko[6] eq "uma4.gif" || $checko[6] eq "uma5.gif") && ($checkm[6] eq "uma3.gif" || $checkm[6] eq "uma4.gif" || $checkm[6] eq "uma5.gif") ){
    $checko[3]++;
    $checko[5]++;
    push(@riron, "栗配合<p>");
    }

# 今年で引退の種牡馬×繁殖牝馬
    if($checko[8] == $osuintai && $checkm[8] == $mesuintai){
    $checko[3] += 2;
    push(@riron, "サヨナラ配合<p>");
    }

# 爆発力D×D
    if($checko[7] eq "D" && $checkm[7] eq "D"){
    $checko[3] += 3;
    $checko[4] += 2;
    push(@riron, "原爆配合<p>");
    }

# 同系配合は弱化
    if($checko[1] eq $checkm[1]){
    $checko[3] -= 2;
    push(@riron, "同系配合<p>");
    }

#各能力値の決定
   @syusei = "";
        if($checko[7] eq "A"){
   @syusei = (0.97 , 1.00 , 1.03 , 1.02 , 1.03 , 1.06 , 0.98 , 1.00 , 1.03 , 0.98 , 1.01);
        }elsif($checko[7] eq "B"){
   @syusei = (0.98 , 1.02 , 0.95 , 0.99 , 1.04 , 1.04 , 0.97 , 0.98 , 1.00 , 0.98 , 1.01);
        }elsif($checko[7] eq "C"){
   @syusei = (0.94 , 0.98 , 0.99 , 1.02 , 0.96 , 0.95 , 0.96 , 0.96 , 1.12 , 0.95 , 1.00);
        }else{
   @syusei = (0.95 , 1.00 , 0.94 , 1.03 , 1.04 , 0.93 , 1.00 , 0.94 , 0.95 , 1.02 , 0.92);
        }
   @hinsei = (0.98 , 1.02 , 0.95 , 0.99 , 1.04 , 1.04 , 0.97 , 0.98 , 1.00 , 0.98 , 1.01);
	$y = int(rand(10));$z = int(rand(10));
	$w = int(rand(10));$t = int(rand(10));
	$r = int(rand(10));$e = int(rand(10));
        $l = int(rand(10));$q = int(rand(10));

$formpow = int(((($checko[3]*$syusei[$y]) + rand(2) + ($checkm[3]*$hinsei[$z]))/2)*10)/10;
$formdef = int(((($checko[4]*$syusei[$w]) + rand(2) + ($checkm[4]*$hinsei[$t]))/2)*10)/10;
$formspe = int(((($checko[5]*$syusei[$r]) + rand(2) + ($checkm[5]*$hinsei[$e]))/2)*10)/10;
$formst =  int(((($checko[9]*1.5) + ($checkm[9]*0.5))/2 + rand(2) - rand(2))*10)/10;
$formkon = int((($checko[2]*$syusei[$l])+ rand(2)-rand(2)+($checkm[2]*$hinsei[$q]))/2);
        if($formpow <= 34 && $formdef <= 33){$formpow = 34;}
        if($formpow <= 33){$formpow = 33;}
        if($formkon <= 8){$formkon = 8;}
        if($formkon >= 25){$formkon = 25;}
if($formpow >= 38){
        open(ST,"$time2file");
	seek(ST,0,0);  @st = <ST>;  close(ST);

        ($hiniti, $hi, $zikan, $rigu, $sedai) = split(/<>/, @st[0]);
      if(($formpow >= 39) || ($formdef >= 36)){
        $sedai = $sedai + 100;
      }else{$sedai++;}
        $zikann = "$hiniti<>$hi<>$zikan<>$rigu<>$sedai<>";
        open(ST,">$time2file") ;
		eval 'flock(ST,2);';
		seek(ST,0,0);	print ST $zikann;
		eval 'flock(ST,8);';
	close(ST);
}
#毛色の決定
#鹿毛　黒鹿毛　栃栗毛　栗毛　尾花栗毛　青鹿毛　青毛　芦毛(濃)　芦毛(薄)　白毛
# 1       2       3     4       5         6      7     8         9        10
           $q = rand(100);
        if($checko[6] eq "uma10.gif" && $checkm[6] eq "uma10.gif"){         #両方が白毛
		if($q > 70){$b = "uma10.gif";}
        	elsif($q > 50){$b = "uma9.gif";}
        	elsif($q > 40){$b = "uma8.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma10.gif" || $checkm[6] eq "uma10.gif"){      #片方が白毛
        	if($q > 80){$b = "uma10.gif";}
        	elsif($q > 70){$b = "uma9.gif";}
        	elsif($q > 50){$b = "uma8.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma9.gif" && $checkm[6] eq "uma9.gif"){        #両方が芦毛(薄)
        	if($q > 93){$b = "uma10.gif";}
        	elsif($q > 50){$b = "uma9.gif";}
        	elsif($q > 40){$b = "uma8.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma9.gif" || $checkm[6] eq "uma9.gif"){        #片方が芦毛(薄)
        	if($q > 95){$b = "uma10.gif";}
        	elsif($q > 60){$b = "uma9.gif";}
        	elsif($q > 50){$b = "uma8.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma8.gif" && $checkm[6] eq "uma8.gif"){        #両方が芦毛(濃)
        	if($q > 95){$b = "uma10.gif";}
        	elsif($q > 65){$b = "uma9.gif";}
        	elsif($q > 55){$b = "uma8.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma8.gif" || $checkm[6] eq "uma8.gif"){        #片方が芦毛(濃)
        	if($q > 98){$b = "uma10.gif";}
        	elsif($q > 70){$b = "uma9.gif";}
        	elsif($q > 60){$b = "uma8.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma7.gif" && $checkm[6] eq "uma7.gif"){        #両方が青毛
        	if($q > 95){$b = "uma9.gif";}
        	elsif($q > 90){$b = "uma8.gif";}
        	elsif($q > 70){$b = "uma7.gif";}
                elsif($q > 50){$b = "uma6.gif";}
                elsif($q > 40){$b = "uma2.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma7.gif" || $checkm[6] eq "uma7.gif"){        #片方が青毛
        	if($q > 97){$b = "uma9.gif";}
        	elsif($q > 94){$b = "uma8.gif";}
        	elsif($q > 75){$b = "uma7.gif";}
                elsif($q > 56){$b = "uma6.gif";}
                elsif($q > 47){$b = "uma2.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma6.gif" && $checkm[6] eq "uma6.gif"){        #両方が青鹿毛
        	if($q > 97){$b = "uma8.gif";}
        	elsif($q > 80){$b = "uma7.gif";}
        	elsif($q > 70){$b = "uma6.gif";}
                elsif($q > 60){$b = "uma2.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma6.gif" || $checkm[6] eq "uma6.gif"){        #片方が青鹿毛
        	if($q > 98){$b = "uma8.gif";}
        	elsif($q > 85){$b = "uma7.gif";}
        	elsif($q > 75){$b = "uma6.gif";}
                elsif($q > 65){$b = "uma2.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma5.gif" && $checkm[6] eq "uma5.gif"){        #両方が尾花栗毛
        	if($q > 90){$b = "uma5.gif";}
        	elsif($q > 60){$b = "uma4.gif";}
        	elsif($q > 50){$b = "uma3.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma5.gif" || $checkm[6] eq "uma5.gif"){        #片方が尾花栗毛
        	if($q > 95){$b = "uma5.gif";}
        	elsif($q > 70){$b = "uma4.gif";}
        	elsif($q > 60){$b = "uma3.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma4.gif" && $checkm[6] eq "uma4.gif"){        #両方が栗毛
        	if($q > 95){$b = "uma5.gif";}
        	elsif($q > 65){$b = "uma4.gif";}
        	elsif($q > 55){$b = "uma3.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma4.gif" || $checkm[6] eq "uma4.gif"){        #片方が栗毛
        	if($q > 97){$b = "uma5.gif";}
        	elsif($q > 70){$b = "uma4.gif";}
        	elsif($q > 60){$b = "uma3.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma3.gif" && $checkm[6] eq "uma3.gif"){        #両方が栃栗毛
        	if($q > 95){$b = "uma5.gif";}
        	elsif($q > 65){$b = "uma4.gif";}
        	elsif($q > 55){$b = "uma3.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma3.gif" || $checkm[6] eq "uma3.gif"){        #片方が栃栗毛
        	if($q > 97){$b = "uma5.gif";}
        	elsif($q > 70){$b = "uma4.gif";}
        	elsif($q > 60){$b = "uma3.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma2.gif" && $checkm[6] eq "uma2.gif"){        #両方が黒鹿毛
        	if($q > 97){$b = "uma8.gif";}
        	elsif($q > 90){$b = "uma7.gif";}
        	elsif($q > 80){$b = "uma6.gif";}
                elsif($q > 50){$b = "uma2.gif";}
        	else{$b = "uma1.gif";}
        }
        elsif($checko[6] eq "uma2.gif" || $checkm[6] eq "uma2.gif"){        #片方が黒鹿毛
        	if($q > 98){$b = "uma8.gif";}
        	elsif($q > 95){$b = "uma7.gif";}
        	elsif($q > 85){$b = "uma6.gif";}
                elsif($q > 60){$b = "uma2.gif";}
        	else{$b = "uma1.gif";}
        }
        else{                                                  #両方が鹿毛
        	if($q > 99){$b = "uma8.gif";}
        	elsif($q > 98){$b = "uma7.gif";}
        	elsif($q > 90){$b = "uma6.gif";}
                elsif($q > 85){$b = "uma4.gif";}
        	elsif($q > 82){$b = "uma3.gif";}
                elsif($q > 77){$b = "uma2.gif";}
        	else{$b = "uma1.gif";}
        }

        $formicon = $b;

#性別の決定
        $seii = rand(10);
        if($seii > 5){$formsei = "牡";}
        else{$formsei = "牝";}

#爆発力の決定
        $bak = rand(7);
        if($bak > 6){$formbaku = "A";}
        elsif($bak > 3){$formbaku = "B";}
        elsif($bak > 2){$formbaku = "C";}
        else{$formbaku = "D";}

# リモートホスト取得

	$host = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};

        if($form{'uiui'} ne "5"){

        for ($i=0; $i<$#lines+1; $i++){
 	@checkip = split(/<>/,$lines[$i]);
        if($host eq $checkip[9]){&error("重複登録不可！");}
        }
        }

# 登録ナンバー

	open(DB,"$logfile");    #chara.dat
	seek(DB,0,0);  @lines = <DB>;  close(DB);

        $koreda = 1;
        foreach $line (@lines){
        @namb = split(/<>/,$line);
        if($namb[0] > $koreda){$koreda = $namb[0];}
        }

        $koreda += 1;    #登録ナンバー

# 登録時刻
	$year += 1900;
	$month = sprintf("%02d",$mon +1);
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
	$sec = sprintf("%02d",$sec);
	$jikan = "$month/$mday $hour:$min:$sec";

#種牡馬の名前
        ($formosu, $tokusyu) = split(/<mm>/,$checko[0]);
        ($titi, $tokusyu) = split(/<mm>/,$checko[10]);
        ($tiha, $tokusyu) = split(/<mm>/,$checko[11]);
        ($tititi, $tokusyu) = split(/<mm>/,$checko[12]);
        ($titiha, $tokusyu) = split(/<mm>/,$checko[13]);
        ($tihati, $tokusyu) = split(/<mm>/,$checko[14]);
        ($tihaha, $tokusyu) = split(/<mm>/,$checko[15]);

#血統の決定
        $formketou = "$checko[1]";
        $checkketou1="$checkm[1]";

#繁殖牝馬の名前
        ($formmesu, $tokusyu) = split(/<mm>/,$checkm[0]);
        ($hati, $tokusyu) = split(/<mm>/,$checkm[10]);
        ($haha, $checkketou2, $tokusyu22) = split(/<mm>/,$checkm[11]);
        $checkm[11] = "$haha<mm>$tokusyu22";
        ($hatiti, $tokusyu) = split(/<mm>/,$checkm[12]);
        ($hatiha, $tokusyu) = split(/<mm>/,$checkm[13]);
        ($hahati, $tokusyu) = split(/<mm>/,$checkm[14]);
        ($hahaha, $checkketou3, $tokusyu33) = split(/<mm>/,$checkm[15]);
        $checkm[15] = "$hahaha<mm>$tokusyu33";

	$kakiko = "$koreda<>名無し<>$formname<>$formhp<>200<>$formpow<>$formdef<>$formspe<>$jikan<>$host<>$formicon<>0<>$formsyu<>0<>5<>$formashi<>$checko[0]<>$checkm[0]<>$formsei<>$formketou<>$formbaku<>$formpass<>$formgazou<>0<>0<><><><><><>$formst<>$checko[10]<>$checko[11]<>$checko[12]<>$checko[13]<>$checko[14]<>$checko[15]<>$checkm[10]<>$checkm[11]<>$checkm[12]<>$checkm[13]<>$checkm[14]<>$checkm[15]<>$checkketou1<>$checkketou2<>$checkketou3<>$dmy<>$formkon<>$dmy<>$dmy<>$dmy<>\n";

# インブリード

        $check = "$kakiko";
        @check = split(/<>/,$check);
        $inbu = 0;
   for ($k=31; $k<43; $k++){
      for ($kk=31; $kk<43; $kk++){
         if($check[$k] eq $check[$kk] && $k ne $kk){$inbu++;last;}
      }
   }

if($inbu > 0){# インブリード

     if($check[31] eq $check[37]){&error("インブリード(２×２)の配合は出来ません。");}
     if($check[32] eq $check[38]){&error("インブリード(２×２)の配合は出来ません。");}

     if($check[31] eq $check[33] || $check[31] eq $check[35] || $check[31] eq $check[39] || $check[31] eq $check[41]){&error("インブリード(２×３)の配合は出来ません。");}

      if($check[37] eq $check[33] || $check[37] eq $check[35] || $check[37] eq $check[39] || $check[37] eq $check[41]){&error("インブリード(２×３)の配合は出来ません。");}

      if($check[32] eq $check[34] || $check[32] eq $check[36] || $check[32] eq $check[40] || $check[32] eq $check[42]){&error("インブリード(２×３)の配合は出来ません。");}

       if($check[38] eq $check[34] || $check[38] eq $check[36] || $check[38] eq $check[40] || $check[38] eq $check[42]){&error("インブリード(２×３)の配合は出来ません。");}

    if($check[33] eq $check[35] || $check[33] eq $check[39] || $check[33] eq $check[41]){
        ($nametiti, $tokusyu) = split(/<mm>/,$check[33]);
      if($tokusyu ne ""){&inshi;}
        $inbaku = int(rand(100));
        if($inbaku <= 30){
        $formpow++;$formdef++;}
        else{$formpow--;$formdef--;}
        $formspe -= 2;
        push(@riron, "インブリード(３×３)<p>");
    }

      if($check[35] eq $check[39] || $check[35] eq $check[41]){
        ($nametiti, $tokusyu) = split(/<mm>/,$check[35]);
      if($tokusyu ne ""){&inshi;}
        $inbaku = int(rand(100));
        if($inbaku <= 30){
        $formpow++;$formdef++;}
        else{$formpow--;$formdef--;}
        $formspe -= 2;
        push(@riron, "インブリード(３×３)<p>");
      }


      if($check[39] eq $check[41]){
        ($nametiti, $tokusyu) = split(/<mm>/,$check[39]);
      if($tokusyu ne ""){&inshi;}
        $inbaku = int(rand(100));
        if($inbaku <= 30){
        $formpow++;$formdef++;}
        else{$formpow--;$formdef--;}
        $formspe -= 2;
        push(@riron, "インブリード(３×３)<p>");
      }

    if($check[34] eq $check[36] || $check[34] eq $check[40] || $check[34] eq $check[42]){
        ($nametiti, $tokusyu) = split(/<mm>/,$check[34]);
      if($tokusyu ne ""){&inshi;}
        $inbaku = int(rand(100));
        if($inbaku <= 30){
        $formpow++;$formdef++;}
        else{$formpow--;$formdef--;}
        $formspe -= 2;
        push(@riron, "インブリード(３×３)<p>");
      }

      if($check[36] eq $check[40] || $check[36] eq $check[42]){
        ($nametiti, $tokusyu) = split(/<mm>/,$check[36]);
      if($tokusyu ne ""){&inshi;}
        $inbaku = int(rand(100));
        if($inbaku <= 30){
        $formpow++;$formdef++;}
        else{$formpow--;$formdef--;}
        $formspe -= 2;
        push(@riron, "インブリード(３×３)<p>");
      }

      if($check[40] eq $check[42]){
        ($nametiti, $tokusyu) = split(/<mm>/,$check[40]);
      if($tokusyu ne ""){&inshi;}
        $inbaku = int(rand(100));
        if($inbaku <= 30){
        $formpow++;$formdef++;}
        else{$formpow--;$formdef--;}
        $formspe -= 2;
        push(@riron, "インブリード(３×３)<p>");
      }

}else{# アウトブリード
      $formspe += 2;
      push(@riron, "アウトブリード<p>");
}

# 名前・パスワードの長さチェック
	
        if((length($formname) < 1)||(length($formname) > $nameleng2 *2)){&error("名前の長さは$nameleng2文字以下にしてね。");}
        if((length($formpass) < 1)||(length($formpass) > 8)){&error("パスワードの長さは8文字までにしてね。");}

	($formhp =~ /^http:\/\/[a-zA-Z0-9]+/) || ($formhp = '');	#ＨＰの判定

        open(DB,"$logfile");    # （馬名・馬主）の重複チェック
        seek(DB,0,0);@lines = <DB>; close(DB);

        foreach $lines (@lines){
        ($lno, $lname, $lsakusya, $lhomepage, $llif, $lpow, $ldef, $lspe, $ldate, $lip, $licon, $lwin, $lsyu, $ltotal, $ltyoushi, $lashi, $losu, $lmesu, $lsei, $lketou, $lbaku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy) = split(/<>/,$lines);

        if($lsakusya eq $formname && $form{'uiui'} eq "5"){

                foreach $check (@lines){             # 旧馬を消す
		@check = split(/<>/,$check);
                if($lname eq "名無し" && $lsakusya eq $check[2]){&error("既に登録されています。");}
		elsif($lsakusya eq $check[2]){$check = '';last;}
		}

        open(DB,">$logfile") ;      # 旧馬を消す
		eval 'flock(DB,2);';
		seek(DB,0,0);	print DB @lines;
	eval 'flock(DB,8);';

        }
        elsif($lsakusya eq $formname){&error("その馬主名はすでに使われています。");}
        }

# ロック開始

        $times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

	open(GL,"+<$lockfile");
	eval 'flock(GL,2);';

	@gamelock = <GL>;

	($gamecheck, $gametime) = split(/<>/, $gamelock[0]);
	if($gamecheck eq 0 || $times > $gametime + 60 * 2){
		$gamelock = "1<>$times<>\n";
	}else{
		&error("現在レース中です。もうちょっと待っててね。");
	}

	truncate (GL, 0);
	seek(GL,0,0);	print GL $gamelock;
	close(GL);
	eval 'flock(GL,8);';

# クッキーを発行
        &set_cookie;

      if($formpow >= 40){$tokusyu = "sp2";}
   elsif($formdef >= 40){$tokusyu = "syu2";}
   elsif($formspe >= 40){$tokusyu = "ki2";}
   elsif($formst >= 40){$tokusyu = "st2";}
   elsif($formkon >= 22){$tokusyu = "kon2";}
   elsif($formpow >= 38.5){$tokusyu = "sp1";}
   elsif($formdef >= 38.5){$tokusyu = "syu1";}
   elsif($formspe >= 38.5){$tokusyu = "ki1";}
   elsif($formst >= 38.5){$tokusyu = "st1";}
   elsif($formkon >= 20){$tokusyu = "kon1";}

# ログへ書き込むスタイルの整形
	$kakiko = "$koreda<>名無し<>$formname<>$formhp<>200<>$formpow<>$formdef<>$formspe<>$jikan<>$host<>$formicon<>0<>$formsyu<>0<>5<>$formashi<>$checko[0]<>$checkm[0]<>$formsei<>$formketou<>$formbaku<>$formpass<>$formgazou<>0<>0<><><><><><>$formst<>$checko[10]<>$checko[11]<>$checko[12]<>$checko[13]<>$checko[14]<>$checko[15]<>$checkm[10]<>$checkm[11]<>$checkm[12]<>$checkm[13]<>$checkm[14]<>$checkm[15]<>$checkketou1<>$checkketou2<>$checkketou3<>$tokusyu<>$formkon<>$dmy<>$dmy<>$dmy<>\n";

# ログへの書き込み
        open(DB,">>$logfile") ;
		eval 'flock(DB,2);';
		print DB $kakiko;
		eval 'flock(DB,8);';
	close(DB);
        push(@lines,$kakiko);

        open(OR,"+<$orfile") || &error('指定されたファイルが開けません。'); # オーナー
	eval 'flock(OR,2);';
                $flag=0;
                @oranks = <OR>;
                $oranka = "$formname<>0<>\n";
         foreach $check (@oranks){
		@check = split(/<>/,$check);
		if($formname eq $check[0]){$flag=1;last;}
		}
                if($flag ne "1"){push(@oranks,$oranka);}


# オーナーログへの書き込み
	truncate (OR, 0); 
	seek(OR,0,0);	print OR @oranks;
	close(OR);
	eval 'flock(OR,8);';

# 記録したしるし

$recflag = '1';

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

}#end record


##### 馬生産
sub seisan{

       open(TK,"$tanefile");
       seek(TK,0,0);  @tk = <TK>;  close(TK);

       for ($i=0; $i<$#tk+1; $i++){
       ($tane[$i], $kettou[$i], $kati[$i], $supi[$i], $syun[$i], $kisei[$i], $keiro[$i]) = split(/<>/,$tk[$i]);
       ($tane[$i], $tokusyu) = split(/<mm>/,$tane[$i]);
       }

       $i = 0;
       @list = ();
       foreach $lists (@tk) {
           push @list, "<option value=\"$tane[$i]\">$tane[$i]（$kettou[$i]系）</option>";
        $i++;
       }

       open(MK,"$tamefile");
       seek(MK,0,0);  @mk = <MK>;  close(MK);

       for ($i=0; $i<$#mk+1; $i++){
       ($tame[$i], $mkettou[$i], $mkati[$i], $msupi[$i], $msyun[$i], $mkisei[$i], $mkeiro[$i]) = split(/<>/,$mk[$i]);
       ($tame[$i], $tokusyu) = split(/<mm>/,$tame[$i]);
       }

       $m = 0;
       @listm = ();
       foreach $listsm (@mk) {
           push @listm, "<option value=\"$tame[$m]\">$tame[$m]（$mkettou[$m]系）</option>";
        $m++;
       }

       open(KK,"$kisyufile");
       seek(KK,0,0);  @kk = <KK>;  close(KK);

       for ($i=0; $i<$#kk+1; $i++){
       ($name[$i], $comm[$i], $win[$i], $lose[$i], $omona[$i], $omona2[$i], $dmy) = split(/<>/,$kk[$i]);
       }

       $k = 0;
       @listk = ();
       foreach $listsk (@kk) {
           push @listk, "<option value=\"$name[$k]\">$name[$k]</option>";
        $k++;
       }
}

##### 馬登録出力
sub rec{

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

<center><font color="$tcolor" size="5"><B>競走馬の登録</B></font>

_HTML1_

if($recflag){

print "<P>登録完了しました。</P>@riron";

} else {

        open(LL,"$logfile");
	seek(LL,0,0);  @kazu = <LL>;  close(LL);
        $zoro = 0;
        foreach $line (@kazu) {
       ($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $osu, $mesu, $sei, $ketou, $baku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,$line);
         if($total eq "0"){$zoro++;}
        }
              if($#kazu+2 > $max_chara && $form{'tourou'} ne "5"){
         print "<br><br><br>最大登録数に達しているので登録出来ません。<BR><BR>シーズン更新時に未出走の馬主データは消えます。（$zoro人）";
              }else{

#### アイコンリストの取得

	$i = 0;
	@iconlist = ();
	foreach(@icon2) {
		push @iconlist, "<option value=\"$icon1[$i].gif\">$_\n";
		$i++;
	}

        if($iconuse){$uses="<select name=gazou>@iconlist</select><br><center><a href=\"$cgifile?mode=icon\" target=\~_blank\">アイコン一覧</a><br>";}else{$uses = "アイコン未使用";}

if($form{'tourou'} ne "5"){

print <<"_HTML3_";

<P>
<table border="1" width="660" cellpadding="5"><tr><td>
<form action="$cgifile" method="$method">
<table width="100%" border="1"><tr><td bgcolor=green>
<center>アイコン</td><td bgcolor=green><center>種牡馬・繁殖牝馬</td><td bgcolor=green><center>脚質</td></tr><tr><td>
<center>$uses</td><td>
<center>

<select name="osu">
@list
</select>：<a href=\"$cgifile?mode=chara\" target=\~_blank\">種牡馬一覧</font></a>
<a href=\"$cgifile?mode=ketou\" target=\~_blank\">血統詳細</font></a>
<br>

<select name="mesu">
@listm
</select>：<a href=\"$cgifile?mode=hinba\" target=\~_blank\">繁殖牝馬一覧</font></a>
<a href=\"$cgifile?mode=mketou\" target=\~_blank\">血統詳細</font></a>
<br>

</td><td><center>
<select name="ashi">
<option value="大逃">大逃
<option value="逃げ">逃げ
<option value="先行">先行
<option value="差し">差し
<option value="追込">追込
</select>
</td><td><tr><td colspan="5">

<select name="syu">
@listk
</select>：主戦騎手 <a href=\"$cgifile?mode=kisyu\" target=\~_blank\">騎手一覧</font></a><br>

<input type="text" name="name" value="$c_name" size="16">：あなたの名前（全角$nameleng2文字まで）<br>
<input type="text" name="hp" value="$c_hp" size="50">：ホームページ(空白\可\)<BR>
<input type="password" name="pass" value="$c_pass" size="10">：パスワード<BR>
</td></tr><tr><td colspan="7">
<br>
<center><input type="submit" value="登録">
</font>
</table>
<input type="hidden" name="record" value="1">
</form>
</td></tr></table>

</P>

_HTML3_

}else{           # 今シーズ用
        $logint = $form{'logint'};

print <<"_HTML3_";

<P>
<table border="1" width="660" cellpadding="5"><tr><td>
<form action="$cgifile" method="$method">
<table width="100%" border="1"><tr><td bgcolor=green>
<center>アイコン</td><td bgcolor=green><center>種牡馬・繁殖牝馬</td><td bgcolor=green><center>脚質</td></tr><tr><td>
<center>$uses</td><td>
<center>

<select name="osu">
@list
</select>：<a href=\"$cgifile?mode=chara\" target=\~_blank\">種牡馬一覧</font></a>
<a href=\"$cgifile?mode=ketou\" target=\~_blank\">血統詳細</font></a>
<br>

<select name="mesu">
@listm
</select>：<a href=\"$cgifile?mode=hinba\" target=\~_blank\">繁殖牝馬一覧</font></a>
<a href=\"$cgifile?mode=mketou\" target=\~_blank\">血統詳細</font></a>
<br>

</td><td><center>
<select name="ashi">
<option value="大逃">大逃
<option value="逃げ">逃げ
<option value="先行">先行
<option value="差し">差し
<option value="追込">追込
</select>
</td><td><tr><td colspan="5">

<select name="syu">
@listk
</select>：主戦騎手 <a href=\"$cgifile?mode=kisyu\" target=\~_blank\">騎手一覧</font></a><br>

<input type="text" name="name" value="$logint" size="16">：あなたの名前（全角$nameleng2文字まで・変更不可）<br>
<input type="text" name="hp" value="$c_hp" size="50">：ホームページ(空白\可\)<BR>
<input type="password" name="pass" value="$c_pass" size="10">：パスワード<BR>
</td></tr><tr><td colspan="7">
<br>
<center><input type="submit" value="登録">
</font>
</table>
<input type="hidden" name="uiui" value="5">
<input type="hidden" name="record" value="1">
</form>
</td></tr></table>

</P>

_HTML3_

}}
               }#100頭かどうかのif

&chosaku;
}#end rec

sub umaname{ # 産まれた後に名前を決める

# ロック開始

        $times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

	open(GL,"+<$lockfile");
	eval 'flock(GL,2);';

	@gamelock = <GL>;

	($gamecheck, $gametime) = split(/<>/, $gamelock[0]);
	if($gamecheck eq 0 || $times > $gametime + 60 * 2){
		$gamelock = "1<>$times<>\n";
	}else{
		&error("現在レース中です。もうちょっと待っててね。");
	}

	truncate (GL, 0);
	seek(GL,0,0);	print GL $gamelock;
	close(GL);
	eval 'flock(GL,8);';

# 変数を置き換える

	$formumaname = $form{'umaname'};     # 馬の名前
	$formsaku = $form{'comsaku'};       # 作者の名前

        open(TK,"$tanefile");
        seek(TK,0,0);  @tk = <TK>;  close(TK);

        foreach $check (@tk){
	   @checks = split(/<>/,$check);
           ($ncheck, $dmy) = split(/<mm>/, $checks[0]);
	   if($formumaname eq $ncheck){&error("その馬名の種牡馬がいます。");}
        }

        open(TM,"$tamefile");
        seek(TM,0,0);  @tm = <TM>;  close(TM);

        foreach $check (@tm){
	   @checks = split(/<>/,$check);
           ($mcheck, $dmy) = split(/<mm>/, $checks[0]);
	   if($formumaname eq $mcheck){&error("その馬名の繁殖牝馬がいます。");}
        }

        if($formumaname eq "名無し"){&error("名前をきちんと決めてね。");}
# 名前の長さチェック
	
        if((length($formumaname) < 1)||(length($formumaname) > $nameleng *2)){&error("名前の長さは$nameleng文字以下にしてね。");}

        open(DB,"$logfile");    # 馬名の重複チェック
        seek(DB,0,0);@lines = <DB>; close(DB);

        foreach $lines (@lines){
        ($lno, $lname, $lsakusya, $lhomepage, $llif, $lpow, $ldef, $lspe, $ldate, $lip, $licon, $lwin, $lsyu, $ltotal, $ltyoushi, $lashi, $losu, $lmesu, $lsei, $lketou, $lbaku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,$lines);
        if($lname eq $formumaname){&error("その馬名はすでに使われています。");}
      if(($lname eq "名無し") && ($formsaku eq $lsakusya)){$nowuma = "$lines";$lines = '';
        open(DB,">$logfile") ;
		eval 'flock(DB,2);';
		seek(DB,0,0);	print DB @lines;
	        eval 'flock(DB,8);';
        close(DB);last;
        }
        }

        ($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $osu, $mesu, $sei, $ketou, $baku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,$nowuma);

        $shiki = 0;
        if($icon eq "uma10.gif"){$shiki = 4;&shinkiro;}
        elsif($icon eq "uma5.gif"){$shiki = 5;&shinkiro;}

# ログへ書き込むスタイルの整形
	$kakiko = "$no<>$formumaname<>$sakusya<>$homepage<>200<>$pow<>$def<>$spe<>$date<>$ip<>$icon<>0<>$syu<>0<>5<>$ashi<>$osu<>$mesu<>$sei<>$ketou<>$baku<>$pass<>$gazou<>0<>0<><><><><><>$st<>$titi<>$tiha<>$tititi<>$titiha<>$tihati<>$tihaha<>$hati<>$haha<>$hatiti<>$hatiha<>$hahati<>$hahaha<>$checkketou1<>$checkketou2<>$checkketou3<>$tokusyu<>$formkon<>$dmy<>$dmy<>$dmy<>\n";

# ログへの書き込み
        open(WI,"$winfile");
	seek(WI,0,0);  @nowwin = <WI>;  close(WI);    # チャンピオンを調べる

        if(@nowwin[0] eq ""){

        open(WI,">>$winfile") ;
		eval 'flock(WI,2);';
		print WI $kakiko;
		eval 'flock(WI,8);';
	close(WI);
        }
        
	open(DB,">>$logfile") ;
		eval 'flock(DB,2);';
		print DB $kakiko;
		eval 'flock(DB,8);';
	close(DB);
push(@lines,$kakiko);


# 記録したしるし

$recflag = '1';

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

}#end umaname

sub ketou{  # 種牡馬血統詳細

print "Content-type: text/html\n\n";#コンテントタイプ出力
print <<"_HTML1_";
<html><head><title>種牡馬血統詳細</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>

<center><font color="$tcolor" size="5"><B>種牡馬血統詳細</B></font><P>

_HTML1_

       open(TK,"$tanefile");     #オス
       seek(TK,0,0);  @tk = <TK>;  close(TK);

       foreach $check (@tk){
       @checko = split(/<>/,$check);

      for ($k=0; $k<16; $k++){
         ($check, $tokusyu) = split(/<mm>/,$checko[$k]);
         if($tokusyu ne ""){$checko[$k]="$check<img src=\"$imgurl/$tokusyu.gif\">";}else{
         $checko[$k]="$check";}
      if($k == 0){$k = 9;}
      }

print "<table border=1 cellspacing=0 cellpadding=4>
<tr>
<td rowspan=4 bgcolor=#1E90FF width=150>$checko[0]<br>($checko[1]系)</td>
<td rowspan=2 bgcolor=#1E90FF width=150>$checko[10]</td>
<td bgcolor=#1E90FF width=150>$checko[12]</td></tr><tr>
<td bgcolor=#FF69B4>$checko[13]</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>$checko[11]</td>
<td bgcolor=#1E90FF>$checko[14]</td></tr><tr>
<td bgcolor=#FF69B4>$checko[15]</td>
</tr>
</table><br>";

}

&chosaku;
}

sub mketou{  # 繁殖牝馬血統詳細

print "Content-type: text/html\n\n";#コンテントタイプ出力
print <<"_HTML1_";
<html><head><title>繁殖牝馬血統詳細</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>

<center><font color="$tcolor" size="5"><B>繁殖牝馬血統詳細</B></font><P>

_HTML1_

       open(TK,"$tamefile");     #オス
       seek(TK,0,0);  @tk = <TK>;  close(TK);

       foreach $check (@tk){
       @checkm = split(/<>/,$check);

      for ($k=0; $k<15; $k++){
         ($check, $tokusyu) = split(/<mm>/,$checkm[$k]);
         if($tokusyu ne ""){$checkm[$k]="$check<img src=\"$imgurl/$tokusyu.gif\">";}else{
         $checkm[$k]="$check";}
      if($k == 0){$k = 9;}
      if($k == 10){$k++;}
      }

        ($checkname, $checkketou2, $tokusyu2) = split(/<mm>/,$checkm[11]);
        if($tokusyu2 ne ""){$checkname="$checkname<img src=\"$imgurl/$tokusyu2.gif\">";}

        ($checkname2, $checkketou3, $tokusyu3) = split(/<mm>/,$checkm[15]);
        if($tokusyu3 ne ""){$checkname2="$checkname2<img src=\"$imgurl/$tokusyu3.gif\">";}

print "<table border=1 cellspacing=0 cellpadding=4>
<tr>
<td rowspan=4 bgcolor=#FF69B4 width=150>$checkm[0]<br>($checkm[1]系)</td>
<td rowspan=2 bgcolor=#1E90FF width=150>$checkm[10]</td>
<td bgcolor=#1E90FF width=150>$checkm[12]</td></tr><tr>
<td bgcolor=#FF69B4>$checkm[13]</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>$checkname<br>($checkketou2系)</td>
<td bgcolor=#1E90FF>$checkm[14]</td></tr><tr>
<td bgcolor=#FF69B4>$checkname2<br>($checkketou3系)</td>
</tr>
</table><br>";

}

&chosaku;
}

sub inshi{

      if($tokusyu eq "sp2"){$formpow += 2;}
   elsif($tokusyu eq "sp1"){$formpow++;}
   elsif($tokusyu eq "syu2"){$formdef += 2;}
   elsif($tokusyu eq "syu1"){$formdef++;}
   elsif($tokusyu eq "ki2"){$formspe += 2;}
   elsif($tokusyu eq "ki1"){$formspe++;}
   elsif($tokusyu eq "st2"){$formst += 2;}
   elsif($tokusyu eq "st1"){$formst++;}
   elsif($tokusyu eq "kon2"){$formkon += 2;}
   elsif($tokusyu eq "kon1"){$formkon++;}
}
