#!/usr/bin/perl

#----------------------------------------------------------------------
#	 ���ڂ����o�g�����C���� ver 1.17 (Free)
#	 �����	: Alpha-kou.
#	 E-MAIL	: dabo@dabo.design.co.jp
#	 URL	: http://D-BR.net/
#
#        ������	: �S�[�h��
#        E-MAIL	: zaza99jp@yahoo.co.jp
#	 URL	: http://godon.bbzone.net/
#
# �g�p�O�ɂ܂����p�K���ǂ�ł�������
#	http://D-BR.net/kitei.html
#       http://godon.bbzone.net/kitei.html
# [���̃X�N���v�g���g�p���ċN���������Ȃ鑹�Q�ɂ��ӔC�͕����܂���B]
#----------------------------------------------------------------------

$| = 1;
require './jcode.pl';
require './uma5.cgi';&kankyou;

##### �L�͂Ȑ��Y�Əo��
sub orank{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>�L�͂Ȑ��Y��</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<center><br><font color=red size=5><B>�L�͂Ȑ��Y��</B></font><P>

<table border="1" width="400">

<tr><td bgcolor=green><center>����</td><td bgcolor=green><center>����</td><td bgcolor=green><center>���O</td><td bgcolor=green><center>�����N</td></tr>

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

          if($win[$i] > 999){$syou[$i] = "���E�n���Y�E�̒��_";}
          elsif($win[$i] > 699){$syou[$i] = "���{�n�E�̐_";}
          elsif($win[$i] > 499){$syou[$i] = "���{�n�E�̉�";}
          elsif($win[$i] > 299){$syou[$i] = "���{�n�E�̋~����";}
          elsif($win[$i] > 199){$syou[$i] = "�n���Y�E�̃g�b�v";}
          elsif($win[$i] > 99){$syou[$i] = "�n���Y�Ƌ�";}
          elsif($win[$i] > 74){$syou[$i] = "�n���Y�l";}
          elsif($win[$i] == 77){$syou[$i] = "(߄t�)�ϰ";}
          elsif($win[$i] > 49){$syou[$i] = "���n��i�E�́E�j��!";}
          elsif($win[$i] > 24){$syou[$i] = "�i�E�́E�j��!�n���Y��";}
          elsif($win[$i] > 14){$syou[$i] = "�����Ɣn�𐶎Y����";}
          elsif($win[$i] > 9){$syou[$i] = "�n�D��";}
          elsif($win[$i] > 4){$syou[$i] = "�n�l";}
          else{$syou[$i] = "��ʐl";}
            
          $f = $i + 1; 
	print "<tr><td><center>$f��</td><td><center><B><font size=$ookisa[$i]>$win[$i]��</font></B></td><td><center>$sakusya[$i]</td><td><center>$syou[$i]</td></tr>";
	}
        print "</table></center><P><center><select>";

        if($#orank >= 50){$hyouzi = 50;}else{$hyouzi = $#orank+1;}
        for ($i=10; $i<$hyouzi; $i++){
	($sakusya[$i], $win[$i], ) = split(/<>/,$orank[$i]);
        $f = $i + 1;
        print "<option>[$f] $win[$i]�� $sakusya[$i]\n";
	}
	print "</select>";

print <<"_HTML2_";
<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" name="orank" value="�L�͂Ȑ��Y��">
<input type="submit" name="kisyu" value="�R�胉���L���O">
<input type="submit" name="syurank" value="�퉲��ɐB�����L���O">
</td></tr></table>
</form>
_HTML2_
&chosaku;
}#end orank


##### �퉲�n�E�ɐB�Ĕn�����L���O
sub syurank{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>�퉲�n�E�ɐB�Ĕn�����L���O</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<center><br><font color=red size=5><B>�퉲�n�E�ɐB�Ĕn�����L���O</B></font><P>

<table border="2" width="300"><tr><td>

<table border="1" width="260">
<tr><td bgcolor=green><center>����</td><td bgcolor=green><center>�퉲�n</td></tr>

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
        
	print "<tr><td><center><B><font color=$iro[$i] size=3>$win[$i]��</font></B></td><td><center>$name[$i]</td></tr>";
	}

        print "</table></center><P><center><select>";

        if($#syurank >= 30){$hyouzi = 30;}else{$hyouzi = $#syurank+1;}
        for ($i=10; $i<$hyouzi; $i++){
	($sakusya[$i], $win[$i],) = split(/<>/,$syurank[$i]);
        ($name[$i], $toku[$i]) = split(/<mm>/,$sakusya[$i]);
        $f = $i + 1;
        print "<option>[$f] $win[$i]�� $name[$i]\n";
	}
	print "</select><P>";

print <<"_HTML1_";

</td><td><table border="1" width="260">

<tr><td bgcolor=green><center>����</td><td bgcolor=green><center>�ɐB�Ĕn</td></tr>

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
        
	print "<tr><td><center><B><font color=$irom[$i] size=3>$winm[$i]��</font></B></td><td><center>$names[$i]</td></tr>";
	}

        print "</table></center><P><center><select>";

        if($#mesrank >= 30){$hyouzi = 30;}else{$hyouzi = $#mesrank+1;}
        for ($i=10; $i<$hyouzi; $i++){
	($sak[$i], $winm[$i], ) = split(/<>/,$mesrank[$i]);
        ($names[$i], $toku[$i]) = split(/<mm>/,$sak[$i]);
        $f = $i + 1;
        print "<option>[$f] $winm[$i]�� $names[$i]\n";
	}
	print "</select><P></td></tr></table>";

print <<"_HTML2_";
<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" name="orank" value="�L�͂Ȑ��Y��">
<input type="submit" name="kisyu" value="�R�胉���L���O">
<input type="submit" name="syurank" value="�퉲��ɐB�����L���O">
</td></tr></table>
</form>
_HTML2_
&chosaku;
}#end suyrank


##### ���R�[�h
sub rtime{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>���R�[�h</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<center><br><font color=red size=5><B>���R�[�h</B></font><P>
<table border="0" width="600"><tr>
_HTML1_

open(RR,"$recordsfile");
	seek(RR,0,0);  @rr = <RR>;  close(RR);

        for($i=0; $i<10; $i++){
	($rkaisai[$i], $rname0[$i], $rtime0[$i], $rname1[$i], $rtime1[$i], $rname2[$i], $rtime2[$i], $rname3[$i], $rtime3[$i], $rname4[$i], $rtime4[$i]) = split(/<>/,$rr[$i]);

        ($hunt0[$i], $byout0[$i], $nant0[$i]) = split(/<t>/,$rtime0[$i]);
        $hjuy0[$i] = "$hunt0[$i]��$byout0[$i]��$nant0[$i]";
        ($hunt1[$i], $byout1[$i], $nant1[$i]) = split(/<t>/,$rtime1[$i]);
        $hjuy1[$i] = "$hunt1[$i]��$byout1[$i]��$nant1[$i]";
        ($hunt2[$i], $byout2[$i], $nant2[$i]) = split(/<t>/,$rtime2[$i]);
        $hjuy2[$i] = "$hunt2[$i]��$byout2[$i]��$nant2[$i]";
        ($hunt3[$i], $byout3[$i], $nant3[$i]) = split(/<t>/,$rtime3[$i]);
        $hjuy3[$i] = "$hunt3[$i]��$byout3[$i]��$nant3[$i]";
        ($hunt4[$i], $byout4[$i], $nant4[$i]) = split(/<t>/,$rtime4[$i]);
        $hjuy4[$i] = "$hunt4[$i]��$byout4[$i]��$nant4[$i]";

	print "<td><table border=1 width=300><tr><td bgcolor=green width=70><center><font color=yellow><B>$rkaisai[$i]</B></font></td><td bgcolor=green width=150><center>�n��</td><td bgcolor=green width=80><center>�^�C��</td></tr><tr><td><center>1600</td><td><center><B>$rname1[$i]</font></B></td><td><center>$hjuy1[$i]</td></tr><tr><td><center>1800</td><td><center><B>$rname2[$i]</font></B></td><td><center>$hjuy2[$i]</td></tr><tr><td><center>2000</td><td><center><B>$rname0[$i]</font></B></td><td><center>$hjuy0[$i]</td></tr><tr><td><center>2200</td><td><center><B>$rname3[$i]</font></B></td><td><center>$hjuy3[$i]</td></tr><tr><td><center>2400</td><td><center><B>$rname4[$i]</font></B></td><td><center>$hjuy4[$i]</td></tr></table><br><br></td>";

            if($i % 2 ne "0"){
             print "</tr><tr>";
            }
        }

&chosaku;
}#end rtime


###### ���D���n

sub past{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>���D���n</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<center><br><font color=red size=5><B>���D���n</B></font><P>

<table border="1" width="700">

<tr>
<td bgcolor=green width=35><center>��</td>
<td bgcolor=green width=60><center>�n</td>
<td bgcolor=green width=165><center>�n/1600m</td>
<td bgcolor=green width=110><center>���/1800m</td>
<td bgcolor=green width=110><center>����/2000m</td>
<td bgcolor=green width=110><center>�A��/2200m</td>
<td bgcolor=green width=110><center>�n��/2400m</td>
</tr>

_HTML1_

        open(PT,"$pastfile");
	seek(PT,0,0);  @pt = <PT>;  close(PT);

        open(FG,"$gaifightfile");                # ���[�X�̋L�^
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
        if($hunt eq ""){$hjuy20[$i] = "���o��";}
        else{$hjuy20[$i] = "$hunt��$byout��$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records16[$i]);
        if($hunt eq ""){$hjuy16[$i] = "���o��";}
        else{$hjuy16[$i] = "$hunt��$byout��$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records18[$i]);
        if($hunt eq ""){$hjuy18[$i] = "���o��";}
        else{$hjuy18[$i] = "$hunt��$byout��$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records22[$i]);
        if($hunt eq ""){$hjuy22[$i] = "���o��";}
        else{$hjuy22[$i] = "$hunt��$byout��$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records24[$i]);
        if($hunt eq ""){$hjuy24[$i] = "���o��";}
        else{$hjuy24[$i] = "$hunt��$byout��$nant";}

        if($no[$i] eq "-2"){$ii = "<font color=gold><b>$ii��</b></font>";}
        else{$ii = "$ii��";}
	print "
<tr>
<td rowspan=2><center>$ii</td>
<td  rowspan=2><center>$icon_pri[$i]</td>
<td><font size=1>$osuu</font><br><center><b>$name[$i]($sei[$i])</b><br><font size=1></center>$mesuu</font></td>
<td><center>$syu[$i]</td>
<td><center>$win[$i]��$lose[$i]�s</td>
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


##### �R��ꗗ
sub kisyu{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>�R��ꗗ</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<!--�L���o�i�[�}���ʒu�A�y�[�W�㕔-->
<center><font color="$tcolor" size="5"><B>�R��ꗗ</B></font><P>
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>

<table border="1" width="800">

<tr>
<td bgcolor=green width=50><center>����</td>
<td bgcolor=green width=70><center>���O</td>
<td bgcolor=green><center>����</td>
<td bgcolor=green width=70><center>����</td>
<td bgcolor=green width=70><center>����</td>
<td bgcolor=green width=60><center>����</td>
<td bgcolor=green width=115><center>����</td>
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
        if( ($win+$lose) eq "0"){$ritu = "���R��";}else{
        $ritu = sprintf("%03d", ( $win/ ($win+$lose) ) * 1000);}
        $total=$win+$lose;
        if($omona3 ne ""){
	print "<tr><td><center>$gg��</td><td><center><b>$name</b></td><td>$comm</td><td><center>$win</td><td><center>$lose</td><td><center>.$ritu</td><td><center>$omona<br>$omona2<br>$omona3</td></tr>\n";
        }else{
        print "<tr><td><center>$gg��</td><td><center><b>$name</b></td><td>$comm</td><td><center>$win</td><td><center>$lose</td><td><center>.$ritu</td><td><center>$omona<br>$omona2</td></tr>\n";}
        }

print <<"_HTML2_";
</table><div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" name="orank" value="�L�͂Ȑ��Y��">
<input type="submit" name="kisyu" value="�R�胉���L���O">
<input type="submit" name="syurank" value="�퉲��ɐB�����L���O">
</td></tr></table>
</form>
_HTML2_
&chosaku;

}#end kisyu
